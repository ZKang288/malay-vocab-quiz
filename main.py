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

# --- Categorise words ---
meN_words = {k: v for k, v in vocab.items() if k.startswith("me")}
peN_words = {k: v for k, v in vocab.items() if k.startswith("pe")}
other_words = {k: v for k, v in vocab.items() if k not in meN_words and k not in peN_words}

# --- Streamlit Interface ---
st.title("🗣️ Malay Vocabulary Tester")
st.write("Test your Malay ↔ English vocabulary knowledge!")

# --- Sidebar Options ---
mode = st.sidebar.selectbox("Test direction:", ["English → Malay", "Malay → English"])
num_questions = st.sidebar.slider("Number of words to test:", 3, 50, 5)

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

# --- Function to pick balanced random quiz ---
def generate_quiz(n):
    # Decide how many meN- / peN- / others to take
    if n < 10:
        n_meN = int(n * 0.4)
        n_peN = int(n * 0.2)
    elif n < 30:
        n_meN = int(n * 0.45)
        n_peN = int(n * 0.25)
    else:
        n_meN = int(n * 0.5)
        n_peN = int(n * 0.25)
    n_other = n - n_meN - n_peN

    selected_meN = random.sample(list(meN_words.items()), min(n_meN, len(meN_words)))
    selected_peN = random.sample(list(peN_words.items()), min(n_peN, len(peN_words)))
    selected_other = random.sample(list(other_words.items()), min(n_other, len(other_words)))

    combined = selected_meN + selected_peN + selected_other
    random.shuffle(combined)
    return combined

# --- Use session_state to keep quiz fixed ---
if "quiz_words" not in st.session_state:
    st.session_state.quiz_words = generate_quiz(num_questions)

st.header("📝 Quiz Section")

for i, (malay, english) in enumerate(st.session_state.quiz_words):
    key = f"q{i}"
    if mode == "Malay → English":
        user_answer = st.text_input(f"What is the English meaning of **{malay}**?", key=key)
        if user_answer:
            if user_answer.strip().lower() == english.lower():
                st.success("✅ Correct!")
            else:
                st.error(f"❌ Wrong. Correct answer: **{english}**")

    else:  # English → Malay
        user_answer = st.text_input(f"What is the Malay word for **{english}**?", key=key)
        if user_answer:
            if user_answer.strip().lower() == malay.lower():
                st.success("✅ Correct!")
            else:
                st.error(f"❌ Wrong. Correct answer: **{malay}**")

# --- Restart quiz button ---
st.write("---")
if st.button("🔁 New Quiz"):
    st.session_state.quiz_words = generate_quiz(num_questions)
    st.rerun()
