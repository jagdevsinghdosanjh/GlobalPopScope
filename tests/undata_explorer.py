import streamlit as st
import json

# 📦 Load data from undata.json
def load_undata(filepath="src/python/undata.json"):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            st.write(f"✅ Loaded {len(data)} entries from UN data.")
            return data
    except Exception as e:
        st.error(f"❌ Error loading UN data: {e}")
        return []

# 🧭 Extract indicators from loaded JSON
def fetch_indicators(undata):
    return [
        {"code": item["code"], "title": item["title"]}
        for item in undata
        if isinstance(item, dict) and "code" in item and "title" in item
    ]

# 🔍 Get full data for a selected indicator
def fetch_indicator_data(undata, indicator_code):
    for item in undata:
        if isinstance(item, dict) and item.get("code") == indicator_code:
            return item
    return None

# 🚀 Load once
undata = load_undata()

st.set_page_config(page_title="UN SDG Data Explorer", layout="wide")
st.header("📊 UN SDG Data Explorer (Offline Mode)")

# 🧪 Preview raw structure
with st.expander("🔍 Preview Raw UN Data"):
    st.json(undata[:3] if isinstance(undata, list) else undata)

indicators = fetch_indicators(undata)

if indicators:
    indicator_options = {ind["code"]: ind["title"] for ind in indicators}
    selected = st.selectbox(
        "Choose an SDG Indicator",
        options=indicator_options.keys(),
        format_func=lambda k: indicator_options[k]
    )
    data = fetch_indicator_data(undata, selected)

    if data:
        st.subheader(f"📌 Data for: {indicator_options[selected]}")
        st.json(data)
    else:
        st.warning("⚠️ No data available for selected indicator.")
else:
    st.error("🚫 Failed to load indicators from undata.json.")
