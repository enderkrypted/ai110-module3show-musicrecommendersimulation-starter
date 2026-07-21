# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Explain your design in plain language.

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
- What information does your `UserProfile` store
- How does your `Recommender` compute a score for each song
- How do you choose which songs to recommend

You can include a simple diagram or bullet list if helpful.

Real-world recommenders like Spotify or YouTube usually work one of two ways: by looking at what similar users liked (collaborative filtering), or by looking at the actual attributes of the songs themselves (content-based filtering). This project is a simple content-based system — there's only one user, so it works by comparing song attributes to that user's stated preferences, rather than comparing users to each other. Each Song has four features: genre, mood, energy (0–1), and valence (0–1, how positive or negative the song feels). The UserProfile stores the same four features as preferences: preferred_genre, preferred_mood, preferred_energy, and preferred_valence.
The Recommender scores each song by comparing it to the user's profile. Genre and mood either match or they don't, and a match adds points (genre counts for more, since it's usually the strongest signal for "vibe"). Energy and valence are scored differently — instead of rewarding high values, the system rewards songs whose energy and valence are close to what the user prefers. All songs are scored this way, sorted from highest to lowest, and the top few are returned as recommendations.

---

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

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:
```

# User profile: {"genre": "pop", "mood": "happy", "energy": 0.8}
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

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



