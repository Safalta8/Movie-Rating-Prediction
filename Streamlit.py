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
.stApp {
    background-color: #091413;
    color: #a9d9ca;
}
[data-testid="stSidebar"] {
    background-color: #2b5d4a;
}
[data-testid="stSidebar"] * {
    color: #a9d9ca !important;
}
h1, h2, h3 {
    color: #a9d9ca;
}
label {
    color: #a9d9ca !important;
}
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
.kpi-card {
    backdrop-filter: blur(10px);
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.6);
    border: 1px solid rgba(255,255,255,0.1);
    margin-bottom: 10px;
    font-weight: bold;
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
with open("Project.pkl", "rb") as file:
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
# SAMPLE DATA
# ----------------------
df = pd.DataFrame({
    "Year": [2000, 2005, 2010, 2015, 2020],
    "Rating": [6.5, 7.0, 7.5, 8.0, 8.3],
    "Gross": [50, 120, 200, 300, 500],
    "Genre": ["Action", "Comedy", "Drama", "Sci-Fi", "Romance"]
})

st.markdown("---")

# ----------------------
# KPI CARDS with Painted Gradient Style
# ----------------------
if Prediction is not None:
    col1, col2, col3 = st.columns(3)

    # Rating card gradient
    if Prediction > 7:
        rating_color = "background: linear-gradient(135deg, #006400, #228B22); color: #d4f5d4;"
    elif Prediction >= 5:
        rating_color = "background: linear-gradient(135deg, #FFD700, #FFA500); color: #fffacd;"
    else:
        rating_color = "background: linear-gradient(135deg, #8B0000, #B22222); color: #ffcccb;"

    # Gross card gradient
    if Gross_in_M > 300:
        gross_color = "background: linear-gradient(135deg, #2b5d4a, #5fa08d); color: #e0fff9;"
    else:
        gross_color = "background: linear-gradient(135deg, #3e7c6f, #2b5d4a); color: #a9d9ca;"

    # Year card gradient
    year_color = "background: linear-gradient(135deg, #091413, #2b5d4a); color: #a9d9ca;"

    with col1:
        st.markdown(f"<div class='kpi-card' style='{rating_color}'>⭐ Rating<br>{round(Prediction,2)}</div>", unsafe_allow_html=True)

    with col2:
        st.markdown(f"<div class='kpi-card' style='{gross_color}'>💰 Gross<br>{Gross_in_M}M</div>", unsafe_allow_html=True)

    with col3:
        st.markdown(f"<div class='kpi-card' style='{year_color}'>📅 Year<br>{Year}</div>", unsafe_allow_html=True)

# ----------------------
# CHARTS (Cinematic Style)
# ----------------------
chart_bg = "#f5f5f5"
text_color = "#091413"
palette = ["#3e7c6f", "#2b5d4a", "#a9d9ca", "#5fa08d", "#1c3b32"]

st.markdown("### 📈 Rating Trend Over Years")
fig1 = px.line(df, x="Year", y="Rating", markers=True,
               color_discrete_sequence=["#3e7c6f"], 
               title="Average Movie Ratings Over Time")
fig1.update_layout(plot_bgcolor=chart_bg, paper_bgcolor=chart_bg, font=dict(color=text_color))
st.plotly_chart(fig1, use_container_width=True)

st.markdown("### 💰 Gross Earnings by Year")
fig2 = px.bar(df, x="Year", y="Gross", 
              color="Gross",  
              color_continuous_scale="Tealgrn",  
              title="Gross Revenue Distribution")
fig2.update_traces(marker=dict(line=dict(color="#091413", width=1), opacity=0.85))
fig2.update_layout(plot_bgcolor=chart_bg, paper_bgcolor=chart_bg, font=dict(color=text_color))
st.plotly_chart(fig2, use_container_width=True)

st.markdown("### 🎭 Genre Distribution")
fig3 = px.pie(df, names="Genre", hole=0.4, color_discrete_sequence=palette, 
              title="Genre Share in Dataset")
fig3.update_layout(plot_bgcolor=chart_bg, paper_bgcolor=chart_bg, font=dict(color=text_color))
st.plotly_chart(fig3, use_container_width=True)

# ----------------------
# SIDEBAR (Final About Section Only)
# ----------------------


# ----------------------
# SIDEBAR (Final About Section Only)
# ----------------------
st.sidebar.header("🎬 About")
st.sidebar.info("""
This Movie Rating Predictor uses a **Machine Learning model** trained on historical movie data.  
Here’s how it works:
1. Enter movie details (Year, Runtime, Gross, Genres, Certificate).
2. The ML model processes these inputs.
3. It predicts the **expected IMDb-style rating**.
4. Visual charts show trends in ratings, revenue, and genre distribution.

✨ Built with **Streamlit + Plotly** for an interactive cinematic dashboard.
""")