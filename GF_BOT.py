import streamlit as st
import openai
import random
import os

# Set your OpenAI API key here
openai.api_key = os.getenv("OPENAI_API_KEY")

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

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a sweet, funny, romantic and emotionally intelligent boyfriend. Always support her, flirt a little, and make her feel special. Be gentle, not robotic."},
                *[
                    {"role": "user" if msg[0] == "You" else "assistant", "content": msg[1]}
                    for msg in st.session_state.chat_history[-6:]  # limit to recent history
                ]
            ]
        )
        bot_reply = response.choices[0].message.content
    except Exception as e:
        bot_reply = "Oops, something went wrong 💔"
        st.error(f"Error from OpenAI: {e}")

    st.session_state.chat_history.append(("Bot", bot_reply))

# Show last few messages
for speaker, message in st.session_state.chat_history[::-1][:5]:
    st.write(f"**{speaker}**: {message}")

# Compliment button
if st.button("Send me a compliment 💌"):
    st.success(random.choice(compliments))
