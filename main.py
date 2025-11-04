import streamlit as st
import random
import pandas as pd
import os
import numpy as np

# --- Default Vocabulary Bank ---
vocab = {
    # meN- verbs
    "melihat": "see (verb)", "memasak": "cook", "menyanyi": "sing", "merasa": "feel", "mewarna": "to color (verb)",
    "memvakum": "to vacuum", "meyakinkan": "convince", "membeli": "buy", "memfoto": "to photograph", 
    "menjawab": "answer", "memohon": "to apply", "mencuci": "to wash", "mendapat": "get", 
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
    "pakwe": "boyfriend", "makwe": "girlfriend",

    # penanda wacana
    "mula-mula": "at first", "pertama": "firstly",
    "selain itu": "besides that", "tambahan pula": "moreover",
    "kemudian": "then", "selepas itu": "after that",
    "walau bagaimanapun": "however",
    "oleh itu": "therefore",
    "contohnya": "for example", "misalnya": "for example",
    "akhirnya": "finally", "akhir sekali": "lastly", "kesimpulannya": "in conclusion"
}

# --- Categorise words ---
meN_words = {k: v for k, v in vocab.items() if k.startswith("me")}
peN_words = {k: v for k, v in vocab.items() if k.startswith("pe")}
ter_words = {k: v for k, v in vocab.items() if k.startswith("ter")}
simpulan_words = {k: v for k, v in vocab.items() if " " in k and k not in meN_words and k not in peN_words and k not in ter_words}
penanda_words = {k: v for k, v in vocab.items() if k in [
    "mula-mula", "pertama", "selain itu", "tambahan pula", "kemudian", "selepas itu",
    "walau bagaimanapun", "oleh itu", "contohnya", "misalnya", "akhirnya", "akhir sekali", "kesimpulannya"
]}
other_words = {k: v for k, v in vocab.items()
               if k not in meN_words and k not in peN_words and k not in ter_words
               and k not in simpulan_words and k not in penanda_words}

categories = {
    "meN- verbs": meN_words,
    "peN- nouns": peN_words,
    "ter- words": ter_words,
    "simpulan bahasa": simpulan_words,
    "others": other_words,
    "penanda wacana": penanda_words
}

# --- Progress Log ---
LOG_FILE = "vocab_log.csv"
if os.path.exists(LOG_FILE):
    log_df = pd.read_csv(LOG_FILE)
else:
    log_df = pd.DataFrame({"word": list(vocab.keys()), "correct": 0, "wrong": 0})

for w in vocab.keys():
    if w not in log_df["word"].values:
        log_df = pd.concat([log_df, pd.DataFrame([{"word": w, "correct": 0, "wrong": 0}])], ignore_index=True)

# --- Helper: Weighted Sampling from One Category ---
def weighted_sample(cat_dict, n):
    log_filtered = log_df[log_df["word"].isin(cat_dict.keys())].copy()
    if log_filtered.empty:
        return []
    log_filtered["weight"] = log_filtered["wrong"] + 1
    weight_dict = dict(zip(log_filtered["word"], log_filtered["weight"]))
    vocab_items = list(cat_dict.items())
    weights = np.array([weight_dict.get(w, 1) for w, _ in vocab_items], dtype=float)
    weights /= weights.sum()
    n = min(n, len(vocab_items))
    indices = np.random.choice(len(vocab_items), size=n, replace=False, p=weights)
    return [vocab_items[i] for i in indices]

# --- Fixed Proportion Generator ---
def generate_quiz(n, selected_cats):
    # Fixed proportions
    simpulan_ratio = 0.1
    penanda_ratio = 0.1
    remaining_ratio = 1 - (simpulan_ratio + penanda_ratio)
    
    simpulan_n = int(n * simpulan_ratio)
    penanda_n = int(n * penanda_ratio)
    remaining_n = n - simpulan_n - penanda_n
    
    selected_vocab = {cat: categories[cat] for cat in selected_cats}
    other_cats = [c for c in selected_cats if c not in ["simpulan bahasa", "penanda wacana"]]
    
    quiz = []
    if "simpulan bahasa" in selected_cats:
        quiz += weighted_sample(simpulan_words, simpulan_n)
    if "penanda wacana" in selected_cats:
        quiz += weighted_sample(penanda_words, penanda_n)
    
    if other_cats and remaining_n > 0:
        per_cat = max(1, remaining_n // len(other_cats))
        for cat in other_cats:
            quiz += weighted_sample(categories[cat], per_cat)
    
    random.shuffle(quiz)
    return quiz[:n]

# --- Streamlit App ---
st.title("🗣️ Malay Vocabulary Tester")
st.sidebar.header("Settings")

mode = st.sidebar.selectbox("Test direction:", ["English → Malay", "Malay → English"])
num_questions = st.sidebar.slider("Number of words:", 3, 50, 20)
selected_cats = st.sidebar.multiselect("Categories to include:", list(categories.keys()), default=list(categories.keys()))

# --- Generate or Refresh Quiz ---
if "quiz_words" not in st.session_state:
    st.session_state.quiz_words = generate_quiz(num_questions, selected_cats)
    st.session_state.answers = [""] * num_questions
    st.session_state.num_questions = num_questions
    st.session_state.last_cats = selected_cats

if num_questions != st.session_state.num_questions or st.session_state.last_cats != selected_cats:
    st.session_state.quiz_words = generate_quiz(num_questions, selected_cats)
    st.session_state.answers = [""] * num_questions
    st.session_state.num_questions = num_questions
    st.session_state.last_cats = selected_cats

score = 0
wrong_list = []

st.header("📝 Quiz")

for i, (malay, english) in enumerate(st.session_state.quiz_words):
    key = f"q{i}"
    if mode == "Malay → English":
        user_answer = st.text_input(f"{i+1}. Meaning of **{malay}**:", value=st.session_state.answers[i], key=key)
        if user_answer:
            st.session_state.answers[i] = user_answer
            if user_answer.strip().lower() == english.lower():
                st.success("✅ Correct!")
                log_df.loc[log_df["word"] == malay, "correct"] += 1
                score += 1
            else:
                st.error(f"❌ Correct: **{english}**")
                log_df.loc[log_df["word"] == malay, "wrong"] += 1
                wrong_list.append(malay)
    else:
        user_answer = st.text_input(f"{i+1}. Malay for **{english}**:", value=st.session_state.answers[i], key=key)
        if user_answer:
            st.session_state.answers[i] = user_answer
            if user_answer.strip().lower() == malay.lower():
                st.success("✅ Correct!")
                log_df.loc[log_df["word"] == malay, "correct"] += 1
                score += 1
            else:
                st.error(f"❌ Correct: **{malay}**")
                log_df.loc[log_df["word"] == malay, "wrong"] += 1
                wrong_list.append(malay)

# Save log
log_df.to_csv(LOG_FILE, index=False)

st.write("---")
st.subheader(f"✅ Score: {score}/{num_questions}")
if wrong_list:
    st.write("Words to review:")
    st.write(", ".join(wrong_list))

if st.button("🔁 New Quiz"):
    st.session_state.quiz_words = generate_quiz(num_questions, selected_cats)
    st.session_state.answers = [""] * num_questions
    st.rerun()









