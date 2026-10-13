"""
Construction Safety AI - Video Processor
Phase 5: Real-time video processing with integrated CV pipeline
"""

import cv2
import numpy as np
from ultralytics import YOLO
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.zones.zone_detection import create_sample_zones
from src.risk_engine.risk_scorer import RiskScorer
from src.risk_engine.temporal_tracker import TemporalEventTracker

class VideoProcessor:
    """Process video frames with detection, tracking, and risk scoring"""
    
    def __init__(self, model_path):
        print("="*70)
        print("🎬 Video Processor - Phase 5")
        print("="*70)
        
        # Load model
        print("\n📦 Loading trained model...")
        self.model = YOLO(model_path)
        
        # Initialize systems
        print("📍 Loading zones...")
        self.zones = create_sample_zones()
        
        print("⚠️  Initializing risk scorer...")
        self.risk_scorer = RiskScorer()
        
        print("⏱️  Initializing temporal tracker...")
        self.temporal_tracker = TemporalEventTracker()
        
        # Tracking dictionary
        self.tracked_objects = {}
        
        print("\n✅ System initialized!")
    
    def process_frame(self, frame, frame_num):
        """Process a single frame"""
        
        # Run YOLO detection
        results = self.model(frame, conf=0.5)
        
        # Extract detections
        detections = []
        for r in results:
            for box in r.boxes:
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                conf = box.conf[0].cpu().numpy()
                cls = int(box.cls[0].cpu().numpy())
                class_name = r.names[cls]
                
                detections.append({
                    'bbox': (x1, y1, x2, y2),
                    'conf': conf,
                    'class': class_name
                })
        
        # Simple tracking
        self.update_tracking(detections, frame_num)
        
        # Draw detections
        annotated_frame = self.draw_detections(frame, detections)
        
        return annotated_frame, detections
    
    def update_tracking(self, detections, frame_num):
        """Simple object tracking by proximity"""
        
        new_tracked = {}
        
        for det in detections:
            x1, y1, x2, y2 = det['bbox']
            cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
            
            # Find closest existing track
            closest_id = None
            min_dist = 50
            
            for obj_id, obj_data in self.tracked_objects.items():
                old_cx, old_cy = obj_data['center']
                dist = np.sqrt((cx - old_cx)**2 + (cy - old_cy)**2)
                
                if dist < min_dist:
                    closest_id = obj_id
                    min_dist = dist
            
            # Assign ID
            if closest_id is not None:
                obj_id = closest_id
            else:
                obj_id = max([int(k) for k in self.tracked_objects.keys()] + [0]) + 1
            
            new_tracked[str(obj_id)] = {
                'center': (cx, cy),
                'bbox': det['bbox'],
                'class': det['class'],
                'conf': det['conf'],
                'frame': frame_num
            }
        
        self.tracked_objects = new_tracked
    
    def draw_detections(self, frame, detections):
        """Draw bounding boxes and labels on frame"""
        
        annotated = frame.copy()
        
        for det in detections:
            x1, y1, x2, y2 = det['bbox']
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            
            cv2.rectangle(annotated, (x1, y1), (x2, y2), (0, 255, 0), 2)
            label = f"{det['class']} {det['conf']:.2f}"
            cv2.putText(annotated, label, (x1, y1-10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        return annotated
    
    def process_image(self, image_path):
        """Process single image"""
        
        print(f"\n🖼️  Processing image: {image_path}")
        
        frame = cv2.imread(image_path)
        
        if frame is None:
            print("❌ Error: Could not load image")
            return []
        
        # Process frame
        annotated_frame, detections = self.process_frame(frame, 0)
        
        print(f"✅ Image processing complete!")
        print(f"  - Detections: {len(detections)}")
        
        return detections
    
    def process_video(self, video_path, output_path=None):
        """Process entire video file"""
        
        print(f"\n🎥 Processing video: {video_path}")
        
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            print("❌ Error: Could not open video")
            return
        
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        print(f"  - Resolution: {width}x{height}")
        print(f"  - FPS: {fps}")
        print(f"  - Total frames: {total_frames}")
        
        if output_path:
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        frame_num = 0
        
        while True:
            ret, frame = cap.read()
            
            if not ret:
                break
            
            frame_num += 1
            if frame_num % 5 != 0:
                continue
            
            try:
                annotated_frame, detections = self.process_frame(frame, frame_num)
                
                if output_path:
                    out.write(annotated_frame)
                
                if frame_num % 50 == 0:
                    print(f"  ✓ Frame {frame_num}/{total_frames}")
                
            except Exception as e:
                print(f"  ⚠️  Error processing frame {frame_num}: {e}")
                continue
        
        cap.release()
        if output_path:
            out.release()
        
        print(f"\n✅ Video processing complete!")
        print(f"  - Processed {frame_num} frames")
        print(f"  - Tracked {len(self.tracked_objects)} objects")
        
        return self.tracked_objects
