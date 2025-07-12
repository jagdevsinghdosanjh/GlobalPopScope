import streamlit as st

st.header("📊 UN SDG Data Explorer (Offline Mode)")

def fetch_indicators():
    # Dummy implementation, replace with actual logic
    return [
        {"code": "SDG1", "title": "No Poverty"},
        {"code": "SDG2", "title": "Zero Hunger"},
        {"code": "SDG3", "title": "Good Health and Well-being"},
        {"code": "SDG4", "title": "Quality Education"},
        {"code": "SD_MDP_CSMP", "title": "Child Specific Multidimensional Poverty"},
    ]

def fetch_indicator_data(indicator_code):
    # Dummy implementation, replace with actual logic
    dummy_data = {
        "SDG1": {"year": 2020, "value": 100},
        "SDG2": {"year": 2020, "value": 200},
        "SDG3": {"year": 2020, "value": 300},
        "SDG4": {"year": 2020, "value": 400},
        "SD_MDP_CSMP": {"year": 2020, "value": 1500},
    }
    return dummy_data.get(indicator_code, None)

indicators = fetch_indicators()
if indicators:
    indicator_options = {ind["code"]: ind["title"] for ind in indicators}
    selected = st.selectbox("Choose an SDG Indicator", options=indicator_options.keys(), format_func=lambda k: indicator_options[k])
    data = fetch_indicator_data(selected)

    if data:
        st.subheader(f"Data for {indicator_options[selected]}")
        st.json(data)
    else:
        st.warning("No data available for selected indicator.")
else:
    st.error("Failed to load indicators.")
