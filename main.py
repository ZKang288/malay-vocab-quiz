import streamlit as st
import random
import pandas as pd
import os

# --- Default Vocabulary Bank ---
vocab = {
    # meN- verbs
    "melihat": "see (verb)", "memasak": "cook", "menyanyi": "sing", "merasa": "feel", "mewarna": "to color (verb)",
    "meyakinkan": "convince", "membeli": "buy", "menfoto": "to photograph", "memvakum": "to vacuum",
    "memohon": "to apply", "mencuci": "to wash", "mendapat": "get", "menjawab": "answer",
    "menulis": "write", "menziarah": "to visit", "menyapu": "sweep", "menyepak": "kick",
    "mengecat": "to paint", "mengelap": "wipe", "mengambil": "take", "mengikal": "to tie",
    "menggosok": "rub", "mengira": "to count",

    # peN- nouns
    "pembaca": "reader", "pemfitnah": "slanderer", "pemotong": "cutter", "pencuri": "thief",
    "pendaki": "climber", "penari": "dancer", "pengguna": "user", "pengkaji": "researcher",
    "penganalisis": "analyst", "penyapu": "broom", "penyukat": "measurer", "pengecat": "painter",
    "pengelap": "wiper",

    # ter- words
    "terlupa": "forgot", "terlalu": "too", "tetap": "still", "tertidur": "fell asleep",
    "terbesar": "very big", "tertinggal": "left behind", "terkejut": "surprised",
    "tertua": "very old", "terlanggar": "hit accidentally", "tercapai": "achievable",
    "terindah": "most beautiful",

    # others
    "makanan": "food", "tulisan": "writing (noun)", "pakaian": "clothing", "tuliskan": "please write",
    "hantarkan": "send/deliver", "bukakan": "open for someone", "sayangi": "love/cherish",
    "dekati": "approach", "jauhi": "stay away from",

    # simpulan bahasa
    "anak emas": "favourite person", "buah tangan": "souvenir", "mulut murai": "talkative person",
    "kaki bangku": "bad at sports", "hidung tinggi": "arrogant", "berat tulang": "lazy",
    "otak udang": "slow-witted", "kaki ayam": "barefoot", "tangan panjang": "likes to steal",
    "telinga kuali": "stubborn", "ulat buku": "bookworm", "besar hati": "happy or proud",
    "buah hati": "beloved", "kaki botol": "alcoholic", "makan angin": "to go on a trip",
    "ringan tulang": "hardworking", "besar kepala": "arrogant", "cakar ayam": "messy handwriting",
    "pakwe": "boyfriend", "makwe": "girlfriend"
}

# --- Categorise words ---
meN_words = {k: v for k, v in vocab.items() if k.startswith("me")}
peN_words = {k: v for k, v in vocab.items() if k.startswith("pe")}
ter_words = {k: v for k, v in vocab.items() if k.startswith("ter")}
simpulan_words = {k: v for k, v in vocab.items() if " " in k and k not in meN_words and k not in peN_words and k not in ter_words}
other_words = {k: v for k, v in vocab.items() if k not in meN_words and k not in peN_words and k not in ter_words and k not in simpulan_words}

# --- Load / Initialize Log ---
LOG_FILE = "vocab_log.csv"

if os.path.exists(LOG_FILE):
    log_df = pd.read_csv(LOG_FILE)
else:
    log_df = pd.DataFrame({"word": list(vocab.keys()), "correct": 0, "wrong": 0})

# Ensure all vocab words are tracked
for w in vocab.keys():
    if w not in log_df["word"].values:
        log_df = pd.concat([log_df, pd.DataFrame([{"word": w, "correct": 0, "wrong": 0}])], ignore_index=True)

# --- Weighted Random Quiz Generator ---
def generate_quiz(n):
    # Ensure the log matches the current vocab set
    log_filtered = log_df[log_df["word"].isin(vocab.keys())].copy()

    # Assign weights based on wrong answers (default 1 if unseen)
    log_filtered["weight"] = log_filtered["wrong"] + 1
    weights = log_filtered["weight"] / log_filtered["weight"].sum()

    # Map the weights in order of vocab.keys()
    vocab_items = list(vocab.items())
    word_order = list(vocab.keys())
    weight_list = [weights.iloc[word_order.index(w)] if w in word_order else 1 for w, _ in vocab_items]

    # Now both vocab and weights have same length
    selected_words = random.choices(vocab_items, weights=weight_list, k=n)

    # Prevent duplicates if possible
    unique_selected = list(dict(selected_words).items())
    return unique_selected[:n]

# --- Streamlit UI ---
st.title("🗣️ Malay Vocabulary Quiz")
st.write("Test your Malay ↔ English vocabulary")

mode = st.sidebar.selectbox("Test direction:", ["English → Malay", "Malay → English"])
num_questions = st.sidebar.slider("Number of words to test:", 3, 50, 20)  # default 20

# --- Initialize Quiz ---
if "quiz_words" not in st.session_state:
    st.session_state.quiz_words = generate_quiz(num_questions)
if "answers" not in st.session_state:
    st.session_state.answers = {}  # stores current text inputs

score = 0
wrong_list = []

st.header("📝 Quiz Section")

for i, (malay, english) in enumerate(st.session_state.quiz_words):
    key = f"q{i}"
    default_value = st.session_state.answers.get(key, "")
    
    if mode == "Malay → English":
        user_answer = st.text_input(f"{i+1}. What is the English meaning of **{malay}**?", value=default_value, key=key)
        st.session_state.answers[key] = user_answer
        if user_answer:
            if user_answer.strip().lower() == english.lower():
                st.success("✅ Correct!")
                log_df.loc[log_df["word"] == malay, "correct"] += 1
                score += 1
            else:
                st.error(f"❌ Wrong. Correct answer: **{english}**")
                log_df.loc[log_df["word"] == malay, "wrong"] += 1
                wrong_list.append(malay)

    else:  # English → Malay
        user_answer = st.text_input(f"{i+1}. What is the Malay word for **{english}**?", value=default_value, key=key)
        st.session_state.answers[key] = user_answer
        if user_answer:
            if user_answer.strip().lower() == malay.lower():
                st.success("✅ Correct!")
                log_df.loc[log_df["word"] == malay, "correct"] += 1
                score += 1
            else:
                st.error(f"❌ Wrong. Correct answer: **{malay}**")
                log_df.loc[log_df["word"] == malay, "wrong"] += 1
                wrong_list.append(malay)

# --- Save Progress ---
log_df.to_csv(LOG_FILE, index=False)

# --- Summary ---
st.write("---")
st.subheader(f"✅ Score: {score}/{num_questions}")
if wrong_list:
    st.write("Words to review:")
    st.write(", ".join(wrong_list))

# --- Restart Quiz Button ---
if st.button("🔁 New Quiz"):
    st.session_state.quiz_words = generate_quiz(num_questions)
    st.session_state.answers = {}  # clear all previous answers
    st.experimental_rerun()

