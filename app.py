# app.py
import streamlit as st
import pandas as pd
import plotly.express as px

# Mock database remains unchanged

# Page configuration
st.set_page_config(page_title="ChainAI Audit System Demo", layout="wide")

# Title section
st.title("🛠️ Supply Chain AI Co-Review System - ChainAI Audit")
st.markdown("---")

# Navigation module
with st.sidebar:
    st.header("Navigation")
    page = st.radio("Select Demo Module", ["Conflict Scenario Simulation", "Arbitration Workflow", "Case Library"])
    
    # Parameter adjustment
    st.header("Parameter Adjustment")
    base_price = st.slider("Set Base Price (10k CNY)", 10.0, 20.0, 14.2)
    risk_threshold = st.slider("Risk Threshold (0-100)", 0, 100, 60)

# Conflict scenario page
if page == "Conflict Scenario Simulation":
    st.header("🔍 Supplier Qualification Review Conflict Simulation")
    
    # ... [metric labels translated below]
    with col1:
        st.subheader("Procurement")
        st.metric("Delivery Capability Score", "92/100", delta="Grade A Recommended")
        st.progress(0.92)
        with st.expander("View Audit Logic"):
            st.code("""Historical On-time Delivery: 98%
Certifications: ISO9001, IATF16949
Cooperation Stability: 5 years uninterrupted""")
    
    with col2:
        st.subheader("Legal")
        risk_level = "High" if risk_threshold < 70 else "Medium"
        st.metric("Risk Rating", risk_level, delta="1 related litigation", delta_color="inverse")
        with st.expander("View Risk Details"):
            st.code("""Related Entity: Xunda Logistics
Case: Transportation Contract Dispute (2023-Hu-01-1234)
Impact Assessment: +15% supply chain disruption risk""")
    
    with col3:
        st.subheader("Finance")
        st.metric("Price Deviation", f"{price_deviation:.1f}%", 
                 delta="Exceeds threshold" if abs(price_deviation)>5 else "Within tolerance", 
                 delta_color="inverse" if abs(price_deviation)>5 else "normal")
        with st.expander("Cost Analysis"):
            st.code(f"""Market Base Price: ¥{base_price:.1f}万
Current Quote: ¥{current_price:.1f}万
Allowed Fluctuation: ±5%""")
    
    st.markdown("---")
    st.subheader("Dynamic Conflict Analysis")
    
    df = pd.DataFrame({
        "Metric": ["Delivery Capability", "Compliance Risk", "Cost Control"],
        "Current Value": [92, 35, 68],
        "Threshold": [80, risk_threshold, 70]
    })
    
    fig = px.bar(df, x="Metric", y=["Current Value", "Threshold"], 
                barmode="group", text_auto=True,
                title="Department Metrics Comparison")
    st.plotly_chart(fig, use_container_width=True)

# Arbitration workflow page
elif page == "Arbitration Workflow":
    st.header("⚙️ Three-Stage Governance Workflow Demo")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Conflict Identification", "Arbitration Meeting", "System Integration", "Execution Tracking"])
    
    with tab1:
        st.subheader("Stage 1: Conflict Classification Matrix")
        matrix_df = pd.DataFrame([
            ["Single metric exceedance", "Auto-compensation negotiation", "2hrs"],
            ["Dual objective conflict", "Cross-department review", "8hrs"],
            ["Triple conflict + confidence divergence", "AI Arbitration Committee", "24hrs"]
        ], columns=["Conflict Type", "Resolution Channel", "Time Limit"])
        
        # ... [rest of the translations follow similar pattern]

# Case library page
else:
    st.header("📚 Case Library")
    
    case_filter = st.selectbox("Filter Cases", ["All", "Triple Conflict", "Dual Conflict", "Single Conflict"])
    
    case_df = pd.DataFrame({
        "Case ID": ["C-2023-045", "C-2024-012", "C-2024-018"],
        "Conflict Type": ["Triple Conflict", "Dual Conflict", "Single Conflict"],
        "Resolution": ["Conditional Approval", "Adjusted Approval", "Auto-Resolution"],
        "Processing Time(hrs)": [24, 8, 2],
        "Outcome": ["Successful Cooperation", "Ongoing", "Terminated"]
    })
    
    # ... [remaining translations]

st.markdown("---")
st.caption("Demo Note: This system uses simulated data to demonstrate core workflows")
