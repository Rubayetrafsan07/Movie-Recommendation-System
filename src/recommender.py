import pandas as pd


class MovieRecommender:

    def __init__(self, model_data, similarity):
        self.model_data = model_data
        self.similarity = similarity

    def recommend(self, movie, n=5):

        
        movie_matches = self.model_data[
            self.model_data['title'].str.lower()
            == movie.strip().lower()
        ]

        if movie_matches.empty:
            return pd.DataFrame(
                columns=['title', 'similarity']
            )

       
        movie_index = movie_matches.index[0]

        # Get similarity scores for this movie
        similar_movies = list(
            enumerate(self.similarity[movie_index])
        )

        similar_movies = sorted(
            similar_movies,
            key=lambda x: x[1],
            reverse=True
        )

        recommendations = []

        for index, score in similar_movies[1:n + 1]:

            recommendations.append({
                'title': self.model_data.iloc[index]['title'],
                'similarity': round(float(score), 3)
            })

        return pd.DataFrame(recommendations)