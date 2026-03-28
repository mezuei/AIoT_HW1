import streamlit as st
import sqlite3
import pandas as pd
import time
import os

DB_FILE = "aiotdb.db"

st.set_page_config(page_title="AIoT Dashboard", layout="wide")
st.title("📟 ESP32 Sensor Dashboard (DHT11 Data)")

def get_data():
    if not os.path.exists(DB_FILE):
        return pd.DataFrame()
        
    conn = sqlite3.connect(DB_FILE)
    query = "SELECT * FROM sensors ORDER BY timestamp DESC"
    try:
        df = pd.read_sql_query(query, conn)
    except Exception as e:
        df = pd.DataFrame()
    finally:
        conn.close()
    return df

placeholder = st.empty()

while True:
    df = get_data()
    
    with placeholder.container():
        if not df.empty:
            latest = df.iloc[0]
            
            kpi1, kpi2, kpi3 = st.columns(3)
            kpi1.metric("🌡️ Latest Temperature", f"{latest['temperature']} °C")
            kpi2.metric("💧 Latest Humidity", f"{latest['humidity']} %")
            kpi3.metric("📊 Total Readings", len(df))
            
            st.subheader("📝 Recent Data (Table)")
            st.dataframe(df.head(10), use_container_width=True)
            
            # Prepare data for charts
            df_chart = df.copy()
            df_chart['timestamp'] = pd.to_datetime(df_chart['timestamp'])
            df_chart = df_chart.sort_values('timestamp')
            
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("📈 Temperature History")
                st.line_chart(df_chart.set_index('timestamp')['temperature'], color="#FF4B4B")
                
            with col2:
                st.subheader("📉 Humidity History")
                st.line_chart(df_chart.set_index('timestamp')['humidity'], color="#0068C9")
                
        else:
            st.info("No data available yet... Please make sure the Flask Server and ESP32 Simulator are running.")
            
    time.sleep(2)
