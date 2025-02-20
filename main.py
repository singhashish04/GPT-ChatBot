import streamlit as st  
import openai

# Ensure `st.set_page_config()` is the first command
st.set_page_config(page_title="ChatBot", page_icon="💭", layout="centered")

# Check API Key in Streamlit Secrets
if "OPENROUTER_API_KEY" in st.secrets:
    OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]
else:
    st.error(" API Key Not Found in Streamlit Secrets!")
    st.stop()

# Configure OpenRouter API
client = openai.OpenAI(api_key=OPENROUTER_API_KEY, base_url="https://openrouter.ai/api/v1")

# Initialize Chat History in Session State
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Streamlit Page Title
st.title("🤖 OpenRouter ChatBot")

# Display Chat History from Session State
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input Field
user_prompt = st.chat_input("Ask me anything...")

if user_prompt:
    # Add User's Message to Chat History and Display
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    try:
        # Send Message to OpenRouter AI
        response = client.chat.completions.create(
            model="google/gemini-2.0-flash-lite-preview-02-05:free",  # Change to an available OpenRouter model
            messages=[{"role": "system", "content": "You are a helpful assistant"},
                      *st.session_state.chat_history]
        )

        # Store and Display Assistant's Response
        if response and response.choices:
            assistant_response = response.choices[0].message.content
            st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

            with st.chat_message("assistant"):
                st.markdown(assistant_response)
        else:
            st.error("Empty response from API.")

    except openai.OpenAIError as e:
        st.error(f"API Error: {str(e)}")
    except Exception as e:
        st.error(f"Unexpected Error: {str(e)}")
