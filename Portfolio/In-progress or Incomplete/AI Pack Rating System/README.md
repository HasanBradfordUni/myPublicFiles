# Ultimate Pack Value Analyzer

## Project Overview

The **Ultimate Pack Value Analyzer** is a web-based tool designed for FIFA/EA FC25 players to analyze the value of their player packs. Users can upload screenshots of their packs, select the pack type, and receive a rating based on the market value of the cards contained within.

## Features

- Upload one or more screenshots of FIFA/EA FC25 player packs.
- Select the pack type from a predefined list.
- AI-based image analysis to extract player information.
- Fetch live card prices from external APIs.
- Calculate and display a pack rating percentage.

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd ultimate-pack-analyzer
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```
   python app.py
   ```

2. Open your web browser and navigate to `http://127.0.0.1:5000`.

3. Use the interface to upload your FIFA pack images and select the appropriate pack type.

4. View the results, including the pack rating and card values.

## Directory Structure

```
AI Pack Rating System
├── brief.md
├── src
    ├── app.py
    ├── static
    │   ├── css
    │   │   └── style.css
    │   └── js
    │       └── main.js
    ├── templates
    │   ├── index.html
    │   └── results.html
    ├── uploads (folder)
    ├── requirements.txt
└── README.md
```

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.