import os
import streamlit as st
from groq import Groq

# -----------------------------------------------------------------------------
# 1. Page Configuration
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="PersonaPulse | Dynamic AI Assistant",
    page_icon="🤖",
    layout="centered",  # Native Streamlit centering
    initial_sidebar_state="expanded",
)

# -----------------------------------------------------------------------------
# 2. Persona Definitions & 3-Color Palettes
# -----------------------------------------------------------------------------
PERSONAS = {
    "Travel Guide": {
        "icon": "✈️",
        "tagline": "Destinations, trip planning, local cultures, and travel advice.",
        "palette": {
            "primary": "#00A896",      # Tropical Teal (Primary Accent)
            "badge_bg": "#122A2F",     # Deep Slate Cyan (Card/Badge Background)
            "text_light": "#A5F3FC",   # Soft Ice Blue (Secondary Highlight)
        },
        "system_prompt": (
            "You are an expert, passionate Travel Guide. You strictly answer questions about "
            "travel destinations, itineraries, sightseeing, local cultures, flights, and packing tips. "
            "If the user asks about ANYTHING unrelated to travel, politely decline by stating: "
            "'I am your Travel Guide and can only assist with travel-related queries.'"
        ),
    },
    "Tech Support": {
        "icon": "💻",
        "tagline": "Devices, software troubleshooting, hardware, and networking.",
        "palette": {
            "primary": "#A855F7",      # Electric Purple (Primary Accent)
            "badge_bg": "#221533",     # Midnight Violet (Card/Badge Background)
            "text_light": "#F472B6",   # Neon Pink (Secondary Highlight)
        },
        "system_prompt": (
            "You are a patient Tech Support Specialist. You strictly answer queries regarding "
            "computers, software troubleshooting, hardware, mobile operating systems, and networking. "
            "If the user asks about ANYTHING unrelated to tech support, politely decline by stating: "
            "'I am your Tech Support Specialist and can only assist with technical queries.'"
        ),
    },
}

# -----------------------------------------------------------------------------
# 3. Sidebar Controls & Credentials
# -----------------------------------------------------------------------------
st.sidebar.header("⚙️ Chat Settings")

# Safe secret loading
try:
    groq_api_key = st.secrets.get("GROQ_API_KEY", "")
except Exception:
    groq_api_key = ""

if not groq_api_key:
    groq_api_key = st.sidebar.text_input(
        "Enter Groq API Key:",
        type="password",
        help="Get your key at https://console.groq.com",
    )

if not groq_api_key:
    st.info("👈 Please enter your Groq API Key in the sidebar to start chatting.")
    st.stop()

# Initialize Groq Client
client = Groq(api_key=groq_api_key)

selected_model = st.sidebar.selectbox(
    "Choose AI Model:",
    options=["llama-3.3-70b-versatile", "llama-3.1-8b-instant"],
    index=0,
)

selected_persona = st.sidebar.selectbox(
    "Choose Persona:",
    options=list(PERSONAS.keys()),
    index=0,
)

# Active role details and color palette
active_role = PERSONAS[selected_persona]
colors = active_role["palette"]

# -----------------------------------------------------------------------------
# 4. Custom Dynamic Theme & Centered Styling
# -----------------------------------------------------------------------------
custom_css = f"""
<style>
    /* Center title & header components */
    .title-container {{
        text-align: center;
        margin-bottom: 25px;
    }}
    
    .persona-accent {{
        color: {colors['primary']} !important;
        font-weight: 700;
    }}
    
    .persona-subaccent {{
        color: {colors['text_light']} !important;
    }}

    /* Sidebar themed card */
    .persona-badge {{
        background-color: {colors['badge_bg']};
        border-left: 4px solid {colors['primary']};
        padding: 14px 18px;
        border-radius: 8px;
        margin-top: 10px;
        margin-bottom: 20px;
    }}

    /* Center user messages accent border */
    .stChatMessage.user {{
        border-left: 3px solid {colors['primary']};
    }}
    
    /* Assistant response focus highlight */
    .stChatMessage.assistant {{
        border-left: 3px solid {colors['text_light']};
    }}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Styled Sidebar Info Badge
st.sidebar.markdown(
    f"""
    <div class="persona-badge">
        <strong style="color: {colors['primary']}; font-size: 1.05rem;">
            {active_role['icon']} {selected_persona} Mode
        </strong>
        <p style="margin-top: 6px; margin-bottom: 0px; font-size: 0.88rem; color: {colors['text_light']}; opacity: 0.9;">
            {active_role['tagline']}
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Clear History Button
if st.sidebar.button("🧹 Clear Chat", use_container_width=True):
    st.session_state.messages = []
    st.rerun()

# -----------------------------------------------------------------------------
# 5. Centered UI Header
# -----------------------------------------------------------------------------
st.markdown(
    f"""
    <div class="title-container">
        <h1 style="margin-bottom: 0px;">🤖 PersonaPulse</h1>
        <p style="font-size: 1.15rem; margin-top: 5px;">
            Active Assistant: <span class="persona-accent">{active_role['icon']} {selected_persona}</span>
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# 6. Memory & State Management
# -----------------------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "active_persona" not in st.session_state or st.session_state.active_persona != selected_persona:
    st.session_state.messages = []
    st.session_state.active_persona = selected_persona

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -----------------------------------------------------------------------------
# 7. User Input & Streaming API Call
# -----------------------------------------------------------------------------
if user_input := st.chat_input(f"Ask your {selected_persona}..."):
    
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    api_messages = [
        {"role": "system", "content": active_role["system_prompt"]}
    ] + [
        {"role": m["role"], "content": m["content"]}
        for m in st.session_state.messages
    ]

    with st.chat_message("assistant"):
        response_box = st.empty()
        full_text = ""

        try:
            stream = client.chat.completions.create(
                model=selected_model,
                messages=api_messages,
                temperature=0.2,
                stream=True,
            )

            for chunk in stream:
                token = chunk.choices[0].delta.content
                if token:
                    full_text += token
                    response_box.markdown(full_text + "▌")

            response_box.markdown(full_text)

        except Exception as err:
            st.error(f"Error contacting Groq API: {err}")
            full_text = "I encountered an error processing your request."

    st.session_state.messages.append({"role": "assistant", "content": full_text})