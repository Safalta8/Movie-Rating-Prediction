import streamlit as st
import pickle
import pandas as pd
import plotly.express as px
import os

# ----------------------
# PAGE CONFIG
# ----------------------
st.set_page_config(
    page_title="Movie Rating Prediction",
    page_icon="🎬",
    layout="centered"
)

# ----------------------
# CUSTOM DARK THEME CSS
# ----------------------
st.markdown("""
<style>

/* Main Background */
.stApp {
    background-color: #091413;
    color: #a9d9ca;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #2b5d4a;
}
[data-testid="stSidebar"] * {
    color: #a9d9ca !important;
}

/* Headings */
h1, h2, h3 {
    color: #a9d9ca;
}

/* Inputs */
label {
    color: #a9d9ca !important;
}

/* Buttons */
div.stButton > button {
    background-color: #2b5d4a;
    color: #a9d9ca;
    border-radius: 8px;
    transition: 0.3s;
}
div.stButton > button:hover {
    background-color: #3e7c6f;
    transform: scale(1.05);
    color: white;
}

/* KPI Cards (Glass Effect) */
.kpi-card {
    background: rgba(62, 124, 111, 0.2);
    backdrop-filter: blur(10px);
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    color: #a9d9ca;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.6);
    border: 1px solid rgba(255,255,255,0.1);
    margin-bottom: 10px;
}

</style>
""", unsafe_allow_html=True)

# ----------------------
# TITLE
# ----------------------
st.markdown("""
<h1 style='text-align:center; font-size:45px; letter-spacing:2px;'>
🎬 MOVIE RATING PREDICTION
</h1>
""", unsafe_allow_html=True)

st.markdown("---")

# ----------------------
# DICTIONARIES
# ----------------------
convertGenreToLabel = {
    'Action': 0, 'Adventure':1, 'Animation':2, 'Biography':3, 'Comedy':4,
    'Crime':5, 'Drama':6, 'Family':7, 'Fantasy':8, 'Film-Noir':9,
    'History':10, 'Horror':11, 'Music':12, 'Musical':13, 'Mystery':14,
    'Romance':15, 'Sci-Fi':16, 'Sport':17, 'Thriller':18, 'War':19, 'Western':20
}

convertRatingToLabel = {
    'Not Rated': 0, 'Unrated': 1, 'U': 2, 'G': 3, '13': 4, 'PG': 5,
    'M/PG': 6, 'PG-13': 7, 'UA': 8, 'TV-PG': 9, 'TV-14': 10,
    'Approved': 11, 'Passed': 12, 'GP': 13, 'A': 14, 'TV-MA': 15,
    'R': 16, '18': 17, 'NC-17': 18
}

# ----------------------
# INPUTS
# ----------------------
col1, col2 = st.columns(2)

with col1:
    Rank = st.number_input("Rank", 1)
    Year = st.number_input("Year", 1900, 2026)
    Runtime_in_min = st.number_input("Runtime (minutes)", 1)
    Metascore = st.number_input("Metascore", 0, 100)

with col2:
    Gross_in_M = st.number_input("Gross ($M)", 0)
    Genre_1 = st.selectbox("Genre 1", list(convertGenreToLabel.keys()))
    Genre_2 = st.selectbox("Genre 2", list(convertGenreToLabel.keys()))
    Genre_3 = st.selectbox("Genre 3", list(convertGenreToLabel.keys()))
    Certificate = st.selectbox("Certificate", list(convertRatingToLabel.keys()))

# ----------------------
# LOAD MODEL
# ----------------------
model_path = os.path.join(os.getcwd(), "Project.pkl")
with open("C:\\Users\\user\\OneDrive\\Desktop\\Move Rating Prediction\\Project.pkl", "rb") as file:
    model = pickle.load(file)

# ----------------------
# PREDICTION
# ----------------------
Prediction = None

if st.button("🔮 Predict Rating"):
    features = [[
        Rank, Year, Runtime_in_min, Metascore, Gross_in_M,
        convertGenreToLabel[Genre_1],
        convertGenreToLabel[Genre_2],
        convertGenreToLabel[Genre_3],
        convertRatingToLabel[Certificate]
    ]]
    Prediction = model.predict(features)[0]
    st.success(f"⭐ Predicted Rating: {round(Prediction, 2)} / 10")

# ----------------------
# SIDEBAR
# ----------------------
st.sidebar.header("🎬 About")
st.sidebar.info("Dark themed Movie Rating Predictor using ML.")

# ----------------------
# SAMPLE DATA (for charts)
# ----------------------
df = pd.DataFrame({
    "Year": [2000, 2005, 2010, 2015, 2020],
    "Rating": [6.5, 7.0, 7.5, 8.0, 8.3],
    "Gross": [50, 120, 200, 300, 500],
    "Genre": ["Action", "Comedy", "Drama", "Sci-Fi", "Romance"]
})

st.markdown("---")

# ----------------------
# CHARTS (LIGHT BACKGROUND)
# ----------------------
chart_bg = "#f5f5f5"  # light background for charts
text_color = "#091413"  # dark text for contrast

# Line Chart
fig1 = px.line(df, x="Year", y="Rating", color_discrete_sequence=["#3e7c6f"])
fig1.update_layout(
    plot_bgcolor=chart_bg,
    paper_bgcolor=chart_bg,
    font=dict(color=text_color)
)
st.plotly_chart(fig1, use_container_width=True)

# Bar Chart
fig2 = px.bar(df, x="Year", y="Gross", color_discrete_sequence=["#2b5d4a"])
fig2.update_layout(
    plot_bgcolor=chart_bg,
    paper_bgcolor=chart_bg,
    font=dict(color=text_color)
)
st.plotly_chart(fig2, use_container_width=True)

# Pie Chart
fig3 = px.pie(df, names="Genre", hole=0.4, color_discrete_sequence=px.colors.sequential.Teal)
fig3.update_layout(
    plot_bgcolor=chart_bg,
    paper_bgcolor=chart_bg,
    font=dict(color=text_color)
)
st.plotly_chart(fig3, use_container_width=True)

# ----------------------
# KPI CARDS
# ----------------------
if Prediction is not None:
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"<div class='kpi-card'>⭐ Rating<br>{round(Prediction,2)}</div>", unsafe_allow_html=True)

    with col2:
        st.markdown(f"<div class='kpi-card'>💰 Gross<br>{Gross_in_M}M</div>", unsafe_allow_html=True)

    with col3:
        st.markdown(f"<div class='kpi-card'>📅 Year<br>{Year}</div>", unsafe_allow_html=True)