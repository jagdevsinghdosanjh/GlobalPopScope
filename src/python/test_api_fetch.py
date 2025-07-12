import streamlit as st

st.header("📊 UN SDG Data Explorer (Offline Mode)")

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
