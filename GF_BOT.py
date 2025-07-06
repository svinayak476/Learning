import streamlit as st
import openai
import random

# Initialize OpenAI client (for v1.x SDK)
client = openai.OpenAI(api_key="sk-REPLACE_WITH_YOUR_KEY")

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

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a sweet, funny, romantic and emotionally intelligent boyfriend. Always support her, flirt a little, and make her feel special. Be gentle, not robotic."},
            *[
                {"role": "user" if msg[0] == "You" else "assistant", "content": msg[1]}
                for msg in st.session_state.chat_history
            ]
        ]
    )

    bot_reply = response.choices[0].message.content
    st.session_state.chat_history.append(("Bot", bot_reply))

for speaker, message in st.session_state.chat_history[::-1][:5]:  # show last 5 messages
    st.write(f"**{speaker}**: {message}")

# Bonus touch: Random compliment button
if st.button("Send me a compliment 💌"):
    st.success(random.choice(compliments))
