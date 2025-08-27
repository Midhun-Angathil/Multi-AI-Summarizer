import streamlit as st
import requests
import os
import time

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
    /* MOBILE SIDEBAR TOGGLE SOLUTION */
    .mobile-sidebar-toggle {
        display: none;
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
        display: flex;
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
    
    /* Show toggle on mobile at ALL times */
    @media (max-width: 768px) {
        .mobile-sidebar-toggle {
            display: flex !important;
        }
    }
    
    /* Hide on desktop completely */
    @media (min-width: 769px) {
        .mobile-sidebar-toggle {
            display: none !important;
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
    
    /* Show toggle button only on mobile */
    @media (max-width: 768px) {
        .mobile-sidebar-toggle {
            display: block !important;
        }
        
        /* Initially hide sidebar on mobile */
        .sidebar-hidden .css-1d391kg,
        .sidebar-hidden .css-1lcbmhc,
        .sidebar-hidden section[data-testid="stSidebar"] {
            transform: translateX(-100%) !important;
            transition: transform 0.3s ease;
        }
        
        /* Show sidebar when not hidden */
        .sidebar-visible .css-1d391kg,
        .sidebar-visible .css-1lcbmhc,
        .sidebar-visible section[data-testid="stSidebar"] {
            transform: translateX(0) !important;
            transition: transform 0.3s ease;
        }
        
        /* Adjust main content when sidebar is hidden */
        .sidebar-hidden .main {
            margin-left: 0 !important;
            padding-left: 1rem !important;
        }
        
        /* Adjust main content when sidebar is visible */
        .sidebar-visible .main {
            margin-left: 250px !important;
        }
    }
    
    /* ENHANCED MOBILE TEXT VISIBILITY FIXES */
    @media (max-width: 768px) {
        /* Force sidebar styling for better visibility */
        .css-1d391kg, 
        .css-1lcbmhc,
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
        .css-1d391kg *, 
        .css-1lcbmhc *,
        section[data-testid="stSidebar"] *,
        .css-1d391kg .stButton button,
        .css-1lcbmhc .stButton button {
            color: #ffffff !important;
            font-weight: 600 !important;
        }
        
        /* Specific element text visibility fixes */
        .css-1d391kg h1, .css-1d391kg h2, .css-1d391kg h3, .css-1d391kg h4,
        .css-1lcbmhc h1, .css-1lcbmhc h2, .css-1lcbmhc h3, .css-1lcbmhc h4 {
            color: #ffffff !important;
            font-weight: bold !important;
        }
        
        .css-1d391kg p, .css-1lcbmhc p {
            color: #ffffff !important;
            font-weight: 500 !important;
        }
        
        /* Multiselect styling improvements */
        .css-1d391kg .stMultiSelect label,
        .css-1lcbmhc .stMultiSelect label {
            color: #ffffff !important;
            font-weight: bold !important;
            font-size: 16px !important;
        }
        
        .css-1d391kg .stMultiSelect > div,
        .css-1lcbmhc .stMultiSelect > div {
            background-color: #333333 !important;
            border: 2px solid #555555 !important;
            border-radius: 8px !important;
        }
        
        .css-1d391kg .stMultiSelect [data-baseweb="tag"],
        .css-1lcbmhc .stMultiSelect [data-baseweb="tag"] {
            background-color: #ff6b6b !important;
            color: white !important;
            font-weight: bold !important;
        }
        
        /* Button improvements with maximum visibility */
        .css-1d391kg .stButton button,
        .css-1lcbmhc .stButton button {
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
        .css-1d391kg .stButton button *,
        .css-1lcbmhc .stButton button *,
        .css-1d391kg .stButton button span *,
        .css-1lcbmhc .stButton button span *,
        .css-1d391kg .stButton p,
        .css-1lcbmhc .stButton p {
            color: #ffffff !important;
            font-weight: 900 !important;
            font-size: 16px !important;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.8) !important;
            opacity: 1 !important;
            visibility: visible !important;
        }
        
        /* Target the specific button content */
        .css-1d391kg .stButton button[kind="secondary"],
        .css-1lcbmhc .stButton button[kind="secondary"] {
            background-color: #2d2d2d !important;
            color: #ffffff !important;
            border: 2px solid #ffffff !important;
        }
        
        /* Force all nested elements to be visible */
        .css-1d391kg .stButton button > *,
        .css-1lcbmhc .stButton button > * {
            color: #ffffff !important;
            opacity: 1 !important;
            visibility: visible !important;
            font-weight: 900 !important;
        }
        
        .css-1d391kg .stButton button:hover,
        .css-1lcbmhc .stButton button:hover {
            background-color: #444444 !important;
            border-color: #777777 !important;
            color: #ffffff !important;
        }
        
        .css-1d391kg .stButton button[kind="primary"],
        .css-1lcbmhc .stButton button[kind="primary"] {
            background-color: #ff6b6b !important;
            border-color: #ff6b6b !important;
            color: white !important;
        }
        
        .css-1d391kg .stButton button[kind="primary"] span,
        .css-1lcbmhc .stButton button[kind="primary"] span {
            color: white !important;
            font-weight: bold !important;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.7) !important;
        }
        
        /* Info and warning boxes */
        .css-1d391kg .stInfo,
        .css-1lcbmhc .stInfo {
            background-color: #2d4a5d !important;
            border: 1px solid #4a7c9d !important;
            border-radius: 8px !important;
        }
        
        .css-1d391kg .stInfo > div,
        .css-1lcbmhc .stInfo > div {
            color: #ffffff !important;
            font-weight: 500 !important;
        }
        
        .css-1d391kg .stWarning,
        .css-1lcbmhc .stWarning {
            background-color: #5d4a2d !important;
            border: 1px solid #9d7c4a !important;
            border-radius: 8px !important;
        }
        
        .css-1d391kg .stWarning > div,
        .css-1lcbmhc .stWarning > div {
            color: #ffffff !important;
            font-weight: 500 !important;
        }
        
        .css-1d391kg .stSuccess,
        .css-1lcbmhc .stSuccess {
            background-color: #2d5d2d !important;
            border: 1px solid #4a9d4a !important;
            border-radius: 8px !important;
        }
        
        .css-1d391kg .stSuccess > div,
        .css-1lcbmhc .stSuccess > div {
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
    // Create toggle button - ALWAYS VISIBLE ON MOBILE
    const toggleButton = document.createElement('button');
    toggleButton.innerHTML = '☰';
    toggleButton.className = 'mobile-sidebar-toggle';
    toggleButton.id = 'mobile-sidebar-toggle';
    toggleButton.title = 'Menu';
    toggleButton.setAttribute('aria-label', 'Toggle sidebar menu');
    
    // Initial state: sidebar hidden on mobile, visible on desktop
    let sidebarVisible = window.innerWidth > 768;
    
    // Set initial classes
    if (window.innerWidth <= 768) {
        document.body.classList.add('sidebar-hidden');
        toggleButton.style.display = 'flex';
    } else {
        document.body.classList.remove('sidebar-hidden', 'sidebar-visible');
        toggleButton.style.display = 'none';
    }
    
    toggleButton.onclick = function(e) {
        e.preventDefault();
        e.stopPropagation();
        
        sidebarVisible = !sidebarVisible;
        
        if (sidebarVisible) {
            document.body.classList.remove('sidebar-hidden');
            document.body.classList.add('sidebar-visible');
            this.innerHTML = '✕';
            this.title = 'Close Menu';
        } else {
            document.body.classList.remove('sidebar-visible');
            document.body.classList.add('sidebar-hidden');
            this.innerHTML = '☰';
            this.title = 'Menu';
        }
    };
    
    document.body.appendChild(toggleButton);
    
    // Auto-hide sidebar when clicking main content on mobile
    document.addEventListener('click', function(e) {
        if (window.innerWidth <= 768 && sidebarVisible) {
            const sidebar = document.querySelector('.css-1d391kg, section[data-testid="stSidebar"]');
            const toggleBtn = document.getElementById('mobile-sidebar-toggle');
            
            if (sidebar && !sidebar.contains(e.target) && e.target !== toggleBtn && !toggleBtn.contains(e.target)) {
                sidebarVisible = false;
                document.body.classList.remove('sidebar-visible');
                document.body.classList.add('sidebar-hidden');
                toggleBtn.innerHTML = '☰';
                toggleBtn.title = 'Menu';
            }
        }
    });
    
    // Handle window resize
    let resizeTimeout;
    window.addEventListener('resize', function() {
        clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(function() {
            if (window.innerWidth > 768) {
                // Desktop
                document.body.classList.remove('sidebar-hidden', 'sidebar-visible');
                toggleButton.style.display = 'none';
                sidebarVisible = true;
            } else {
                // Mobile
                toggleButton.style.display = 'flex';
                if (!sidebarVisible) {
                    document.body.classList.add('sidebar-hidden');
                    document.body.classList.remove('sidebar-visible');
                    toggleButton.innerHTML = '☰';
                } else {
                    document.body.classList.add('sidebar-visible');
                    document.body.classList.remove('sidebar-hidden');
                    toggleButton.innerHTML = '✕';
                }
            }
        }, 100);
    });
    
    // Ad management functions
    window.closeFloatingAd = function() {
        const ad = document.getElementById('floating-ad');
        if (ad) {
            ad.style.display = 'none';
        }
    };
    
    window.showFloatingAd = function() {
        const ad = document.getElementById('floating-ad');
        if (ad) {
            ad.style.display = 'flex';
        }
    };
});
</script>
""", unsafe_allow_html=True)

# Initialize session state
if "chats" not in st.session_state:
    st.session_state["chats"] = {}
if "active_chat" not in st.session_state:
    st.session_state["active_chat"] = None
if "selected_providers" not in st.session_state:
    st.session_state["selected_providers"] = ["Gemini", "Cohere"]
if "pending_question" not in st.session_state:
    st.session_state["pending_question"] = None
if "awaiting_response" not in st.session_state:
    st.session_state["awaiting_response"] = False
if "show_intro" not in st.session_state:
    st.session_state["show_intro"] = True
if "confirm_clear_all" not in st.session_state:
    st.session_state["confirm_clear_all"] = False
if "chat_to_delete" not in st.session_state:
    st.session_state["chat_to_delete"] = None

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Settings")
    
    providers_list = ["OpenAI", "Claude", "Gemini", "Cohere", "Perplexity"]
    st.session_state["selected_providers"] = st.multiselect(
        "Select AI Providers",
        providers_list,
        default=st.session_state["selected_providers"],
        help="Choose which AI providers to query. More providers = more comprehensive answers!"
    )
    
    st.markdown("---")
    
    if st.button("➕ New Chat", use_container_width=True):
        new_id = len(st.session_state["chats"]) + 1
        st.session_state["chats"][new_id] = {"title": "New Chat", "messages": []}
        st.session_state["active_chat"] = new_id
        st.session_state["pending_question"] = None
        st.session_state["awaiting_response"] = False
        st.session_state["show_intro"] = True
        st.rerun()
    
    st.subheader("💬 Chat History")
    
    # Display chat history with delete buttons
    if st.session_state["chats"]:
        for cid, chat in st.session_state["chats"].items():
            chat_title = chat["title"]
            if len(chat_title) > 25:  # Truncate long titles for mobile
                display_title = chat_title[:25] + "..."
            else:
                display_title = chat_title
            
            # Create columns for chat button and delete button
            col1, col2 = st.columns([4, 1])
            
            with col1:
                if st.button(
                    display_title, 
                    key=f"chat_{cid}",
                    use_container_width=True,
                    type="secondary" if st.session_state["active_chat"] != cid else "primary",
                    help=chat_title if len(chat_title) > 25 else None
                ):
                    st.session_state["active_chat"] = cid
                    st.session_state["pending_question"] = None
                    st.session_state["awaiting_response"] = False
                    st.session_state["show_intro"] = False
                    st.session_state["chat_to_delete"] = None  # Clear any pending deletion
                    st.rerun()
            
            with col2:
                if st.button("🗑️", key=f"delete_{cid}", help=f"Delete chat: {display_title}"):
                    st.session_state["chat_to_delete"] = cid
                    st.rerun()
        
        # Handle individual chat deletion confirmation
        if st.session_state["chat_to_delete"]:
            chat_to_delete = st.session_state["chat_to_delete"]
            if chat_to_delete in st.session_state["chats"]:
                chat_title = st.session_state["chats"][chat_to_delete]["title"]
                st.warning(f"⚠️ Delete chat: '{chat_title[:30]}...'?" if len(chat_title) > 30 else f"⚠️ Delete chat: '{chat_title}'?")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("✅ Yes, Delete", use_container_width=True, type="primary"):
                        # Delete the specific chat
                        del st.session_state["chats"][chat_to_delete]
                        # If this was the active chat, clear it
                        if st.session_state["active_chat"] == chat_to_delete:
                            st.session_state["active_chat"] = None
                            st.session_state["show_intro"] = True
                        st.session_state["chat_to_delete"] = None
                        st.session_state["pending_question"] = None
                        st.session_state["awaiting_response"] = False
                        st.rerun()
                
                with col2:
                    if st.button("❌ Cancel", use_container_width=True, type="secondary"):
                        st.session_state["chat_to_delete"] = None
                        st.rerun()
    else:
        st.info("No chats yet. Create your first chat!")
    
    st.markdown("---")
    
    # Clear all chats functionality
    if st.session_state["chats"]:
        if not st.session_state["confirm_clear_all"]:
            if st.button("🗑️ Clear All Chats", use_container_width=True, type="secondary"):
                st.session_state["confirm_clear_all"] = True
                st.rerun()
        else:
            st.warning("⚠️ This will delete ALL chats permanently!")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ Yes, Clear All", use_container_width=True, type="primary"):
                    st.session_state["chats"] = {}
                    st.session_state["active_chat"] = None
                    st.session_state["pending_question"] = None
                    st.session_state["awaiting_response"] = False
                    st.session_state["show_intro"] = True
                    st.session_state["confirm_clear_all"] = False
                    st.session_state["chat_to_delete"] = None
                    st.success("✅ All chats cleared!")
                    time.sleep(1)  # Brief pause to show success message
                    st.rerun()
            
            with col2:
                if st.button("❌ Cancel", use_container_width=True, type="secondary"):
                    st.session_state["confirm_clear_all"] = False
                    st.rerun()
    else:
        st.info("No chats to clear")
    
    # Donation section with responsive design - moved to sidebar bottom
    st.markdown("---")
    
    # SIDEBAR AD PLACEMENT (Subtle)
    st.markdown("""
    <div class="ad-sidebar">
        <small style="color: #777;">Ad</small>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 💝 Support Us")
    st.markdown("""
    <div style="text-align:center; margin-top:10px;">
        <a href="https://www.paypal.com/donate?business=multiaisummarizer@gmail.com&currency_code=USD"
           target="_blank"
           style="text-decoration:none; color:#fff; background-color:#ff6600;
                  padding:6px 12px; border-radius:6px; font-weight:bold; 
                  display:inline-block; font-size:12px;">
            ❤️ Support Us
        </a>
    </div>
    <p style="font-size:10px; text-align:center; margin-top:6px; color:gray;">
        Free project using free models.<br>
        Donate to enable premium AI!
    </p>
    """, unsafe_allow_html=True)

# Main content area
st.title("🤖 Multi AI Summarizer")
st.markdown("*Compare and combine responses from multiple AI providers for comprehensive insights*")

# TOP BANNER AD PLACEMENT (Subtle)
st.markdown("""
<div class="ad-banner">
    <small style="color: #bbb;">Advertisement space</small>
</div>
""", unsafe_allow_html=True)

def infer_title(messages):
    for msg in messages:
        if msg["role"] == "user" and msg["content"].strip():
            title = msg["content"][:50] + "..." if len(msg["content"]) > 50 else msg["content"]
            return title
    return "New Chat"

# Educational content for new users
if st.session_state["active_chat"] is None or (st.session_state["show_intro"] and not st.session_state["chats"].get(st.session_state["active_chat"], {}).get("messages")):
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 🎯 How It Works")
        st.markdown("""
        1. **Select Providers** - Choose AI models from sidebar
        2. **Ask Questions** - Type your question below
        3. **Get Smart Summary** - AI combines all responses
        4. **Compare Details** - View individual responses
        """)
        
        if not st.session_state["selected_providers"]:
            st.warning("⚠️ Select AI providers from sidebar to start")
        else:
            st.success(f"✅ Ready! Using: {', '.join(st.session_state['selected_providers'])}")
    
    with col2:
        st.markdown("### 💡 Quick Tips")
        st.info("**More providers = better insights**\nDifferent AIs excel at different tasks")
        st.success("**Perfect for:** Research, creative writing, technical questions, decision making")
    
    if st.session_state["active_chat"] is None:
        st.info("👆 Click the '☰' button on mobile or 'New Chat' to get started!")

# AD BETWEEN INTRO AND CHAT (Subtle)
if st.session_state["active_chat"] is None or (st.session_state["show_intro"] and not st.session_state["chats"].get(st.session_state["active_chat"], {}).get("messages")):
    st.markdown("""
    <div class="ad-between-chats">
        <small>Sponsored content</small>
    </div>
    """, unsafe_allow_html=True)

# Chat interface
if st.session_state["active_chat"] is not None:
    chat = st.session_state["chats"][st.session_state["active_chat"]]
    chat["title"] = infer_title(chat["messages"])
    
    # Chat messages display
    chat_container = st.container()
    
    with chat_container:
        for idx, msg in enumerate(chat["messages"]):
            if msg["role"] == "user":
                st.markdown(f"""
                <div class="user-message">
                    <strong>🙋 You:</strong> {msg['content']}
                </div>
                """, unsafe_allow_html=True)
                
                # Handle pending response
                if (st.session_state["awaiting_response"] and 
                    st.session_state["pending_question"] == msg["content"] and 
                    idx == len(chat["messages"]) - 1):
                    
                    with st.spinner(f"🔍 Querying {len(st.session_state['selected_providers'])} AI providers..."):
                        history = chat["messages"][:-1] if len(chat["messages"]) > 1 else []
                        
                        try:
                            start_time = time.time()
                            response = requests.post(
                                f"{API_URL}/ask",
                                json={
                                    "query": msg["content"],
                                    "providers": st.session_state["selected_providers"],
                                    "history": history
                                },
                                timeout=60
                            )
                            response_time = round(time.time() - start_time, 1)
                            
                            if response.status_code == 200:
                                data = response.json()
                                chat["messages"].append({
                                    "role": "assistant",
                                    "content": data["summary"],
                                    "providers": data["responses"],
                                    "response_time": response_time
                                })
                                st.success("✅ Response received!")
                            else:
                                error_msg = f"⚠️ Backend error: {response.status_code}"
                                chat["messages"].append({
                                    "role": "assistant", 
                                    "content": error_msg, 
                                    "providers": {}
                                })
                                
                        except requests.exceptions.Timeout:
                            error_msg = "⚠️ Request timed out. Please try again."
                            chat["messages"].append({
                                "role": "assistant", 
                                "content": error_msg, 
                                "providers": {}
                            })
                        except Exception as e:
                            error_msg = f"⚠️ Connection error: Please check if the backend is running."
                            chat["messages"].append({
                                "role": "assistant", 
                                "content": error_msg, 
                                "providers": {}
                            })
                        
                        st.session_state["pending_question"] = None
                        st.session_state["awaiting_response"] = False
                        st.rerun()
            
            elif msg["role"] == "assistant":
                # AI response header
                response_time_info = f" • {msg.get('response_time', 'N/A')}s" if msg.get('response_time') else ""
                st.markdown(f"""
                <div class="ai-summary">
                    <strong>🤖 AI Summary</strong>{response_time_info}
                </div>
                """, unsafe_allow_html=True)
                
                # AI response content
                st.markdown(f"""
                <div class="ai-content">
                    {msg['content']}
                </div>
                """, unsafe_allow_html=True)
                
                # Provider details
                providers_data = msg.get("providers", {})
                if providers_data:
                    with st.expander("🔍 **Provider Details** - Compare individual responses", expanded=False):
                        successful_providers = []
                        failed_providers = []
                        
                        for provider, response in providers_data.items():
                            if response.startswith("⚠️"):
                                failed_providers.append((provider, response))
                            else:
                                successful_providers.append((provider, response))
                        
                        # Successful responses
                        if successful_providers:
                            st.markdown("#### ✅ **Successful Responses:**")
                            for provider, response in successful_providers:
                                st.markdown(f"**🔹 {provider}:**")
                                st.success(response)
                        
                        # Failed responses
                        if failed_providers:
                            st.markdown("#### ❌ **Failed Responses:**")
                            for provider, response in failed_providers:
                                st.error(f"**{provider}:** {response}")
                        
                        # Summary statistics
                        total = len(providers_data)
                        successful = len(successful_providers)
                        st.info(f"📊 **Response Summary:** {successful}/{total} providers successful")

# Chat input - always at bottom
if st.session_state["active_chat"] is not None:
    # Input validation and UX
    input_disabled = (not st.session_state["selected_providers"] or 
                     st.session_state["awaiting_response"])
    
    placeholder_text = ("Ask your question..." if st.session_state["selected_providers"] 
                       else "Select AI providers first")
    
    user_input = st.chat_input(
        placeholder_text,
        disabled=input_disabled
    )
    
    # Handle new user input
    if user_input and not st.session_state["awaiting_response"] and st.session_state["selected_providers"]:
        st.session_state["pending_question"] = user_input
        st.session_state["awaiting_response"] = True
        st.session_state["show_intro"] = False
        
        chat["messages"].append({"role": "user", "content": user_input})
        if len(chat["messages"]) == 1:
            chat["title"] = infer_title(chat["messages"])
        
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
    <button class="ad-close" onclick="closeFloatingAd()">×</button>
    <div>
        <small style="color: #888;">Premium features coming soon</small>
    </div>
</div>

<script>
setTimeout(function() {
    if (typeof showFloatingAd === 'function') {
        showFloatingAd();
    }
}, 15000); // Show after 15 seconds
</script>
""", unsafe_allow_html=True)