# **Project Brief: EA Sports FC25 Pack Rating Web Application**

## **Project Title:**

**Ultimate Pack Value Analyzer** – A FIFA/EA FC25 Pack Rating Tool

---

## **Project Overview:**

The **Ultimate Pack Value Analyzer** is a web-based tool that allows users to upload screenshots of FIFA/EA FC25 player packs and select the pack type from a predefined list. Using AI-based image analysis and live price data fetched from the transfer market, the application calculates the total value of cards within the pack. It then compares the market value to the expected value of that pack type and returns a **pack rating percentage**, offering users insights into the real-world worth of their digital packs.

---

## **Objectives:**

1. Enable users to upload one or more screenshots of FIFA/FC25 player packs.
2. Provide a dropdown menu to select the pack type.
3. Use AI to analyze uploaded screenshots and extract card/player information.
4. Fetch live card prices from an external API (e.g., Futbin) dynamically.
5. Compute and return a pack rating based on total player value vs expected pack value.
6. Present results cleanly in a user-friendly frontend using vanilla JavaScript.

---

## **Key Features:**

1. **Screenshot Upload**: Upload one or multiple pack screenshots.
2. **Pack Type Selector**: Choose from a list of predefined FIFA pack types.
3. **AI Analysis**: Use Google Vertex AI or Google Cloud Vision to extract card/player names from images.
4. **Live Pricing Integration**: Query real-time prices via the Futbin API or a similar source.
5. **Pack Rating Calculation**: Rate the pack based on market value vs pack cost/value.
6. **Web Interface**: Simple HTML/CSS/JavaScript interface integrated with Flask.
7. **Cloud Integration**: Store uploaded images using Google Cloud Storage.

---

## **Technical Specifications:**

### **Programming Language:**

* Python (Backend)
* HTML, CSS, JavaScript (Frontend)

### **Frameworks & Libraries:**

* **Flask** – Backend Web Framework
* **Pillow / OpenCV** – Image preprocessing
* **Google Cloud Vision or Vertex AI** – OCR/Image Analysis
* **Requests** – API communication with card pricing APIs
* **Jinja2** – Templating engine for rendering HTML from Flask

### **APIs and Services:**

* **Futbin API** (or unofficial endpoints) – Card market values
* **Google Cloud Vision / Vertex AI** – OCR or image classification
* **Google Cloud Storage** – Store uploaded pack images

### **Database (optional):**

* SQLite (or JSON-based caching) for local card price caching

### **Frontend:**

* **HTML/CSS/JavaScript (Vanilla)** – For UI
* **No frameworks (like React)** – Lightweight and simple
* **AJAX (fetch API)** – To communicate with Flask backend

### **Deployment:**

* Google Cloud Run or App Engine for Flask backend
* Firebase Hosting or serve frontend directly via Flask

---

## **Expected Outcomes:**

1. A fully functional Flask web app with card recognition and rating.
2. Accurate value estimation of FIFA/FC25 packs based on real-time data.
3. Fast, clean, and responsive UI with no framework dependency.
4. Cloud-hosted and accessible from desktop and mobile browsers.

---

## **Risks and Mitigations:**

| Risk                           | Mitigation                                                           |
| ------------------------------ | -------------------------------------------------------------------- |
| **Image Recognition Accuracy** | Improve OCR/AI model with training; use Google Vision as fallback    |
| **API Rate Limits (Futbin)**   | Add local caching of player prices; limit request frequency          |
| **User Upload Issues**         | Validate and compress uploaded images; provide clear UI instructions |
| **Pack Type Mismatches**       | Lock pack types to predefined list with known average values         |
| **Frontend Usability**         | Use minimal JS with progressive enhancement and fallback messages    |

---

## **Project Milestones:**

| Phase                   | Tasks                                                            |
| ----------------------- | ---------------------------------------------------------------- |
| **1. Setup**            | Flask app skeleton, image upload form, pack type dropdown        |
| **2. Image Analysis**   | Integrate Vertex AI / Google Vision OCR to extract card names    |
| **3. Pricing API**      | Connect to Futbin or similar API and fetch card prices           |
| **4. Rating Logic**     | Implement and test rating algorithm                              |
| **5. Frontend**         | Display results with card names, prices, and rating (vanilla JS) |
| **6. Cloud Deployment** | Deploy backend to GCP, frontend served via Flask or Firebase     |
| **7. Polish**           | UI cleanup, error handling, performance tuning                   |
