import pandas as pd
import streamlit as st

# -----------------------------
# Load Data
# -----------------------------
@st.cache_data
def load_data():
    return pd.read_csv(
        "C:/Users/umesh/OneDrive/Desktop/cleaned_ola_Dataset_fixed.csv",
        low_memory=False
    )

# -----------------------------
# App Layout
# -----------------------------
st.set_page_config(page_title="Ola Rides Dashboard", layout="wide")
st.title("🚖 Ola Rides Data Dashboard (Cleaned Dataset)")

# Load dataset
df = load_data()

# -----------------------------
# Dataset Overview
# -----------------------------
st.header("📊 Dataset Overview")

col1, col2, col3 = st.columns(3)
col1.metric("Rows", f"{df.shape[0]:,}")
col2.metric("Columns", f"{df.shape[1]:,}")
col3.metric("Missing Values", df.isnull().sum().sum())

st.write("### First 10 Rows")
st.dataframe(df.head(10))

st.write("### Column Names")
st.write(list(df.columns))

# -----------------------------
# Summary Statistics
# -----------------------------
st.header("📈 Summary Statistics")
st.write(df.describe(include="all"))

# -----------------------------
# Exploratory Analysis
# -----------------------------
st.header("🔍 Exploratory Visualizations")

# 1. Rides per Day
if "ride_date" in df.columns:
    st.subheader("📅 Rides Per Day")
    rides_per_day = df.groupby(df["ride_date"]).size()
    st.line_chart(rides_per_day, height=300, use_container_width=True)

# 2. Average Fare per City
if "city" in df.columns and "fare" in df.columns:
    st.subheader("💰 Average Fare per City")
    avg_fare_city = df.groupby("city")["fare"].mean().sort_values()
    st.bar_chart(avg_fare_city, height=300, use_container_width=True)

# 3. Trip Distance Distribution
if "distance" in df.columns:
    st.subheader("📍 Trip Distance Distribution")
    st.histogram(df["distance"], bins=40)

# 4. Payment Method Usage
if "payment_method" in df.columns:
    st.subheader("💳 Payment Method Distribution")
    pm_counts = df["payment_method"].value_counts()
    st.bar_chart(pm_counts, height=300, use_container_width=True)

# 5. Top 10 Cities by Ride Count
if "city" in df.columns:
    st.subheader("🏙️ Top 10 Cities by Ride Count")
    top_cities = df["city"].value_counts().head(10)
    st.bar_chart(top_cities, height=300, use_container_width=True)

# -----------------------------
# Filters
# -----------------------------
st.header("🎛️ Interactive Filters")

if "city" in df.columns:
    city_choice = st.selectbox("Select a City:", options=["All"] + sorted(df["city"].unique().tolist()))
    if city_choice != "All":
        df = df[df["city"] == city_choice]

if "payment_method" in df.columns:
    payment_choice = st.multiselect("Filter by Payment Method:", options=df["payment_method"].unique())
    if payment_choice:
        df = df[df["payment_method"].isin(payment_choice)]

st.write("### Filtered Data Preview")
st.dataframe(df.head(20))
