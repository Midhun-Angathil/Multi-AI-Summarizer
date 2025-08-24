import streamlit as st
import requests
import os

API_URL = os.getenv("SUMMARIZER_API_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="Multi AI Summarizer", layout="wide")
st.title("🤖 Multi AI Summarizer")

st.info(
    "Currently, we are using **free models based on availability**. "
    "Paid models will be enabled in future updates. "
    "You can help support development via donations below."
)

paypal_link = "https://www.paypal.com/donate?hosted_button_id=YOUR_BUTTON_ID"
st.markdown(f"[💖 Donate to support this project]({paypal_link})")

with st.sidebar:
    st.header("Settings")
    providers = st.multiselect(
        "Select Providers",
        ["openai", "claude", "gemini", "cohere", "perplexity"],
        default=["cohere", "gemini"]
    )

question = st.text_area("Enter your question:")

if st.button("Run Query"):
    if not question.strip():
        st.warning("Please enter a question first.")
    else:
        with st.spinner("Calling providers..."):
            try:
                r = requests.post(f"{API_URL}/ask", json={"query": question, "providers": providers})
                if r.status_code == 200:
                    data = r.json()
                    st.subheader("📝 Unified Summary (Aggregated across all providers)")
                    st.write(data["summary"])
                    st.caption(f"Responses aggregated from: {', '.join(data['sources'])}")

                    with st.expander("📜 View Individual Provider Responses"):
                        for provider, response in data["responses"].items():
                            if "⚠️" in response:
                                st.warning(f"**{provider}:** {response}")
                            elif response.lower().startswith("["):
                                st.error(f"**{provider}:** {response}")
                            else:
                                st.markdown(f"**{provider}:**\n\n{response}")
                else:
                    st.error(f"⚠️ Error communicating with backend (status {r.status_code})")
            except Exception as e:
                st.error(f"⚠️ Frontend error: {str(e)}")
