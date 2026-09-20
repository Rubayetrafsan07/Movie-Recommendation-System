import streamlit as st
import pandas as pd

from src.model import build_model
from src.recommender import MovieRecommender



st.set_page_config(
    page_title="Movie Recommendation System",
    page_icon="🎬",
    layout="centered"
)

st.markdown(
    """
    <style>
        .stApp,
        [data-testid="stAppViewContainer"],
        [data-testid="stAppViewContainer"] > .main {
            background-color: #f7f4ef !important;
            color: #20252b !important;
        }

        [data-testid="stHeader"] {
            background: #f7f4ef !important;
        }

        .block-container {
            max-width: 820px;
            padding-top: 4rem;
            padding-bottom: 4rem;
        }

        h1 {
            color: #20252b;
            font-size: 3rem !important;
            letter-spacing: -0.04em;
            margin-bottom: 0.25rem !important;
        }

        h2, h3 {
            color: #20252b;
        }

        [data-testid="stTextInput"] label,
        [data-testid="stSelectbox"] label {
            color: #59616a;
            font-weight: 600;
        }

        [data-testid="stTextInput"] input {
            background: #fffdf9 !important;
            color: #20252b !important;
            caret-color: #e0644f !important;
            border: 1px solid #d8d1c8;
            border-radius: 10px;
        }

        [data-testid="stTextInput"] input::placeholder {
            color: #858b91 !important;
            opacity: 1;
        }

        [data-testid="stSelectbox"] [data-baseweb="select"] > div {
            background: #fffdf9 !important;
            color: #20252b !important;
            border-color: #d8d1c8 !important;
        }

        [data-testid="stSelectbox"] [data-baseweb="select"] * {
            color: #20252b !important;
        }

        [role="listbox"],
        [role="option"] {
            background: #fffdf9 !important;
            color: #20252b !important;
        }

        [data-testid="stButton"] button {
            min-height: 42px;
            margin-top: 1.75rem;
            border: 0;
            border-radius: 10px;
            background: #e0644f;
            color: white;
            font-weight: 700;
            transition: background 150ms ease, transform 150ms ease;
        }

        [data-testid="stButton"] button:hover {
            background: #c9513e;
            transform: translateY(-1px);
        }

        [data-testid="stMarkdownContainer"] strong {
            color: #20252b;
        }

        [data-testid="stAlert"] {
            background: #fff0d6 !important;
            border: 1px solid #e2aa5b !important;
            border-radius: 10px;
            color: #6b3d0c !important;
        }

        [data-testid="stAlert"] p,
        [data-testid="stAlert"] span,
        [data-testid="stAlert"] div {
            color: #6b3d0c !important;
        }

        @media (max-width: 640px) {
            .block-container {
                padding-top: 2rem;
            }

            h1 {
                font-size: 2.25rem !important;
            }
        }
    </style>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# Load data and build model
# --------------------------------------------------

@st.cache_data
def load_data():
    return pd.read_csv(
        "data/processed/movies_cleaned.csv"
    )


@st.cache_resource
def load_model(model_data):
    tfidf_matrix, similarity = build_model(
        model_data
    )

    return MovieRecommender(
        model_data,
        similarity
    )


model_data = load_data()
recommender = load_model(model_data)


# --------------------------------------------------
# Session state
# --------------------------------------------------

if "selected_movie" not in st.session_state:
    st.session_state.selected_movie = ""

if "recommendations" not in st.session_state:
    st.session_state.recommendations = None

if "search_requested" not in st.session_state:
    st.session_state.search_requested = False


def handle_search_change():
    """Submit committed input and clear results when the input is empty."""
    if st.session_state.movie_search.strip():
        st.session_state.search_requested = True
    else:
        st.session_state.selected_movie = ""
        st.session_state.recommendations = None




st.title("🎬 Movie Recommendation System")

st.write(
    "Find movies similar to your favorite movies "
    "using content-based filtering."
)


# --------------------------------------------------
# Search input
# --------------------------------------------------

search_column, button_column = st.columns([5, 1])

with search_column:
    search_text = st.text_input(
        "🔎 Search for a movie:",
        placeholder="Type a movie title...",
        key="movie_search",
        on_change=handle_search_change
    )

with button_column:
    search_clicked = st.button(
        "Search",
        type="primary",
        use_container_width=True
    )


# --------------------------------------------------
# Run recommendation
# --------------------------------------------------

if search_clicked:

    st.session_state.search_requested = True


if st.session_state.search_requested:

    st.session_state.search_requested = False

    typed_title = search_text.strip()
    title_matches = model_data[
        model_data["title"].str.contains(
            typed_title,
            case=False,
            na=False,
            regex=False
        )
    ]["title"].tolist()

    if not typed_title or not title_matches:

        st.warning(
            "Please enter a movie title that exists in the dataset."
        )

    else:

        exact_match = next(
            (
                title for title in title_matches
                if title.lower() == typed_title.lower()
            ),
            title_matches[0]
        )

        st.session_state.selected_movie = typed_title

        st.session_state.recommendations = (
            recommender.recommend(
                exact_match,
                n=5
            )
        )


# --------------------------------------------------
# Display selected movie
# --------------------------------------------------

if st.session_state.selected_movie:

    with st.container(border=True):
        st.subheader("🎬 Your Movie")
        st.write(
            f"⭐ **{st.session_state.selected_movie}**"
        )


# --------------------------------------------------
# Display recommendations
# --------------------------------------------------

if st.session_state.recommendations is not None:

    with st.container(border=True):
        st.subheader("🎯 Recommended Movies")

        for _, row in st.session_state.recommendations.iterrows():
            st.write(
                f"🎬 **{row['title']}** — "
                f"Similarity: {row['similarity']:.3f}"
            )