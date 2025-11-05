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
    "anak emas": "favourite person", 
    "buah tangan": "souvenir", 
    "mulut murai": "talkative person", 
    "kaki bangku": "bad at sports", 
    "hidung tinggi": "arrogant", 
    "berat tulang": "lazy", 
    "otak udang": "slow-witted", 
    "kaki ayam": "barefoot", 
    "tangan panjang": "likes to steal", 
    "telinga kuali": "stubborn", 
    "ulat buku": "bookworm", 
    "besar hati": "happy or proud", 
    "buah hati": "beloved", 
    "kaki botol": "alcoholic", 
    "makan angin": "to go on a trip", 
    "ringan tulang": "hardworking", 
    "besar kepala": "arrogant", 
    "cakar ayam": "messy handwriting", 
    "pakwe": "boyfriend", 
    "makwe": "girlfriend"
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

meN_verbs = {
    "melihat": "see", "memasak": "cook", "menyanyi": "sing", "merasa": "feel",
    "mewarna": "color", "meyakinkan": "convince", "membeli": "buy", "menfoto": "photograph",
    "memvakum": "vacuum", "memohon": "apply", "mencuci": "wash", "mendapat": "get",
    "menjawab": "answer", "menulis": "write", "menziarah": "visit", "menyapu": "sweep",
    "menyepak": "kick", "mengecat": "paint", "mengelap": "wipe", "mengambil": "take",
    "mengikal": "tie", "menggosok": "rub", "mengira": "to count"
}

meN_kan_verbs = {
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
    "membaikkan": "to improve",
    "mendekatkan": "bring closer",
    "memasukkan": "insert",
    "mendudukan": "place",
    "menaikkan": "increase",
    "membelikan": "buy for someone",
    "menyeronokkan": "enjoy/have fun",
}

meN_i_verbs = {
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

peN_nouns = {
    "pembaca": "reader", "pemfitnah": "slanderer", "pemotong": "cutter", "pencuri": "thief", "penghantar": "delivery man",
    "pendaki": "climber", "penari": "dancer", "pengguna": "user", "pengkaji": "researcher",
    "penganalisis": "analyst", "penyapu": "broom", "penyukat": "measurer", "pengecat": "painter", "pengelap": "wiper", "pelukis": "artist"
}

peN_an_nouns = {
    "pemakanan": "diet",
    "pembacaan": "reading",
    "penggunaan": "usage",
    "pemandangan": "view/scenery",
    "pengalaman": "experience",
    "penulisan": "writing",
    "perjalanan": "journey",
    "pekerjaan": "occupation",
    "persoalan": "question",
    "pembuatan": "production",
    "pemakaian": "to wear clothes",
    "kepanasan": "feeling hot",
    "kebaikan": "goodness",
    "kesakitan": "pain",
}

ter_words = {
    "terlupa": "forgot", "terlalu": "too", "tetap": "still", "tertidur": "fell asleep",
    "terbesar": "very big", "tertinggal": "left behind", "terkejut": "surprised",
    "tertua": "very old", "terlanggar": "hit accidentally", "tercapai": "achievable", "terindah": "most beautiful"
}

others = {
    "makanan": "food", "tulisan": "writing", "pakaian": "clothing", "tuliskan": "please write",
    "hantarkan": "send/deliver", "bukakan": "open for someone", "sayangi": "love/cherish",
    "dekati": "approach", "jauhi": "stay away from"
}

categories = {
    "Simpulan Bahasa": simpulan_bahasa,
    "Penanda Wacana": penanda_wacana,
    "meN- verbs": meN_verbs,
    "meN-kan verbs": meN_kan_verbs,
    "meN-i verbs": meN_i_verbs,
    "peN- nouns": peN_nouns,
    "peN-an/ke-an nouns": peN_an_nouns,
    "ter- words": ter_words,
    "Others": others
}

# ---------------------
# STREAMLIT UI
# ---------------------
st.title("🗣️ Malay Vocabulary Quiz")
st.write("Test your Malay vocabulary knowledge")

# Quiz configuration in sidebar
st.sidebar.header("Quiz Settings")

# Test direction selection
test_direction = st.sidebar.selectbox(
    "Test direction:",
    ["English → Malay", "Malay → English"]
)

# Select categories
selected_categories = st.sidebar.multiselect(
    "Select categories to be tested:", 
    list(categories.keys()), 
    default=list(categories.keys())
)

# Number of questions
num_questions = st.sidebar.slider("Number of questions:", 10, 200, 20)

# ---------------------
# GENERATE QUIZ FUNCTION
# ---------------------
def generate_quiz(num_questions):
    selected_dicts = [categories[c] for c in selected_categories if c in categories]
    if not selected_dicts:
        return []

    # Even distribution
    per_cat = num_questions // len(selected_dicts)
    remainder = num_questions % len(selected_dicts)
    quiz_items = []

    for i, cat_dict in enumerate(selected_dicts):
        n = per_cat + (1 if i < remainder else 0)
        items = list(cat_dict.items())
        if len(items) <= n:
            quiz_items.extend(items)
        else:
            quiz_items.extend(random.sample(items, n))
    random.shuffle(quiz_items)
    return quiz_items[:num_questions]

# ---------------------
# SESSION STATE
# ---------------------
if "quiz_words" not in st.session_state:
    st.session_state.quiz_words = generate_quiz(num_questions)
if "answers" not in st.session_state:
    st.session_state.answers = [""] * len(st.session_state.quiz_words)
if "test_direction" not in st.session_state:
    st.session_state.test_direction = test_direction

# Restart Quiz if direction changes or manually
if (test_direction != st.session_state.test_direction or 
    st.sidebar.button("🔁 Restart Quiz")):
    st.session_state.quiz_words = generate_quiz(num_questions)
    st.session_state.answers = [""] * len(st.session_state.quiz_words)
    st.session_state.test_direction = test_direction
    st.rerun()

# ---------------------
# QUIZ DISPLAY
# ---------------------
st.header("📝 Quiz Section")
score = 0
wrong_answers = []

for i, (malay, english) in enumerate(st.session_state.quiz_words):
    if test_direction == "Malay → English":
        # Malay to English direction
        user_answer = st.text_input(
            f"{i+1}. What is the English meaning of **{malay}**?", 
            value=st.session_state.answers[i],
            key=f"q_{i}"
        )
        st.session_state.answers[i] = user_answer
        
        # Check answer if user has provided one
        if user_answer.strip():
            if user_answer.strip().lower() == english.lower():
                st.success("✅ Correct!")
                score += 1
            else:
                st.error(f"❌ Wrong! The correct answer is: **{english}**")
                wrong_answers.append((malay, english, user_answer, "Malay → English"))
    
    else:  # English → Malay direction
        user_answer = st.text_input(
            f"{i+1}. What is the Malay word for **{english}**?", 
            value=st.session_state.answers[i],
            key=f"q_{i}"
        )
        st.session_state.answers[i] = user_answer
        
        # Check answer if user has provided one
        if user_answer.strip():
            if user_answer.strip().lower() == malay.lower():
                st.success("✅ Correct!")
                score += 1
            else:
                st.error(f"❌ Wrong! The correct answer is: **{malay}**")
                wrong_answers.append((malay, english, user_answer, "English → Malay"))

# ---------------------
# RESULTS
# ---------------------
st.write("---")
st.subheader("📊 Results")

if st.button("✅ Submit Quiz"):
    st.success(f"You scored **{score}** out of **{len(st.session_state.quiz_words)}**!")
    
    if wrong_answers:
        st.subheader("📝 Words to review:")
        for malay, english, user_ans, direction in wrong_answers:
            if direction == "Malay → English":
                st.write(f"- **{malay}**: Your answer: '{user_ans}' | Correct: **{english}**")
            else:
                st.write(f"- **{english}**: Your answer: '{user_ans}' | Correct: **{malay}**")

# ---------------------
# PROGRESS TRACKING
# ---------------------
st.sidebar.header("Progress Tracking")
st.sidebar.write(f"Total words in database: {sum(len(cat) for cat in categories.values())}")
st.sidebar.write(f"Selected categories: {len(selected_categories)}")
st.sidebar.write(f"Questions in current quiz: {len(st.session_state.quiz_words)}")
st.sidebar.write(f"Test direction: {test_direction}")




