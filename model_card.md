# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

--- TuneQuest

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

--- This recommender generates song recommendations for a single user based on a simple taste profile — a favorite genre, favorite mood, and target energy level (with an optional preference for acoustic songs). Given that profile, it scores every song in a small 18-song catalog and returns the top matches, each with a plain-language explanation of why it was picked (e.g. "genre match, energy closeness").

It assumes the user can articulate their taste as a few discrete preferences — one genre, one mood, one energy level — rather than a broader, evolving, or multi-faceted set of tastes. It also assumes the user's stated preferences are internally consistent (e.g. it doesn't detect or warn about contradictory input like wanting both "sad" mood and very high energy). It has no concept of a returning user, listening history, or feedback over time — every recommendation is generated fresh from the profile provided.

This is a classroom exploration project, not a system built for real users. It's meant to demonstrate, at a small and inspectable scale, how content-based recommendation works: turning song attributes and stated preferences into a numeric score and a ranked list. It intentionally trades away the complexity of real systems (large catalogs, collaborative filtering, learned weights, user history) for something simple enough to fully explain and reason about.

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

--- Every song in the catalog has a few basic traits: its genre, its mood, and how much energy it has (on a scale from calm to intense). The user tells the system what they're in the mood for — a favorite genre, a favorite mood, and a target energy level.

To figure out what to recommend, the system compares each song to what the user asked for. If the song's genre matches, it earns points. If the mood matches, it earns a few more points. For energy, instead of just checking for an exact match, the system checks how close the song's energy is to what the user wants — a song that's almost right still earns most of the points, while a song that's way off earns very little. Genre counts for the most, mood a bit less, and energy is scored on a sliding scale rather than a strict yes/no.

Once every song has a score, the system just sorts them from highest to lowest and hands back the top few. Each recommendation also comes with a short explanation, like "genre match, energy close to what you wanted," so it's not just a mystery ranking — you can see exactly why each song made the list.

The starter version of this project didn't have any of this scoring logic filled in yet — it just returned whatever songs happened to be first in the list, with no real reasoning. What we built adds the actual comparison rules, the point system, the sliding-scale energy scoring, and the plain-language explanations.

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

--- The catalog contains 18 songs in total. It started as a 10-song starter file and was expanded by adding 8 more songs to cover genres and moods that weren't represented yet.

Genres represented: pop, indie pop, lofi, rock, ambient, jazz, synthwave, hip hop, classical, country, folk, EDM, R&B, metal, and reggae.

Moods represented: happy, chill, intense, relaxed, moody, focused, energetic, nostalgic, romantic, sad, triumphant, angry, and dreamy.

Each song also has numeric attributes: energy, tempo (BPM), valence (how positive or negative it feels), danceability, and acousticness. The scoring system currently only uses genre, mood, and energy, so valence, danceability, tempo, and acousticness are present in the data but mostly unused (acousticness is used only as a small bonus when a user says they like acoustic songs).

There's a lot of musical taste this dataset can't capture. It has no lyrics or language data, no artist popularity or era information beyond a single artist name, and only one genre/mood label per song, even though real songs often blend styles or shift mood partway through. With only 18 songs and one example per genre in most cases, the catalog can't represent the range of variation that exists within any single genre in real life — every "lofi" song here has to stand in for the entire genre.

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

--- Features it does not consider: The system ignores valence, danceability, tempo, and (mostly) acousticness. Two songs with the same genre, mood, and energy score identically even if their overall "feel" differs. It also has no memory — no listening history, no learning from skips or likes over time.

Underrepresented genres and moods: With only 18 songs, most genres and moods appear once or twice. Users who like well-covered genres (pop, lofi) get more differentiated recommendations than users who like something like reggae or classical, where there's only one matching song.

Overfitting to one preference: Genre is weighted highest (+2.0), so it can dominate the score even when mood and energy match better elsewhere. A close-but-not-exact genre (like "indie pop" vs. "pop") gets zero genre credit, unfairly punishing songs that are actually a strong stylistic match.

Unintentional favoritism in scoring: Testing with an out-of-range energy value (1.5, outside the valid 0–1 scale) produced negative score contributions, since the formula doesn't validate or clamp input. A user who submits an unusual value gets silently penalized in an unpredictable way rather than getting an error.

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  


No need for numeric metrics unless you created some.
```

---I tested 8 user profiles in total: three typical taste profiles (High-Energy Pop, Chill Lofi, Deep Intense Rock) to confirm the system behaves sensibly for normal users, and five adversarial edge cases designed to try to break the scoring logic (conflicting mood and energy, a genre that doesn't exist in the catalog, empty preferences, an energy value outside the valid 0-1 range, and an extreme "opposite of everything" profile). For each one I checked whether the ranking made intuitive sense and whether the explanation matched the score. The most surprising result was the out-of-range energy profile, which produced a negative "energy closeness" contribution instead of an error, revealing that the scoring formula doesn't validate its inputs.

=== High-Energy Pop ({'genre': 'pop', 'mood': 'happy', 'energy': 0.8}) ===
Top recommendations:
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

=== Chill Lofi ({'genre': 'lofi', 'mood': 'chill', 'energy': 0.35}) ===
Top recommendations:
Library Rain - Score: 4.50
Because: genre match (+2.0), mood match (+1.0), energy closeness (+1.50)
Midnight Coding - Score: 4.39
Because: genre match (+2.0), mood match (+1.0), energy closeness (+1.40)
Focus Flow - Score: 3.42
Because: genre match (+2.0), energy closeness (+1.42)
Spacewalk Thoughts - Score: 2.40
Because: mood match (+1.0), energy closeness (+1.40)
Coffee Shop Stories - Score: 1.47
Because: energy closeness (+1.47)

=== Deep Intense Rock ({'genre': 'rock', 'mood': 'intense', 'energy': 0.9}) ===
Top recommendations:
Storm Runner - Score: 4.48
Because: genre match (+2.0), mood match (+1.0), energy closeness (+1.48)
Gym Hero - Score: 2.46
Because: mood match (+1.0), energy closeness (+1.46)
Pulse Overdrive - Score: 1.41
Because: energy closeness (+1.41)
Iron Verdict - Score: 1.40
Because: energy closeness (+1.40)
Sunrise City - Score: 1.38
Because: energy closeness (+1.38)

=== Conflicting Energy+Mood ({'genre': 'rock', 'mood': 'sad', 'energy': 0.9}) ===
Top recommendations:
Storm Runner - Score: 3.48
Because: genre match (+2.0), energy closeness (+1.48)
Fading Photograph - Score: 1.60
Because: mood match (+1.0), energy closeness (+0.60)
Gym Hero - Score: 1.46
Because: energy closeness (+1.46)
Pulse Overdrive - Score: 1.41
Because: energy closeness (+1.41)
Iron Verdict - Score: 1.40
Because: energy closeness (+1.40)

=== Nonexistent Genre ({'genre': 'k-pop', 'mood': 'happy', 'energy': 0.7}) ===
Top recommendations:
Rooftop Lights - Score: 2.41
Because: mood match (+1.0), energy closeness (+1.41)
Sunrise City - Score: 2.32
Because: mood match (+1.0), energy closeness (+1.32)
Night Drive Loop - Score: 1.42
Because: energy closeness (+1.42)
Concrete Dreams - Score: 1.35
Because: energy closeness (+1.35)
Backroad Sunset - Score: 1.28
Because: energy closeness (+1.28)

=== Empty Preferences ({}) ===
Top recommendations:
Sunrise City - Score: 0.00
Because: no strong matches
Midnight Coding - Score: 0.00
Because: no strong matches
Storm Runner - Score: 0.00
Because: no strong matches
Library Rain - Score: 0.00
Because: no strong matches
Gym Hero - Score: 0.00
Because: no strong matches

=== Out-of-Range Energy ({'genre': 'ambient', 'mood': 'chill', 'energy': 1.5}) ===
Top recommendations:
Spacewalk Thoughts - Score: 2.67
Because: genre match (+2.0), mood match (+1.0), energy closeness (+-0.33)
Midnight Coding - Score: 0.88
Because: mood match (+1.0), energy closeness (+-0.12)
Library Rain - Score: 0.78
Because: mood match (+1.0), energy closeness (+-0.22)
Iron Verdict - Score: 0.70
Because: energy closeness (+0.70)
Pulse Overdrive - Score: 0.69
Because: energy closeness (+0.69)

=== Opposite Extreme ({'genre': 'opera', 'mood': 'furious', 'energy': 0.0}) ===
Top recommendations:
Autumn Piano - Score: 1.12
Because: energy closeness (+1.12)
Spacewalk Thoughts - Score: 1.08
Because: energy closeness (+1.08)
Fading Photograph - Score: 1.05
Because: energy closeness (+1.05)
Library Rain - Score: 0.98
Because: energy closeness (+0.98)
Coffee Shop Stories - Score: 0.95
Because: energy closeness (+0.95)
```

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

--- Additional features or preferences: Bring valence, danceability, and tempo into the actual scoring formula instead of leaving them unused in the data. Also let users express more nuanced preferences, like a range of acceptable energy rather than one exact target, or a secondary "backup" genre.

Better ways to explain recommendations: Right now explanations just list which rules fired ("genre match, energy closeness"). A better version could rank the reasons by how much they contributed to the score, or phrase them more naturally, like "this is a strong match because it's the same genre and has almost identical energy to what you wanted."

Improving diversity among the top results: The current system can return several very similar songs in the top 5 if they all score well on the same features (as seen with the Chill Lofi results, which were dominated by lofi tracks). A future version could cap how many songs from the same genre or artist appear in one recommendation list, to surface a wider variety.

Handling more complex user tastes: Real listeners like more than one genre or mood depending on context (working out vs. relaxing). The model could support multiple taste profiles per user, or accept a small set of "example songs I like" instead of forcing preferences into single fixed categories.

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  

Building this project made the gap between "recommendation" and "mind reading" a lot clearer to me. A recommender doesn't actually know what a listener wants — it just turns a handful of numbers and labels into a score, and the quality of the result depends entirely on which features you chose to weight and how. Watching a rock/intense/high-energy profile confidently rank a song near the top just because its energy happened to be close, even with zero genre or mood match, was a good reminder that "the algorithm recommended it" doesn't mean the system actually understood the request.

The most interesting discovery was the negative-score bug from the out-of-range energy test. I didn't expect a single bad input to quietly produce a nonsensical score instead of an obvious error — it made me realize how much of what looks like "the algorithm's judgment" in real systems is really just unvalidated math doing exactly what it was told, even when the input doesn't make sense.

This changed how I think about apps like Spotify or YouTube. Their recommendations feel personal and almost intuitive, but underneath they're running the same basic idea I built here, just at a much larger scale with far more signals. Knowing how easily a simple scoring rule can be skewed by weighting choices, missing validation, or a small unbalanced catalog makes me a lot more skeptical of treating any recommendation as neutral or purely "smart" — it's really just a reflection of the decisions someone made about what to measure and how much to count it.