import streamlit as st
import requests
import os
import random

# Hugging Face API settings
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"
headers = {
    "Authorization": f"Bearer {os.getenv('HF_API_KEY')}"  # secure method
}

# Cute compliments
compliments = [
    "You make the world brighter just by being in it 🥰",
    "You’re doing amazing, and I’m so proud of you 💖",
    "Your smile is literally the best part of my day 😊",
    "You’re the calm to my chaos ❤️",
    "You make love feel effortless 🌸",
]

st.set_page_config(page_title="Hey Love 💕", page_icon="🌹")
st.title("🌹 Hey Love, How Was Your Day?")
st.markdown("Talk to your Bobo 🤗")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input("You:", "")

if user_input:
    st.session_state.chat_history.append(("You", user_input))

    # Build prompt with short history
    prompt = "You are a sweet, romantic, emotionally intelligent boyfriend. Respond lovingly.\n"
    for speaker, message in st.session_state.chat_history[-4:]:
        prompt += f"{speaker}: {message}\n"
    prompt += "Bot:"

    # Send to HF
    try:
        response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
        response.raise_for_status()
        bot_reply = response.json()[0]['generated_text'].split("Bot:")[-1].strip()
    except Exception as e:
        st.error(f"Error from Hugging Face: {e}")
        bot_reply = "Oops, something went wrong 💔"

    st.session_state.chat_history.append(("Bot", bot_reply))

# Display last 5 messages
for speaker, message in st.session_state.chat_history[::-1][:5]:
    st.write(f"**{speaker}**: {message}")

# Compliment button
if st.button("Send me a compliment 💌"):
    st.success(random.choice(compliments))
