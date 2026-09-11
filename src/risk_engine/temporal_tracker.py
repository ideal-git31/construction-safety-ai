"""
Construction Safety AI - Temporal Event Tracker
Phase 3: Track event sequences and patterns over time
"""

from datetime import datetime

class TemporalEvent:
    """Single event with timestamp"""
    
    def __init__(self, event_type, object_id, details):
        self.timestamp = datetime.now()
        self.event_type = event_type
        self.object_id = object_id
        self.details = details
    
    def __str__(self):
        return f"[{self.timestamp.strftime('%H:%M:%S')}] {self.event_type} - Object {self.object_id}: {self.details}"

class TemporalEventTracker:
    """Track event sequences and detect patterns"""
    
    def __init__(self):
        print("="*60)
        print("⏱️  Temporal Event Tracker - Phase 3")
        print("="*60)
        
        self.events = []
        self.event_sequences = {}  # Track sequences per object
    
    def log_event(self, event_type, object_id, details):
        """Log a new event"""
        event = TemporalEvent(event_type, object_id, details)
        self.events.append(event)
        
        # Track sequences per object
        if object_id not in self.event_sequences:
            self.event_sequences[object_id] = []
        self.event_sequences[object_id].append(event)
        
        print(f"✓ {event}")
    
    def get_object_sequence(self, object_id):
        """Get event sequence for specific object"""
        return self.event_sequences.get(object_id, [])
    
    def detect_escalation_pattern(self, object_id):
        """Detect if events are escalating (high-risk pattern)"""
        sequence = self.get_object_sequence(object_id)
        
        if len(sequence) < 2:
            return False, "Not enough events"
        
        # Check for escalation: zone → proximity → ppe violation
        event_types = [e.event_type for e in sequence[-3:]]  # Last 3 events
        
        escalating_patterns = [
            ['zone_entry', 'proximity_hazard', 'ppe_violation'],
            ['zone_entry', 'proximity_hazard'],
            ['proximity_hazard', 'ppe_violation'],
        ]
        
        for pattern in escalating_patterns:
            if all(et in event_types for et in pattern):
                return True, f"Escalating pattern detected: {' → '.join(pattern)}"
        
        return False, "No escalation pattern"
    
    def get_violation_duration(self, object_id):
        """Calculate how long object has been violating rules"""
        sequence = self.get_object_sequence(object_id)
        
        if len(sequence) < 1:
            return 0
        
        first_event = sequence[0].timestamp
        last_event = sequence[-1].timestamp
        
        duration = (last_event - first_event).total_seconds()
        return duration
    
    def print_event_summary(self):
        """Print summary of all events and patterns"""
        print("\n" + "-"*60)
        print("📋 Temporal Event Summary")
        print("-"*60)
        
        print(f"\n✅ Total Events Logged: {len(self.events)}")
        
        # Summary per object
        for object_id, events in self.event_sequences.items():
            print(f"\n🎯 Object {object_id}:")
            print(f"   Events: {len(events)}")
            
            # Check for escalation
            is_escalating, pattern = self.detect_escalation_pattern(object_id)
            if is_escalating:
                print(f"   ⚠️  {pattern}")
            
            # Violation duration
            duration = self.get_violation_duration(object_id)
            print(f"   Duration: {duration:.1f} seconds")

if __name__ == "__main__":
    # Test the temporal tracker
    tracker = TemporalEventTracker()
    
    print("\n📋 Simulating Event Sequence for Worker #5")
    print("-"*60)
    
    # Simulate escalating sequence
    tracker.log_event("zone_entry", 5, "Entered crane area")
    tracker.log_event("proximity_hazard", 5, "2 meters from equipment")
    tracker.log_event("ppe_violation", 5, "Missing helmet detected")
    
    # Print summary
    tracker.print_event_summary()
    
    # Detect pattern
    is_escalating, pattern = tracker.detect_escalation_pattern(5)
    print(f"\n{'🚨' if is_escalating else '✓'} Pattern Detection: {pattern}")
