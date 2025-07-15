# 🧠 Reddit Persona Generator

This project generates a psychological persona of any public Reddit user by scraping their Reddit activity, analyzing it using Google's Gemini LLM, and converting it into a beautiful PDF.

## ✅ Features

- Scrapes latest posts & comments from any Reddit user
- Uses **Google Gemini** to infer:
  - Age, Occupation, Location, Archetype, Status
- Renders a **premium HTML/CSS layout**
- Converts the output into a **PDF report**
- Includes **Personality Traits**, **Habits**, **Frustrations**, **Goals**, and **Motivations (with bar graph)**

## Files Included

- `reddit_persona.py` → Main script to run everything (scraping → LLM → PDF)
- `persona_template.html` → Jinja2 HTML template for persona layout
- `.env` → Stores API keys (not pushed)
- `requirements.txt` → Python dependencies

## ⚙️ Setup Instructions

### 1. Clone the Repository
git clone https://github.com/samakshdaksh21/Reddit_Scraper.git
cd Reddit_Scraper

### Install Python Libraries
pip install -r requirements.txt

### Add Your API Keys
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_client_secret
GEMINI_API_KEY=your_google_gemini_key

### How to Run
python reddit_persona.py

### Additionally 
install wkhtmltopdf manually:
Download from: https://wkhtmltopdf.org/downloads.html
