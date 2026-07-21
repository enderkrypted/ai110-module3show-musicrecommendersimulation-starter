from src.recommender import Song, UserProfile, Recommender


def make_small_recommender() -> Recommender:
    songs = [
        Song(
            id=1,
            title="Test Pop Track",
            artist="Test Artist",
            genre="pop",
            mood="happy",
            energy=0.8,
            tempo_bpm=120,
            valence=0.9,
            danceability=0.8,
            acousticness=0.2,
        ),
        Song(
            id=2,
            title="Chill Lofi Loop",
            artist="Test Artist",
            genre="lofi",
            mood="chill",
            energy=0.4,
            tempo_bpm=80,
            valence=0.6,
            danceability=0.5,
            acousticness=0.9,
        ),
        Song(
            id=3,
            title="Mismatch Track",
            artist="Test Artist",
            genre="rock",
            mood="intense",
            energy=0.1,
            tempo_bpm=150,
            valence=0.2,
            danceability=0.3,
            acousticness=0.05,
        ),
    ]
    return Recommender(songs)


# ---------- recommend() ----------

def test_recommend_returns_songs_sorted_by_score():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    results = rec.recommend(user, k=2)

    assert len(results) == 2
    # Starter expectation: the pop, happy, high energy song should score higher
    assert results[0].genre == "pop"
    assert results[0].mood == "happy"


def test_recommend_respects_k_limit():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    results = rec.recommend(user, k=1)
    assert len(results) == 1


def test_recommend_k_larger_than_catalog_returns_all_songs():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    results = rec.recommend(user, k=10)
    assert len(results) == 3  # catalog only has 3 songs


def test_recommend_worst_match_ranks_last():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    results = rec.recommend(user, k=3)
    # "Mismatch Track" has no genre/mood match and energy far from 0.8
    assert results[-1].title == "Mismatch Track"


def test_recommend_scores_are_actually_descending():
    user = UserProfile(
        favorite_genre="lofi",
        favorite_mood="chill",
        target_energy=0.4,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    results = rec.recommend(user, k=3)
    scores = [rec._score(user, song)[0] for song in results]
    assert scores == sorted(scores, reverse=True)


def test_recommend_empty_catalog_returns_empty_list():
    rec = Recommender(songs=[])
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    results = rec.recommend(user, k=5)
    assert results == []


def test_recommend_with_no_matching_genre_or_mood_still_returns_results():
    user = UserProfile(
        favorite_genre="jazz",       # not in the small catalog
        favorite_mood="relaxed",     # not in the small catalog
        target_energy=0.5,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    results = rec.recommend(user, k=3)
    # Should not crash, should still return all 3 songs ranked by energy closeness alone
    assert len(results) == 3


def test_likes_acoustic_boosts_high_acousticness_song():
    user_no_pref = UserProfile(
        favorite_genre="lofi",
        favorite_mood="chill",
        target_energy=0.4,
        likes_acoustic=False,
    )
    user_likes_acoustic = UserProfile(
        favorite_genre="lofi",
        favorite_mood="chill",
        target_energy=0.4,
        likes_acoustic=True,
    )
    rec = make_small_recommender()
    lofi_song = rec.songs[1]  # acousticness=0.9

    score_without, _ = rec._score(user_no_pref, lofi_song)
    score_with, _ = rec._score(user_likes_acoustic, lofi_song)

    assert score_with > score_without


# ---------- explain_recommendation() ----------

def test_explain_recommendation_returns_non_empty_string():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    song = rec.songs[0]

    explanation = rec.explain_recommendation(user, song)
    assert isinstance(explanation, str)
    assert explanation.strip() != ""


def test_explain_recommendation_mentions_genre_match_when_applicable():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    song = rec.songs[0]  # pop, happy

    explanation = rec.explain_recommendation(user, song)
    assert "genre match" in explanation
    assert "mood match" in explanation


def test_explain_recommendation_no_matches_still_returns_string():
    user = UserProfile(
        favorite_genre="jazz",
        favorite_mood="relaxed",
        target_energy=0.5,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    song = rec.songs[2]  # rock, intense - no genre/mood match

    explanation = rec.explain_recommendation(user, song)
    assert isinstance(explanation, str)
    assert explanation.strip() != ""
    assert "genre match" not in explanation
    assert "mood match" not in explanation