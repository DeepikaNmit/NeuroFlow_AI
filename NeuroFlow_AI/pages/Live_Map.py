import streamlit as st
import folium
from streamlit_folium import st_folium

# -----------------------------
# 🗺️ LIVE TRAFFIC MAP
# -----------------------------
st.markdown("---")
st.subheader("🗺️ Live Traffic Overview")

# Create base map (Bangalore coords)
m = folium.Map(location=[12.97, 77.59], zoom_start=12)

# 🔴 High traffic zone
folium.Circle(
    location=[12.97, 77.59],
    radius=1000,
    color="red",
    fill=True,
    fill_opacity=0.5,
    popup="High Traffic 🚨"
).add_to(m)

# 🟢 Smooth traffic zone
folium.Circle(
    location=[12.99, 77.57],
    radius=800,
    color="green",
    fill=True,
    fill_opacity=0.5,
    popup="Smooth Traffic ✅"
).add_to(m)

# 🔵 Route simulation (Google Maps style line)
route = [
    [12.97, 77.59],
    [12.98, 77.60],
    [12.99, 77.61]
]

folium.PolyLine(route, color="blue", weight=5, tooltip="Suggested Route").add_to(m)

# Show map in Streamlit
st_folium(m, width=900, height=500)