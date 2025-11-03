import streamlit as st
import random

# --- Default Vocabulary Bank ---
vocab = {
    # meN- verbs
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

    # peN- nouns
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

    # ter- words
    "terlupa": "forgot",
    "terlalu": "too",
    "tetap": "still",
    "tertidur": "fell asleep",
    "terbesar": "very big",
    "tertinggal": "left behind",
    "terkejut": "surprised",
    "tertua": "very old",
    "terlanggar": "hit accidentally",
    "tercapai": "achievable",
    "tertindah": "most beautiful",

    # others
    "makanan": "food",
    "tulisan": "writing",
    "pakaian": "clothing",
    "tuliskan": "please write",
    "hantarkan": "send/deliver",
    "bukakan": "open for someone",
    "sayangi": "love/cherish",
    "dekati": "approach",
    "jauhi": "stay away from",

    # simpulan bahasa
    "anak emas": "favourite person",
    "buah tangan": "souvenir, gift from a trip",
    "mulut murai": "talkative person",
    "kaki bangku": "bad at sports",
    "hidung tinggi": "arrogant",
    "berat tulang": "lazy",
    "otak udang": "slow-witted",
    "kaki ayam": "barefoot, not wearing shoes",
    "tangan panjang": "likes to steal",
    "telinga kuali": "stubborn, does not listen",
    "ulat buku": "bookworm",
    "besar hati": "happy or proud",
    "buah hati": "beloved, someone you love deeply",
    "kaki botol": "alcoholic",
    "makan angin": "to go on a trip or vacation",
    "ringan tulang": "hardworking",
    "besar kepala": "arrogant or overconfident",
    "cakar ayam": "messy handwriting",
    "pakwe": "boyfriend",
    "makwe": "girlfriend"
}

# --- Categorise words ---
meN_words = {k: v for k, v in vocab.items() if k.startswith("me")}
peN_words = {k: v for k, v in vocab.items() if k.startswith("pe")}
ter_words = {k: v for k, v in vocab.items() if k.startswith("ter")}
simpulan_words = {
    k: v for k, v in vocab.items()
    if " " in k and k not in meN_words and k not in peN_words and k not in ter_words
}
other_words = {
    k: v for k, v in vocab.items()
    if k not in meN_words and k not in peN_words and k not in ter_words and k not in simpulan_words
}

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

# --- Balanced Random Selection Function ---
def generate_quiz(n):
    # Adjust proportions based on quiz size
    if n < 20:
        n_meN = int(n * 0.4)
        n_peN = int(n * 0.2)
        n_ter = int(n * 0.1)
        n_simpulan = int(n * 0.1)
    else:
        n_meN = int(n * 0.35)
        n_peN = int(n * 0.2)
        n_ter = int(n * 0.1)
        n_simpulan = int(n * 0.2)
    n_other = n - (n_meN + n_peN + n_ter + n_simpulan)

    # Randomly sample from each category
    selected_meN = random.sample(list(meN_words.items()), min(n_meN, len(meN_words)))
    selected_peN = random.sample(list(peN_words.items()), min(n_peN, len(peN_words)))
    selected_ter = random.sample(list(ter_words.items()), min(n_ter, len(ter_words)))
    selected_simpulan = random.sample(list(simpulan_words.items()), min(n_simpulan, len(simpulan_words)))
    selected_other = random.sample(list(other_words.items()), min(n_other, len(other_words)))

    combined = selected_meN + selected_peN + selected_ter + selected_simpulan + selected_other
    random.shuffle(combined)
    return combined

# --- Use session_state to keep quiz fixed ---
if "quiz_words" not in st.session_state:
    st.session_state.quiz_words = generate_quiz(num_questions)

st.header("📝 Quiz Section")

# --- Display Questions ---
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

# --- Restart Quiz Button ---
st.write("---")
if st.button("🔁 New Quiz"):
    st.session_state.quiz_words = generate_quiz(num_questions)
    st.rerun()
