# visualize.py
import os
import pandas as pd
import plotly.express as px

# Path to cleaned data
CSV = os.path.join("data", "books_cleaned.csv")

if not os.path.exists(CSV):
    raise FileNotFoundError(f"{CSV} not found. Run clean_data.py first.")

# Load data
df = pd.read_csv(CSV)

print("✅ Loaded data with columns:", list(df.columns))

def safe_show_hist(col, title, nbins=20):
    """Show histogram if column exists."""
    if col not in df.columns:
        print(f"⚠ Skipping {title}: column '{col}' not found.")
        return
    fig = px.histogram(df, x=col, nbins=nbins, title=title,
                       color_discrete_sequence=["#4CAF50"])
    fig.show()

def safe_show_bar_count(col, title, top_n=20):
    """Show bar chart from value counts if column exists, with unique col names."""
    if col not in df.columns:
        print(f"⚠ Skipping {title}: column '{col}' not found.")
        return
    counts = df[col].value_counts().reset_index()
    counts.columns = [col, "Count"]  # ✅ Ensure unique names
    fig = px.bar(counts.head(top_n), x=col, y="Count", title=title,
                 color_discrete_sequence=["#2196F3"])
    fig.show()

# 1️⃣ Price distribution
if "PriceNum" in df.columns:
    safe_show_hist("PriceNum", "📊 Book Price Distribution", nbins=30)

# 2️⃣ Stock distribution
if "Stock" in df.columns:
    safe_show_hist("Stock", "📦 Book Stock Distribution", nbins=20)

# 3️⃣ Books per category
if "Category" in df.columns and df["Category"].notna().any():
    safe_show_bar_count("Category", "📚 Books per Category", top_n=15)

# 4️⃣ Ratings distribution
if "Rating" in df.columns and df["Rating"].notna().any():
    safe_show_bar_count("Rating", "⭐ Books by Rating", top_n=10)
elif "RatingText" in df.columns:
    safe_show_bar_count("RatingText", "⭐ Books by Rating Text", top_n=10)

# 5️⃣ Top 10 expensive books
if "PriceNum" in df.columns and "Title" in df.columns:
    top10 = df.sort_values("PriceNum", ascending=False).head(10)
    fig = px.bar(top10, x="Title", y="PriceNum",
                 title="💰 Top 10 Most Expensive Books",
                 color_discrete_sequence=["#FF5722"])
    fig.update_layout(xaxis={'categoryorder': 'total descending'}, xaxis_tickangle=-45)
    fig.show()
