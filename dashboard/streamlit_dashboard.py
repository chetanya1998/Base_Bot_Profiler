# dashboard/streamlit_dashboard.py
import streamlit as st
import pandas as pd
from clustering.cluster_profiles import cluster_behaviors
from visualization.visualize_clusters import plot_clusters

st.title("Bot Behavior Profiler Dashboard")

uploaded_file = st.file_uploader("Upload access logs CSV", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file, parse_dates=['timestamp'])
    feature_df = cluster_behaviors(df)
    
    st.subheader("Cluster Summary")
    st.dataframe(feature_df)
    
    st.subheader("Cluster Visualization")
    plot_clusters(feature_df)
