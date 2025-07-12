import streamlit as st
import json
import os

# 📦 Load data from undata.json
def load_undata(filepath="undata.json"):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error loading UN data: {e}")
        return None

# 🧭 Extract indicators from loaded JSON
def fetch_indicators(undata):
    if not undata:
        return []
    
    # Adjust depending on structure of undata.json
    # Example: if undata["indicators"] is a list of dicts
    indicators = undata.get("indicators", [])  # Replace this key based on actual structure
    return [{"code": ind.get("code"), "title": ind.get("title")} for ind in indicators if ind.get("code")]

# 🔍 Get full data for a selected indicator
def fetch_indicator_data(undata, indicator_code):
    if not undata:
        return None
    
    # Replace with actual logic—example assumes list of indicators
    for ind in undata.get("indicators", []):
        if ind.get("code") == indicator_code:
            return ind  # Return full dict with metadata + values

    return None

# 🚀 Load once
undata = load_undata()

st.header("📊 UN SDG Data Explorer (Offline Mode)")

indicators = fetch_indicators(undata)

if indicators:
    indicator_options = {ind["code"]: ind["title"] for ind in indicators}
    selected = st.selectbox("Choose an SDG Indicator", options=indicator_options.keys(), format_func=lambda k: indicator_options[k])
    data = fetch_indicator_data(undata, selected)

    if data:
        st.subheader(f"Data for {indicator_options[selected]}")
        st.json(data)  # You can later format this as a table or chart
    else:
        st.warning("No data available for selected indicator.")
else:
    st.error("Failed to load indicators from undata.json.")
