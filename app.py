import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from pipeline.ingestion import load_scada_data
from pipeline.features import engineering_features
from models.anomaly_detector import SCADAAnomalyDetector
import config

st.set_page_config(page_title="Vattenfall Wind - Operational Intelligence Dashboard", layout="wide")

st.title("⚡ Vattenfall Wind Operations: SCADA Power Curve & Anomaly Monitor")
st.subheader("Asset Optimization Engine — Operational Intelligence Demo")

# 1. Pipeline execution setup
@st.cache_data
def run_pipeline():
    raw_data = load_scada_data(days=14)
    processed_data = engineering_features(raw_data)
    
    detector = SCADAAnomalyDetector()
    final_df = detector.fit(processed_data).predict(processed_data)
    return final_df

df = run_pipeline()

# 2. Key High-Level Operational Metrics
total_anomalies = int(df['is_anomaly'].sum())
anomaly_rate = (total_anomalies / len(df)) * 100

m1, m2, m3 = st.columns(3)
m1.metric("Monitored Asset Status", "WTG-01 (ONLINE)", delta="Optimal Efficiency")
m2.metric("Total Flagged Sensor Anomalies", f"{total_anomalies} intervals", delta=f"{anomaly_rate:.2f}% contamination", delta_color="inverse")
m3.metric("Max Gearbox Temp Registered", f"{df['gearbox_temperature'].max():.1f} °C", delta="Threshold limit: 80°C", delta_color="off")

st.markdown("---")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 📈 Multivariate Power Curve Performance")
    
    # Highlighting normal vs anomalous behaviors on the curve
    fig = px.scatter(
        df, 
        x="wind_speed", 
        y="active_power", 
        color="is_anomaly",
        color_discrete_map={0: "#22c55e", 1: "#ef4444"},
        labels={"wind_speed": "Wind Speed (m/s)", "active_power": "Active Power Output (kW)", "is_anomaly": "Anomaly Flag"},
        title="Actual Power Production vs Wind Speed (Highlighted Anomaly Logs)"
    )
    
    # Overlay the ideal physics curve for baseline verification
    ideal_sorted = df.sort_values('wind_speed')
    fig.add_trace(go.Scatter(
        x=ideal_sorted['wind_speed'], 
        y=ideal_sorted['theoretical_power'], 
        mode='lines', 
        name='Theoretical Power Curve',
        line=dict(color='#3b82f6', width=3, dash='dash')
    ))
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("### ⚠️ Actionable Operational Alerts")
    st.write("High-priority intervals flagged for physical inspection or maintenance review:")
    
    # Filter out critical anomalies for technical teams
    high_priority_events = df[df['is_anomaly'] == 1].sort_values(by='anomaly_score', ascending=False).head(10)
    
    st.dataframe(
        high_priority_events[['timestamp', 'wind_speed', 'active_power', 'gearbox_temperature']], 
        hide_index=True
    )
    
    st.markdown("##### Technical Diagnostic Insight:")
    st.caption("Anomalies marked in red typically fall into two categories: **Sub-optimal power output during peak wind windows** (potential aerodynamic pitch/yaw misalignment) or **unwarranted localized temperature spikes** indicating system degradation or bearing friction anomalies.")