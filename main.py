import os
import json
import streamlit as st
import openai

#Ensure set_page_config is first
st.set_page_config(
    page_title="ChatBot",
    page_icon="💭",
    layout="centered"
)

# Load OpenRouter API Key
working_dir = os.path.dirname(os.path.abspath(__file__))
config_data = json.load(open(f"{working_dir}/config.json"))
#OPENROUTER_API_KEY = config_data["OPENROUTER_API_KEY"]

# Load API Key from Streamlit Secrets
OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]

# Configure OpenRouter API
client = openai.OpenAI(api_key=OPENROUTER_API_KEY, base_url="https://openrouter.ai/api/v1")

# Initialize Chat Session
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Streamlit Page Title
st.title("🤖 ChatBot ")

# Display Chat History
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input Field
user_prompt = st.chat_input("Ask GPT-4o....")

if user_prompt:
    # Add User's Message to Chat History and Display
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    try:
        # Use OpenRouter model
        response = client.chat.completions.create(
            model="google/gemini-2.0-flash-lite-preview-02-05:free",  # Use a free OpenRouter model like "gemini-2.0-flash-lite"
            messages=[{"role": "system", "content": "You are a helpful assistant"},
                      *st.session_state.chat_history]
        )

        # Validate API response
        if response and response.choices:
            assistant_response = response.choices[0].message.content
            st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

            # Display Assistant Response
            with st.chat_message("assistant"):
                st.markdown(assistant_response)
        else:
            st.error("API response was empty. Try again later.")

    except openai.OpenAIError as e:
        st.error(f"Error: {str(e)}")
    except Exception as e:
        st.error(f"Unexpected Error: {str(e)}")
