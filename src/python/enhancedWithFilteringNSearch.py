import streamlit as st
import json
import pandas as pd
from collections import Counter

st.set_page_config(page_title="UN SDG Data Explorer", layout="wide")

# 📦 Load data from undata.json
def load_undata(filepath="src/python/undata.json"):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except Exception as e:
        st.error(f"❌ Error loading UN data: {e}")
        return []

# 🧭 Extract indicators from loaded JSON
def fetch_indicators(undata):
    indicators = []
    for item in undata:
        if isinstance(item, dict):
            code = item.get("code")
            title = item.get("description")
            goal = item.get("goal")
            if code and title and goal:
                indicators.append({"code": code, "title": title, "goal": goal})
    return indicators

# 🔍 Get full data for a selected indicator
def fetch_indicator_data(undata, indicator_code):
    for item in undata:
        if isinstance(item, dict) and item.get("code") == indicator_code:
            return item
    return None

# 📊 Build release chart data
def build_release_chart(series_data):
    releases = [s.get("release") for s in series_data if isinstance(s, dict) and s.get("release")]
    counts = Counter(releases)
    df = pd.DataFrame.from_dict(counts, orient="index", columns=["Series Count"])
    df.index.name = "Release"
    df = df.sort_index()
    return df.reset_index()

# 🚀 Load once
undata = load_undata()
st.header("📊 UN SDG Data Explorer (Offline Mode)")

with st.expander("🔍 Preview Raw UN Data"):
    if undata:
        st.json(undata[:3])
    else:
        st.warning("UN data is empty or not structured as a list.")

indicators = fetch_indicators(undata)

if indicators:
    # 📘 Goal-wise filtering
    unique_goals = sorted(set(ind["goal"] for ind in indicators))
    selected_goal = st.selectbox("📘 Filter by SDG Goal", options=unique_goals)

    # 🔎 Search box for indicator title
    search_query = st.text_input("🔍 Search indicator description", value="")

    # Filter indicators
    filtered_indicators = [
        ind for ind in indicators
        if ind["goal"] == selected_goal and search_query.lower() in ind["title"].lower()
    ]

    if filtered_indicators:
        indicator_options = {ind["code"]: ind["title"] for ind in filtered_indicators}
        selected = st.selectbox(
            "Choose an SDG Indicator",
            options=indicator_options.keys(),
            format_func=lambda k: indicator_options[k]
        )
        data = fetch_indicator_data(undata, selected)

        if data:
            st.subheader(f"📌 Data for: {indicator_options[selected]}")
            st.markdown(f"**Goal:** {data.get('goal')}")
            st.markdown(f"**Target:** {data.get('target')}")
            st.markdown(f"**Tier:** {data.get('tier')}")
            st.markdown(f"**Description:** {data.get('description')}")

            series_data = data.get("series", [])
            if series_data:
                st.markdown("### 📊 Related Series Table")
                table_rows = [
                    {
                        "Code": s.get("code"),
                        "Description": s.get("description"),
                        "Release": s.get("release"),
                        "Goal": ", ".join(s.get("goal", [])),
                        "Target": ", ".join(s.get("target", [])),
                        "Indicator": ", ".join(s.get("indicator", [])),
                        "URI": s.get("uri")
                    }
                    for s in series_data if isinstance(s, dict)
                ]
                st.dataframe(table_rows, use_container_width=True)

                st.markdown("### 📈 Series Release Chart")
                release_df = build_release_chart(series_data)
                st.bar_chart(release_df.set_index("Release"), use_container_width=True)
            else:
                st.info("No series data available for this indicator.")
        else:
            st.warning("⚠️ No data available for selected indicator.")
    else:
        st.info("No indicators match your filters.")
else:
    st.error("🚫 No indicators found in undata.json.")
