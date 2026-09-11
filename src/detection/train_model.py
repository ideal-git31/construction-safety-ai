"""
Construction Safety AI - Model Training Script
Phase 1: Train baseline object detection model
"""

from ultralytics import YOLO
import sys

def train_model():
    """Train YOLOv8n on Construction-PPE dataset"""
    
    print("="*60)
    print("🚀 Construction Safety AI - Model Training")
    print("="*60)
    
    # Load pre-trained model
    print("\n📦 Loading YOLOv8n pre-trained model...")
    model = YOLO('yolov8n.pt')
    
    # Train on Construction-PPE dataset
    print("🎯 Starting training on Construction-PPE dataset...")
    results = model.train(
        data='coco8.yaml',  # Will auto-download dataset
        epochs=50,
        imgsz=640,
        batch=16,
        device='mps',
        patience=20,
        save=True,
        project='models/trained',
        name='construction_ppe_v1'
    )
    
    print("\n✅ Training complete!")
    print(f"Model saved to: models/trained/construction_ppe_v1/weights/best.pt")
    
    return results

if __name__ == "__main__":
    train_model()
