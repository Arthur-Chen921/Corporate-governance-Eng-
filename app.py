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

    # 新增Integration部分
    with tab3:
        st.subheader("System Integration")
        
        # 拓扑图数据
        nodes = pd.DataFrame([
            {"Node": "ChainAI Core", "Type": "Core", "x": 2, "y": 2},
            {"Node": "ERP", "Type": "Business", "x": 1, "y": 1},
            {"Node": "Contract DB", "Type": "Legal", "x": 3, "y": 1},
            {"Node": "Finance", "Type": "Finance", "x": 2, "y": 0},
            {"Node": "News Monitor", "Type": "External", "x": 4, "y": 2}
        ])
        
        edges = [
            {"From": "ChainAI Core", "To": "ERP", "Type": "Realtime"},
            {"From": "ChainAI Core", "To": "Contract DB", "Type": "API"},
            {"From": "ChainAI Core", "To": "Finance", "Type": "Sync"},
            {"From": "ChainAI Core", "To": "News Monitor", "Type": "Scrape"}
        ]
        
        fig = px.scatter(nodes, x="x", y="y",
                        size=[30,20,20,20,20],
                        color="Type",
                        text="Node",
                        title="System Integration Map")
        
        # 添加连接线
        for edge in edges:
            source = nodes[nodes["Node"] == edge["From"]].iloc[0]
            target = nodes[nodes["Node"] == edge["To"]].iloc[0]
            fig.add_shape(
                type="line",
                x0=source["x"], y0=source["y"],
                x1=target["x"], y1=target["y"],
                line=dict(color="#BDBDBD", width=2)
            )
            
        fig.update_traces(marker=dict(size=100),
                         textfont=dict(size=14))
        st.plotly_chart(fig, use_container_width=True)
        
        # 数据流监控
        st.markdown("**Realtime Data Flow**")
        flow_df = pd.DataFrame([
            ["ERP→Core", "Orders", "Normal", "5ms"],
            ["Legal→Core", "Contracts", "Delay", "320ms"],
            ["Finance→Core", "Cost", "Normal", "8ms"],
            ["News→Core", "Risk", "Normal", "120ms"]
        ], columns=["Channel", "Data", "Status", "Latency"])
        st.dataframe(flow_df.style.applymap(
            lambda x: "color: red" if x=="Delay" else None), 
            use_container_width=True)

    # 新增Tracking部分
    with tab4:
        st.subheader("Execution Tracking")
        task_df = pd.DataFrame([
            ["Contract Update", "Legal", "Audit", "Risk<30"],
            ["Payment Adjust", "Finance", "SCM", "Deviation<5%"],
            ["CRM", "Procurement", "CS", "Rating≥4"]
        ], columns=["Task", "Owner", "Supervisor", "KPI"])
        
        st.dataframe(task_df.style.applymap(
            lambda x: "background-color: #e6f3ff" if x=="Legal" else ""), 
            use_container_width=True)
        
        st.button("Simulate Completion", help="Send completion notification")


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
