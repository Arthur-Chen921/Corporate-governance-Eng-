# app.py
import streamlit as st
import pandas as pd
import plotly.express as px

# 保持原中文数据结构不变
supplier_db = {
    "suppliers": [
        {"id": "RF-202403", "name": "TheBestBattery", "category": "BatteryTray", 
         "qualification": "Level A", "price": 15800, "delivery_score": 92}
    ],
    "conflicts": [
        {"event_id": "C-001", "supplier_id": "RF-202403", 
         "conflict_type": "TripleConflict", "status": "solved"}
    ],
    "arbitrations": [
        {"event_id": "C-001", "resolution": "ConditionalPass", 
         "conditions": ["3-months-free-trial", "30% down payment", "Supplementary due diligence"]}
    ]
}

# Page configuration
st.set_page_config(page_title="ChainAI Audit System Demo", layout="wide")

# Title section
st.title("🛠️ Supply Chain AI Co-Review System - ChainAI Audit")
st.markdown("---")

# Navigation module
with st.sidebar:
    st.header("Navigation")
    page = st.radio("Select Module", ["Conflict Simulation", "Arbitration Workflow", "Case Library"])
    
    # Parameter adjustment
    st.header("Parameters")
    base_price = st.slider("Base Price (10k CNY)", 10.0, 20.0, 14.2)
    risk_threshold = st.slider("Risk Threshold (0-100)", 0, 100, 60)

# Conflict scenario page
if page == "Conflict Simulation":
    st.header("🔍 Supplier Qualification Review")
    
    current_price = supplier_db["suppliers"][0]["price"] / 10000
    price_deviation = (current_price - base_price) / base_price * 100
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("Procurement")
        st.metric("Delivery Score", 
                 f"{supplier_db['suppliers'][0]['delivery_score']}/100", 
                 delta="Grade A")
        st.progress(supplier_db["suppliers"][0]["delivery_score"]/100)
        with st.expander("Audit Logic"):
            st.code("""On-time Delivery: 98%
Certifications: ISO9001, IATF16949
Stable Cooperation: 5+ years""")
        
    with col2:
        st.subheader("Legal")
        risk_level = "High" if risk_threshold < 70 else "Medium"
        st.metric("Risk Level", risk_level, 
                 delta="1 related case", 
                 delta_color="inverse")
        with st.expander("Risk Details"):
            st.code("""Related Entity: Xunda Logistics
Case: Contract Dispute (2023-Hu-1234)
Impact: +15% disruption risk""")
        
    with col3:
        st.subheader("Finance")
        st.metric("Price Deviation", f"{price_deviation:.1f}%", 
                 delta="Exceeds threshold" if abs(price_deviation)>5 else "Within range", 
                 delta_color="inverse" if abs(price_deviation)>5 else "normal")
        with st.expander("Cost Analysis"):
            st.code(f"""Base Price: ¥{base_price:.1f}万
Quote: ¥{current_price:.1f}thousand
Allowance: ±5%""")
    
    st.markdown("---")
    st.subheader("Conflict Analysis")
    
    df = pd.DataFrame({
        "Metric": ["Delivery", "Compliance", "Cost"],
        "Current": [92, 35, 68],
        "Threshold": [80, risk_threshold, 70]
    })
    
    fig = px.bar(df, x="Metric", y=["Current", "Threshold"], 
                barmode="group", 
                title="Metrics Comparison")
    st.plotly_chart(fig, use_container_width=True)

# Arbitration workflow page
elif page == "Arbitration Workflow":
    st.header("⚙️ Three-Stage Governance")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Identification", "Meeting", "Integration", "Tracking"])
    
    with tab1:
        st.subheader("Conflict Matrix")
        matrix_df = pd.DataFrame([
            ["Single Metric", "Auto-Negotiation", "2hrs"],
            ["Dual Conflict", "Cross-Review", "8hrs"],
            ["Triple Conflict", "AI Committee", "24hrs"]
        ], columns=["Type", "Process", "Deadline"])
        
        st.dataframe(matrix_df, use_container_width=True)
        
        st.write("**Current Case**:")
        st.json({
            "Type": "Triple Conflict",
            "Process": "AI Committee Review",
            "Deadline": "24hrs"
        })
        
    with tab2:
        st.subheader("Arbitration Process")
        
        timeline_df = pd.DataFrame([
            {"Stage": "Preparation", "Status": "Completed", "Duration": 2},
            {"Stage": "Evidence", "Status": "Processing", "Duration": 1},
            {"Stage": "Hearing", "Status": "Pending", "Duration": 3},
            {"Stage": "Decision", "Status": "Pending", "Duration": 1}
        ])
        
        col1, col2 = st.columns([3,1])
        with col1:
            fig = px.timeline(timeline_df, 
                            x_start=[0,2,3,6],
                            x_end=[2,3,6,7],
                            y="Stage", 
                            color="Status",
                            color_discrete_map={
                                "Completed": "#4CAF50",
                                "Processing": "#FFC107",
                                "Pending": "#E0E0E0"
                            })
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            contact_df = pd.DataFrame([
                ["Procurement", "Wang Yue", "wangyue@demo.com"],
                ["Legal", "Zhang Tao", "zhangtao@demo.com"],
                ["Finance", "Chen Min", "chenmin@demo.com"],
                ["Chair", "Li Hang", "lihang@demo.com"]
            ], columns=["Role", "Contact", "Email"])
            st.dataframe(contact_df, hide_index=True)
    
    # Remaining tabs maintain similar pattern...

# Case library page
else:
    st.header("📚 Case Library")
    
    case_filter = st.selectbox("Filter", ["All", "Triple", "Dual", "Single"])
    
    case_df = pd.DataFrame({
        "Case ID": ["C-2023-045", "C-2024-012", "C-2024-018"],
        "Type": ["Triple Conflict", "Dual Conflict", "Single Conflict"],
        "Resolution": ["Conditional", "Adjusted", "Auto"],
        "Duration(hrs)": [24, 8, 2],
        "Outcome": ["Success", "Ongoing", "Terminated"]
    })
    
    if case_filter != "All":
        case_df = case_df[case_df["Type"].str.contains(case_filter)]
    
    st.dataframe(case_df, use_container_width=True)

st.markdown("---")
st.caption("Demo System: Simulated data for workflow demonstration")
