import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def _score(self, user: UserProfile, song: Song) -> Tuple[float, List[str]]:
        """Internal helper: scores one Song against a UserProfile."""
        score = 0.0
        reasons = []

        if user.favorite_genre == song.genre:
            score += 2.0
            reasons.append("genre match (+2.0)")

        if user.favorite_mood == song.mood:
            score += 1.0
            reasons.append("mood match (+1.0)")

        gap = abs(user.target_energy - song.energy)
        energy_points = 1.5 * (1 - gap)
        score += energy_points
        reasons.append(f"energy closeness (+{energy_points:.2f})")

        if user.likes_acoustic and song.acousticness >= 0.7:
            score += 0.5
            reasons.append("acoustic preference match (+0.5)")

        return score, reasons

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Returns the top k songs ranked against the given user profile."""
        scored = [(song, self._score(user, song)[0]) for song in self.songs]
        scored.sort(key=lambda item: item[1], reverse=True)
        return [song for song, _ in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Explains why a given song was recommended to the user."""
        _, reasons = self._score(user, song)
        return ", ".join(reasons) if reasons else "no strong matches"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    songs = []
    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["id"] = int(row["id"])
            row["energy"] = float(row["energy"])
            row["tempo_bpm"] = float(row["tempo_bpm"])
            row["valence"] = float(row["valence"])
            row["danceability"] = float(row["danceability"])
            row["acousticness"] = float(row["acousticness"])
            songs.append(row)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py

    Algorithm Recipe:
      - genre match: +2.0
      - mood match: +1.0
      - energy closeness: up to +1.5, scaled by how close the song's
        energy is to the user's target_energy (max gap is 1.0 since
        energy is on a 0-1 scale)
    """
    score = 0.0
    reasons = []

    if user_prefs.get("genre") == song.get("genre"):
        score += 2.0
        reasons.append("genre match (+2.0)")

    if user_prefs.get("mood") == song.get("mood"):
        score += 1.0
        reasons.append("mood match (+1.0)")

    if "energy" in user_prefs and song.get("energy") is not None:
        gap = abs(user_prefs["energy"] - song["energy"])
        energy_points = 1.5 * (1 - gap)
        score += energy_points
        reasons.append(f"energy closeness (+{energy_points:.2f})")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = ", ".join(reasons) if reasons else "no strong matches"
        scored.append((song, score, explanation))

    scored.sort(key=lambda item: item[1], reverse=True)

    return scored[:k]