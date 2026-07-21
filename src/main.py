"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")

    # Three distinct user taste profiles to compare recommendation behavior
    user_profiles = {
        "High-Energy Pop": {"genre": "pop", "mood": "happy", "energy": 0.8},
        "Chill Lofi": {"genre": "lofi", "mood": "chill", "energy": 0.35},
        "Deep Intense Rock": {"genre": "rock", "mood": "intense", "energy": 0.9},

        # Edge case / adversarial profiles
        "Conflicting Energy+Mood": {"genre": "rock", "mood": "sad", "energy": 0.9},
        "Nonexistent Genre": {"genre": "k-pop", "mood": "happy", "energy": 0.7},
        "Empty Preferences": {},
        "Out-of-Range Energy": {"genre": "ambient", "mood": "chill", "energy": 1.5},
        "Opposite Extreme": {"genre": "opera", "mood": "furious", "energy": 0.0},
    }

    for profile_name, user_prefs in user_profiles.items():
        print(f"\n=== {profile_name} ({user_prefs}) ===")

        recommendations = recommend_songs(user_prefs, songs, k=5)

        print("\nTop recommendations:\n")
        for rec in recommendations:
            # You decide the structure of each returned item.
            # A common pattern is: (song, score, explanation)
            song, score, explanation = rec
            print(f"{song['title']} - Score: {score:.2f}")
            print(f"Because: {explanation}")
            print()


if __name__ == "__main__":
    main()