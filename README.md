# 📸 Smart Event Photo Sorter

A Python tool I built to solve a real problem: **finding my graduation photos among 11,000 other images.**

Instead of scrolling for hours, I wrote this script to automate the process using **Face Recognition**. I also built an automated **Web Scraper** to gather test datasets efficiently.

## 💡 The Story (Why I built this)

After my graduation, the photographers gave us access to a huge folder with thousands of unsorted photos. Finding myself was a nightmare.
I realized this was a perfect opportunity to use Python and Computer Vision to save time—not just for me, but for anyone in a similar situation.

To stress-test my solution without violating privacy, I built a custom **Web Scraper** to collect celebrity datasets (e.g., Red Carpet events) and simulate the "finding a needle in a haystack" scenario.

## 🚀 What it does

1.  **The Collector (Scraper):** Automatically downloads images from the web to build a dataset.
2.  **The Indexer:** Scans the crowd and creates a biometric database.
3.  **The Searcher:** Takes one selfie and finds all matches in seconds.

## 🛠️ Tech Stack

* **Python 3**
* **Selenium & WebDriver** (for Web Scraping & Automation)
* **DeepFace & OpenCV** (for Computer Vision logic)
* **YuNet** (High-performance Face Detection)
* **Pickle** (for Data Serialization)

## ⚙️ Project Structure

```text
Smart-Event-Photo-Sorter/
│
├── src/
│   ├── scraper.py    # (NEW) Automates image collection from the web
│   ├── indexer.py    # Analyzes the photos and builds the database
│   └── searcher.py   # Finds the specific person
│
├── dataset/          # Where the photos go
├── found_photos/     # Where the results appear
├── requirements.txt
└── README.md
📥 How to run it
1. Clone the repo:

Bash

git clone https://github.com/AnstArvanitis/Smart-Event-Photo-Sorter.git

2. Install requirements:

Bash

pip install -r requirements.txt
3. Step 1: Collection (Optional) If you don't have photos, let the bot gather them for you:

Bash

python src/scraper.py
Downloads images to dataset/raw_gallery.

4. Step 2: Indexing (The Heavy Lifting) Run the indexer to analyze the gallery:

Bash

python src/indexer.py
Creates a faces.pkl file for instant lookups later.

5. Step 3: Searching Put your selfie in dataset/target/target.jpg and run:

Bash

python src/searcher.py
✅ Result: Check the found_photos folder!

🧠 Challenges & What I Learned
During this project, I faced some interesting technical challenges:

1. Data Collection & Lazy Loading
Websites often don't load all images at once.

Problem: My scraper only found the first 10 images.

Solution: I implemented a Selenium script that simulates user scrolling (window.scrollTo) to trigger lazy loading and capture high-quality images dynamically.

2. Speed vs. Accuracy
Scanning thousands of photos takes a long time.

Solution: I split the architecture. The Indexer runs once and saves data to a binary file. The Searcher runs instantly .

3. Detecting Faces in Crowds
Standard detection methods failed on side-profiles or crowded shots.

Solution: I integrated YuNet, a modern deep-learning detector within DeepFace, which significantly improved detection rates in challenging angles.

Created by Anastasis - Junior Python Developer.