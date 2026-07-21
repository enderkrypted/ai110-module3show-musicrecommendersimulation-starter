# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

--- This project is a small music recommender that works off a catalog of 18 songs. Each song has attributes like genre, mood, and energy, and the user has a "taste profile" with a favorite genre, favorite mood, and target energy level. The system compares every song to that profile and gives it a score — matching genre and mood earns points, and energy is scored by how close it is to what the user wants, not just whether it's high or low. All songs get ranked by score, and the top few are recommended, each with a short explanation of why. I tested it with normal user tastes and also with weird edge-case inputs to see where it breaks, which showed both what the system does well and where it has real flaws, like leaning too hard on genre and not handling bad input gracefully. These are small versions of the same kinds of tradeoffs real recommenders like Spotify make.

## How The System Works

Explain your design in plain language.

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
- What information does your `UserProfile` store
- How does your `Recommender` compute a score for each song
- How do you choose which songs to recommend

You can include a simple diagram or bullet list if helpful.



--- Real-world recommenders like Spotify or YouTube usually work one of two ways: by looking at what similar users liked (collaborative filtering), or by looking at the actual attributes of the songs themselves (content-based filtering). This project is a simple content-based system — there's only one user, so it works by comparing song attributes to that user's stated preferences, rather than comparing users to each other. Each Song has four features: genre, mood, energy (0–1), and valence (0–1, how positive or negative the song feels). The UserProfile stores the same four features as preferences: preferred_genre, preferred_mood, preferred_energy, and preferred_valence.
The Recommender scores each song by comparing it to the user's profile. Genre and mood either match or they don't, and a match adds points (genre counts for more, since it's usually the strongest signal for "vibe"). Energy and valence are scored differently — instead of rewarding high values, the system rewards songs whose energy and valence are close to what the user prefers. All songs are scored this way, sorted from highest to lowest, and the top few are returned as recommendations.

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

--- tests/test_recommender.py::test_recommend_returns_songs_sorted_by_score PASSED     [9%]
tests/test_recommender.py::test_recommend_respects_k_limit PASSED                     [18%]
tests/test_recommender.py::test_recommend_k_larger_than_catalog_returns_all_songs PASSED [27%]
tests/test_recommender.py::test_recommend_worst_match_ranks_last PASSED               [36%]
tests/test_recommender.py::test_recommend_scores_are_actually_descending PASSED       [45%]
tests/test_recommender.py::test_recommend_empty_catalog_returns_empty_list PASSED     [54%]
tests/test_recommender.py::test_recommend_with_no_matching_genre_or_mood_still_returns_results PASSED [63%]
tests/test_recommender.py::test_likes_acoustic_boosts_high_acousticness_song PASSED[72%]
tests/test_recommender.py::test_explain_recommendation_returns_non_empty_string PASSED [81%]
tests/test_recommender.py::test_explain_recommendation_mentions_genre_match_when_applicable PASSED [90%]
tests/test_recommender.py::test_explain_recommendation_no_matches_still_returns_string PASSED [100%]

==================================== 11 passed in 0.30s ====================================



## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:
```


**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

--- # User profile: {"genre": "pop", "mood": "happy", "energy": 0.8}
# Recommendations:

Sunrise City - Score: 4.47
Because: genre match (+2.0), mood match (+1.0), energy closeness (+1.47)

Gym Hero - Score: 3.30
Because: genre match (+2.0), energy closeness (+1.30)

Rooftop Lights - Score: 2.44
Because: mood match (+1.0), energy closeness (+1.44)

Concrete Dreams - Score: 1.50
Because: energy closeness (+1.50)

Night Drive Loop - Score: 1.42
Because: energy closeness (+1.42)
```

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---Different types of users. I ran the recommender against three different taste profiles (High-Energy Pop, Chill Lofi, Deep Intense Rock). All three produced clean, sensible top results, but the gap between #1 and the rest looked different for each — Deep Intense Rock had a steep drop-off after Storm Runner since only one song is genre-rock, while Chill Lofi had several close contenders since lofi is better represented in the catalog. Lowering the weight actually changed the ranking, not just the numbers: Rooftop Lights (indie pop) jumped from #3 to #2, passing Gym Hero (exact genre "pop," but no mood match). At the old weight, an exact genre match beat a strong mood+energy match almost automatically; at the lower weight, mood and energy mattered more. This confirms the genre-dominance bias — the weight you pick directly decides whether "close genre" or "close vibe" wins. Adding tempo to the score. I added a tempo-closeness term (same formula style as energy) targeting 118 BPM: The top 3 stayed in the same order — tempo didn't flip any major rankings, just stretched the score gaps. It did cause a small swap: Night Drive Loop edged past Concrete Dreams into #4. This suggests tempo works well as a tie-breaker but wouldn't fix the bigger genre-dominance issue on its own.

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

--- Tiny catalog — only 18 songs, so most genres and moods are represented by just one or two tracks
No language or lyric understanding — the system only looks at genre, mood, and energy; it has no idea what a song is actually about
Genre-dominant scoring — genre is weighted highest, so it can over-favor exact genre matches even when a different-genre song is actually a strong mood/energy fit (confirmed in the experiments above)
No input validation — an out-of-range energy value can produce a negative, nonsensical score instead of an error
No memory or personalization over time — every recommendation is generated from a single static profile, with no learning from what a user actually likes or skips

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this

Building this project made it clear that a "recommendation" is really just a scoring
formula wearing a friendly face. The system doesn't understand music — it turns a handful of numbers and labels into points, adds them up, and sorts the results. Watching the same catalog produce completely different rankings just from changing one weight (genre from 2.0 to 0.5) showed how much of what feels like "the algorithm's opinion" is actually just a design decision someone made about what to count and how much.

Bias showed up in a few concrete ways once I actually tested it. The genre-weighted scoring meant close-but-not-exact matches (like indie pop vs. pop) got penalized as if they were completely unrelated, even when the rest of the profile matched well — a subtle unfairness toward songs that don't fit neatly into one label. The uneven catalog meant some users (whose taste matched well-covered genres) got richer, more differentiated recommendations than others almost by accident. And the out-of-range energy bug showed that unfairness doesn't even require bad intentions — a system can quietly misbehave just because nobody validated an input. That's the part that changed how I think about real recommenders the most: bias and unfairness aren't always dramatic or intentional, they're often just the unexamined side effects of small, reasonable-looking choices in the scoring logic.



