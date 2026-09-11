"""
Construction Safety AI - Object Tracking
Phase 2: Track objects across frames with unique IDs
"""

from ultralytics import YOLO

def track_video(source):
    """Track objects in video/images with unique IDs"""
    
    print("="*60)
    print("🎯 Object Tracking - Phase 2")
    print("="*60)
    
    # Load your trained model
    print("\n📦 Loading trained model...")
    model = YOLO('models/trained/construction_ppe_v1_best.pt')
    
    # Run tracking
    print(f"\n🎯 Tracking objects in: {source}")
    results = model.track(source=source, conf=0.5, persist=True)
    
    # Summary
    print(f"\n✅ Tracking complete!")
    print(f"Processed {len(results)} frames")
    
    return results

if __name__ == "__main__":
    # Test with YOLO's sample image
    results = track_video('https://ultralytics.com/images/bus.jpg')
