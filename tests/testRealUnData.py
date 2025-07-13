import streamlit as st
import json

# 📦 Load data from undata.json
def load_undata(filepath="src/python/undata.json"):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error loading UN data: {e}")
        return []

# 🧭 Extract indicators from loaded JSON
def fetch_indicators(undata):
    indicators = []
    for item in undata:
        if isinstance(item, dict) and "code" in item and "title" in item:
            indicators.append({"code": item["code"], "title": item["title"]})
    return indicators

# 🔍 Get full data for a selected indicator
def fetch_indicator_data(undata, indicator_code):
    for item in undata:
        if isinstance(item, dict) and item.get("code") == indicator_code:
            return item
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
        st.json(data)
    else:
        st.warning("No data available for selected indicator.")
else:
    st.error("Failed to load indicators from undata.json.")
