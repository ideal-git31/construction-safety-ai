"""
Construction Safety AI - Phase 3 Complete System
Combines: Risk Scoring + Temporal Events + Tracking + Zones (MAIN NOVELTY)
"""

from ultralytics import YOLO
from src.zones.zone_detection import create_sample_zones
from src.risk_engine.risk_scorer import RiskScorer
from src.risk_engine.temporal_tracker import TemporalEventTracker

class SafetyAssessmentSystem:
    """Complete Phase 3 safety assessment system with risk scoring"""
    
    def __init__(self, model_path):
        print("="*70)
        print("🏗️  Construction Safety AI - Phase 3 Complete System")
        print("="*70)
        
        # Load model
        print("\n📦 Loading trained model...")
        self.model = YOLO(model_path)
        
        # Load zones
        print("📍 Loading restricted zones...")
        self.zones = create_sample_zones()
        
        # Initialize risk scorer
        print("⚠️  Initializing risk scoring engine...")
        self.risk_scorer = RiskScorer()
        
        # Initialize temporal tracker
        print("⏱️  Initializing temporal event tracker...")
        self.temporal_tracker = TemporalEventTracker()
        
        print("\n✅ System initialized!")
        print(f"   - Model: YOLOv8n (trained)")
        print(f"   - Zones: {len(self.zones)}")
        print(f"   - Risk Factors: 4 (PPE, Zone, Proximity, Temporal)")
        print(f"   - Pattern Detection: Enabled")
    
    def analyze_worker(self, worker_id, has_helmet=False, in_zone=False, proximity_cm=100):
        """Analyze worker safety status"""
        
        print(f"\n🔍 Analyzing Worker {worker_id}...")
        print("-"*70)
        
        # Log temporal events
        if not has_helmet:
            self.temporal_tracker.log_event("ppe_violation", worker_id, "Missing helmet")
        
        if in_zone:
            self.temporal_tracker.log_event("zone_entry", worker_id, "In restricted zone")
        
        if proximity_cm < 200:
            self.temporal_tracker.log_event("proximity_hazard", worker_id, f"Too close to equipment ({proximity_cm}cm)")
        
        # Calculate risk
        self.risk_scorer.set_ppe_risk(1 if not has_helmet else 0)
        self.risk_scorer.set_zone_risk(1 if in_zone else 0)
        self.risk_scorer.set_proximity_risk(proximity_cm)
        self.risk_scorer.set_temporal_risk(30)  # 30 seconds duration
        
        risk_score = self.risk_scorer.calculate_total_risk()
        risk_level = self.risk_scorer.get_risk_level()
        risk_color = self.risk_scorer.get_risk_color()
        
        # Detect pattern escalation
        is_escalating, pattern = self.temporal_tracker.detect_escalation_pattern(worker_id)
        
        # Print assessment
        print(f"\n📊 Safety Assessment for Worker {worker_id}:")
        print(f"   - Helmet: {'✓ Yes' if has_helmet else '✗ No'}")
        print(f"   - Zone Status: {'In restricted zone' if in_zone else 'Safe area'}")
        print(f"   - Proximity: {proximity_cm}cm from equipment")
        print(f"   - Risk Score: {risk_score:.1f}/100")
        print(f"   - Risk Level: {risk_color} {risk_level}")
        
        if is_escalating:
            print(f"   - ⚠️  ESCALATION DETECTED: {pattern}")
        
        return risk_score, risk_level
    
    def generate_full_report(self):
        """Generate comprehensive safety report"""
        
        print("\n" + "="*70)
        print("📋 PHASE 3 COMPLETE SAFETY REPORT")
        print("="*70)
        
        # Risk Summary
        print("\n⚠️  RISK ASSESSMENT:")
        print(f"   - Total Risk Score: {self.risk_scorer.total_risk_score:.1f}/100")
        print(f"   - Risk Level: {self.risk_scorer.get_risk_color()} {self.risk_scorer.get_risk_level()}")
        
        # Events Summary
        print(f"\n📋 TEMPORAL EVENTS:")
        print(f"   - Total Events Logged: {len(self.temporal_tracker.events)}")
        
        for obj_id, events in self.temporal_tracker.event_sequences.items():
            print(f"   - Worker {obj_id}: {len(events)} events")
            
            is_escalating, pattern = self.temporal_tracker.detect_escalation_pattern(obj_id)
            if is_escalating:
                print(f"     ⚠️  Pattern: {pattern}")
        
        # Zones Summary
        print(f"\n📍 ZONES MONITORED:")
        for zone in self.zones:
            print(f"   - {zone.name}: {len(zone.violations)} violations")
        
        print("\n" + "="*70)
        print("✅ PHASE 3 SYSTEM COMPLETE")
        print("="*70)

if __name__ == "__main__":
    # Initialize system
    system = SafetyAssessmentSystem('models/trained/construction_ppe_v1_best.pt')
    
    # Analyze different worker scenarios
    print("\n" + "🎯 SCENARIO 1: Dangerous (No helmet, in zone, close to equipment)")
    system.analyze_worker(worker_id=1, has_helmet=False, in_zone=True, proximity_cm=100)
    
    print("\n" + "🎯 SCENARIO 2: Safe (Has helmet, safe area, far from equipment)")
    system.analyze_worker(worker_id=2, has_helmet=True, in_zone=False, proximity_cm=800)
    
    # Generate full report
    system.generate_full_report()
