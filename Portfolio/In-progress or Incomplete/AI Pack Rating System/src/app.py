from importlib.metadata import files

from flask import Flask, render_template, request, jsonify
import os
import cv2
import pytesseract
import numpy as np
import re
import requests
import time
import json
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import random
import glob

app = Flask(__name__)
this_dir = os.path.dirname(os.path.abspath(__file__))
app.config['UPLOAD_FOLDER'] = os.path.join(this_dir, 'uploads')
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

PALETTE_DIR = os.path.join(this_dir, "card_palettes")
DEFAULT_YEAR = "fc26"
VALID_YEARS = {"fifa20", "fifa21", "fifa22", "fifa23", "fc24", "fc25", "fc26"}

def normalize_game_year(value: str) -> str:
    y = (value or "").strip().lower()
    return y if y in VALID_YEARS else DEFAULT_YEAR

def hex_to_bgr(hex_color: str):
    s = (hex_color or "").strip().lstrip("#")
    if len(s) != 6:
        return None
    try:
        r = int(s[0:2], 16)
        g = int(s[2:4], 16)
        b = int(s[4:6], 16)
        return (b, g, r)
    except ValueError:
        return None

def bgr_to_lab_tuple(bgr):
    arr = np.uint8([[bgr]])
    lab = cv2.cvtColor(arr, cv2.COLOR_BGR2LAB)[0][0]
    return (float(lab[0]), float(lab[1]), float(lab[2]))

def parse_palette_file(file_path: str):
    """
    Expected line format:
    Card Type,#RRGGBB
    Example:
    Rare Gold,#D8A847
    """
    entries = []
    with open(file_path, "r", encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            parts = [p.strip() for p in line.split(",", 1)]
            if len(parts) != 2:
                continue
            card_type, hex_color = parts
            bgr = hex_to_bgr(hex_color)
            if not bgr:
                continue
            entries.append({
                "card_type": card_type,
                "hex": hex_color,
                "bgr": bgr,
                "lab": bgr_to_lab_tuple(bgr)
            })
    return entries

def load_random_palette_for_year(game_year: str):
    year = normalize_game_year(game_year)
    pattern = os.path.join(PALETTE_DIR, f"{year}_*.txt")
    files = glob.glob(pattern)

    if not files:
        exact = os.path.join(PALETTE_DIR, f"{year}.txt")
        if os.path.exists(exact):
            files = [exact]

    if not files:
        return [], None

    chosen = random.choice(files)
    return parse_palette_file(chosen), chosen

def detect_representative_card_color(image_region):
    if image_region is None or image_region.size == 0:
        return None

    h, w = image_region.shape[:2]
    y1, y2 = int(h * 0.12), int(h * 0.88)
    x1, x2 = int(w * 0.12), int(w * 0.88)
    roi = image_region[y1:y2, x1:x2]
    if roi.size == 0:
        roi = image_region

    small = cv2.resize(roi, (80, 80), interpolation=cv2.INTER_AREA)
    hsv = cv2.cvtColor(small, cv2.COLOR_BGR2HSV)

    # Prefer colorful/non-dark pixels to avoid text/background bias
    mask = (hsv[:, :, 1] > 35) & (hsv[:, :, 2] > 40)
    pixels = small[mask]
    if len(pixels) < 50:
        pixels = small.reshape(-1, 3)

    pixels = np.float32(pixels)
    K = min(3, len(pixels))
    if K == 0:
        return None

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 1.0)
    _, labels, centers = cv2.kmeans(pixels, K, None, criteria, 5, cv2.KMEANS_PP_CENTERS)
    counts = np.bincount(labels.flatten(), minlength=K)
    dominant = centers[np.argmax(counts)].astype(np.uint8)
    return (int(dominant[0]), int(dominant[1]), int(dominant[2]))

def classify_card_type(image_region, palette_entries, max_distance=42.0):
    """
    Find closest card type by LAB distance against the selected year's palette.
    """
    if not palette_entries:
        return "Unknown"

    detected_bgr = detect_representative_card_color(image_region)
    if detected_bgr is None:
        return "Unknown"

    detected_lab = bgr_to_lab_tuple(detected_bgr)

    best = None
    best_dist = 1e9
    for entry in palette_entries:
        d = np.linalg.norm(np.array(detected_lab) - np.array(entry["lab"]))
        if d < best_dist:
            best_dist = d
            best = entry

    if best is None or best_dist > max_distance:
        return "Unknown"
    return best["card_type"]

# Tesseract path
pytesseract.pytesseract.tesseract_cmd = "C:\\Users\\fifau\\AppData\\Local\\Programs\\Tesseract-OCR\\tesseract.exe"

# Cache for price data
PRICE_CACHE = {}
CACHE_DURATION = 300  # 5 minutes cache

def resolve_platforms(selected_platform: str):
    """
    Maps one UI platform value to:
    - OCR layout platform: pc/console/mobile/auto
    - price platform: pc/ps/xbox
    """
    selected = (selected_platform or "auto").strip().lower()

    # OCR layout selection
    if selected in {"pc", "console", "mobile"}:
        ocr_layout = selected
    else:
        ocr_layout = "auto"

    # FUTBIN market platform selection
    price_map = {
        "pc": "pc",
        "console": "ps",   # default console market
        "mobile": "ps",    # companion/mobile usually aligns with console market
        "ps": "ps",
        "xbox": "xbox",
        "auto": "ps",
    }
    price_platform = price_map.get(selected, "auto")

    return ocr_layout, price_platform

# -----------------------------
# FUTBIN PRICE INTEGRATION
# -----------------------------
def get_player_price_futbin(player_name, rating, platform="ps"):
    """
    Get player price from FUTBin scraping their website (from your working test code)
    """
    cache_key = f"{player_name}_{rating}_{platform}"
    current_time = datetime.now()
    
    # Check cache first
    if cache_key in PRICE_CACHE:
        cached_data, cache_time = PRICE_CACHE[cache_key]
        if (current_time - cache_time).seconds < CACHE_DURATION:
            return cached_data
    
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        # Step 1: Search for player
        search_url = f"https://www.futbin.com/players?page=1&search={player_name}"
        print(f"Searching for player: {search_url}")
        resp = requests.get(search_url, headers=headers, timeout=10)
        resp.raise_for_status()

        # Look for player link in search results
        player_link_match = re.search(r'<a[^>]+href="(/26/player/\d+/[^"]+)"', resp.text)
        if not player_link_match:
            print(f"No player found for {player_name}")
            return {"price": estimate_price_by_rating(rating), "source": "estimated", "error": "Player not found"}

        player_path = player_link_match.group(1)
        player_id = re.search(r'/26/player/(\d+)/', player_path).group(1)
        print(f"Found player ID: {player_id}")

        # Step 2: Get player page
        player_url = f"https://www.futbin.com{player_path}"
        print(f"Fetching player page: {player_url}")
        page_resp = requests.get(player_url, headers=headers, timeout=10)
        page_resp.raise_for_status()

        soup = BeautifulSoup(page_resp.text, "html.parser")

        # Step 3: Extract price from HTML using multiple methods
        price_data = extract_price_from_page(soup, platform)
        
        if price_data and price_data.get('price'):
            result = {
                'price': price_data['price'],
                'source': 'futbin',
                'method': price_data.get('method', 'html_parsing')
            }
            PRICE_CACHE[cache_key] = (result, current_time)
            return result
        else:
            # Fallback to estimation
            estimated_price = estimate_price_by_rating(rating)
            result = {'price': estimated_price, 'source': 'estimated'}
            PRICE_CACHE[cache_key] = (result, current_time)
            return result

    except Exception as e:
        print(f"Exception occurred fetching price for {player_name}: {str(e)}")
        estimated_price = estimate_price_by_rating(rating)
        result = {'price': estimated_price, 'source': 'estimated', 'error': str(e)}
        PRICE_CACHE[cache_key] = (result, current_time)
        return result

def extract_price_from_page(soup, platform="ps"):
    """
    Extract price from the FUTBIN page using multiple HTML parsing methods
    """
    
    # Method 1: Look for price in data attributes
    price_elements = soup.find_all(attrs={"data-price": True})
    for elem in price_elements:
        price_text = elem.get('data-price')
        price = parse_price_text(price_text)
        if price:
            print(f"Found price via data-price: {price}")
            return {'price': price, 'method': 'data-attribute'}
    
    # Method 2: Look for price in specific CSS classes
    price_selectors = [
        '.price-value',
        '.coin-value', 
        '[class*="price"]',
        '[class*="coin"]',
        '.futbin-price',
        '.market-price'
    ]
    
    for selector in price_selectors:
        elements = soup.select(selector)
        for elem in elements:
            text = elem.get_text().strip()
            price = parse_price_text(text)
            if price and price > 500:  # Reasonable minimum
                print(f"Found price via CSS selector {selector}: {price}")
                return {'price': price, 'method': f'css_selector_{selector}'}
    
    # Method 3: Look for price in script tags (inline JavaScript)
    script_tags = soup.find_all('script')
    for script in script_tags:
        if script.string:
            # Look for price patterns in JavaScript
            price_patterns = [
                r'"price":\s*(\d+)',
                r'"LCPrice":\s*(\d+)',
                r'price:\s*(\d+)',
                r'coins?["\']?\s*:\s*["\']?(\d+)',
            ]
            
            for pattern in price_patterns:
                matches = re.findall(pattern, script.string)
                for match in matches:
                    price = int(match)
                    if price > 500:  # Reasonable minimum
                        print(f"Found price via script pattern {pattern}: {price}")
                        return {'price': price, 'method': 'javascript_parsing'}
    
    # Method 4: Look for any number that could be a price
    all_text = soup.get_text()
    
    # Look for patterns like "1,234,567" or "123K" or "1.2M"
    price_patterns = [
        r'(\d{1,3}(?:,\d{3})+)',  # 1,234,567 format
        r'(\d+(?:\.\d+)?)\s*[KM]',  # 123K or 1.2M format
        r'(\d{4,})',  # Any number with 4+ digits
    ]
    
    potential_prices = []
    for pattern in price_patterns:
        matches = re.findall(pattern, all_text)
        for match in matches:
            price = parse_price_text(match)
            if price and 1000 <= price <= 50000000:  # Reasonable range
                potential_prices.append(price)
    
    if potential_prices:
        # Return the most reasonable price (median value)
        potential_prices.sort()
        median_price = potential_prices[len(potential_prices)//2]
        print(f"Found price via text pattern: {median_price}")
        return {'price': median_price, 'method': 'text_pattern_analysis'}
    
    print("Could not extract price from page")
    return None

def parse_price_text(text):
    """
    Enhanced price text parser
    """
    if not text:
        return None
    
    try:
        # Clean the text
        text = str(text).strip().replace(',', '').replace(' ', '').replace('"', '').replace("'", '')
        
        # Handle K/M suffixes
        if text.upper().endswith('K'):
            number = float(text[:-1])
            return int(number * 1000)
        elif text.upper().endswith('M'):
            number = float(text[:-1])
            return int(number * 1000000)
        
        # Extract pure numbers
        number_match = re.search(r'(\d+(?:\.\d+)?)', text)
        if number_match:
            number = float(number_match.group(1))
            return int(number)
            
    except (ValueError, AttributeError):
        pass
    
    return None

def estimate_price_by_rating(rating):
    """
    Fallback price estimation based on rating
    """
    if not rating or rating < 50:
        return 1000
    
    if rating >= 95:
        return 100000 + (rating - 95) * 50000
    elif rating >= 90:
        return 50000 + (rating - 90) * 10000
    elif rating >= 85:
        return 20000 + (rating - 85) * 6000
    elif rating >= 80:
        return 5000 + (rating - 80) * 3000
    elif rating >= 75:
        return 2000 + (rating - 75) * 600
    else:
        return 500 + rating * 20

# -----------------------------
# OCR & IMAGE PREPROCESSING (Keep your existing code)
# -----------------------------
def preprocess_for_ocr(image_region):
    """Apply multiple preprocessing methods and return the best for OCR."""
    gray = cv2.cvtColor(image_region, cv2.COLOR_BGR2GRAY)
    gray = cv2.fastNlMeansDenoising(gray, None, 20, 7, 21)
    gray = cv2.equalizeHist(gray)

    # Try adaptive thresholding
    adaptive = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                     cv2.THRESH_BINARY, 11, 2)
    # Simple binary
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # Combine both
    combined = cv2.bitwise_or(adaptive, binary)
    return combined

def ocr_rating(image_region):
    """OCR for rating digits with multiple attempts."""
    # Upscale the region for better OCR
    scale = 3
    image_region = cv2.resize(image_region, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
    
    results = []
    gray = cv2.cvtColor(image_region, cv2.COLOR_BGR2GRAY)
    gray = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)

    # Try multiple threshold approaches
    preprocessed_variants = []
    
    # Variant 1: OTSU
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    preprocessed_variants.append(binary)
    
    # Variant 2: Inverted OTSU
    _, binary_inv = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    preprocessed_variants.append(binary_inv)
    
    # Variant 3: Adaptive
    adaptive = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                     cv2.THRESH_BINARY, 11, 2)
    preprocessed_variants.append(adaptive)

    configs = [
        "--psm 8 -c tessedit_char_whitelist=0123456789",
        "--psm 7 -c tessedit_char_whitelist=0123456789",
        "--psm 6 -c tessedit_char_whitelist=0123456789",
    ]

    for img in preprocessed_variants:
        for config in configs:
            text = pytesseract.image_to_string(img, config=config)
            text = re.sub(r'[^0-9]', '', text)
            if text.isdigit():
                rating = int(text)
                if 50 <= rating <= 99:
                    results.append(rating)

    if results:
        # Return the most common result
        return max(set(results), key=results.count)
    return None


def ocr_name(image_region):
    """OCR for player names with upscaling and multiple configs."""
    # Upscale for better OCR accuracy
    scale = 3
    image_region = cv2.resize(image_region, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
    
    gray = cv2.cvtColor(image_region, cv2.COLOR_BGR2GRAY)
    gray = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)
    
    results = []
    
    preprocessed_variants = []
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    preprocessed_variants.append(binary)
    _, binary_inv = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    preprocessed_variants.append(binary_inv)
    
    configs = [
        "--psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz ",
        "--psm 8 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz ",
        "--psm 13 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz ",
    ]
    
    for img in preprocessed_variants:
        for config in configs:
            text = pytesseract.image_to_string(img, config=config)
            text = re.sub(r'[^A-Za-z ]+', '', text).strip()
            text = re.sub(r'\s+', ' ', text).strip()
            if len(text) >= 2:
                results.append(text.title())
    
    if results:
        # Return longest result (usually most complete name)
        return max(results, key=len)
    return None

# Keep all your existing layout and analysis code...
def analyze_pack_image(image_path, platform="auto", palette_entries=None):
    LAYOUTS = {
        "pc": { #Full layout has dimensions of 1920x1080 but layout is different to console
            "slots": [
                {
                    "rating": (0.380, 0.139, 0.442, 0.172),  # Rating 1: 456,307 -> 530,378
                    "name":   (0.642, 0.133, 0.763, 0.167),  # Name 1: 770,293 -> 915,367
                    "card":   (0.371, 0.114, 0.616, 0.273)   # Card 1: 445,251 -> 739,600
                },
                {
                    "rating": (0.380, 0.342, 0.453, 0.374),  # Rating 2: 456,752 -> 544,823
                    "name":   (0.651, 0.339, 0.848, 0.371),  # Name 2: 781,745 -> 1018,816
                    "card":   (0.355, 0.314, 0.628, 0.477)   # Card 2: 426,690 -> 754,1050
                },
                {
                    "rating": (0.398, 0.546, 0.453, 0.580),  # Rating 3: 477,1201 -> 544,1275
                    "name":   (0.657, 0.540, 0.866, 0.575),  # Name 3: 788,1187 -> 1039,1265
                    "card":   (0.377, 0.522, 0.645, 0.681)   # Card 3: 452,1148 -> 774,1498
                },
                {
                    "rating": (0.409, 0.750, 0.463, 0.772),  # Rating 4: 491,1650 -> 555,1699
                    "name":   (0.657, 0.739, 0.843, 0.774),  # Name 4: 788,1625 -> 1011,1703
                    "card":   (0.383, 0.713, 0.648, 0.877)   # Card 4: 459,1568 -> 777,1929
                },
                {
                    "rating": (0.415, 0.941, 0.471, 0.970),  # Rating 5: 498,2070 -> 565,2133
                    "name":   (0.674, 0.931, 0.839, 0.970),  # Name 5: 809,2049 -> 1007,2133
                    "card":   (0.394, 0.909, 0.666, 0.977)   # Card 5: 473,1999 -> 799,2151
                }
            ]
        },
        "console": { #Full layout has dimensions of 1920x1080 but layout is different to PC/Web App
            "slots": [
                {
                    "rating": (0.109, 0.435, 0.135, 0.472),  # Rating 1: 210,470 -> 260,510
                    "name":   (0.104, 0.565, 0.208, 0.593),  # Name 1: 200,610 -> 400,640
                    "card":   (0.099, 0.407, 0.214, 0.685)   # Card 1: 190,440 -> 410,740
                },
                {
                    "rating": (0.219, 0.444, 0.234, 0.472),  # Rating 2: 420,480 -> 450,510
                    "name":   (0.214, 0.537, 0.276, 0.565),  # Name 2: 410,580 -> 530,610
                    "card":   (0.214, 0.426, 0.276, 0.685)   # Card 2: 410,460 -> 530,740
                },
                {
                    "rating": (0.276, 0.444, 0.292, 0.472),  # Rating 3: 530,480 -> 560,510
                    "name":   (0.276, 0.537, 0.333, 0.565),  # Name 3: 530,580 -> 640,610
                    "card":   (0.276, 0.426, 0.333, 0.685)   # Card 3: 530,460 -> 640,740
                },
                {
                    "rating": (0.339, 0.444, 0.354, 0.472),  # Rating 4: 650,480 -> 680,510
                    "name":   (0.333, 0.537, 0.401, 0.565),  # Name 4: 640,580 -> 770,610
                    "card":   (0.333, 0.426, 0.401, 0.685)   # Card 4: 640,460 -> 770,740
                },
                {
                    "rating": (0.401, 0.444, 0.417, 0.472),  # Rating 5: 770,480 -> 800,510
                    "name":   (0.401, 0.537, 0.469, 0.565),  # Name 5: 770,580 -> 900,610
                    "card":   (0.401, 0.426, 0.469, 0.685)   # Card 5: 770,460 -> 900,740
                },
                {
                    "rating": (0.469, 0.444, 0.484, 0.472),  # Rating 6: 900,480 -> 930,510
                    "name":   (0.469, 0.537, 0.536, 0.565),  # Name 6: 900,580 -> 1030,610
                    "card":   (0.469, 0.426, 0.536, 0.685)   # Card 6: 900,460 -> 1030,740
                },
                {
                    "rating": (0.536, 0.444, 0.552, 0.472),  # Rating 7: 1030,480 -> 1060,510
                    "name":   (0.536, 0.537, 0.604, 0.565),  # Name 7: 1030,580 -> 1160,610
                    "card":   (0.536, 0.426, 0.604, 0.685)   # Card 7: 1030,460 -> 1160,740
                },
                {
                    "rating": (0.604, 0.444, 0.620, 0.472),  # Rating 8: 1160,480 -> 1190,510
                    "name":   (0.604, 0.537, 0.672, 0.565),  # Name 8: 1160,580 -> 1290,610
                    "card":   (0.604, 0.426, 0.672, 0.685)   # Card 8: 1160,460 -> 1290,740
                },
                {
                    "rating": (0.672, 0.444, 0.688, 0.472),  # Rating 9: 1290,480 -> 1320,510
                    "name":   (0.672, 0.537, 0.740, 0.565),  # Name 9: 1290,580 -> 1420,610
                    "card":   (0.672, 0.426, 0.740, 0.685)   # Card 9: 1290,460 -> 1420,740
                },
                {
                    "rating": (0.740, 0.444, 0.755, 0.472),  # Rating 10: 1420,480 -> 1450,510
                    "name":   (0.740, 0.537, 0.807, 0.565),  # Name 10: 1420,580 -> 1550,610
                    "card":   (0.740, 0.426, 0.807, 0.685)   # Card 10: 1420,460 -> 1550,740
                }
            ]
        },
        "mobile": { #Full layout has dimensions of 1080x2039
            "slots": [
                {
                    "rating": (0.057, 0.275, 0.102, 0.294),  # Rating 1: 62,561 -> 110,600
                    "name":   (0.035, 0.247, 0.261, 0.385),  # Name 1: 38,503 -> 282,786
                    "card":   (0.272, 0.263, 0.420, 0.291)   # Card 1: 294,536 -> 454,594
                },
                {
                    "rating": (0.055, 0.439, 0.106, 0.462),  # Rating 2: 59,896 -> 115,942
                    "name":   (0.272, 0.431, 0.382, 0.457),  # Name 2: 294,880 -> 413,932
                    "card":   (0.034, 0.415, 0.261, 0.548)   # Card 2: 37,846 -> 282,1118
                },
                {
                    "rating": (0.056, 0.606, 0.103, 0.628),  # Rating 3: 61,1235 -> 111,1280
                    "name":   (0.269, 0.592, 0.556, 0.623),  # Name 3: 291,1208 -> 600,1270
                    "card":   (0.038, 0.581, 0.252, 0.712)   # Card 3: 41,1184 -> 272,1452
                },
                {
                    "rating": (0.057, 0.771, 0.100, 0.792),  # Rating 4: 62,1573 -> 108,1615
                    "name":   (0.269, 0.757, 0.419, 0.791),  # Name 4: 291,1543 -> 453,1612
                    "card":   (0.033, 0.741, 0.256, 0.882)   # Card 4: 36,1511 -> 277,1799
                },
                {
                    "rating": (0.056, 0.935, 0.102, 0.958),  # Rating 5: 61,1907 -> 110,1955
                    "name":   (0.259, 0.921, 0.495, 0.964),  # Name 5: 280,1877 -> 535,1966
                    "card":   (0.038, 0.907, 0.254, 1.044)   # Card 5: 41,1850 -> 274,2128
                }
            ]
        }
    }

    image = cv2.imread(image_path)
    if image is None:
        return {"error": "Could not load image"}

    h, w = image.shape[:2]
    requested_layout = resolve_platforms(platform)[0]  # Get OCR layout platform
    
    # Prevent KeyError: 'auto'
    if requested_layout == "auto":
        # Simple heuristic: portrait images are usually mobile
        layout = "mobile" if h > w else "console"
    else:
        layout = requested_layout

    # Final safety fallback
    if layout not in LAYOUTS:
        layout = "console"

    print(f"Selected layout: {layout}")

    players = []
    for slot in LAYOUTS[layout]["slots"]:
        rating_img = crop_region(image, w, h, slot["rating"])
        name_img = crop_region(image, w, h, slot["name"])
        card_img = crop_region(image, w, h, slot["card"])
        card_type = classify_card_type(card_img, palette_entries or [])

        rating = ocr_rating(rating_img)
        name = ocr_name(name_img)
        if not rating and not name:
            continue  # Skip if both missing

        # Relaxed validation — accept one missing value
        if not name:
            name = "Unknown"
        if not rating:
            rating = 0

        players.append({
            "name": name,
            "rating": rating,
            "card_type": card_type
        })

    return {"players": players, "total_players": len(players)}

def crop_region(image, width, height, coords):
    x1, y1, x2, y2 = coords
    return image[int(y1 * height):int(y2 * height), int(x1 * width):int(x2 * width)]

# -----------------------------
# UPDATED PRICE CALCULATION
# -----------------------------
def calculate_pack_value(players, selected_platform="auto"):
    """
    Calculate total pack value using the working FUTBIN integration
    """
    total_value = 0
    total_rating = 0
    valid_players = 0
    
    for player in players:
        name = player.get('name', 'Unknown')
        rating = player.get('rating') or 0  # Handle None/0
        
        print(f"Fetching price for: {name} ({rating} OVR) [{selected_platform}]")
        
        # Add rate limiting to avoid being blocked
        time.sleep(0.5)
        
        price_data = get_player_price_futbin(name, rating, platform=resolve_platforms(selected_platform)[1])  # Get price platform
        
        player['price'] = price_data.get('price', 0)
        player['price_source'] = price_data.get('source', 'unknown')
        
        if player['price']:
            total_value += player['price']
            if rating > 0:
                total_rating += rating
            valid_players += 1
            print(f"Price found: {player['price']} coins ({player['price_source']})")
        else:
            # Still count the player, just use estimation
            estimated = estimate_price_by_rating(rating)
            player['price'] = estimated
            player['price_source'] = 'estimated'
            total_value += estimated
            if rating > 0:
                total_rating += rating
            valid_players += 1
            print(f"Using estimated price for {name}: {estimated}")
    
    average_rating = total_rating / valid_players if valid_players > 0 else 0
    
    if total_value >= 500000:
        pack_rating = 95
    elif total_value >= 200000:
        pack_rating = 85 + (total_value - 200000) / 30000
    elif total_value >= 100000:
        pack_rating = 75 + (total_value - 100000) / 10000
    elif total_value >= 50000:
        pack_rating = 60 + (total_value - 50000) / 3333
    else:
        pack_rating = max(10, total_value / 2500)
    
    return {
        'total_value': int(total_value),
        'average_rating': round(average_rating, 1),
        'pack_rating': min(100, round(pack_rating, 1)),
        'player_count': valid_players
    }

# -----------------------------
# FLASK ROUTES (Updated)
# -----------------------------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'image-upload' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    files = request.files.getlist('image-upload')
    pack_type = request.form.get('pack-type', '')
    selected_platform = request.form.get('platform', 'auto')
    selected_year = normalize_game_year(request.form.get('game-year', DEFAULT_YEAR))
    palette_entries, palette_file = load_random_palette_for_year(selected_year)

    if not palette_entries:
        return jsonify({
            'error': f'No palette file found for {selected_year}. Expected files like "{selected_year}_*.txt" in src/card_palettes.'
        }), 400
    
    all_players = []

    for file in files:
        if file.filename:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            result = analyze_pack_image(
                file_path,
                platform=selected_platform,
                palette_entries=palette_entries
            )
            
            # Debug: save cropped regions to check OCR quality
            print(f"Image analysis result: {result}")
            
            if 'error' in result:
                return jsonify({'error': result['error']}), 500
            all_players.extend(result['players'])

    if not all_players:
        return jsonify({'error': 'No players detected. Check image quality or layout coordinates.'}), 400

    print(f"Calculating pack value for {len(all_players)} players...")
    stats = calculate_pack_value(all_players, selected_platform=selected_platform)
    
    return jsonify({
        'players': all_players,
        'pack_type': pack_type.replace('-', ' ').title(),
        'game_year': selected_year,
        'palette_file': os.path.basename(palette_file) if palette_file else None,
        'total_players': stats['player_count'],
        'average_rating': stats['average_rating'],
        'pack_value': stats['total_value'],
        'pack_rating': stats['pack_rating']
    })

if __name__ == '__main__':
    app.run(debug=True)
