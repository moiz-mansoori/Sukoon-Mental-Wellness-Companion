"""
A compassionate AI chatbot designed to provide emotional support
for people dealing with depression, anxiety, and overthinking.

"""

import streamlit as st
from groq import Groq
from typing import Optional
import os

# Import local modules
from config.settings import (
    MOOD_OPTIONS, 
    SAFETY_DISCLAIMER, 
    THEME_COLORS,
    QUICK_ACTIONS,
    GROQ_API_KEY,
    GROQ_MODEL,
    MAX_TOKENS,
    TEMPERATURE
)
from prompts.templates import (
    SYSTEM_PROMPT,
    MOOD_PROMPTS,
    CONVERSATION_STARTERS,
    CRISIS_RESPONSE
)
from utils import (
    analyze_sentiment,
    get_empathy_level,
    format_sentiment_for_prompt,
    detect_crisis,
    get_crisis_response,
    format_crisis_for_prompt,
    detect_language,
    format_language_context,
    get_breathing_exercise,
    format_breathing_exercise,
    get_grounding_exercise,
    format_grounding_exercise,
    get_cbt_technique,
    format_cbt_technique,
    get_journal_prompt,
    format_journal_prompt,
    get_affirmation,
    get_meditation,
    format_meditation
)

# RAG Imports
from rag import (
    EmbeddingService,
    VectorStore,
    WellnessRetriever,
    index_knowledge_base
)

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Sukoon - Mental Wellness Companion",
    page_icon="🧘",
    layout="wide",
    initial_sidebar_state="expanded"
)

# GROQ API CONFIGURATION
def get_groq_client() -> Optional[Groq]:
    """Get Groq client instance."""
    if GROQ_API_KEY:
        return Groq(api_key=GROQ_API_KEY)
    return None
 
 # Custom Styling
def apply_custom_css():
    """Apply custom CSS for a calming, readable UI."""
    st.markdown("""
    <style>
        /* Main background - force dark theme everywhere */
        .stApp {
            background: #1e1e2e !important;
        }
        
        .main .block-container {
            background: #1e1e2e !important;
        }
        
        [data-testid="stAppViewBlockContainer"] {
            background: #1e1e2e !important;
        }
        
        /* Header area */
        [data-testid="stHeader"] {
            background: #1e1e2e !important;
        }
        
        header {
            background: #1e1e2e !important;
        }
        
        /* Bottom chat input area */
        [data-testid="stBottom"] {
            background: #1e1e2e !important;
        }
        
        [data-testid="stBottomBlockContainer"] {
            background: #1e1e2e !important;
        }
        
        /* Footer area */
        footer {
            background: #1e1e2e !important;
        }
        
        /* Chat input container */
        [data-testid="stChatInput"] {
            background: #2a2a3e !important;
            border: 1px solid transparent !important; /* Base border for transition */
            border-radius: 25px !important;
            box-shadow: none !important;
            outline: none !important;
            padding: 2px 10px !important;
            margin: 0 !important;
            transition: all 0.3s ease !important;
        }
        
        [data-testid="stChatInput"] > div {
            background: transparent !important;
            border: none !important;
        }
        
        /* Active Focus Indicator */
        [data-testid="stChatInput"]:focus-within {
            border: 1px solid #6366f1 !important;
            box-shadow: 0 0 15px rgba(99, 102, 241, 0.3) !important;
            background: #31314d !important;
        }

        /* The actual textarea - add padding for search icon if needed */
        [data-testid="stChatInputTextArea"] {
            background: transparent !important;
            color: #f0f0f5 !important;
            padding-left: 5px !important;
        }

        /* Adding a subtle search icon on focus using background-image */
        [data-testid="stChatInput"]:focus-within::before {
            content: "🔍";
            position: absolute;
            left: 15px;
            top: 50%;
            transform: translateY(-50%);
            font-size: 14px;
            opacity: 0.7;
            pointer-events: none;
            z-index: 10;
        }
        
        /* Adjust textarea padding when icon appears */
        [data-testid="stChatInput"]:focus-within textarea {
            padding-left: 35px !important;
        }

        textarea {
            background: transparent !important;
            color: #f0f0f5 !important;
            border: none !important;
            outline: none !important;
        }
        
        textarea:focus {
            border: none !important;
            box-shadow: none !important;
            outline: none !important;
        }
        
        textarea::placeholder {
            color: #a0a0b8 !important;
        }
        
        /* Remove any white backgrounds */
        .stApp > div, .main > div {
            background: transparent !important;
        }
        
        /* Sidebar - cleaner, readable */
        [data-testid="stSidebar"] {
            background: #2a2a3e;
        }
        
        /* All text should be bright and readable */
        .stApp, .stApp p, .stApp span, .stApp div {
            color: #f0f0f5 !important;
        }
        
        /* Sidebar text */
        [data-testid="stSidebar"] * {
            color: #e8e8f0 !important;
        }
        
        /* Headers - clear and visible */
        h1, h2, h3 {
            color: #a5b4fc !important;
            font-weight: 600 !important;
            letter-spacing: -0.5px;
        }
        
        h1 {
            font-size: 2.2rem !important;
            margin-bottom: 0.5rem !important;
        }
        
        /* Subheadings in sidebar */
        [data-testid="stSidebar"] h3 {
            color: #c7d2fe !important;
            font-size: 1.1rem !important;
            margin-top: 1rem !important;
        }
        
        /* Info boxes - higher contrast */
        .stAlert {
            background: #3a3a52 !important;
            border: 1px solid #5a5a7a !important;
            border-radius: 12px !important;
        }
        
        .stAlert p {
            color: #f5f5ff !important;
            line-height: 1.7 !important;
        }
        
        /* Chat messages - clear contrast */
        .stChatMessage {
            background: #2d2d42 !important;
            border-radius: 12px;
            padding: 12px;
            margin: 8px 0;
        }
        
        [data-testid="stChatMessageContent"] p {
            color: #f0f0f5 !important;
            line-height: 1.6 !important;
            font-size: 1rem !important;
        }
        
        /* Buttons - visible and clickable */
        .stButton > button {
            background: #6366f1 !important;
            color: white !important;
            border: none !important;
            border-radius: 20px !important;
            padding: 10px 20px !important;
            font-weight: 500 !important;
            transition: all 0.2s ease;
        }
        
        .stButton > button:hover {
            background: #818cf8 !important;
            transform: translateY(-1px);
        }
        
        /* Input box - visible placeholder */
        .stChatInput textarea {
            background: #3a3a52 !important;
            color: #f0f0f5 !important;
            border: 1px solid #5a5a7a !important;
            border-radius: 12px !important;
        }
        
        .stChatInput textarea::placeholder {
            color: #a0a0b8 !important;
        }
        
        /* Dividers */
        hr {
            border-color: #4a4a6a !important;
            margin: 1.5rem 0 !important;
        }
        
        /* Caption text */
        .stCaption, small {
            color: #b0b0c8 !important;
        }
        
        /* Links */
        a {
            color: #93c5fd !important;
        }
        
        /* Footer */
        footer {
            color: #8888a8 !important;
        }
        
        /* Remove default Streamlit footer */
        .stDeployButton {
            display: none !important;
        }
        
        /* Scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: #1e1e2e;
        }
        
        ::-webkit-scrollbar-thumb {
            background: #6366f1;
            border-radius: 4px;
        }

        /* Hide Streamlit default menu, search, and footer */
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
        .stDeployButton {display:none !important;}
    </style>
    """, unsafe_allow_html=True)

# SESSION STATE INITIALIZATION
def init_session_state():
    """Initialize all session state variables."""
    defaults = {
        "messages": [],          # Chat history
        "current_mood": None,    # User's selected mood
        "mood_key": None,        # Mood key for prompts
        "show_disclaimer": True, # Show initial disclaimer
        "crisis_mode": False,    # Whether crisis was detected
        "conversation_started": False,  # Whether conversation has started
        "conversation_history": [],  # Groq conversation history
        "rag_initialized": False,     # Whether RAG vector store is index
        "emotional_context": "",     # Hidden emotional memory
        "conversation_themes": []    # Detected themes for continuity
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

# LLM RESPONSE GENERATION (GROQ)
def generate_response(user_message: str, mood_context: str = "") -> str:
    """
    Generate an empathetic response using Groq API.
    
    Args:
        user_message: The user's input message
        mood_context: Additional context based on user's mood
        
    Returns:
        AI-generated response string
    """
    # Analyze sentiment
    sentiment = analyze_sentiment(user_message)
    sentiment_context = format_sentiment_for_prompt(sentiment)
    
    # Check for crisis indicators
    crisis = detect_crisis(user_message)
    
    if crisis["is_crisis"]:
        st.session_state.crisis_mode = True
        # Return pre-defined crisis response
        return get_crisis_response(crisis["severity"])
    
    # Build context for the message
    context_parts = []
    
    # 0. Language Detection - Respond in user's language
    language_context = format_language_context(user_message)
    if language_context:
        context_parts.append(language_context)
    
    # 1. RAG Retrieval - Treat as lived wisdom
    try:
        if "retriever" in st.session_state:
            results = st.session_state.retriever.retrieve(user_message)
            rag_context = st.session_state.retriever.format_context_for_prompt(results)
            if rag_context:
                context_parts.append(f"[LIVED WISDOM & INSIGHTS]\n{rag_context}")
    except Exception as e:
        # Silent fail for RAG to maintain conversation flow
        pass
    
    if mood_context:
        context_parts.append(f"[EMOTIONAL TONE GUIDE]\n{mood_context}")
    
    context_parts.append(sentiment_context)
    
    # 3. Hidden Memory
    if st.session_state.emotional_context:
        context_parts.append(f"[HIDDEN MEMORY]\n{st.session_state.emotional_context}")
    
    # Combine context with user message
    enhanced_message = "\n\n".join(context_parts) + f"\n\n[USER MESSAGE]: {user_message}"
    
    try:
        client = get_groq_client()
        if not client:
            return "⚠️ **API Key Required**: Please add your Groq API key to the `.env` file. You can get a free key at [Groq Console](https://console.groq.com). 💙"
        
        # Build messages with system prompt and conversation history
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        
        # Add conversation history for context
        for msg in st.session_state.conversation_history[-10:]:  # Keep last 10 messages for therapist-like continuity
            messages.append(msg)
        
        # Add current user message
        messages.append({"role": "user", "content": enhanced_message})
        
        # Generate response with Groq (ultra-fast inference)
        chat_completion = client.chat.completions.create(
            messages=messages,
            model=GROQ_MODEL,
            max_tokens=MAX_TOKENS,
            temperature=TEMPERATURE,
        )
        
        response_text = chat_completion.choices[0].message.content
        
        # Update hidden context and themes
        if sentiment["emotional_intensity"] in ["moderate", "severe"]:
            st.session_state.emotional_context = f"The user has been feeling {sentiment['emotional_intensity']} {', '.join(sentiment['detected_emotions'][:2])}."
        
        for emotion in sentiment["detected_emotions"]:
            if emotion not in st.session_state.conversation_themes:
                st.session_state.conversation_themes.append(emotion)
        
        # Update conversation history
        st.session_state.conversation_history.append({"role": "user", "content": user_message})
        st.session_state.conversation_history.append({"role": "assistant", "content": response_text})
        
        return response_text
        
    except Exception as e:
        error_msg = str(e)
        if "API_KEY" in error_msg.upper() or "authentication" in error_msg.lower():
            return "⚠️ **API Key Required**: Please add your Groq API key to the `.env` file. You can get a free key at [Groq Console](https://console.groq.com). 💙"
        return f"I'm having trouble connecting right now, but I'm still here with you. 💙 Please try again in a moment. (Error: {error_msg[:100]})"

# SIDEBAR COMPONENTS
def render_sidebar():
    """Render the sidebar with mood selection and options."""
    with st.sidebar:
        st.markdown("## 🕊️ Sukoon")
        st.markdown("*Your Mental Wellness Companion*")
        st.divider()
        
        # Mood Selection
        st.markdown("### How are you feeling?")
        st.markdown("*Select your current mood*")
        
        selected_mood = None
        for mood_label, mood_data in MOOD_OPTIONS.items():
            if st.button(
                mood_label, 
                key=f"mood_{mood_data['key']}",
                use_container_width=True,
                type="secondary" if st.session_state.current_mood != mood_label else "primary"
            ):
                st.session_state.current_mood = mood_label
                st.session_state.mood_key = mood_data["key"]
                # Add starter message if conversation hasn't started
                if not st.session_state.conversation_started:
                    starter = CONVERSATION_STARTERS.get(mood_data["key"], 
                        "Hi there! 💙 I'm here to listen. How can I support you today?")
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": starter
                    })
                    st.session_state.conversation_started = True
                st.rerun()
        
        # Show current mood
        if st.session_state.current_mood:
            st.success(f"Current mood: {st.session_state.current_mood}")
        
        st.divider()
        
        # Quick Actions
        st.markdown("### 🛠️ Quick Support")
        
        col1, col2 = st.columns(2)
        
        actions = QUICK_ACTIONS
        for i, action in enumerate(actions):
            with col1 if i % 2 == 0 else col2:
                if st.button(
                    f"{action['icon']}",
                    key=f"action_{action['action']}",
                    help=action['label'],
                    use_container_width=True
                ):
                    handle_quick_action(action['action'])
                st.caption(action['label'])
        
        
        # Clear chat
        if st.button("🗑️ Clear Conversation", use_container_width=True, type="secondary"):
            st.session_state.messages = []
            st.session_state.conversation_started = False
            st.session_state.crisis_mode = False
            st.session_state.conversation_history = []  # Reset Groq conversation
            st.rerun()

# QUICK ACTION HANDLERS
def handle_quick_action(action: str):
    """Handle quick action button clicks."""
    
    if action == "breathing":
        exercise = get_breathing_exercise()
        content = format_breathing_exercise(exercise)
        st.session_state.messages.append({
            "role": "assistant",
            "content": content
        })
    
    elif action == "grounding":
        exercise = get_grounding_exercise()
        content = format_grounding_exercise(exercise)
        st.session_state.messages.append({
            "role": "assistant",
            "content": content
        })
    
    elif action == "cbt":
        technique = get_cbt_technique()
        content = format_cbt_technique(technique)
        st.session_state.messages.append({
            "role": "assistant",
            "content": content
        })
    
    elif action == "journal":
        prompt = get_journal_prompt()
        content = format_journal_prompt(prompt)
        st.session_state.messages.append({
            "role": "assistant",
            "content": content
        })
    
    elif action == "affirmation":
        affirmation = get_affirmation()
        st.session_state.messages.append({
            "role": "assistant",
            "content": f"✨ {affirmation}"
        })
    
    elif action == "meditation":
        meditation = get_meditation()
        content = format_meditation(meditation)
        st.session_state.messages.append({
            "role": "assistant",
            "content": content
        })
    
    st.rerun()

def render_chat_interface():
    """Render the main chat interface."""
    
    # Header
    st.markdown("#  Sukoon - Mental Wellness Companion")
    st.markdown("*A compassionate space for your mental wellness*")
    
    # Show initial disclaimer if first visit
    if st.session_state.show_disclaimer and not st.session_state.conversation_started:
        with st.container():
            st.info("""
            **Welcome to Sukoon 🕊️** 💙
            
            I'm here to listen, support, and help you navigate difficult emotions. 
            Whether you're feeling anxious, sad, stressed, or overwhelmed, you're not alone.
            
            **Please select your current mood in the sidebar to begin.**
            
            *Remember: I'm an AI companion, not a therapist. For professional help, please consult a mental health professional.*
            """)
    
    # Chat container
    chat_container = st.container()
    
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"], avatar="🧘" if message["role"] == "assistant" else "👤"):
                st.markdown(message["content"])
    
    if prompt := st.chat_input("Share what's on your mind... 💭"):
        if not st.session_state.conversation_started:
            st.session_state.conversation_started = True
        
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)
        
        with st.chat_message("assistant", avatar="🧘"):
            with st.spinner("Thinking with care..."):
                mood_context = ""
                if st.session_state.mood_key:
                    mood_context = MOOD_PROMPTS.get(st.session_state.mood_key, "")
                
                response = generate_response(prompt, mood_context)
                st.markdown(response)
        
        # Add assistant response to history
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Check if we should show crisis resources after a crisis response
        if st.session_state.crisis_mode:
            st.warning("If you need immediate help, please check the crisis helplines in the sidebar.")

# MAIN APPLICATION
def main():
    """Main application entry point."""
    # Apply custom styling
    apply_custom_css()
    
    # Initialize session state
    init_session_state()
    
    # Initialize RAG Components
    if not st.session_state.rag_initialized:
        with st.spinner("Preparing wellness wisdom..."):
            try:
                # Use local embeddings (no API key needed)
                embeddings = EmbeddingService()
                
                vector_store = VectorStore(persist_directory="./chroma_db")
                vector_store.initialize_collection()
                
                # Index knowledge base if folder exists
                kb_path = "./knowledge_base"
                if os.path.exists(kb_path):
                    index_knowledge_base(vector_store, embeddings, kb_path)
                
                st.session_state.retriever = WellnessRetriever(embeddings, vector_store)
                st.session_state.rag_initialized = True
            except Exception as e:
                # Silenced for cleaner UI during testing
                # st.error(f"Wellness engine notice: {str(e)}")
                st.session_state.rag_initialized = True
    
    # Render sidebar
    render_sidebar()
    
    # Render main chat interface
    render_chat_interface()
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #888; padding: 20px;'>"
        "Made with 💙 by Moiz Mansoori"
        "</div>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
