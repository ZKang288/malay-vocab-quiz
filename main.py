import streamlit as st
import random

# --- Default Vocabulary Bank ---
vocab = {
    "melihat": "see",
    "memasak": "cook",
    "menyanyi": "sing",
    "merasa": "feel",
    "mewarna": "color",
    "meyakinkan": "convince",
    "membeli": "buy",
    "menfoto": "photograph",
    "memvakum": "vacuum",
    "memohon": "apply",
    "mencuci": "wash",
    "mendapat": "get",
    "menjawab": "answer",
    "menulis": "write",
    "menziarah": "visit",
    "menyapu": "sweep",
    "menyepak": "kick",
    "mengecat": "paint",
    "mengelap": "wipe",
    "mengambil": "take",
    "mengikal": "tie",
    "menggosok": "rub",
    "mengira": "to count",
    "pembaca": "reader",
    "pemfitnah": "slanderer",
    "pemotong": "cutter",
    "pencuri": "thief",
    "pendaki": "climber",
    "penari": "dancer",
    "pengguna": "user",
    "pengkaji": "researcher",
    "penganalisis": "analyst",
    "penyapu": "broom",
    "penyukat": "measurer",
    "pengecat": "painter",
    "pengelap": "wiper",
    "makanan": "food",
    "tulisan": "writing",
    "pakaian": "clothing",
    "tuliskan": "please write",
    "hantarkan": "send/deliver",
    "bukakan": "open for someone",
    "sayangi": "love/cherish",
    "dekati": "approach",
    "jauhi": "stay away from"
}

# --- Streamlit Interface ---
st.title("🗣️ Malay Vocabulary Tester")
st.write("Test your Malay ↔ English vocabulary knowledge!")

# --- Sidebar Options ---
mode = st.sidebar.selectbox("Test direction:", ["English → Malay", "Malay → English"])
num_questions = st.sidebar.slider("Number of words to test:", 3, 20, 5)

# --- Add New Words ---
st.sidebar.subheader("➕ Add New Word")
new_malay = st.sidebar.text_input("Malay word:")
new_english = st.sidebar.text_input("English meaning:")

if st.sidebar.button("Add to Vocab Bank"):
    if new_malay and new_english:
        vocab[new_malay] = new_english
        st.sidebar.success(f"Added '{new_malay} = {new_english}' to vocab bank!")
    else:
        st.sidebar.warning("Please fill both Malay and English fields.")

# --- Quiz Logic ---
quiz_words = random.sample(list(vocab.items()), num_questions)
score = 0

st.header("📝 Quiz Section")

for malay, english in quiz_words:
    if mode == "Malay → English":
        user_answer = st.text_input(f"What is the English meaning of **{malay}**?", key=malay)
        if user_answer:
            if user_answer.strip().lower() == english.lower():
                st.success("✅ Correct!")
                score += 1
            else:
                st.error(f"❌ Wrong. Correct answer: **{english}**")

    else:  # English → Malay
        user_answer = st.text_input(f"What is the Malay word for **{english}**?", key=english)
        if user_answer:
            if user_answer.strip().lower() == malay.lower():
                st.success("✅ Correct!")
                score += 1
            else:
                st.error(f"❌ Wrong. Correct answer: **{malay}**")

# --- Score Display ---
st.write("---")
st.subheader(f"Your score: {score} / {num_questions}")