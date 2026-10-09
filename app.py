import pandas as pd
import streamlit as st
from anthropic import Anthropic

st.set_page_config(page_title="Feedback Helper", page_icon="📊")
st.title("📊 Customer Feedback Helper")

# API key environment variable ANTHROPIC_API_KEY se khud padh leta hai
client = Anthropic()


def ask_ai(prompt: str) -> str:
    try:
        reply = client.messages.create(
            model="claude-sonnet-5-5",
            max_tokens=800,
            messages=[{"role": "user", "content": prompt}],
        )
        return reply.content[0].text
    except Exception as e:
        return f"Kuch masla aaya: {e}"


# 1) Data load karein
file = st.file_uploader("Apni CSV upload karein (column ka naam: review)", type="csv")
df = pd.read_csv(file) if file else pd.read_csv("sample_data.csv")

if "review" not in df.columns:
    st.error("CSV mein 'review' naam ka column hona chahiye.")
    st.stop()

st.subheader("Data")
st.dataframe(df, use_container_width=True)

# AI ko sirf pehle 50 reviews bhejte hain (tez aur sasta)
reviews = "\n".join(f"- {text}" for text in df["review"].dropna().head(50))

# 2) Summary
st.subheader("AI Summary")
if st.button("Summary banao"):
    with st.spinner("AI soch raha hai..."):
        st.write(
            ask_ai(
                "Neeche customer reviews hain. 5 bullet points mein batayein ke "
                "customers kis cheez ki tareef karte hain aur kis par shikayat.\n\n"
                + reviews
            )
        )

# 3) Sawal-jawab
st.subheader("Data se sawal poochein")
question = st.text_input("Misal: Sab se zyada shikayat kis cheez par hai?")
if question:
    with st.spinner("AI jawab dhoond raha hai..."):
        st.write(
            ask_ai(
                "Sirf in reviews ki bunyaad par jawab dein. Agar jawab data mein "
                "na ho to kahein 'data mein nahi hai'.\n\n"
                f"Reviews:\n{reviews}\n\nSawal: {question}"
            )
        )
