import json
import os


class MovieRecommender:
    def __init__(self, data_path="data/movies.json"):
        self.data_path = data_path
        self.movies = self._load_movies()

    def _load_movies(self):
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        full_path = os.path.join(base_path, self.data_path)
        try:
            with open(full_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return self._default_movies()

    def _default_movies(self):
        return {
            "happy": ["The Grand Budapest Hotel", "La La Land", "Superbad", "The Intouchables", "About Time"],
            "sad": ["The Shawshank Redemption", "Manchester by the Sea", "Eternal Sunshine of the Spotless Mind", "Grave of the Fireflies", "Requiem for a Dream"],
            "neutral": ["Inception", "The Matrix", "Pulp Fiction", "Parasite", "The Prestige"],
            "angry": ["John Wick", "Gladiator", "Die Hard", "Mad Max: Fury Road", "Kill Bill"],
            "surprised": ["Shutter Island", "Prisoners", "Memento", "The Sixth Sense", "Arrival"],
            "tired": ["The Secret Life of Walter Mitty", "Chef", "Up", "Inside Out", "Ratatouille"],
            "excited": ["Mad Max: Fury Road", "The Dark Knight", "Interstellar", "Dune", "Everything Everywhere All at Once"]
        }

    def get_movies_by_mood(self, mood):
        return self.movies.get(mood.lower(), self.movies.get("neutral", []))

    def recommend(self, mood):
        movies = self.get_movies_by_mood(mood)
        return movies[:5]