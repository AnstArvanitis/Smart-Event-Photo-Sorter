from deepface import DeepFace
import os
import pickle
import time

# --- CONFIGURATION (PATHS) ---
# Determine the project root directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Define input/output paths
GALLERY_DIR = os.path.join(BASE_DIR, "dataset", "raw_gallery")
DB_FILE = os.path.join(BASE_DIR, "dataset", "faces.pkl")

# AI Model Configuration
MODEL_NAME = "VGG-Face"
DETECTOR_BACKEND = "yunet"  # Lightweight and effective for various angles

def create_index():
    print("------------------------------------------------")
    print(f"🤖 AI INDEXER: Starting process using {MODEL_NAME}...")
    print(f"📂 Source Directory: {GALLERY_DIR}")
    print("------------------------------------------------")

    # Check if directory exists
    if not os.path.exists(GALLERY_DIR):
        print(f"❌ ERROR: Directory '{GALLERY_DIR}' not found!")
        return

    faces_database = []
    
    # Get all files
    files = os.listdir(GALLERY_DIR)
    # Filter for valid image formats
    valid_images = [f for f in files if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    print(f"📊 Found {len(valid_images)} images. Starting analysis...\n")
    start_time = time.time()

    for i, filename in enumerate(valid_images):
        path = os.path.join(GALLERY_DIR, filename)
        print(f"[{i+1}/{len(valid_images)}] 📸 Processing: {filename}...", end=" ")

        try:
            # Generate Embeddings using DeepFace
            embeddings = DeepFace.represent(
                img_path=path, 
                model_name=MODEL_NAME, 
                detector_backend=DETECTOR_BACKEND,
                enforce_detection=False
            )

            if embeddings:
                for face in embeddings:
                    # Store filename and vector embedding
                    faces_database.append({
                        "filename": filename,
                        "embedding": face["embedding"]
                    })
                print("✅ OK")
            else:
                print("⚠️ No face detected")

        except Exception as e:
            print(f"❌ Error: {e}")

    # Save to Pickle file
    print("\n💾 Saving database to disk...")
    with open(DB_FILE, 'wb') as f:
        pickle.dump(faces_database, f)

    total_time = time.time() - start_time
    print("\n------------------------------------------------")
    print(f"🎉 INDEXING COMPLETE!")
    print(f"⏱️ Time elapsed: {total_time:.2f} seconds")
    print(f"📁 Database file: {DB_FILE}")
    print("------------------------------------------------")

if __name__ == "__main__":
    create_index()