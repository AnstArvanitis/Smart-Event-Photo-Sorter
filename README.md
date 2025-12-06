# 📸 Smart Event Photo Sorter

A Python tool I built to solve a real problem: **finding my graduation photos among 11,000 other images.**

Instead of scrolling for hours, I wrote this script to automate the process using **Face Recognition**.

## 💡 The Story (Why I built this)

After my graduation, the photographers gave us access to a huge folder with thousands of unsorted photos. Finding myself was a nightmare.
I realized this was a perfect opportunity to use Python and Computer Vision to save time—not just for me, but for anyone in a similar situation.

## 🚀 What it does

* **It scans the crowd:** Reads through a folder of mixed photos.
* **It learns your face:** Takes one selfie as a reference.
* **It finds matches:** Automatically copies every photo you appear in into a new folder.

## 🛠️ Tech Stack

* **Python 3**
* **DeepFace** (for face recognition logic)
* **Pickle** (for saving the data)
* **OpenCV & YuNet** (for detecting faces in crowds)

## ⚙️ Project Structure

```text
Smart-Event-Photo-Sorter/
│
├── src/
│   ├── indexer.py    # Analyzes the photos and saves the data
│   └── searcher.py   # Finds the specific person
│
├── dataset/          # Where the photos go
├── found_photos/     # Where the results appear
├── requirements.txt
└── README.md
📥 How to run it
Clone the repo:

Bash

git clone https://github.com/AnstArvanitis/Smart-Event-Photo-Sorter.git
Install requirements:

Bash

pip install -r requirements.txt
Step 1: Indexing (Run this once) Put the event photos in dataset/raw_gallery and run:

Bash

python src/indexer.py
This creates a faces.pkl file so we don't have to scan images every time.

Step 2: Searching Put your selfie in dataset/target/target.jpg and run:

Bash

python src/searcher.py
Check the found_photos folder for results!

🧠 Challenges & What I Learned
During this project, I faced some interesting technical challenges:

1. Speed vs. Accuracy
Scanning 11,000 photos takes a long time.

My Solution: I split the code into two parts. The Indexer runs once and saves the face data into a file (pickle). The Searcher just reads that file. This makes searching instant!

2. Detecting Faces in Crowds
At first, I used the default OpenCV detector, but it missed faces that were turned sideways or far away.

My Solution: I switched to YuNet, a modern deep-learning detector which is much better at finding faces in difficult angles.

3. Privacy
Since these are personal photos, I didn't want to upload them to any cloud API.

My Solution: Everything runs locally on the computer. No data leaves the machine.

Created by Anastasis - Junior Python Developer.