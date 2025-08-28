import streamlit as st
import requests
import os
import time

# Use a consistent session state key for the sidebar
# This prevents it from disappearing on refreshes
if 'sidebar_visible' not in st.session_state:
    st.session_state.sidebar_visible = True

API_URL = os.getenv("SUMMARIZER_API_URL", "http://127.0.0.1:8000")

st.set_page_config(
    page_title="Multi AI Summarizer",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "Multi AI Summarizer - Compare responses from multiple AI providers and get intelligent unified summaries!"
    }
)

# Enhanced CSS with better mobile support and sidebar toggle
st.markdown("""
<style>
    /* Global styles to ensure full-screen layout on all devices */
    html, body {
        height: 100%;
        margin: 0;
        padding: 0;
    }
    
    /* MOBILE SIDEBAR TOGGLE SOLUTION */
    .mobile-sidebar-toggle {
        position: fixed;
        top: 10px;
        left: 10px;
        z-index: 999999;
        background: #4CAF50;
        color: white !important;
        border: none;
        padding: 8px 12px;
        border-radius: 8px;
        font-size: 20px;
        font-weight: bold;
        cursor: pointer;
        box-shadow: 0 3px 12px rgba(0,0,0,0.4);
        transition: all 0.3s ease;
        min-width: 44px;
        min-height: 44px;
        text-align: center;
        display: none; /* Initially hide on all screens and show via media query */
        align-items: center;
        justify-content: center;
    }
    
    .mobile-sidebar-toggle:hover {
        background: #45a049 !important;
        transform: scale(1.05);
    }
    
    .mobile-sidebar-toggle:active {
        transform: scale(0.95);
    }
    
    /* Show toggle on mobile at ALL times and handle body class */
    @media (max-width: 768px) {
        .mobile-sidebar-toggle {
            display: flex !important;
        }

        /* Initially hide sidebar on mobile */
        body {
            overflow-x: hidden;
            transition: margin-left 0.3s ease;
        }

        .sidebar-hidden section[data-testid="stSidebar"] {
            transform: translateX(-100%);
            transition: transform 0.3s ease;
        }
        
        .sidebar-hidden .st-emotion-cache-1c5t105.e1g8p9av3 {
            transform: translateX(-100%);
            transition: transform 0.3s ease;
        }

        .sidebar-visible section[data-testid="stSidebar"] {
            transform: translateX(0);
            transition: transform 0.3s ease;
        }
        
        .sidebar-visible .st-emotion-cache-1c5t105.e1g8p9av3 {
            transform: translateX(0);
            transition: transform 0.3s ease;
        }
    }
    
    /* Floating toggle button styling */
    .sidebar-hidden .mobile-sidebar-toggle {
        background: #ff6b6b !important;
        animation: gentle-pulse 3s infinite;
    }
    
    .sidebar-visible .mobile-sidebar-toggle {
        background: #4CAF50 !important;
        animation: none;
    }
    
    @keyframes gentle-pulse {
        0%, 100% { 
            box-shadow: 0 3px 12px rgba(255, 107, 107, 0.4);
            transform: scale(1);
        }
        50% { 
            box-shadow: 0 5px 20px rgba(255, 107, 107, 0.6);
            transform: scale(1.02);
        }
    }
    
    /* ENHANCED MOBILE TEXT VISIBILITY FIXES */
    @media (max-width: 768px) {
        /* Force sidebar styling for better visibility */
        .st-emotion-cache-1c5t105.e1g8p9av3,
        section[data-testid="stSidebar"] {
            background: #1a1a1a !important;
            width: 280px !important;
            min-width: 280px !important;
            position: fixed !important;
            left: 0 !important;
            top: 0 !important;
            height: 100vh !important;
            z-index: 999998 !important;
            overflow-y: auto !important;
            border-right: 2px solid #333 !important;
        }
        
        /* Force white text throughout sidebar with higher specificity */
        .st-emotion-cache-1c5t105.e1g8p9av3 *,
        section[data-testid="stSidebar"] *,
        .st-emotion-cache-1c5t105.e1g8p9av3 .stButton button,
        section[data-testid="stSidebar"] .stButton button {
            color: #ffffff !important;
            font-weight: 600 !important;
        }
        
        /* Specific element text visibility fixes */
        .st-emotion-cache-1c5t105.e1g8p9av3 h1, .st-emotion-cache-1c5t105.e1g8p9av3 h2, .st-emotion-cache-1c5t105.e1g8p9av3 h3, .st-emotion-cache-1c5t105.e1g8p9av3 h4,
        section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] h3, section[data-testid="stSidebar"] h4 {
            color: #ffffff !important;
            font-weight: bold !important;
        }
        
        .st-emotion-cache-1c5t105.e1g8p9av3 p, section[data-testid="stSidebar"] p {
            color: #ffffff !important;
            font-weight: 500 !important;
        }
        
        /* Multiselect styling improvements */
        .st-emotion-cache-1c5t105.e1g8p9av3 .stMultiSelect label,
        section[data-testid="stSidebar"] .stMultiSelect label {
            color: #ffffff !important;
            font-weight: bold !important;
            font-size: 16px !important;
        }
        
        .st-emotion-cache-1c5t105.e1g8p9av3 .stMultiSelect > div,
        section[data-testid="stSidebar"] .stMultiSelect > div {
            background-color: #333333 !important;
            border: 2px solid #555555 !important;
            border-radius: 8px !important;
        }
        
        .st-emotion-cache-1c5t105.e1g8p9av3 .stMultiSelect [data-baseweb="tag"],
        section[data-testid="stSidebar"] .stMultiSelect [data-baseweb="tag"] {
            background-color: #ff6b6b !important;
            color: white !important;
            font-weight: bold !important;
        }
        
        /* Button improvements with maximum visibility */
        .st-emotion-cache-1c5t105.e1g8p9av3 .stButton button,
        section[data-testid="stSidebar"] .stButton button {
            background-color: #333333 !important;
            color: #ffffff !important;
            border: 2px solid #555555 !important;
            font-weight: bold !important;
            font-size: 16px !important;
            padding: 10px 16px !important;
            border-radius: 8px !important;
            text-shadow: none !important;
            box-shadow: 0 2px 4px rgba(0,0,0,0.3) !important;
        }
        
        /* MAXIMUM FORCE for button text visibility */
        .st-emotion-cache-1c5t105.e1g8p9av3 .stButton button *,
        section[data-testid="stSidebar"] .stButton button *,
        .st-emotion-cache-1c5t105.e1g8p9av3 .stButton button span *,
        section[data-testid="stSidebar"] .stButton button span *,
        .st-emotion-cache-1c5t105.e1g8p9av3 .stButton p,
        section[data-testid="stSidebar"] .stButton p {
            color: #ffffff !important;
            font-weight: 900 !important;
            font-size: 16px !important;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.8) !important;
            opacity: 1 !important;
            visibility: visible !important;
        }
        
        /* Target the specific button content */
        .st-emotion-cache-1c5t105.e1g8p9av3 .stButton button[kind="secondary"],
        section[data-testid="stSidebar"] .stButton button[kind="secondary"] {
            background-color: #2d2d2d !important;
            color: #ffffff !important;
            border: 2px solid #ffffff !important;
        }
        
        /* Force all nested elements to be visible */
        .st-emotion-cache-1c5t105.e1g8p9av3 .stButton button > *,
        section[data-testid="stSidebar"] .stButton button > * {
            color: #ffffff !important;
            opacity: 1 !important;
            visibility: visible !important;
            font-weight: 900 !important;
        }
        
        .st-emotion-cache-1c5t105.e1g8p9av3 .stButton button:hover,
        section[data-testid="stSidebar"] .stButton button:hover {
            background-color: #444444 !important;
            border-color: #777777 !important;
            color: #ffffff !important;
        }
        
        .st-emotion-cache-1c5t105.e1g8p9av3 .stButton button[kind="primary"],
        section[data-testid="stSidebar"] .stButton button[kind="primary"] {
            background-color: #ff6b6b !important;
            border-color: #ff6b6b !important;
            color: white !important;
        }
        
        .st-emotion-cache-1c5t105.e1g8p9av3 .stButton button[kind="primary"] span,
        section[data-testid="stSidebar"] .stButton button[kind="primary"] span {
            color: white !important;
            font-weight: bold !important;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.7) !important;
        }
        
        /* Info and warning boxes */
        .st-emotion-cache-1c5t105.e1g8p9av3 .stInfo,
        section[data-testid="stSidebar"] .stInfo {
            background-color: #2d4a5d !important;
            border: 1px solid #4a7c9d !important;
            border-radius: 8px !important;
        }
        
        .st-emotion-cache-1c5t105.e1g8p9av3 .stInfo > div,
        section[data-testid="stSidebar"] .stInfo > div {
            color: #ffffff !important;
            font-weight: 500 !important;
        }
        
        .st-emotion-cache-1c5t105.e1g8p9av3 .stWarning,
        section[data-testid="stSidebar"] .stWarning {
            background-color: #5d4a2d !important;
            border: 1px solid #9d7c4a !important;
            border-radius: 8px !important;
        }
        
        .st-emotion-cache-1c5t105.e1g8p9av3 .stWarning > div,
        section[data-testid="stSidebar"] .stWarning > div {
            color: #ffffff !important;
            font-weight: 500 !important;
        }
        
        .st-emotion-cache-1c5t105.e1g8p9av3 .stSuccess,
        section[data-testid="stSidebar"] .stSuccess {
            background-color: #2d5d2d !important;
            border: 1px solid #4a9d4a !important;
            border-radius: 8px !important;
        }
        
        .st-emotion-cache-1c5t105.e1g8p9av3 .stSuccess > div,
        section[data-testid="stSidebar"] .stSuccess > div {
            color: #ffffff !important;
            font-weight: 500 !important;
        }
        
        /* Main content adjustments for persistent toggle */
        .main .block-container {
            padding-left: 70px !important; /* Space for always-visible toggle */
            padding-right: 1rem !important;
            max-width: 100% !important;
            padding-top: 1rem !important;
        }
        
        /* Adjust main content when sidebar is hidden */
        .sidebar-hidden .main .block-container {
            padding-left: 70px !important; /* Keep space for toggle */
            margin-left: 0 !important;
        }
        
        /* Adjust main content when sidebar is visible */
        .sidebar-visible .main {
            margin-left: 280px !important;
        }
        
        .sidebar-visible .main .block-container {
            padding-left: 1rem !important;
            margin-left: 0 !important;
        }
        
        /* Chat input improvements for mobile */
        .stChatInput > div {
            border: 2px solid #4CAF50 !important;
            border-radius: 20px !important;
            background: #ffffff !important;
            box-shadow: 0 2px 10px rgba(76, 175, 80, 0.3) !important;
            margin: 10px 5px !important;
        }
        
        .stChatInput > div:focus-within {
            border-color: #66BB6A !important;
            box-shadow: 0 4px 15px rgba(76, 175, 80, 0.4) !important;
        }
        
        .stChatInput input {
            font-size: 16px !important;
            padding: 12px 16px !important;
            color: #333 !important;
            font-weight: 500 !important;
        }
        
        .stChatInput input::placeholder {
            color: #777 !important;
            font-weight: 400 !important;
        }
        
        /* Remove animated label on mobile for clarity */
        .stChatInput > div::before {
            display: none !important;
        }
    }
    
    /* DESKTOP STYLES - PRESERVED */
    @media (min-width: 769px) {
        /* Hide toggle button on desktop */
        .mobile-sidebar-toggle {
            display: none !important;
        }
        
        /* Desktop chat input styling - preserved */
        .stChatInput > div {
            border: 3px solid #4CAF50 !important;
            border-radius: 30px !important;
            background: linear-gradient(135deg, #1e3a1e, #2d5a2d) !important;
            box-shadow: 0 6px 20px rgba(76, 175, 80, 0.3) !important;
            transition: all 0.3s ease;
            position: relative;
        }
        
        .stChatInput > div:focus-within {
            border-color: #66BB6A !important;
            box-shadow: 0 8px 25px rgba(76, 175, 80, 0.4) !important;
            transform: translateY(-3px);
        }
        
        .stChatInput > div::before {
            content: "💬 Type your question here - AI is ready to help!";
            position: absolute;
            top: -35px;
            left: 15px;
            font-size: 14px;
            color: #4CAF50;
            font-weight: 600;
            background: var(--background-color, #0e1117);
            padding: 4px 12px;
            border-radius: 15px;
            border: 1px solid #4CAF50;
            animation: glow 2s ease-in-out infinite alternate;
        }
        
        @keyframes glow {
            from { box-shadow: 0 0 5px rgba(76, 175, 80, 0.3); }
            to { box-shadow: 0 0 15px rgba(76, 175, 80, 0.6); }
        }
        
        .stChatInput input {
            font-size: 16px !important;
            padding: 12px 20px !important;
            color: #333 !important;
        }
    }
    
    /* AD PLACEMENT STYLES - SUBTLE VERSION */
    .ad-banner {
        background: linear-gradient(135deg, #f8f9fa, #ffffff);
        border: 1px solid #e9ecef;
        border-radius: 8px;
        padding: 10px 15px;
        margin: 15px auto;
        text-align: center;
        max-width: 728px;
        min-height: 60px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #888;
        font-size: 12px;
        font-weight: 400;
        opacity: 0.7;
        transition: opacity 0.3s ease;
    }
    
    .ad-banner:hover {
        opacity: 1;
    }
    
    .ad-sidebar {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 6px;
        padding: 8px;
        margin: 10px 0;
        text-align: center;
        min-height: 80px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #666;
        font-size: 10px;
        opacity: 0.6;
        transition: opacity 0.3s ease;
    }
    
    .ad-sidebar:hover {
        opacity: 0.8;
    }
    
    .ad-floating {
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: #ffffff;
        border: 1px solid #f0f0f0;
        border-radius: 8px;
        padding: 10px;
        max-width: 250px;
        min-height: 80px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        z-index: 1000;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #777;
        font-size: 11px;
        opacity: 0.8;
        transition: all 0.3s ease;
    }
    
    .ad-close {
        position: absolute;
        top: 3px;
        right: 5px;
        background: #ccc;
        color: white;
        border: none;
        border-radius: 50%;
        width: 18px;
        height: 18px;
        font-size: 10px;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        opacity: 0.7;
    }
    
    .ad-between-chats {
        background: rgba(248, 249, 250, 0.5);
        border: 1px solid rgba(233, 236, 239, 0.5);
        border-radius: 6px;
        padding: 8px 12px;
        margin: 10px 0;
        text-align: center;
        min-height: 50px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #999;
        font-size: 11px;
        font-weight: 400;
        opacity: 0.5;
    }
    
    /* Mobile ad adjustments */
    @media (max-width: 768px) {
        .ad-banner {
            max-width: 100%;
            margin: 10px 0;
            min-height: 50px;
            font-size: 10px;
            padding: 8px;
        }
        
        .ad-floating {
            bottom: 80px; /* Above chat input */
            right: 10px;
            max-width: 200px;
            min-height: 60px;
            font-size: 10px;
            padding: 8px;
        }
        
        .ad-sidebar {
            min-height: 60px;
            margin: 8px 0;
            font-size: 9px;
        }
        
        .ad-between-chats {
            margin: 8px 0;
            min-height: 40px;
            font-size: 10px;
            padding: 6px 8px;
        }
    }
    
    /* GENERAL STYLES - Mobile and Desktop */
    /* Chat message styling */
    .user-message {
        padding: 12px;
        margin: 8px 0;
        background: linear-gradient(90deg, #e3f2fd, #bbdefb);
        border-left: 4px solid #2196f3;
        border-radius: 8px;
        color: #0d47a1;
        font-weight: 500;
    }
    
    .ai-summary {
        padding: 12px;
        margin: 8px 0;
        background: linear-gradient(90deg, #e8f5e8, #c8e6c9);
        border-left: 4px solid #4caf50;
        border-radius: 8px;
        color: #1b5e20;
        font-weight: 500;
    }
    
    .ai-content {
        padding: 12px;
        margin: 8px 0 12px 0;
        background: #f1f8e9;
        border-radius: 6px;
        color: #33691e;
        line-height: 1.6;
    }
    
    /* Intro section styling */
    .intro-section h3 {
        color: #1976d2 !important;
        margin-bottom: 1rem;
        font-weight: 600;
    }
    
    .intro-section {
        background: #f8f9ff !important;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border: 1px solid #e3f2fd;
        color: #333 !important;
    }
    
    .intro-section p, .intro-section li, .intro-section div {
        color: #333 !important;
        line-height: 1.6;
    }
    
    /* Footer styling */
    .footer-section {
        text-align: center;
        padding: 12px;
        background: rgba(255, 255, 255, 0.03);
        border-radius: 8px;
        margin: 15px auto;
        border: 1px solid rgba(255, 255, 255, 0.1);
        max-width: 400px;
    }
    
    .footer-section h4 {
        color: #888 !important;
        margin-bottom: 6px !important;
        font-size: 14px !important;
        font-weight: 400 !important;
    }
    
    .footer-section p {
        font-size: 12px !important;
        color: #999 !important;
        margin-bottom: 8px !important;
    }
    
    .footer-section a {
        color: #aaa !important;
        text-decoration: none !important;
        font-weight: normal !important;
        background: rgba(255, 255, 255, 0.05) !important;
        padding: 3px 8px !important;
        border-radius: 10px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        font-size: 12px !important;
        transition: all 0.2s ease;
    }
    
    .footer-section a:hover {
        background: rgba(255, 255, 255, 0.1) !important;
        border-color: rgba(255, 255, 255, 0.2) !important;
    }
    
    /* Status indicators */
    .status-success {
        background: #d4edda;
        color: #155724;
        border: 1px solid #c3e6cb;
        padding: 8px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 500;
        display: inline-block;
        margin: 4px;
    }
    
    .status-error {
        background: #f8d7da;
        color: #721c24;
        border: 1px solid #f5c6cb;
        padding: 8px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 500;
        display: inline-block;
        margin: 4px;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Chat input positioning */
    .stChatInput {
        position: sticky;
        bottom: 0;
        background: var(--background-color, #0e1117);
        z-index: 100;
        padding: 15px 0;
        border-top: 3px solid #4CAF50;
        box-shadow: 0 -4px 15px rgba(76, 175, 80, 0.2);
    }
    
    .stChatInput input::placeholder {
        color: #666 !important;
        font-weight: 500 !important;
    }
</style>
""", unsafe_allow_html=True)

# Enhanced JavaScript for sidebar toggle functionality
st.markdown("""
<script>
    document.addEventListener('DOMContentLoaded', function() {
        const toggleButton = document.createElement('button');
        toggleButton.innerHTML = '☰';
        toggleButton.className = 'mobile-sidebar-toggle';
        toggleButton.id = 'mobile-sidebar-toggle';
        toggleButton.title = 'Menu';
        toggleButton.setAttribute('aria-label', 'Toggle sidebar menu');
        document.body.appendChild(toggleButton);

        const toggleSidebar = () => {
            const body = document.body;
            const sidebar = document.querySelector('section[data-testid="stSidebar"]');
            const toggleButton = document.getElementById('mobile-sidebar-toggle');
            
            if (body.classList.contains('sidebar-visible')) {
                body.classList.remove('sidebar-visible');
                body.classList.add('sidebar-hidden');
                if (toggleButton) {
                    toggleButton.innerHTML = '☰';
                    toggleButton.title = 'Menu';
                }
            } else {
                body.classList.remove('sidebar-hidden');
                body.classList.add('sidebar-visible');
                if (toggleButton) {
                    toggleButton.innerHTML = '✕';
                    toggleButton.title = 'Close Menu';
                }
            }
        };

        toggleButton.onclick = function(e) {
            e.preventDefault();
            e.stopPropagation();
            toggleSidebar();
        };

        // Initialize state based on the current window size
        const checkWindowSize = () => {
            const body = document.body;
            const toggleButton = document.getElementById('mobile-sidebar-toggle');
            
            if (window.innerWidth <= 768) {
                // If the sidebar is expanded by default on desktop, collapse it on mobile
                if (body.classList.contains('sidebar-visible')) {
                    body.classList.remove('sidebar-visible');
                    body.classList.add('sidebar-hidden');
                    if (toggleButton) {
                        toggleButton.innerHTML = '☰';
                        toggleButton.title = 'Menu';
                    }
                }
                if (toggleButton) {
                    toggleButton.style.display = 'flex';
                }
            } else {
                // On desktop, ensure sidebar is visible and toggle button is hidden
                body.classList.remove('sidebar-hidden');
                body.classList.add('sidebar-visible');
                if (toggleButton) {
                    toggleButton.style.display = 'none';
                }
            }
        };

        // Attach event listeners
        window.addEventListener('resize', checkWindowSize);
        checkWindowSize();
        
    });
</script>
""", unsafe_allow_html=True)

# Main app logic
st.header("Multi AI Summarizer")
st.subheader("Compare responses from multiple AI providers and get intelligent unified summaries!")

# Sidebar content
with st.sidebar:
    st.image("https://placehold.co/250x100/4CAF50/FFFFFF?text=Logo+Placeholder", use_column_width=True)
    st.write("### AI Providers")
    providers = ["Provider A", "Provider B", "Provider C"]
    st.session_state["selected_providers"] = st.multiselect("Select providers to use", providers, default=providers, key="providers_multiselect")

    st.markdown("""
    <div class="ad-sidebar">
        <small>Ad Placeholder</small>
    </div>
    """, unsafe_allow_html=True)

# Placeholder for main content - will be replaced with chat
if "chat" not in st.session_state:
    st.session_state["chat"] = {"title": "New Chat", "messages": []}
if "show_intro" not in st.session_state:
    st.session_state["show_intro"] = True
if "awaiting_response" not in st.session_state:
    st.session_state["awaiting_response"] = False
if "pending_question" not in st.session_state:
    st.session_state["pending_question"] = ""

def infer_title(messages):
    if messages:
        first_message = messages[0]["content"]
        response = requests.post(f"{API_URL}/infer_title", json={"text": first_message})
        if response.status_code == 200:
            return response.json().get("title", "New Chat")
    return "New Chat"

if st.session_state["show_intro"]:
    with st.container(border=True):
        st.markdown("""
        <div class="intro-section">
            <h3>Welcome to Multi AI Summarizer! ✨</h3>
            <p><strong>Powered by multiple state-of-the-art AI models.</strong></p>
            <ul>
                <li><strong>Compare:</strong> Get different summaries and insights from various AI providers simultaneously.</li>
                <li><strong>Unify:</strong> Receive a single, intelligent summary that combines the best of all worlds.</li>
                <li><strong>Customize:</strong> Select the AI models you want to use in the sidebar.</li>
            </ul>
            <p>Start by asking a question or providing text below. For example, "Summarize the key findings from the latest climate report," or "What are the pros and cons of renewable energy?"</p>
        </div>
        """, unsafe_allow_html=True)

for message in st.session_state["chat"]["messages"]:
    if message["role"] == "user":
        st.markdown(f'<div class="user-message">🗣️ {message["content"]}</div>', unsafe_allow_html=True)
    elif message["role"] == "assistant":
        st.markdown(f'<div class="ai-summary">🧠 <strong>Summary:</strong><br>{message["content"]["summary"]}</div>', unsafe_allow_html=True)
        with st.expander("Show Detailed Responses"):
            for provider, content in message["content"]["details"].items():
                st.markdown(f"**{provider}:**")
                st.markdown(f'<div class="ai-content">{content}</div>', unsafe_allow_html=True)
        if message["content"]["status_code"] != 200:
            st.markdown(f'<div class="status-error">⚠️ Error fetching from some providers: {message["content"]["status_message"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="status-success">✅ Responses from all providers successfully received.</div>', unsafe_allow_html=True)

user_input = st.chat_input("Enter your text or question here...")

if st.session_state["awaiting_response"]:
    with st.spinner("Thinking..."):
        time.sleep(2) # Simulate API call delay for now
        
        # This part of the code would normally make an actual API call
        try:
            response = requests.post(f"{API_URL}/summarize", json={"text": st.session_state["pending_question"], "providers": st.session_state["selected_providers"]})
            response.raise_for_status()
            
            response_data = response.json()
            st.session_state["chat"]["messages"].append({
                "role": "assistant",
                "content": response_data
            })
            st.session_state["awaiting_response"] = False
            st.session_state["pending_question"] = ""
            st.rerun()
            
        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred: {e}. Please check if your backend API is running.")
            st.session_state["awaiting_response"] = False
            st.session_state["pending_question"] = ""
            st.rerun()

# This is the new user input handler
if user_input and not st.session_state["awaiting_response"] and st.session_state["selected_providers"]:
    st.session_state["pending_question"] = user_input
    st.session_state["awaiting_response"] = True
    st.session_state["show_intro"] = False
    
    st.session_state["chat"]["messages"].append({"role": "user", "content": user_input})
    if len(st.session_state["chat"]["messages"]) == 1:
        st.session_state["chat"]["title"] = infer_title(st.session_state["chat"]["messages"])
    
    st.rerun()

# Footer - much more subtle now
st.markdown("---")

# FOOTER BANNER AD (Subtle)
st.markdown("""
<div class="ad-banner">
    <small style="color: #aaa;">Advertisement</small>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="footer-section">
    <h4>📬 Get in Touch</h4>
    <p>Questions, feedback, or business inquiries?</p>
    <a href="mailto:multiaisummarizer@gmail.com">
        ✉️ multiaisummarizer@gmail.com
    </a>
</div>
""", unsafe_allow_html=True)

# FLOATING AD (Subtle - appears after 15 seconds)
st.markdown("""
<div id="floating-ad" class="ad-floating" style="display: none;">
    <button class="ad-close" onclick="closeFloatingAd()">✕</button>
    <small style="color: #888;">Advertisement</small>
</div>

<script>
    function closeFloatingAd() {
        document.getElementById('floating-ad').style.display = 'none';
    }

    // Show floating ad after 15 seconds, if not already closed
    setTimeout(function() {
        const ad = document.getElementById('floating-ad');
        if (ad && ad.style.display !== 'none') {
            ad.style.display = 'flex';
        }
    }, 15000);
</script>
""", unsafe_allow_html=True)
