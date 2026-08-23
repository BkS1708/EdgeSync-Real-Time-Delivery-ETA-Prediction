# ========================= ui.py =========================

import streamlit as st
import folium
from streamlit_folium import st_folium
import requests
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from config import get_region

st.set_page_config(layout="wide")

st.title("EdgeSync ETA - Distributed Delivery Simulator")

# ---------------- SESSION ----------------
if "points" not in st.session_state:
    st.session_state.points = []

if "clicked" not in st.session_state:
    st.session_state.clicked = None

if "result" not in st.session_state:
    st.session_state.result = None

# ---------------- MAP ----------------
def create_map():
    m = folium.Map(location=[19.0760, 72.8777], zoom_start=11)

    # -------- USER POINTS --------
    for i, point in enumerate(st.session_state.points):
        if i == 0:
            folium.Marker(
                point,
                popup="Source",
                icon=folium.Icon(color="red")
            ).add_to(m)

        elif i == 1:
            folium.Marker(
                point,
                popup="Destination",
                icon=folium.Icon(color="green")
            ).add_to(m)

    # -------- PATH --------
    if len(st.session_state.points) == 2:
        folium.PolyLine(
            st.session_state.points,
            color="blue",
            weight=4
        ).add_to(m)

    return m

map_data = st_folium(
    create_map(),
    height=500,
    width=1000,
    key="map_" + str(len(st.session_state.points)), 
    returned_objects=["last_clicked"]
)

# ---------------- CLICK ----------------
if map_data and map_data.get("last_clicked"):

    clicked = (
        map_data["last_clicked"]["lat"],
        map_data["last_clicked"]["lng"]
    )

    if st.session_state.clicked != clicked:

        st.session_state.clicked = clicked

        if len(st.session_state.points) < 2:
            st.session_state.points.append(clicked)

            st.rerun()   

st.write("📍 Selected Points:", st.session_state.points)

# ---------------- RESET ----------------
if st.button("🔄 Reset"):
    st.session_state.points = []
    st.session_state.result = None
    st.session_state.clicked = None
    st.rerun()

# ---------------- INPUTS ----------------
food = st.selectbox("🍔 Food", ["Pizza", "Burger", "Sandwich", "Taco"])

rider_option = st.selectbox(
    "🛵 Rider Distance",
    ["Near (0.5-2 km)", "Medium (2-5 km)", "Far (5-8 km)"]
)

traffic = st.selectbox("🚦 Traffic", ["Low", "Medium", "High"])

# ---------------- REGION ----------------
if len(st.session_state.points) == 2:
    src = st.session_state.points[0]
    dst = st.session_state.points[1]

    src_region = get_region(src[0], src[1])
    dst_region = get_region(dst[0], dst[1])

    col1, col2 = st.columns(2)
    col1.success(f"🔴 Source Region: {src_region}")
    col2.success(f"🟢 Destination Region: {dst_region}")

# ---------------- COMPUTE ETA ----------------
if len(st.session_state.points) == 2:

    if st.button("🚀 Compute ETA"):

        region_url = {
            "EAST": "http://localhost:8000/custom_eta",
            "WEST": "http://localhost:9000/custom_eta",
            "CENTRAL": "http://localhost:10000/custom_eta"
        }

        try:
            res = requests.post(region_url[src_region], json={
                "source": src,
                "destination": dst,
                "food": food,
                "traffic": traffic,
                "rider": rider_option
            }).json()

            st.session_state.result = res

        except:
            st.error("⚠️ Backend not running. Start east, west, central servers.")

# ---------------- RESULT ----------------
if st.session_state.result:

    data = st.session_state.result

    eta = data["ETA"]
    pickup = data["pickup"]
    prep = data["prep"]
    delivery = data["delivery"]
    traffic = data.get("traffic", "N/A")

    st.subheader("Final ETA Result")

    col1, col2, col3 = st.columns(3)
    col1.metric("⏱️ ETA", f"{eta:.2f} mins")
    col2.metric("🚦 Traffic", traffic)
    col3.metric("📦 Delivery Time", f"{delivery:.2f} mins")

    final_time = datetime.now() + timedelta(minutes=eta)
    st.success(f"🕒 Estimated Delivery Time: {final_time.strftime('%H:%M:%S')}")

    # ---------------- CHART ----------------
    st.subheader("ETA Breakdown")

    labels = ["Pickup", "Preparation", "Delivery"]
    values = [pickup, prep, delivery]

    fig, ax = plt.subplots()
    ax.bar(labels, values)
    ax.set_ylabel("Time (mins)")
    st.pyplot(fig)

    # ---------------- REGION CONTRIBUTION ----------------
    st.subheader("Distributed Contribution")

    st.write(f"""
    - **{src_region} Node** → Handles Pickup & Preparation  
    - **{dst_region} Node** → Handles Delivery  
    - Gossip Protocol → Synchronizes ETA trends across nodes  
    """)

    # ---------------- GOSSIP LOGS ----------------
    st.subheader("🔄 Live Gossip Logs")

    try:
        logs = []

        urls = [
            "http://localhost:8000/logs",
            "http://localhost:9000/logs",
            "http://localhost:10000/logs"
        ]

        for url in urls:
            res = requests.get(url).json()
            logs.extend(res["logs"])

        for log in logs[-10:]:
            st.text(log)

    except:
        st.warning("Gossip logs not available")