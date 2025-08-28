import streamlit as st
import requests
import os
import time
import json

# Define the API URL from environment variables
API_URL = os.getenv("SUMMARIZER_API_URL", "http://127.0.0.1:8000")

# --- UI Customization and CSS Injections ---
st.set_page_config(
    page_title="Multi AI Summarizer",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "Multi AI Summarizer - Compare responses from multiple AI providers and get intelligent unified summaries!"
    }
)

# Custom CSS to hide the Streamlit sidebar toggle and provide better mobile and desktop styling.
st.markdown("""
<style>
    /* Hide the default Streamlit sidebar toggle button */
    [data-testid="stSidebar"][aria-expanded="false"] [data-testid="stSidebarToggleButton"] {
        display: none;
    }

    /* General styling for the main container */
    .main .block-container {
        padding-top: 2rem;
        padding-right: 2rem;
        padding-left: 2rem;
        padding-bottom: 2rem;
    }

    /* Style the main title */
    .st-emotion-cache-1jmpspo {
        text-align: center;
        font-size: 2.5rem;
        font-weight: bold;
        color: #4CAF50;
    }

    /* Style the chat messages */
    .user-message-bubble {
        background-color: #e0e0e0;
        padding: 10px 15px;
        border-radius: 20px;
        margin: 5px 0;
        align-self: flex-end;
        max-width: 80%;
    }

    .ai-message-bubble {
        background-color: #4CAF50;
        color: white;
        padding: 10px 15px;
        border-radius: 20px;
        margin: 5px 0;
        align-self: flex-start;
        max-width: 80%;
    }

    /* Style for the ad banners */
    .ad-banner {
        width: 100%;
        text-align: center;
        padding: 10px;
        background-color: #f0f0f0;
        border-radius: 10px;
        margin-top: 20px;
        font-size: 0.8em;
    }

    /* Floating ad style */
    .ad-floating {
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: #f9f9f9;
        border: 1px solid #ccc;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        z-index: 1000;
        max-width: 300px;
        animation: fadeIn 0.5s ease-in-out;
    }
    .ad-close {
        position: absolute;
        top: 5px;
        right: 5px;
        background: #ccc;
        border: none;
        border-radius: 50%;
        width: 20px;
        height: 20px;
        cursor: pointer;
    }
    .footer-section {
        margin-top: 2rem;
        padding: 1rem;
        background-color: #f9f9f9;
        border-radius: 10px;
        text-align: center;
    }
    .footer-section a {
        color: #4CAF50;
        text-decoration: none;
        font-weight: bold;
    }
    .footer-section a:hover {
        text-decoration: underline;
    }
    /* Simple fade-in animation for the floating ad */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
</style>
""", unsafe_allow_html=True)

# --- Streamlit Session State Management ---
# Initialize chat history and other session variables if they don't exist
if "chat" not in st.session_state:
    st.session_state["chat"] = {"messages": [], "title": ""}
if "selected_providers" not in st.session_state:
    st.session_state["selected_providers"] = []
if "awaiting_response" not in st.session_state:
    st.session_state["awaiting_response"] = False
if "pending_question" not in st.session_state:
    st.session_state["pending_question"] = None
if "show_intro" not in st.session_state:
    st.session_state["show_intro"] = True

# --- API Functions ---
def get_providers():
    """Fetches the list of available AI providers from the API."""
    try:
        response = requests.get(f"{API_URL}/providers")
        response.raise_for_status()
        return response.json().get("providers", [])
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching providers: {e}")
        return []

def get_response_from_api(user_message, providers):
    """Sends a user message to the API and gets a summary."""
    try:
        data = {
            "query": user_message,
            "providers": providers
        }
        response = requests.post(f"{API_URL}/summarize", json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error getting summary: {e}")
        return None

def infer_title(messages):
    """Placeholder function to infer a chat title from the first message."""
    if messages and messages[0]["role"] == "user":
        return messages[0]["content"][:30] + "..."
    return "New Chat"

# --- Main App Logic ---
st.title("Multi AI Summarizer")

# Sidebar for Provider Selection
st.sidebar.title("AI Providers")
providers = get_providers()
st.session_state["selected_providers"] = st.sidebar.multiselect(
    "Select AI providers:",
    options=providers,
    default=st.session_state["selected_providers"] if st.session_state["selected_providers"] else None
)

# New Chat button
if st.sidebar.button("New Chat", use_container_width=True):
    st.session_state["chat"] = {"messages": [], "title": ""}
    st.session_state["show_intro"] = True
    st.session_state["awaiting_response"] = False
    st.session_state["pending_question"] = None
    st.rerun()

# Introduction message
if st.session_state["show_intro"] and not st.session_state["chat"]["messages"]:
    st.info("Welcome to the Multi AI Summarizer! Select your AI providers on the left and start a conversation below.")

# Display chat history
chat_history_container = st.container()
with chat_history_container:
    for message in st.session_state["chat"]["messages"]:
        if message["role"] == "user":
            st.markdown(f'<div class="user-message-bubble">{message["content"]}</div>', unsafe_allow_html=True)
        elif message["role"] == "assistant":
            # Display the unified summary first
            summary_content = message.get("unified_summary", "No unified summary available.")
            st.markdown(f'<div class="ai-message-bubble">**Unified Summary:**<br>{summary_content}</div>', unsafe_allow_html=True)
            
            # Display individual provider responses in an expander
            provider_responses = message.get("responses", [])
            with st.expander("Show detailed provider responses"):
                for provider_response in provider_responses:
                    st.markdown(f"**{provider_response['provider']}**: {provider_response['content']}")

# User input field
user_input = st.chat_input("Ask a question to get a summary...", disabled=st.session_state["awaiting_response"])

# Handle user input and trigger API call
if user_input and not st.session_state["awaiting_response"] and st.session_state["selected_providers"]:
    st.session_state["pending_question"] = user_input
    st.session_state["awaiting_response"] = True
    st.session_state["show_intro"] = False
    
    st.session_state["chat"]["messages"].append({"role": "user", "content": user_input})
    if len(st.session_state["chat"]["messages"]) == 1:
        st.session_state["chat"]["title"] = infer_title(st.session_state["chat"]["messages"])
    
    st.rerun()

# Logic to handle the API response after a rerun
if st.session_state["awaiting_response"] and st.session_state["pending_question"]:
    with st.spinner("Generating summary..."):
        api_response = get_response_from_api(
            st.session_state["pending_question"],
            st.session_state["selected_providers"]
        )
    
    if api_response:
        st.session_state["chat"]["messages"].append({"role": "assistant", **api_response})
    
    st.session_state["awaiting_response"] = False
    st.session_state["pending_question"] = None
    st.rerun()

# --- Footer and Ads (Optional) ---
st.markdown("---")

# Footer with contact information
st.markdown("""
<div class="footer-section">
    <h4>📬 Get in Touch</h4>
    <p>Questions, feedback, or business inquiries?</p>
    <a href="mailto:multiaisummarizer@gmail.com">
        ✉️ multiaisummarizer@gmail.com
    </a>
</div>
""", unsafe_allow_html=True)

# Floating ad script - subtle and delayed
st.markdown("""
<script>
    setTimeout(function() {
        var ad = document.getElementById('floating-ad');
        if (ad) {
            ad.style.display = 'block';
        }
    }, 15000); // Show after 15 seconds
    function closeFloatingAd() {
        var ad = document.getElementById('floating-ad');
        if (ad) {
            ad.style.display = 'none';
        }
    }
</script>
""", unsafe_allow_html=True)

# Floating ad HTML
st.markdown("""
<div id="floating-ad" class="ad-floating" style="display: none;">
    <button class="ad-close" onclick="closeFloatingAd()">x</button>
    <strong>Try our other awesome app!</strong>
    <p>Check out our new tool for collaborative mind-mapping.</p>
    <a href="#">Learn More</a>
</div>
""", unsafe_allow_html=True)
