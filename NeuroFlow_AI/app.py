import streamlit as st
import pandas as pd
import time
import folium
from streamlit_folium import st_folium

from models.predict import predict_traffic
from utils.suggestions import get_suggestions
from simulation.simulate import simulate_reduction

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="NeuroFlow AI", layout="wide")

# -----------------------------
# CLEAN LIGHT UI
# -----------------------------
st.markdown("""
<style>
[data-testid="stMetricLabel"] {
    color: #6b7280 !important;
}

[data-testid="stMetricValue"] {
    color: #111827 !important;
}

/* -------- REMOVE SIDEBAR -------- */
[data-testid="stSidebar"] {display: none;}

/* -------- BACKGROUND -------- */
[data-testid="stAppViewContainer"] {
    background: #f8fafc;
}

/* -------- MAIN CONTAINER -------- */
section.main > div {
    max-width: 1100px;
    margin: auto;
}

/* -------- TEXT FIX -------- */
h1, h2, h3, h4 {
    color: #1f2937 !important;  /* DARK TEXT */
}

p, label, span {
    color: #374151 !important;
}

/* -------- HERO SECTION -------- */
.hero {
    background: linear-gradient(135deg, #4f46e5, #2563eb);
    padding: 30px;
    border-radius: 20px;
    color: white;
    margin-bottom: 25px;
}


/* -------- NAV BUTTONS -------- */
/* LIGHT BLUE NAV BUTTONS */
.stButton button {
    background: #e0f2fe !important;
    color: #111827 !important;
    border-radius: 12px;
    padding: 10px 20px;
    border: none;
    transition: 0.3s;
    font-weight: 500;
}

.stButton button:hover {
    background: #bae6fd !important;
    transform: scale(1.05);
}
/* -------- INPUT FIX -------- */
input, textarea {
    background-color: white !important;
    color: black !important;
}

/* -------- METRIC -------- */
[data-testid="stMetricValue"] {
    color: #111827 !important;
}

/* -------- PROFILE -------- */
.profile {
    position: absolute;
    top: 20px;
    right: 30px;
    background: white;
    padding: 8px 14px;
    border-radius: 10px;
    box-shadow: 0px 3px 8px rgba(0,0,0,0.1);
}

.card {
    background: #f1f5f9;
    padding: 20px;
    border-radius: 16px;
    border: 1px solid #e2e8f0;
    transition: 0.3s;
}

.card:hover {
    transform: translateY(-5px);
    box-shadow: 0px 10px 20px rgba(0,0,0,0.08);
}
/* -------- FADE ANIMATION -------- */
.fade-in {
    animation: fadeIn 0.6s ease-in-out;
}

@keyframes fadeIn {
    from {opacity: 0; transform: translateY(15px);}
    to {opacity: 1; transform: translateY(0);}
}
            
.stTextInput input {
    background-color: #ffffff !important;
    color: #111827 !important;
    border: 1px solid #d1d5db !important;
    border-radius: 10px;
}
            
/* LOGIN BUTTON */
button[kind="primary"] {
    background: #e0f2fe !important;
    color: #111827 !important;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# SESSION INIT (IMPORTANT)
# -----------------------------
if "user" not in st.session_state:
    st.session_state.user = "Guest"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# -----------------------------
# 🔐 LOGIN SYSTEM
# -----------------------------
if not st.session_state.logged_in:

    st.markdown('<div class="login-box fade-in">', unsafe_allow_html=True)

    st.markdown("## 🔐 Welcome to NeuroFlow AI")
    st.write("Smart Traffic Optimization System")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username and password:
            st.session_state.logged_in = True
            st.session_state.user = username
            st.rerun()
        else:
            st.error("Enter credentials")

    st.markdown('</div>', unsafe_allow_html=True)

    st.stop()
# -----------------------------
# SESSION INIT
if "user" not in st.session_state:
    st.session_state.user = "Guest"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "page" not in st.session_state:
    st.session_state.page = "Home"

# 🔥 ADD HERE
if "confirm_logout" not in st.session_state:
    st.session_state.confirm_logout = False
# -----------------------------
# 👤 PROFILE 
# -----------------------------
colA, colB = st.columns([8,2])

with colB:
    st.markdown(f"""
    <div style="
    text-align:right;
    font-size:14px;
    color:#111827;
    ">
    👤 {st.session_state.get("user", "Guest")}
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<h2 style="color:#111827; margin-bottom:10px;">
🚦 NeuroFlow AI
</h2>
""", unsafe_allow_html=True)
# -----------------------------
# NAVIGATION
# -----------------------------

st.markdown("### ")
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    if st.button("🏠 Home"):
        st.session_state.page = "Home"

with col2:
    if st.button("📊 Dashboard"):
        st.session_state.page = "Dashboard"

with col3:
    if st.button("🗺️ Map"):
        st.session_state.page = "Map"

with col4:
    if st.button("🚗 Ride Share"):
        st.session_state.page = "Ride Share"   # 🔥 FIXED (IMPORTANT)

with col5:
    # 🔥 ADD LOGOUT BUTTON FIRST
    if st.button("🚪 Logout"):
        st.session_state.confirm_logout = True

# -----------------------------
# 🔥 CONFIRMATION (KEEP SAME)
# -----------------------------
if st.session_state.confirm_logout:
    st.warning("⚠️ Are you sure you want to logout?")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("✅ Yes, Logout"):
            st.session_state.logged_in = False
            st.session_state.user = "Guest"
            st.session_state.confirm_logout = False
            st.rerun()

    with col2:
        if st.button("❌ Cancel"):
            st.session_state.confirm_logout = False

st.markdown("---")
# -----------------------------
# 🏠 HOME PAGE
# -----------------------------
if st.session_state.page == "Home":

    st.markdown('<div class="fade-in">', unsafe_allow_html=True)

    # 🔥 HERO SECTION (TOP)
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)

    st.markdown("""
    <h1 style="
    font-size:48px;
    color:#111827;
    margin-bottom:5px;
    ">
    🚦 NeuroFlow AI
    </h1>

    <h3 style="color:#374151;">
    Predict. Influence. Synchronize.
    </h3>

    <p style="color:#6b7280;">
    Traffic is not a road problem — it’s a coordination problem.
    </p>
    """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")

    # 🚀 FEATURES
    st.markdown("<h2 style='color:#111827;'>🚀 Core Features</h2>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("<h3 style='color:#1f2937;'>🔮 Traffic Prediction</h3>", unsafe_allow_html=True)
        st.markdown("<p style='color:#4b5563;'>Predict congestion before it happens</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 🎯 Behavior AI")
        st.write("Suggest best time & travel mode")
        st.markdown('</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 🤝 Smart Sync")
        st.write("Connect people, companies & govt")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    # 🌍 SDG SECTION
    st.markdown("## 🌍 SDG Impact")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 🌆 SDG 11")
        st.write("Sustainable Cities → Less traffic & pollution")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 🤝 SDG 17")
        st.write("Partnerships → People + Govt + Companies")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    # 📊 METRICS
    st.markdown("## 📊 Real-Time Impact")

    col3, col4, col5 = st.columns(3)

    col3.metric("🚗 Traffic Reduced", "1200+", "↓ 35%")
    col4.metric("⏱ Time Saved", "320 hrs", "↑ efficiency")
    col5.metric("🌱 CO₂ Saved", "150 kg", "eco impact")

    st.markdown("---")

    # 🔥 WOW FEATURE (IMPORTANT)
    st.markdown("## 🧠 AI Future Simulation")

    users = st.slider("People Following AI (%)", 0, 100, 30)

    impact = users * 1.5

    st.success(f"If {users}% follow AI → Traffic reduces by {int(impact)}% 🚀")

    st.markdown('</div>', unsafe_allow_html=True)
# -----------------------------
# 📊 DASHBOARD PAGE
# -----------------------------
elif st.session_state.page == "Dashboard":
    st.title("📊 Dashboard")

    # -----------------------------
    # 🏅 BADGES (ADDED)
    # -----------------------------
    st.subheader("🏅 Your Achievements")

    colb1, colb2, colb3 = st.columns(3)

    with colb1:
        st.success("🌟 Smart Commuter")

    with colb2:
        st.info("🚗 Carpool Champion")

    with colb3:
        st.warning("🌍 Eco Saver")

    st.markdown("---")

    # Inputs
    col1, col2 = st.columns(2)

    with col1:
        hour = st.slider("Hour", 0, 23, 9)
        day = st.selectbox("Day", list(range(7)))

    with col2:
        temp = st.slider("Temperature", -10, 40, 20)
        rain = st.slider("Rain", 0.0, 10.0, 0.0)
        snow = st.slider("Snow", 0.0, 5.0, 0.0)

    # Prediction
    traffic = predict_traffic(hour, day, temp, rain, snow)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.metric("🚗 Traffic Volume", int(traffic))
    st.markdown('</div>', unsafe_allow_html=True)

    # Suggestions
    for s in get_suggestions(traffic):
        st.success(s)

    # Chart
    st.subheader("📊 Traffic Trend")

    data = pd.DataFrame([traffic], columns=["Traffic"])
    chart = st.line_chart(data)

    for i in range(5):
        time.sleep(0.5)
        new_value = traffic - (i * 100)
        data.loc[len(data)] = [new_value]
        chart.line_chart(data)

    st.markdown("---")
    st.subheader("🧠 AI Impact Simulator")

    users = st.slider("Users", 0, 1000, 300)
    carpool = st.slider("Carpool %", 0, 100, 40)

    reduction = users * (carpool/100) * 2

    st.success(f"🚗 Vehicles Reduced: {int(reduction)}")
    st.info(f"🌱 CO₂ Reduction: {int(reduction*0.5)} kg")
    # -----------------------------
    # 🤖 AI CHAT (UPGRADED)
    # -----------------------------
    st.markdown("---")
    st.subheader("🤖 Ask NeuroFlow AI")

    query = st.text_input("Ask about traffic, carpool, or routes...")

    if query:
        q = query.lower()

        if "traffic" in q:
            st.success("🚦 Peak traffic expected around 9 AM & 6 PM. Try leaving early.")

        elif "carpool" in q:
            st.success("🚗 Carpooling can reduce traffic by up to 30%. Matching nearby users...")

        elif "route" in q or "map" in q:
            st.success("🗺️ Suggested route avoids high congestion zones.")

        elif "time" in q:
            st.success("⏱️ Best departure time is 15–20 mins earlier than peak.")

        else:
            st.success("✅ Smart suggestion: Avoid peak hours, use shared rides, and follow AI recommendations.")

# -----------------------------
# 🗺️ MAP PAGE
# -----------------------------
elif st.session_state.page == "Map":
    st.markdown("### 🔴 High Traffic Zone")
    st.markdown("### 🟢 Low Traffic Zone")  
    st.title("🗺️ Live Traffic Map")

    m = folium.Map(location=[12.97, 77.59], zoom_start=12)

    folium.Circle([12.97, 77.59], radius=1000, color="red", fill=True).add_to(m)
    folium.Circle([12.99, 77.57], radius=800, color="green", fill=True).add_to(m)

    route = [
        [12.97, 77.59],
        [12.98, 77.60],
        [12.99, 77.61]
    ]

    folium.PolyLine(route, color="blue").add_to(m)

    # 🔥 ANIMATION ADDED HERE
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)
    st_folium(m, width=900, height=500)
    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# 🚗 RIDE SHARE PAGE
# -----------------------------
elif st.session_state.page == "Ride Share":
    st.title("🚗 Smart Ride Sharing")

    col1, col2 = st.columns(2)

    with col1:
        start = st.text_input("📍 Start Location")
        end = st.text_input("🎯 Destination")

    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 💡 Why Ride Share?")
        st.write("Reduce traffic & emissions")
        st.write("Save fuel & cost")
        st.write("Help environment 🌱")
        st.markdown('</div>', unsafe_allow_html=True)

    # 🔥 BUTTON + RESULT INSIDE CARD
    if st.button("Find Smart Matches"):

        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.success("Matched with 3 users on same route ✅")

        st.markdown("""
        👤 Rahul - 90% route match  
        👤 Sneha - 80% route match  
        👤 Arjun - Nearby route  
        """)
   

        
        st.info("💡 Carpooling reduces traffic by 30%")
        st.markdown('</div>', unsafe_allow_html=True)