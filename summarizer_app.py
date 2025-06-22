import streamlit as st
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

# تحميل النموذج
@st.cache_resource
def load_model():
    model_name = "moussaKam/AraBART"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name).to(device)
    return tokenizer, model

device = "cuda" if torch.cuda.is_available() else "cpu"
tokenizer, model = load_model()

# دالة التلخيص
def summarize_arabart(text, max_chunk_len=800, summary_max_len=200, summary_min_len=50):
    sentences = text.split('.')
    chunks, chunk = [], ''
    for sentence in sentences:
        if len(chunk) + len(sentence) < max_chunk_len:
            chunk += sentence.strip() + '. '
        else:
            chunks.append(chunk.strip())
            chunk = sentence.strip() + '. '
    if chunk:
        chunks.append(chunk.strip())

    summaries = []
    for chunk in chunks:
        inputs = tokenizer.encode(chunk, return_tensors="pt", max_length=1024, truncation=True).to(device)
        summary_ids = model.generate(
            inputs,
            num_beams=4,
            max_length=summary_max_len,
            min_length=summary_min_len,
            no_repeat_ngram_size=2,
            length_penalty=2.0,
            early_stopping=True
        )
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        summaries.append(summary.strip())
    return "\n\n".join(summaries)

# واجهة Streamlit
st.set_page_config(page_title="ملخص ذكي", layout="wide")
st.title("🧠 تلخيص النصوص العربية باستخدام AraBART")

text_input = st.text_area("📜 أدخل نصًا عربيًا طويلًا لتلخيصه:", height=300)

if st.button("تلخيص"):
    if text_input.strip():
        with st.spinner("يتم تلخيص النص..."):
            summary = summarize_arabart(text_input)
            st.subheader("📌 الملخص:")
            st.success(summary)
    else:
        st.warning("يرجى إدخال نص أولاً.")
