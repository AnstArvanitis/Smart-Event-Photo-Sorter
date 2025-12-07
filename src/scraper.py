from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import requests
import os
import time
import base64
import shutil

# --- CONFIGURATION ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOWNLOAD_DIR = os.path.join(BASE_DIR, "dataset", "raw_gallery")

# SMART SEARCH QUERIES
# We target "Interview" and "Close up" to avoid sunglasses/obstructions
SEARCH_QUERIES = [
    "Leonardo DiCaprio Interview Close up",  # TARGET: Clear face, no sunglasses
    "Leonardo DiCaprio Oscars Stage",        # TARGET: Good lighting
    "Brad Pitt Interview",                   # NOISE: Similar looking actor
    "Red Carpet Crowd"                       # NOISE: Multiple faces/chaos
]

LIMIT_PER_QUERY = 5  # Total approx 20 images

def download_images():
    print("------------------------------------------------")
    print(f"🕷️ SMART SCRAPER: Initializing...")
    print("------------------------------------------------")

    # Clean up previous data for a fresh start
    if os.path.exists(DOWNLOAD_DIR):
        try:
            shutil.rmtree(DOWNLOAD_DIR)
            # Brief pause to ensure the OS releases file locks before recreating the directory
            time.sleep(1)
        except:
            pass
    
    if not os.path.exists(DOWNLOAD_DIR):
        os.makedirs(DOWNLOAD_DIR)

    # Browser Setup
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless") # Uncomment to run in background
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    global_count = 0 

    for query in SEARCH_QUERIES:
        print(f"\n🔎 Searching for: '{query}'...")
        
        # DuckDuckGo Images (Less strict on bot detection)
        url = f"https://duckduckgo.com/?q={query}&t=h_&iax=images&ia=images"
        driver.get(url)
        
        # Scroll to trigger lazy loading
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, 1000);")
        time.sleep(2)

        # Find all images
        images = driver.find_elements(By.TAG_NAME, "img")
        
        count = 0
        for img in images:
            if count >= LIMIT_PER_QUERY:
                break
            
            try:
                # Filter out small icons/thumbnails
                if img.size['width'] < 150 or img.size['height'] < 150:
                    continue

                src = img.get_attribute('src')
                if not src: continue

                # Download logic
                # Handle two types of image sources:
                # 1. Standard HTTP URLs (download via requests)
                # 2. Base64 Encoded Images (embedded data, needs decoding)
                img_data = None
                if src.startswith('http'):
                    response = requests.get(src, timeout=5)
                    if response.status_code == 200:
                        # Use .content to get raw bytes (binary data). 
                        # .text would attempt to decode it as a string, corrupting the image file.
                        img_data = response.content
                elif src.startswith('data:image'):
                    # Base64 images are embedded directly in the HTML as text strings.
                    # We split the metadata header (e.g., "data:image/jpeg;base64") from the actual encoded data.
                    header, encoded = src.split(",", 1)
                    
                    # Convert the Base64 ASCII string back into binary image data (bytes).
                    img_data = base64.b64decode(encoded)

                if img_data:
                    # Create readable filename (e.g., leonardo_0.jpg)
                    prefix = query.split()[0].lower()
                    filename = f"{prefix}_{global_count}.jpg"
                    file_path = os.path.join(DOWNLOAD_DIR, filename)
                    
                    with open(file_path, 'wb') as f:
                        f.write(img_data)
                    
                    print(f"   ⬇️ Downloaded: {filename}")
                    count += 1
                    global_count += 1

            except Exception:
                pass

    driver.quit()
    print("\n------------------------------------------------")
    print(f"✅ SCRAPING COMPLETE! Total images: {global_count}")
    print(f"📁 Location: {DOWNLOAD_DIR}")
    print("------------------------------------------------")

if __name__ == "__main__":
    download_images()