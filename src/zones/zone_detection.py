"""
Construction Safety AI - Zone Detection
Phase 2: Detect when tracked objects enter restricted zones
"""

class Zone:
    """Define a restricted zone"""
    
    def __init__(self, zone_id, name, polygon_points):
        self.zone_id = zone_id
        self.name = name
        self.polygon_points = polygon_points  # List of (x, y) coordinates
        self.violations = []
    
    def check_point_in_zone(self, x, y):
        """Check if point (x,y) is inside this zone (simple bounding box)"""
        xs = [p[0] for p in self.polygon_points]
        ys = [p[1] for p in self.polygon_points]
        
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        
        return min_x <= x <= max_x and min_y <= y <= max_y
    
    def log_violation(self, object_id, frame_number):
        """Log a violation when object enters zone"""
        violation = {
            'object_id': object_id,
            'zone_id': self.zone_id,
            'zone_name': self.name,
            'frame': frame_number,
            'timestamp': None
        }
        self.violations.append(violation)
        print(f"⚠️  ZONE VIOLATION: Object {object_id} entered {self.name} at frame {frame_number}")

def create_sample_zones():
    """Create sample restricted zones"""
    
    zones = []
    
    # Zone 1: Crane area (top-left)
    zone1 = Zone(
        zone_id=1,
        name="Crane Area",
        polygon_points=[(50, 50), (250, 50), (250, 200), (50, 200)]
    )
    zones.append(zone1)
    
    # Zone 2: Excavator area (bottom-right)
    zone2 = Zone(
        zone_id=2,
        name="Excavator Area",
        polygon_points=[(400, 300), (600, 300), (600, 480), (400, 480)]
    )
    zones.append(zone2)
    
    return zones

if __name__ == "__main__":
    print("="*60)
    print("📍 Zone Detection - Phase 2")
    print("="*60)
    
    # Create zones
    zones = create_sample_zones()
    
    print(f"\n✅ Created {len(zones)} restricted zones:")
    for zone in zones:
        print(f"  - Zone {zone.zone_id}: {zone.name}")
    
    # Test: Check if a point is in a zone
    test_x, test_y = 100, 100
    for zone in zones:
        if zone.check_point_in_zone(test_x, test_y):
            print(f"\n🎯 Point ({test_x}, {test_y}) is in {zone.name}")
            zone.log_violation(object_id=5, frame_number=10)
