from flask import Flask, jsonify, request, render_template
import requests
import re
from bs4 import BeautifulSoup
import json
import time
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('futbinTest.html')

def transform_name(name):
    return name.lower().replace(' ', '-')

PRICE_CACHE = {}
CACHE_DURATION = 300  # 5 minutes cache

def get_player_price_futbin(player_name, rating, platform="pc"):
    """
    Get player price from FUTBin scraping their website
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
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        # Step 1: Search for player
        search_url = f"https://www.futbin.com/players"
        params = {"page": 1, "search": player_name}
        
        response = requests.get(search_url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Find player ID from search results
        player_id_match = re.search(r'/26/player/(\d+)/', response.text)
        if not player_id_match:
            return {"price": None, "source": "futbin", "error": "Player not found"}
        
        player_id = player_id_match.group(1)
        name_slug = player_name.lower().replace(' ', '-')
        
        # Step 2: Get player page
        player_url = f"https://www.futbin.com/26/player/{player_id}/{name_slug}"
        page_response = requests.get(player_url, headers=headers, timeout=10)
        page_response.raise_for_status()
        
        # Step 3: Parse the HTML for price data
        soup = BeautifulSoup(page_response.text, "html.parser")
        
        # Method 1: Try to find the price in the price display elements
        price = extract_price_from_html(soup, platform)
        
        if price:
            result = {"price": price, "source": "futbin"}
            PRICE_CACHE[cache_key] = (result, current_time)
            return result
        
        # Method 2: If HTML parsing fails, try JSON data
        script_tag = soup.find("script", id="__NEXT_DATA__")
        if script_tag and script_tag.string:
            data = json.loads(script_tag.string)
            price = extract_price_from_json(data, platform)
            
            if price:
                result = {"price": price, "source": "futbin"}
                PRICE_CACHE[cache_key] = (result, current_time)
                return result
        
        # Fallback to estimation
        return {"price": estimate_price_by_rating(rating), "source": "estimated"}
        
    except Exception as e:
        print(f"Error fetching price for {player_name}: {e}")
        return {"price": estimate_price_by_rating(rating), "source": "estimated"}

def extract_price_from_html(soup, platform="pc"):
    """
    Extract price from HTML elements on the FUTBIN page
    """
    try:
        # Look for price containers - FUTBIN uses various class names
        price_selectors = [
            f"[data-platform='{platform}'] .coin-value",
            f"[data-platform='{platform}'] .price-value",
            ".price-box .coin-value",
            ".price-container .price",
            "[class*='price'] [class*='coin']",
            ".price-display .value"
        ]
        
        for selector in price_selectors:
            price_elements = soup.select(selector)
            for element in price_elements:
                price_text = element.get_text().strip()
                price = parse_price_text(price_text)
                if price:
                    return price
        
        # Fallback: look for any element containing coin/price data
        all_price_elements = soup.find_all(string=re.compile(r'\d+[,.]?\d*[KM]?\s*(coins?)?', re.I))
        for text in all_price_elements:
            price = parse_price_text(text)
            if price and price > 100:  # Reasonable minimum price
                return price
                
    except Exception as e:
        print(f"Error parsing HTML price: {e}")
    
    return None

def extract_price_from_json(data, platform="pc"):
    """
    Extract price from JSON data embedded in the page
    """
    try:
        def find_price_data(obj):
            if isinstance(obj, dict):
                # Look for price-related keys
                for key in ["prices", "price", "LCPrice", "marketPrice"]:
                    if key in obj:
                        price_data = obj[key]
                        
                        # Handle different price data structures
                        if isinstance(price_data, dict):
                            # Platform-specific prices
                            if platform in price_data:
                                platform_price = price_data[platform]
                                if isinstance(platform_price, dict):
                                    return platform_price.get("LCPrice") or platform_price.get("price")
                                return platform_price
                            
                            # Generic price data
                            return price_data.get("LCPrice") or price_data.get("price") or price_data.get(platform)
                        
                        elif isinstance(price_data, (int, float)) and price_data > 0:
                            return price_data
                
                # Recursively search nested objects
                for value in obj.values():
                    result = find_price_data(value)
                    if result:
                        return result
            
            elif isinstance(obj, list):
                for item in obj:
                    result = find_price_data(item)
                    if result:
                        return result
            
            return None
        
        price = find_price_data(data)
        return price if price and price > 0 else None
        
    except Exception as e:
        print(f"Error parsing JSON price: {e}")
        return None

def parse_price_text(text):
    """
    Parse price text and convert to integer
    """
    if not text:
        return None
    
    try:
        # Clean the text
        text = str(text).strip().replace(',', '').replace(' ', '')
        
        # Extract numbers and multipliers
        match = re.search(r'(\d+(?:\.\d+)?)\s*([KkMm]?)', text)
        if not match:
            return None
        
        number = float(match.group(1))
        multiplier = match.group(2).upper()
        
        # Apply multiplier
        if multiplier == 'K':
            return int(number * 1000)
        elif multiplier == 'M':
            return int(number * 1000000)
        else:
            return int(number)
            
    except (ValueError, AttributeError):
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

def get_player_price(player_name, rating, card_type="Rare Gold", platform="pc"):
    """
    Wrapper function to get player price with fallback
    """
    # Get price from FUTBIN
    price_data = get_player_price_futbin(player_name, rating, platform)
    
    # If no price found, use estimation
    if not price_data.get("price"):
        estimated_price = estimate_price_by_rating(rating)
        return {"price": estimated_price, "source": "estimated"}
    
    return price_data

def calculate_pack_value(players):
    """
    Calculate total pack value and rating based on player prices
    """
    total_value = 0
    total_rating = 0
    valid_players = 0
    
    for player in players:
        if player.get('rating') and player.get('name'):
            # Get player price with rate limiting
            time.sleep(0.5)  # Avoid being blocked
            
            price_data = get_player_price(
                player['name'], 
                player['rating'], 
                player.get('card_type', 'Rare Gold'),
                platform="pc"
            )
            
            player['price'] = price_data.get('price', 0)
            player['price_source'] = price_data.get('source', 'unknown')
            
            if player['price']:
                total_value += player['price']
                total_rating += player['rating']
                valid_players += 1
    
    # Calculate metrics
    average_rating = total_rating / valid_players if valid_players > 0 else 0
    
    # Calculate pack rating based on total value
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

@app.route('/api/player', methods=['GET'])
def get_player_api():
    player_name = request.args.get('name', '').strip()
    platform = request.args.get('platform', 'pc').lower()

    if not player_name:
        return jsonify({'error': 'Missing player name'}), 400

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
            return jsonify({'error': f'No player found for "{player_name}"'}), 404

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
        
        if price_data:
            result = {
                'player_id': player_id,
                'player_name': player_name,
                'platform': platform,
                'price': price_data.get('price'),
                'updated': price_data.get('updated', 'N/A'),
                'method': price_data.get('method', 'html_parsing')
            }
            return jsonify(result)
        else:
            # Fallback to estimation
            estimated_price = estimate_price_by_rating(85)  # Default rating assumption
            return jsonify({
                'player_id': player_id,
                'player_name': player_name,
                'platform': platform,
                'price': estimated_price,
                'method': 'estimated',
                'note': 'Could not extract price from page'
            })

    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

def extract_price_from_page(soup, platform="pc"):
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
    
    # Method 5: Look for hidden elements or data
    hidden_elements = soup.find_all(style=re.compile(r'display:\s*none', re.I))
    for elem in hidden_elements:
        text = elem.get_text().strip()
        price = parse_price_text(text)
        if price and price > 500:
            print(f"Found price in hidden element: {price}")
            return {'price': price, 'method': 'hidden_element'}
    
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

if __name__ == '__main__':
    app.run(debug=True)