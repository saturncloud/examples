import streamlit as st
import pandas as pd
from confluent_kafka import Consumer
import json
import plotly.express as px
import time

st.set_page_config(page_title="Local Kafka Stream", layout="wide")
st.title("📈 Real-Time Sensor Dashboard")

# 1. Initialize history
if 'history' not in st.session_state:
    st.session_state.history = pd.DataFrame({
        'timestamp': pd.Series(dtype='datetime64[ns]'),
        'temperature': pd.Series(dtype='float64')
    })

# 2. Setup Consumer (Cached so it doesn't recreate on rerun)
@st.cache_resource
def get_consumer():
    c = Consumer({
        'bootstrap.servers': 'localhost:9092',
        'group.id': 'st_dashboard_group',
        'auto.offset.reset': 'latest'
    })
    c.subscribe(["sensor_data"])
    return c

consumer = get_consumer()

# 3. Poll for new data
# We only poll once per script execution to stay within Streamlit's architecture
msg = consumer.poll(0.1) 
if msg is not None and not msg.error():
    data = json.loads(msg.value().decode('utf-8'))
    new_row = pd.DataFrame([{
        "timestamp": pd.to_datetime(data['timestamp'], unit='s'), 
        "temperature": data['temperature']
    }])
    st.session_state.history = pd.concat([st.session_state.history, new_row]).tail(50)

# 4. Display the visual
if not st.session_state.history.empty:
    fig = px.line(st.session_state.history, x='timestamp', y='temperature', title="Live Temperature")
    # We can now use the key safely because the script finishes execution
    st.plotly_chart(fig, width='stretch', key="sensor_chart")
    st.metric("Latest", f"{st.session_state.history['temperature'].iloc[-1]}°C")
else:
    st.info("Waiting for data from Kafka...")

# 5. Trigger a rerun
# This replaces the 'while True' loop and is the standard Streamlit way to stream
time.sleep(0.5)
st.rerun()