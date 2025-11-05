import streamlit as st
import pandas as pd
import numpy as np
import random
import os

# ------------------------------
# 🔹 CSV log setup
# ------------------------------
LOG_FILE = "vocab_log.csv"

if os.path.exists(LOG_FILE):
    log_df = pd.read_csv(LOG_FILE)
else:
    log_df = pd.DataFrame(columns=["word", "correct", "wrong"])
    log_df.to_csv(LOG_FILE, index=False)


# ------------------------------
# 🔹 Define categories
# ------------------------------
simpulan_bahasa = {
    "buah fikiran": "idea",
    "kaki bangku": "bad at sports",
    "hidung tinggi": "arrogant",
    "tangan kosong": "empty-handed",
    "mulut manis": "flattering",
    "naik darah": "angry",
    "telinga nipis": "sensitive to criticism",
    "makan angin": "go on holiday",
    "besar hati": "grateful / proud",
    "ambil hati": "to please someone",
    "berat mulut": "not talkative",
}

penanda_wacana = {
    "mula-mula": "at first",
    "pertama": "firstly",
    "selain itu": "besides that",
    "tambahan pula": "moreover",
    "kemudian": "then",
    "selepas itu": "after that",
    "walau bagaimanapun": "however",
    "oleh itu": "therefore",
    "contohnya": "for example",
    "misalnya": "for example",
    "akhirnya": "finally",
    "akhir sekali": "lastly",
    "kesimpulannya": "in conclusion",
}

men_kan_verbs = {
    "membesarkan": "enlarge",
    "mengajarkan": "teach",
    "mengingatkan": "remind",
    "menjalankan": "carry out",
    "melarikan": "run away",
    "memainkan": "play something",
    "mengerjakan": "work on",
    "mendirikan": "establish/build",
    "menggerakkan": "move something",
    "menghentikan": "stop something",
    "mencantikkan": "beautify",
    "membaikan": "to improve",
    "mendekatkan": "bring closer",
    "memasukan": "insert",
    "mendudukan": "place",
    "menaikkan": "increase",
    "membelikan": "buy for someone",
    "menyeronkkan": "enjoy/have fun",
}

men_i_verbs = {
    "menaiki": "to get on board",
    "menikmati": "to enjoy",
    "menyayangi": "to love",
    "mendekati": "to approach something",
    "membaiki": "repair",
    "mengingati": "remember",
    "menjalani": "undergo",
    "memasuki": "enter",
    "menduduki": "occupy",
}

pen_an_nouns = {
    "pemakanan": "diet",
    "pembacaan": "reading",
    "pengunaan": "usage",
    "pemandangan": "view/scenery",
    "pengelaman": "experience",
    "penuliskan": "writing",
    "perjalanan": "journey",
    "pekerjaan": "occupation",
    "persoalan": "question",
    "pembuatan": "production",
    "pemakaian": "to wear clothes",
    "kepanasan": "feeling hot",
    "kebaikan": "goodness",
    "kesakitan": "pain",
}

categories = {
    "simpulan bahasa": simpulan_bahasa,
    "penanda wacana": penanda_wacana,
    "meN-kan verbs": men_kan_verbs,
    "men-i verbs": men_i_verbs,
    "peN-an / ke-an nouns": pen_an_nouns,
}


# ------------------------------
# 🔹 Weighted sampling helper
# ------------------------------
def weighted_sample(word_dict, n):
    """Select up to n items from a category, weighted by wrong answers."""
    log_filtered = log_df[log_df["word"].isin(word_dict.keys())].copy()
    log_filtered["weight"] = log_filtered["wrong"] + 1
    weight_dict = dict(zip(log_filtered["word"], log_filtered["weight"]))

    vocab_items = list(word_dict.items())
    weights = np.array([weight_dict.get(w, 1) for w, _ in vocab_items], dtype=float)
    weights /= weights.sum()

    n = min(n, len(vocab_items))
    indices = np.random.choice(len(vocab_items), size=n, replace=False, p=weights)
    return [vocab_items[i] for i in indices]


# ------------------------------
# 🔹 Generate quiz logic
# ------------------------------
def generate_quiz(n, selected_cats):
    """Generate quiz with n questions distributed equally among selected categories."""
    selected_cats = [c for c in selected_cats if c in categories]
    if not selected_cats:
        return []

    # Single category → take all from that
    if len(selected_cats) == 1:
        return weighted_sample(categories[selected_cats[0]], n)

    # Multi-category → equal distribution
    per_cat = max(1, n // len(selected_cats))
    quiz = []

    for cat in selected_cats:
        cat_dict = categories[cat]
        quiz.extend(weighted_sample(cat_dict, per_cat))

    # Fill remainder if not enough
    if len(quiz) < n:
        remaining = n - len(quiz)
        pool = []
        for cat in selected_cats:
            pool.extend(list(categories[cat].items()))
        extra = random.sample(pool, min(remaining, len(pool)))
        quiz.extend(extra)

    random.shuffle(quiz)
    return quiz[:n]


# ------------------------------
# 🔹 Streamlit UI
# ------------------------------
st.title("🗣️ Malay Vocabulary Quiz")

st.sidebar.header("Quiz Settings")
selected_cats = st.sidebar.multiselect("Select categories", list(categories.keys()), default=["simpulan bahasa"])
num_questions = st.sidebar.slider("Number of questions", 5, 30, 20)

if "quiz_words" not in st.session_state or st.sidebar.button("Restart Quiz"):
    st.session_state.quiz_words = generate_quiz(num_questions, selected_cats)
    st.session_state.user_answers = [""] * len(st.session_state.quiz_words)
    st.session_state.show_results = False

quiz_words = st.session_state.quiz_words

# ------------------------------
# 🔹 Quiz display
# ------------------------------
st.write("### Translate the following Malay words:")

for i, (malay, english) in enumerate(quiz_words):
    st.session_state.user_answers[i] = st.text_input(f"{i+1}. {malay}", st.session_state.user_answers[i])

if st.button("Submit Answers"):
    correct = 0
    for (malay, english), ans in zip(quiz_words, st.session_state.user_answers):
        ans_clean = ans.strip().lower()
        correct_ans = english.lower()

        if ans_clean == correct_ans:
            correct += 1
            if malay in log_df["word"].values:
                log_df.loc[log_df["word"] == malay, "correct"] += 1
            else:
                log_df.loc[len(log_df)] = [malay, 1, 0]
        else:
            if malay in log_df["word"].values:
                log_df.loc[log_df["word"] == malay, "wrong"] += 1
            else:
                log_df.loc[len(log_df)] = [malay, 0, 1]

    log_df.to_csv(LOG_FILE, index=False)
    st.session_state.show_results = True
    st.session_state.score = f"{correct}/{len(quiz_words)}"

# ------------------------------
# 🔹 Show results
# ------------------------------
if st.session_state.get("show_results", False):
    st.success(f"Your score: {st.session_state.score}")
    with st.expander("Show correct answers"):
        for (malay, english), ans in zip(quiz_words, st.session_state.user_answers):
            st.write(f"**{malay}** — your answer: *{ans}* → correct: **{english}**")
