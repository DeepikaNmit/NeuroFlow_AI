import streamlit as st
import time
import pandas as pd
from models.predict import predict_traffic

# Page config
st.set_page_config(page_title="Dashboard", layout="wide")

# Light UI
st.markdown("""
<style>
body {
    background-color: #f5f7fa;
}
.card {
    background-color: #ffffff;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# TITLE
st.title("📊 User Dashboard")

# 🔢 USER STATS
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.metric("🚗 Traffic", "3200")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.metric("⏱ Time Saved", "25 mins")
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.metric("🌱 CO₂ Saved", "3 kg")
    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# 🗺️ LIVE TRAFFIC SECTION (ADD HERE)
# -----------------------------
st.markdown("---")
st.subheader("🗺️ Live Traffic Overview")

st.info("Map and traffic zones will appear here")
# 🏅 BADGES
st.subheader("🏅 Badges")

col4, col5, col6 = st.columns(3)

with col4:
    st.success("🌟 Smart Commuter")

with col5:
    st.info("🚗 Carpool Champion")

with col6:
    st.warning("🌍 Eco Saver")

# -----------------------------
# 🎛 INPUTS (IMPORTANT ADDITION)
# -----------------------------
st.markdown("---")
st.subheader("🎛️ Traffic Prediction Input")

col7, col8 = st.columns(2)

with col7:
    hour = st.slider("Hour", 0, 23, 9)
    day = st.selectbox("Day (0=Mon)", list(range(7)))

with col8:
    temp = st.slider("Temperature", -10, 40, 20)
    rain = st.slider("Rain", 0.0, 10.0, 0.0)
    snow = st.slider("Snow", 0.0, 5.0, 0.0)

# -----------------------------
# 🤖 PREDICTION
# -----------------------------
traffic = predict_traffic(hour, day, temp, rain, snow)

st.markdown("---")
st.subheader("📊 Prediction Results")

st.markdown('<div class="card">', unsafe_allow_html=True)
st.metric("🚗 Traffic Volume", int(traffic))
st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# 📊 LIVE TRAFFIC TREND (ANIMATION)
# -----------------------------
st.subheader("📊 Traffic Trend (Live Simulation)")

data = pd.DataFrame([traffic], columns=["Traffic"])

chart = st.line_chart(data)

for i in range(5):
    time.sleep(1)
    new_value = traffic - (i * 100)
    data.loc[len(data)] = [new_value]
    chart.line_chart(data)