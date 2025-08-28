import streamlit as st
import requests
import os
import time

API_URL = os.getenv("SUMMARIZER_API_URL", "http://127.0.0.1:8000")

st.set_page_config(
    page_title="Multi AI Summarizer", 
    layout="wide",
    initial_sidebar_state="auto",
    menu_items={
        'About': "Multi AI Summarizer - Compare responses from multiple AI providers and get intelligent unified summaries!"
    }
)

# Add Google AdSense script to head
st.markdown("""
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-1587919634342405"
      crossorigin="anonymous"></script>
""", unsafe_allow_html=True)

# Simplified mobile-first CSS approach with a new section for the floating ad
st.markdown("""
<style>
    /* Mobile-first approach - simpler and more reliable */
    
    /* Basic responsive adjustments */
    @media (max-width: 768px) {
        /* Ensure scrolling works */
        html, body {
            overflow-x: hidden !important;
            overflow-y: auto !important;
            height: auto !important;
        }
        
        /* Main content padding for mobile */
        .main .block-container {
            padding: 1rem 0.5rem !important;
            max-width: 100% !important;
        }
        
        /* Better mobile typography */
        .main h1 {
            font-size: 2rem !important;
            line-height: 1.2 !important;
            margin-bottom: 0.5rem !important;
        }
        
        /* Chat input improvements */
        .stChatInput {
            position: sticky !important;
            bottom: 0 !important;
            background: var(--background-color) !important;
            padding: 1rem 0.5rem !important;
            border-top: 2px solid #4CAF50 !important;
            z-index: 100 !important;
        }
        
        .stChatInput > div {
            border: 2px solid #4CAF50 !important;
            border-radius: 15px !important;
            background: white !important;
        }
        
        .stChatInput input {
            font-size: 16px !important;
            padding: 12px 16px !important;
        }
        
        /* Sidebar improvements for mobile - use Streamlit's native behavior */
        section[data-testid="stSidebar"] {
            background-color: #1a1a1a !important;
        }
        
        section[data-testid="stSidebar"] * {
            color: #ffffff !important;
        }
        
        section[data-testid="stSidebar"] .stButton button {
            background-color: #333 !important;
            color: #fff !important;
            border: 1px solid #555 !important;
            border-radius: 5px !important;
            width: 100% !important;
        }
        
        section[data-testid="stSidebar"] .stButton button[kind="primary"] {
            background-color: #ff6b6b !important;
            border-color: #ff6b6b !important;
        }
        
        section[data-testid="stSidebar"] .stMultiSelect > div {
            background-color: #333 !important;
            border: 1px solid #555 !important;
        }
        
        section[data-testid="stSidebar"] .stMultiSelect [data-baseweb="tag"] {
            background-color: #ff6b6b !important;
            color: white !important;
        }
        
        /* Card layouts for better mobile UX */
        .mobile-card {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 1rem;
            margin: 1rem 0;
            border: 1px solid #e9ecef;
        }
        
        .mobile-card h3 {
            color: #1976d2 !important;
            margin-bottom: 0.5rem !important;
        }
        
        .mobile-card p, .mobile-card li {
            color: #333 !important;
            line-height: 1.5 !important;
        }
    }
    
    /* Desktop styles */
    @media (min-width: 769px) {
        .stChatInput > div {
            border: 3px solid #4CAF50 !important;
            border-radius: 25px !important;
            background: linear-gradient(135deg, #1e3a1e, #2d5a2d) !important;
            box-shadow: 0 5px 15px rgba(76, 175, 80, 0.3) !important;
            position: relative;
        }
        
        .stChatInput > div::before {
            content: "💬 Type your question here - AI is ready to help!";
            position: absolute;
            top: -30px;
            left: 15px;
            font-size: 13px;
            color: #4CAF50;
            font-weight: 600;
            background: var(--background-color);
            padding: 2px 8px;
            border-radius: 10px;
            border: 1px solid #4CAF50;
        }
    }
    
    /* Message styling - works on all devices */
    .user-message {
        background: linear-gradient(90deg, #e3f2fd, #bbdefb);
        border-left: 4px solid #2196f3;
        border-radius: 8px;
        padding: 12px;
        margin: 8px 0;
        color: #0d47a1;
        font-weight: 500;
    }
    
    .ai-summary {
        background: linear-gradient(90deg, #e8f5e8, #c8e6c9);
        border-left: 4px solid #4caf50;
        border-radius: 8px;
        padding: 12px;
        margin: 8px 0;
        color: #1b5e20;
        font-weight: 500;
    }
    
    .ai-content {
        background: #f1f8e9;
        border-radius: 6px;
        padding: 12px;
        margin: 8px 0 12px 0;
        color: #33691e;
        line-height: 1.6;
    }
    
    /* Ad placements - subtle and responsive */
    .ad-banner {
        background: #f8f9fa;
        border: 1px solid #e9ecef;
        border-radius: 8px;
        padding: 15px;
        margin: 20px auto;
        text-align: center;
        max-width: 728px;
        color: #888;
        font-size: 12px;
        min-height: 60px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .ad-sidebar {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 6px;
        padding: 10px;
        margin: 15px 0;
        text-align: center;
        color: #888;
        font-size: 11px;
        min-height: 80px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .footer-section {
        text-align: center;
        padding: 15px;
        background: rgba(255, 255, 255, 0.02);
        border-radius: 8px;
        margin: 20px auto;
        max-width: 400px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .footer-section h4 {
        color: #888 !important;
        font-size: 14px !important;
        margin-bottom: 8px !important;
    }
    
    .footer-section p {
        color: #999 !important;
        font-size: 12px !important;
    }
    
    .footer-section a {
        color: #aaa !important;
        text-decoration: none !important;
        background: rgba(255, 255, 255, 0.05) !important;
        padding: 4px 10px !important;
        border-radius: 8px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        font-size: 12px !important;
        transition: all 0.2s ease;
    }
    
    .footer-section a:hover {
        background: rgba(255, 255, 255, 0.1) !important;
    }
    
    /* Status indicators */
    .status-success {
        background: #d4edda;
        color: #155724;
        border: 1px solid #c3e6cb;
        padding: 6px 12px;
        border-radius: 15px;
        font-size: 12px;
        font-weight: 500;
        display: inline-block;
        margin: 4px;
    }
    
    .status-error {
        background: #f8d7da;
        color: #721c24;
        border: 1px solid #f5c6cb;
        padding: 6px 12px;
        border-radius: 15px;
        font-size: 12px;
        font-weight: 500;
        display: inline-block;
        margin: 4px;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Mobile responsiveness for columns */
    @media (max-width: 768px) {
        .row-widget.stHorizontal {
            flex-direction: column !important;
        }
        
        .row-widget.stHorizontal > div {
            width: 100% !important;
            margin-bottom: 1rem !important;
        }
    }
    
    /* Floating Ad */
    .ad-floating {
        position: fixed;
        bottom: 20px;
        left: 20px;
        background: #ff6600;
        color: white;
        padding: 12px 18px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        z-index: 1000;
        animation: fadeIn 0.5s ease-out;
        display: flex;
        align-items: center;
        gap: 10px;
        cursor: pointer;
        font-size: 14px;
        font-weight: 600;
    }
    
    .ad-floating:hover {
        background: #e65c00;
    }

    .ad-floating .arrow {
        font-size: 24px;
        animation: bounce 1s infinite;
        transform: rotate(25deg);
        line-height: 1;
    }
    
    .ad-floating .ad-close {
        position: absolute;
        top: -10px;
        right: -10px;
        background: #ff6600;
        color: white;
        border: none;
        border-radius: 50%;
        width: 25px;
        height: 25px;
        font-size: 16px;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes bounce {
        0%, 100% { transform: translateY(0) rotate(25deg); }
        50% { transform: translateY(-5px) rotate(25deg); }
    }
</style>
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
# New session state variables for the floating ad
if "floating_ad_shown" not in st.session_state:
    st.session_state["floating_ad_shown"] = False

# Sidebar configuration - using Streamlit's native mobile behavior
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
            if len(chat_title) > 25:
                display_title = chat_title[:25] + "..."
            else:
                display_title = chat_title
            
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
                    st.session_state["chat_to_delete"] = None
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
                        del st.session_state["chats"][chat_to_delete]
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
                    time.sleep(1)
                    st.rerun()
            
            with col2:
                if st.button("❌ Cancel", use_container_width=True, type="secondary"):
                    st.session_state["confirm_clear_all"] = False
                    st.rerun()
    else:
        st.info("No chats to clear")
    
    st.markdown("---")
    
    # SIDEBAR AD PLACEMENT
    st.markdown("""
    <div class="ad-sidebar">
        <small>Advertisement</small>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 💝 Support Us")
    st.markdown("""
    <div style="text-align:center; margin-top:10px;">
        <a href="https://paypal.me/multiaisummarizer"
            target="_blank"
            style="text-decoration:none; color:#fff; background-color:#ff6600;
                   padding:8px 12px; border-radius:6px; font-weight:bold; 
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

# TOP BANNER AD PLACEMENT
st.markdown("""
<div class="ad-banner">
    Advertisement space
</div>
""", unsafe_allow_html=True)

def infer_title(messages):
    for msg in messages:
        if msg["role"] == "user" and msg["content"].strip():
            title = msg["content"][:50] + "..." if len(msg["content"]) > 50 else msg["content"]
            return title
    return "New Chat"

# Educational content for new users - mobile-friendly cards
if st.session_state["active_chat"] is None or (st.session_state["show_intro"] and not st.session_state["chats"].get(st.session_state["active_chat"], {}).get("messages")):
    
    # Use mobile-friendly single column layout
    st.markdown("""
    <div class="mobile-card">
        <h3>🎯 How It Works</h3>
        <ol>
            <li><strong>Select Providers</strong> - Choose AI models from sidebar</li>
            <li><strong>Ask Questions</strong> - Type your question below</li>
            <li><strong>Get Smart Summary</strong> - AI combines all responses</li>
            <li><strong>Compare Details</strong> - View individual responses</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state["selected_providers"]:
        st.warning("⚠️ Select AI providers from sidebar to start")
    else:
        st.success(f"✅ Ready! Using: {', '.join(st.session_state['selected_providers'])}")
    
    st.markdown("""
    <div class="mobile-card">
        <h3>💡 Quick Tips</h3>
        <p><strong>More providers = better insights</strong><br>
        Different AIs excel at different tasks</p>
        <p><strong>Perfect for:</strong> Research, creative writing, technical questions, decision making</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state["active_chat"] is None:
        st.info("👈 Click 'New Chat' to get started! Mobile users: Open the left sidebar if visible (else, hold the phone in landscape mode)")

# Chat interface
if st.session_state["active_chat"] is not None:
    chat = st.session_state["chats"][st.session_state["active_chat"]]
    chat["title"] = infer_title(chat["messages"])
    
    # Chat messages display
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
    # Input validation
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

# Logic to show the floating ad after a few messages
if st.session_state["active_chat"] is not None:
    if len(st.session_state["chats"][st.session_state["active_chat"]]["messages"]) >= 2 and not st.session_state["floating_ad_shown"]:
        st.markdown("""
        <div id="floating-ad" class="ad-floating">
            <span class="arrow">➡️</span>
            <span>Enjoying this? Support us!</span>
        </div>
        <script>
            // Simple JS to hide the ad on click
            const ad = document.getElementById('floating-ad');
            if (ad) {
                ad.onclick = function() {
                    // Navigate to the sidebar link
                    const sidebarLink = window.parent.document.querySelector('.sidebar a[href*="paypal"]');
                    if (sidebarLink) {
                        sidebarLink.click();
                    }
                    ad.style.display = 'none';
                    // Inform streamlit that the ad has been clicked/closed
                    // This is for demonstration, actual state management needs backend
                    // and would be more complex
                };
            }
        </script>
        """, unsafe_allow_html=True)
        # Set session state to true so it only shows once per session
        st.session_state["floating_ad_shown"] = True

# Footer
st.markdown("---")

# FOOTER BANNER AD
st.markdown("""
<div class="ad-banner">
    Advertisement
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
