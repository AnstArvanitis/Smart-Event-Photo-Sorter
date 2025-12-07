from deepface import DeepFace
import pickle
import os
import shutil
from scipy.spatial.distance import cosine

# --- CONFIGURATION (PATHS) ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DB_FILE = os.path.join(BASE_DIR, "dataset", "faces.pkl")
TARGET_IMG_DIR = os.path.join(BASE_DIR, "dataset", "target")
# Target image is named 'target.jpg' inside the target folder
TARGET_IMG = os.path.join(TARGET_IMG_DIR, "target.jpg")

SOURCE_DIR = os.path.join(BASE_DIR, "dataset", "raw_gallery")
OUTPUT_DIR = os.path.join(BASE_DIR, "found_photos")

# AI Settings
MODEL_NAME = "VGG-Face"
DETECTOR_BACKEND = "yunet"
THRESHOLD = 0.7 # Adjust based on testing (lower is stricter)

def find_my_photos():
    print("------------------------------------------------")
    print("🔎 AI SEARCHER: Looking for target...")
    print("------------------------------------------------")

    # 1. Validation Checks
    if not os.path.exists(DB_FILE):
        print("❌ ERROR: Database file (faces.pkl) not found. Run indexer.py first!")
        return
    
    if not os.path.exists(TARGET_IMG):
        print(f"❌ ERROR: Target image not found at: {TARGET_IMG}")
        return

    # 2. Load Database
    print("📚 Loading database...")
    with open(DB_FILE, 'rb') as f:
        database = pickle.load(f)
    print(f"✅ Loaded {len(database)} face encodings.")

    # 3. Analyze Target Image
    print(f"🎯 Analyzing target: {TARGET_IMG}")
    try:
        target_objs = DeepFace.represent(
            img_path=TARGET_IMG, 
            model_name=MODEL_NAME, 
            detector_backend=DETECTOR_BACKEND,
            enforce_detection=True
        )
        # Take the first face found in target image
        target_embedding = target_objs[0]["embedding"]
        print("✅ Target face analyzed successfully.")
    except Exception as e:
        print(f"❌ ERROR: Could not detect face in target image. Details: {e}")
        return

    # 4. Compare & Extract
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    
    print("\n🚀 Starting comparison...")
    found_count = 0
    processed_files = set() 

    for entry in database:
        filename = entry["filename"]
        db_embedding = entry["embedding"]

        # Calculate Cosine Distance
        distance = cosine(target_embedding, db_embedding)

        # Check if match is within threshold
        if distance < THRESHOLD:
            if filename not in processed_files:
                print(f"✅ MATCH FOUND! -> {filename} (Score: {distance:.3f})")
                
                # Copy file to output folder
                src_path = os.path.join(SOURCE_DIR, filename)
                dst_path = os.path.join(OUTPUT_DIR, filename)
                shutil.copy(src_path, dst_path)
                
                processed_files.add(filename)
                found_count += 1

    print("------------------------------------------------")
    print(f"🎉 FINISHED! Found {found_count} matching photos.")
    print(f"📁 Output Folder: {OUTPUT_DIR}")
    print("------------------------------------------------")

if __name__ == "__main__":
    find_my_photos()