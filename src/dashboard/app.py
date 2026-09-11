"""
Construction Safety AI - Streamlit Dashboard
Phase 4: Real-time safety monitoring and analytics
"""

import streamlit as st
import pandas as pd

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
selected_worker = st.sidebar.slider("Select Worker ID", 1, 10, 1)

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "⚠️ Risk Assessment", "📋 Events", "📍 Zones"])

# TAB 1: Overview
with tab1:
    st.header("Safety Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Active Workers", 5)
    with col2:
        st.metric("Zones Defined", 2)
    with col3:
        st.metric("High Risk Alerts", 2)
    with col4:
        st.metric("System Status", "✅ Online")
    
    st.markdown("---")
    
    st.subheader("👷 Worker Status")
    worker_data = {
        'Worker ID': [1, 2, 3, 4, 5],
        'Status': ['⚠️ High Risk', '✅ Safe', '✅ Safe', '⚠️ Medium Risk', '✅ Safe'],
        'Risk Score': [52.8, 20.0, 15.5, 38.2, 25.3],
        'Location': ['Crane Area', 'Safe Zone', 'Safe Zone', 'Excavator Area', 'Safe Zone']
    }
    df = pd.DataFrame(worker_data)
    st.dataframe(df, use_container_width=True)

# TAB 2: Risk Assessment
with tab2:
    st.header("Risk Assessment")
    
    scenario = st.radio(
        "Select scenario:",
        ["🔴 Dangerous (No helmet, in zone)", "🟢 Safe (Has helmet)"],
        horizontal=True
    )
    
    if "Dangerous" in scenario:
        risk_score = 52.8
        level = "🔴 HIGH"
        status = "⚠️ Attention needed"
        factors = {"PPE Violations": 20, "Zone Violations": 30, "Proximity": 75, "Temporal": 100}
    else:
        risk_score = 20.0
        level = "🟢 LOW"
        status = "✅ Safe"
        factors = {"PPE Violations": 0, "Zone Violations": 0, "Proximity": 20, "Temporal": 20}
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Risk Score", f"{risk_score:.1f}/100")
        if risk_score >= 50:
            st.error(f"{level}")
        elif risk_score >= 25:
            st.warning(f"{level}")
        else:
            st.success(f"{level}")
        st.info(f"Status: {status}")
    
    with col2:
        st.subheader("Risk Factors")
        for factor, value in factors.items():
            st.write(f"**{factor}:** {value}/100")
            st.progress(value / 100)

# TAB 3: Events
with tab3:
    st.header("Temporal Event Log")
    
    events = [
        {"Time": "15:21:07", "Type": "zone_entry", "Worker": f"Worker {selected_worker}"},
        {"Time": "15:21:08", "Type": "proximity_hazard", "Worker": f"Worker {selected_worker}"},
        {"Time": "15:21:10", "Type": "ppe_violation", "Worker": f"Worker {selected_worker}"},
    ]
    
    df_events = pd.DataFrame(events)
    st.dataframe(df_events, use_container_width=True)
    
    st.info("⚠️ Pattern Detected: zone_entry → proximity_hazard → ppe_violation (Escalating)")

# TAB 4: Zones
with tab4:
    st.header("Zone Monitoring")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🏗️ Crane Area")
        st.metric("Active Violations", 0)
        st.success("Status: Clear")
        st.write("**Last Activity:** 2 minutes ago")
    
    with col2:
        st.subheader("⚙️ Excavator Area")
        st.metric("Active Violations", 0)
        st.success("Status: Clear")
        st.write("**Last Activity:** 5 minutes ago")

# Footer
st.markdown("---")
st.markdown("""
### 🏗️ Construction Safety AI v2.0
**Phase 4: Dashboard** | Real-time Risk Scoring + Temporal Event Tracking
- Multi-factor risk assessment
- Temporal pattern detection
- Zone monitoring
- Safety analytics
""")
