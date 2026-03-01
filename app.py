import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

# ===================================================
# PAGE CONFIG
# ===================================================
st.set_page_config(
    page_title="Colorado Workforce Intelligence",
    layout="wide"
)

# ===================================================
# CUSTOM PROFESSIONAL THEME
# ===================================================
st.markdown("""
<style>
body {
    background-color: #F5F7FA;
}

h1, h2, h3 {
    color: #0B3C5D;
}

.metric-card {
    background-color: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.05);
}

.sidebar .sidebar-content {
    background-color: #0B3C5D;
    color: white;
}

footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ===================================================
# LOAD DATA
# ===================================================

@st.cache_data
def load_data():
    return pd.read_parquet("data/processed/city_skill_lift.parquet")

lift_df = load_data()

# ===================================================
# SIDEBAR NAVIGATION
# ===================================================   
st.sidebar.title("Colorado Workforce Intelligence")

page = st.sidebar.radio(
    "Navigation",
    [
        "State Overview",
        "City Intelligence",
        "Regional Clusters",
        "Opportunity Gaps",
        "Training Strategy"
    ]
)

# ===================================================
# HEADER
# ===================================================
st.title("Colorado Workforce Intelligence Platform")
st.markdown("Strategic Workforce & Skill Demand Insights for Economic Development")
st.markdown("---")

# ===================================================
# STATE OVERVIEW
# ===================================================
if page == "State Overview":

    
    total_cities = lift_df["city"].nunique()
    total_skills = lift_df["Taxonomy Skill"].nunique()
    total_jobs = lift_df["total_jobs"].sum()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Total Jobs Analyzed", f"{total_jobs:,}")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Unique Skills Identified", f"{total_skills:,}")
        st.markdown('</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Cities Covered", total_cities)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    statewide = (
        lift_df.groupby("Taxonomy Skill")["skill_weight"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig = px.bar(
        statewide,
        x="skill_weight",
        y="Taxonomy Skill",
        orientation="h",
        color_discrete_sequence=["#1CA7A6"]
    )

    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        yaxis=dict(autorange="reversed"),
        title="Top 10 Most Demanded Skills in Colorado"
    )

    st.plotly_chart(fig, use_container_width=True)

# ===================================================
# CITY INTELLIGENCE
# ===================================================
elif page == "City Intelligence":

    city = st.selectbox("Select City", sorted(lift_df["city"].unique()))
    city_df = lift_df[lift_df["city"] == city].sort_values("lift", ascending=False)
    top10 = city_df.head(10)

    colA, colB, colC = st.columns(3)

    colA.metric("Specialized Skills", len(city_df))
    colB.metric("Highest Lift", round(city_df["lift"].max(), 2))
    colC.metric("Avg Lift (Top 10)", round(top10["lift"].mean(), 2))

    st.markdown("---")

    fig = px.bar(
        top10,
        x="lift",
        y="Taxonomy Skill",
        orientation="h",
        color_discrete_sequence=["#3A7CA5"]
    )

    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        yaxis=dict(autorange="reversed"),
        title=f"Top Specialized Skills in {city}"
    )

    st.plotly_chart(fig, use_container_width=True)

# ===================================================
# REGIONAL CLUSTERS
# ===================================================
elif page == "Regional Clusters":

    pivot = lift_df.pivot_table(
        index="city",
        columns="Taxonomy Skill",
        values="lift",
        fill_value=0
    )

    kmeans = KMeans(n_clusters=5, random_state=42)
    clusters = kmeans.fit_predict(pivot)

    cluster_df = pd.DataFrame({
        "City": pivot.index,
        "Cluster": clusters
    })

    st.subheader("Workforce Archetypes")
    st.dataframe(cluster_df.sort_values("Cluster"))

    st.markdown("---")
    st.subheader("Cluster Profiles")

    for cluster_id in sorted(cluster_df["Cluster"].unique()):
        st.markdown(f"### Cluster {cluster_id}")

        cluster_cities = cluster_df[cluster_df["Cluster"] == cluster_id]["City"]
        cluster_skill_data = lift_df[lift_df["city"].isin(cluster_cities)]

        cluster_profile = (
            cluster_skill_data.groupby("Taxonomy Skill")["lift"]
            .mean()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )

        fig = px.bar(
            cluster_profile,
            x="lift",
            y="Taxonomy Skill",
            orientation="h",
            color_discrete_sequence=["#1CA7A6"]
        )

        fig.update_layout(
            plot_bgcolor="white",
            paper_bgcolor="white",
            yaxis=dict(autorange="reversed")
        )

        st.plotly_chart(fig, use_container_width=True)

# ===================================================
# OPPORTUNITY GAPS
# ===================================================
elif page == "Opportunity Gaps":

    city = st.selectbox("Select City", sorted(lift_df["city"].unique()))
    city_data = lift_df[lift_df["city"] == city]

    state_avg = lift_df.groupby("Taxonomy Skill")["skill_share"].mean()

    gap_df = city_data.copy()
    gap_df["state_avg"] = gap_df["Taxonomy Skill"].map(state_avg)
    gap_df["gap"] = gap_df["state_avg"] - gap_df["skill_share"]

    opportunities = gap_df.sort_values("gap", ascending=False).head(10)

    st.subheader("Underdeveloped High-Demand Skills")
    st.dataframe(opportunities[["Taxonomy Skill", "gap"]].round(4))

# ===================================================
# TRAINING STRATEGY
# ===================================================
elif page == "Training Strategy":

    city = st.selectbox("Select City", sorted(lift_df["city"].unique()))
    city_df = lift_df[lift_df["city"] == city].sort_values("lift", ascending=False)

    st.subheader("Recommended Workforce Investment Tracks")

    for skill in city_df.head(5)["Taxonomy Skill"]:
        st.markdown(f"- Develop certification pathway in **{skill}**")

# ===================================================
# FOOTER
# ===================================================
st.markdown("---")
st.markdown(
    "<div style='text-align:center; color:#666;'>"
    "Colorado Workforce Intelligence Platform | Built for Economic Development Strategy"
    "</div>",
    unsafe_allow_html=True
)