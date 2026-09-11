"""
Construction Safety AI - Risk Scoring Engine
Phase 3: Multi-factor risk assessment (MAIN NOVELTY)
"""

class RiskScorer:
    """Calculate risk score from multiple safety factors"""
    
    def __init__(self):
        print("="*60)
        print("⚠️  Risk Scoring Engine - Phase 3")
        print("="*60)
        
        # Risk factors and their weights
        self.risk_factors = {
            'ppe_violations': {'weight': 0.25, 'value': 0},      # 25%
            'zone_violations': {'weight': 0.30, 'value': 0},     # 30%
            'proximity_hazard': {'weight': 0.25, 'value': 0},    # 25%
            'temporal_escalation': {'weight': 0.20, 'value': 0}, # 20%
        }
        
        self.total_risk_score = 0
    
    def set_ppe_risk(self, num_violations):
        """Set PPE violation risk (0-100)"""
        # Each violation adds risk
        self.risk_factors['ppe_violations']['value'] = min(num_violations * 20, 100)
    
    def set_zone_risk(self, num_violations):
        """Set zone violation risk (0-100)"""
        # Each zone violation adds risk
        self.risk_factors['zone_violations']['value'] = min(num_violations * 30, 100)
    
    def set_proximity_risk(self, distance_cm):
        """Set proximity risk based on distance to equipment (0-100)"""
        # Closer distance = higher risk
        if distance_cm < 100:  # < 1 meter
            self.risk_factors['proximity_hazard']['value'] = 100
        elif distance_cm < 300:  # 1-3 meters
            self.risk_factors['proximity_hazard']['value'] = 75
        elif distance_cm < 500:  # 3-5 meters
            self.risk_factors['proximity_hazard']['value'] = 50
        else:
            self.risk_factors['proximity_hazard']['value'] = 0
    
    def set_temporal_risk(self, violation_duration_seconds):
        """Set temporal escalation risk based on how long violation persists"""
        # Longer violations = higher risk
        self.risk_factors['temporal_escalation']['value'] = min(violation_duration_seconds * 5, 100)
    
    def calculate_total_risk(self):
        """Calculate weighted total risk score (0-100)"""
        total = 0
        for factor_name, factor_data in self.risk_factors.items():
            weighted_value = factor_data['value'] * factor_data['weight']
            total += weighted_value
        
        self.total_risk_score = total
        return round(total, 2)
    
    def get_risk_level(self):
        """Determine risk level based on score"""
        score = self.total_risk_score
        
        if score >= 75:
            return "CRITICAL"
        elif score >= 50:
            return "HIGH"
        elif score >= 25:
            return "MEDIUM"
        else:
            return "LOW"
    
    def get_risk_color(self):
        """Return color for visualization"""
        level = self.get_risk_level()
        colors = {
            'LOW': '🟢',
            'MEDIUM': '🟡',
            'HIGH': '🔴',
            'CRITICAL': '🔴🔴'
        }
        return colors.get(level, '⚪')
    
    def print_risk_assessment(self):
        """Print detailed risk assessment"""
        print("\n" + "-"*60)
        print("📊 Risk Assessment Report")
        print("-"*60)
        
        # Print each factor
        for factor_name, factor_data in self.risk_factors.items():
            print(f"\n{factor_name.upper().replace('_', ' ')}")
            print(f"  Value: {factor_data['value']:.1f}/100")
            print(f"  Weight: {factor_data['weight']*100:.0f}%")
            print(f"  Contribution: {factor_data['value'] * factor_data['weight']:.1f}")
        
        # Print total
        print("\n" + "="*60)
        print(f"TOTAL RISK SCORE: {self.total_risk_score:.1f}/100")
        print(f"RISK LEVEL: {self.get_risk_color()} {self.get_risk_level()}")
        print("="*60)

if __name__ == "__main__":
    # Test the risk scorer
    scorer = RiskScorer()
    
    # Simulate a dangerous scenario
    print("\n📋 Test Scenario: Worker in crane area without helmet")
    scorer.set_ppe_risk(1)           # Missing helmet
    scorer.set_zone_risk(1)          # In restricted zone
    scorer.set_proximity_risk(150)   # 1.5 meters from crane
    scorer.set_temporal_risk(30)     # Been there for 30 seconds
    
    # Calculate and print
    scorer.calculate_total_risk()
    scorer.print_risk_assessment()
