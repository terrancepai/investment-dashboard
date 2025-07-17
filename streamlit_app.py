import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Set page configuration
st.set_page_config(page_title="Modular Investment Platform", layout="wide")

st.markdown("### Modular Investment Analysis Platform with Real Real-Time Data for Portfolio Optimization and Advisory")
st.markdown("---")

# Sample investment data
data = {
    "Investment Name": [
        "US Equity Fund", "Global Bond ETF", "Commercial Real Estate", "Gold ETF",
        "Life Settlements Fund", "Direct Lending Fund", "Infrastructure Trust"
    ],
    "Category": [
        "Equities", "Bonds", "Real Estate", "Commodities",
        "Life Settlements", "Direct Lending", "Infrastructure"
    ],
    "Expected Return (%)": [8.5, 4.2, 7.8, 5.1, 10, 9.5, 6.7],
    "Risk Level (1-10)": [7, 3, 6, 5, 4, 5, 4],
    "Cap Rate (%)": [None, None, 6.5, None, None, None, 5.5],
    "Liquidity (1-10)": [9, 8, 3, 9, 2, 4, 3],
    "Volatility (1-10)": [7, 3, 4, 5, 2, 3, 3],
    "Fees (%)": [1, 0.2, 1.5, 0.4, 1.8, 1.2, 1.0],
    "Time Horizon": ["Long", "Medium", "Long", "Medium", "Long", "Medium", "Long"],
    "Inflation Hedge": ["No", "No", "Yes", "Yes", "No", "No", "Yes"],
    "Minimum Investment ($)": [10000, 5000, 50000, 10000, 10000, 75000, 60000]
}

df = pd.DataFrame(data)

# Interactive filters
categories = st.multiselect("Choose investment categories:", df["Category"].unique(), default=list(df["Category"].unique()))
df_filtered = df[df["Category"].isin(categories)]

# Display investment table
st.markdown("### Configure Investment Data")
st.dataframe(df_filtered, use_container_width=True)

# Portfolio Averages and Returns
st.markdown("## Portfolio Averages and Returns")
cols = st.columns(7)
metrics = {
    "Avg Return (%)": df_filtered["Expected Return (%)"].mean(),
    "Avg Risk": df_filtered["Risk Level (1-10)"].mean(),
    "Avg Cap Rate (%)": df_filtered["Cap Rate (%)"].dropna().mean(),
    "Avg Liquidity": df_filtered["Liquidity (1-10)"].mean(),
    "Avg Volatility": df_filtered["Volatility (1-10)"].mean(),
    "Avg Fees (%)": df_filtered["Fees (%)"].mean(),
    "Avg Min Inv ($)": df_filtered["Minimum Investment ($)"].mean()
}
for i, (label, value) in enumerate(metrics.items()):
    cols[i].metric(label, f"{value:.2f}" if isinstance(value, float) else value)

# Graphs
st.markdown("## Portfolio Graphs and Trends")
col1, col2, col3, col4 = st.columns(4)
with col1:
    df_filtered.plot(kind="bar", x="Investment Name", y="Expected Return (%)", color="salmon", legend=False)
    st.pyplot(plt.gcf())
    plt.clf()
with col2:
    plt.scatter(df_filtered["Volatility (1-10)"], df_filtered["Liquidity (1-10)"], color="red")
    plt.xlabel("Volatility (1-10)")
    plt.ylabel("Liquidity (1-10)")
    st.pyplot(plt.gcf())
    plt.clf()
with col3:
    plt.scatter(df_filtered["Fees (%)"], df_filtered["Expected Return (%)"], color="red")
    plt.xlabel("Fees (%)")
    plt.ylabel("Expected Return (%)")
    st.pyplot(plt.gcf())
    plt.clf()
with col4:
    df_filtered["Risk Level (1-10)"].hist(color="salmon")
    plt.xlabel("Risk Level (1-10)")
    st.pyplot(plt.gcf())
    plt.clf()

# Constraints section
st.markdown("## Portfolio Choices and Constraints")
min_inv = st.slider("Min Investment ($)", 0, 100000, 0)
min_return = st.slider("Min Return (%)", 0.0, 15.0, 0.0)
max_risk = st.slider("Max Risk level", 0, 10, 10)
time_horizon = st.selectbox("Time Horizon", ["Short", "Medium", "Long"])
inflation_only = st.checkbox("Inflation Hedge Only")

# Apply filters
df_constraints = df_filtered[
    (df_filtered["Minimum Investment ($)"] >= min_inv) &
    (df_filtered["Expected Return (%)"] >= min_return) &
    (df_filtered["Risk Level (1-10)"] <= max_risk) &
    (df_filtered["Time Horizon"] == time_horizon)
]
if inflation_only:
    df_constraints = df_constraints[df_constraints["Inflation Hedge"] == "Yes"]

# Filtered results
st.markdown("## Filtered Investments")
st.dataframe(df_constraints, use_container_width=True)

# Download buttons
st.markdown("## Export Data and Reports")
col1, col2 = st.columns(2)
with col1:
    st.download_button("Download PowerPoint", data=df_constraints.to_csv().encode(), file_name="portfolio_data.csv")
with col2:
    st.download_button("Download Word", data=df_constraints.to_csv().encode(), file_name="portfolio_data.csv")

# Footer
st.markdown("---")
st.markdown("[💼 LinkedIn](https://www.linkedin.com/in/terrancepai/)")