"""
Construction Safety AI - Live Dashboard
Phase 5: Real-time display with live CV data
"""

import streamlit as st
import pandas as pd
import json
from pathlib import Path

# Set page config
st.set_page_config(
    page_title="Construction Safety AI",
    page_icon="🏗️",
    layout="wide"
)

# Title
st.title("🏗️ Construction Safety Monitoring Dashboard")
st.markdown("**Real-time safety assessment with AI-powered risk scoring**")

# Sidebar
st.sidebar.header("⚙️ Configuration")

# Try to load latest results
results_file = Path('latest_results.json')

if results_file.exists():
    with open(results_file) as f:
        results = json.load(f)
    
    st.sidebar.success("✅ Live data loaded!")
    
    # Extract data
    detections = results['detections']
    risk_data = results['risk_assessment']
    metrics = results['metrics']
    frame_info = results['frame_info']
    
else:
    st.sidebar.warning("⚠️ No live data available")
    results = None

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "⚠️ Risk Assessment", "📋 Detections", "📍 Metrics"])

# TAB 1: Overview
with tab1:
    st.header("Live Safety Overview")
    
    if results:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Detections", metrics['total_objects'])
        
        with col2:
            st.metric("Persons Detected", metrics['persons'])
        
        with col3:
            st.metric("Equipment Detected", metrics['equipment'])
        
        with col4:
            st.metric("Inference Time", metrics['inference_time'])
        
        st.markdown("---")
        
        # Detection breakdown
        st.subheader("👷 Detection Breakdown")
        
        detection_summary = {}
        for det in detections:
            cls = det['class']
            detection_summary[cls] = detection_summary.get(cls, 0) + 1
        
        df_summary = pd.DataFrame([
            {'Class': k, 'Count': v, 'Confidence': 'High'} 
            for k, v in detection_summary.items()
        ])
        
        st.dataframe(df_summary, use_container_width=True)
    
    else:
        st.info("📊 No live data available. Run the processor first.")

# TAB 2: Risk Assessment
with tab2:
    st.header("⚠️ Risk Assessment (Live)")
    
    if results:
        risk_score = risk_data['score']
        risk_level = risk_data['level']
        factors = risk_data['factors']
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Risk Score", f"{risk_score:.1f}/100")
            
            # Color-coded level
            if risk_score >= 75:
                st.error(f"🔴 CRITICAL")
            elif risk_score >= 50:
                st.warning(f"🔴 HIGH")
            elif risk_score >= 25:
                st.info(f"🟡 MEDIUM")
            else:
                st.success(f"🟢 LOW")
        
        with col2:
            st.subheader("Risk Factors")
            for factor, value in factors.items():
                st.write(f"**{factor.upper()}:** {value:.1f}/100")
                st.progress(value / 100)
    
    else:
        st.info("⚠️ No risk data available yet.")

# TAB 3: Detections
with tab3:
    st.header("📋 Detected Objects")
    
    if results:
        df_detections = pd.DataFrame([
            {
                'Class': d['class'],
                'Confidence': f"{d['confidence']:.2f}",
                'BBox': f"({d['bbox'][0]:.0f}, {d['bbox'][1]:.0f}, {d['bbox'][2]:.0f}, {d['bbox'][3]:.0f})"
            }
            for d in detections
        ])
        
        st.dataframe(df_detections, use_container_width=True)
    
    else:
        st.info("📋 No detections yet.")

# TAB 4: Metrics
with tab4:
    st.header("📊 System Metrics")
    
    if results:
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Image Info**")
            st.write(f"File: {frame_info['image']}")
            st.write(f"Total Detections: {frame_info['detection_count']}")
            st.write(f"Persons: {frame_info['person_count']}")
            st.write(f"Equipment: {frame_info['equipment_count']}")
        
        with col2:
            st.write("**Performance**")
            st.write(f"Inference Time: {metrics['inference_time']}")
            st.write(f"FPS: {metrics['fps']}")
        
        # Risk summary
        st.write("**Risk Summary**")
        st.write(f"Score: {risk_data['score']:.1f}/100")
        st.write(f"Level: {risk_data['level']}")
    
    else:
        st.info("📊 No metrics available.")

# Footer
st.markdown("---")
st.markdown("""
**Construction Safety AI v3.0** | Phase 5: Live CV Pipeline
- Real-time detection & tracking
- Multi-factor risk scoring
- Live dashboard with real data
""")
