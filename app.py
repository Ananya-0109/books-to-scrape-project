import pandas as pd
import plotly.express as px
import streamlit as st
import os

# Path to CSV
csv_file = "data/books_cleaned.csv"

# Check if file exists
if not os.path.exists(csv_file):
    st.error("❌ Run clean_data.py first to generate books_cleaned.csv")
    st.stop()

# Load data
df = pd.read_csv(csv_file)

# Dashboard title
st.title("📚 Books to Scrape Dashboard")
st.write("Interactive dashboard generated from scraped data.")

# -----------------------------
# Price distribution
# -----------------------------
fig1 = px.histogram(
    df,
    x="Price",
    nbins=20,
    title="Book Price Distribution",
    color_discrete_sequence=["#4CAF50"]
)
st.plotly_chart(fig1)

# -----------------------------
# Books per category
# -----------------------------
category_count = df["Category"].value_counts().reset_index()
category_count.columns = ["Category", "Count"]  # Rename columns for clarity

fig2 = px.bar(
    category_count,
    x="Category",
    y="Count",
    title="Books per Category",
    color_discrete_sequence=["#2196F3"]
)
st.plotly_chart(fig2)

# -----------------------------
# Show raw data option
# -----------------------------
if st.checkbox("Show Raw Data"):
    st.dataframe(df)
