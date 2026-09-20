from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def build_model(model_data):

    tfidf = TfidfVectorizer(
        max_features=5000,
        stop_words='english'
    )

    tfidf_matrix = tfidf.fit_transform(model_data['tags'])

    similarity = cosine_similarity(tfidf_matrix)

    return tfidf_matrix, similarity