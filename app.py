"""
A compassionate AI chatbot designed to provide emotional support
for people dealing with depression, anxiety, and overthinking.

"""

import streamlit as st
from groq import Groq
from typing import Optional

# Import local modules
from config.settings import (
    MOOD_OPTIONS, 
    SAFETY_DISCLAIMER, 
    EMERGENCY_HELPLINES,
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
    TECHNIQUE_INTROS,
    CRISIS_RESPONSE
)
from utils import (
    analyze_sentiment,
    get_empathy_level,
    format_sentiment_for_prompt,
    detect_crisis,
    get_crisis_response,
    format_crisis_for_prompt,
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
    """Apply custom CSS for a calming, modern UI."""
    st.markdown(f"""
    <style>
        /* Main background and theme */
        .stApp {{
            background: linear-gradient(135deg, {THEME_COLORS["background"]} 0%, #1E2140 100%);
        }}
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {{
            background: linear-gradient(180deg, {THEME_COLORS["card_bg"]} 0%, #1A1D29 100%);
        }}
        
        /* Chat message styling */
        .stChatMessage {{
            background-color: {THEME_COLORS["card_bg"]};
            border-radius: 15px;
            padding: 10px;
            margin: 5px 0;
        }}
        
        /* User message bubble */
        [data-testid="stChatMessageContent"] {{
            padding: 10px 15px;
        }}
        
        /* Button styling */
        .stButton > button {{
            background: linear-gradient(135deg, {THEME_COLORS["primary"]} 0%, #8B5CF6 100%);
            color: white;
            border: none;
            border-radius: 25px;
            padding: 10px 20px;
            font-weight: 500;
            transition: all 0.3s ease;
        }}
        
        .stButton > button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(107, 115, 255, 0.4);
        }}
        
        /* Quick action buttons */
        .quick-action {{
            background: {THEME_COLORS["card_bg"]};
            border-radius: 15px;
            padding: 15px;
            text-align: center;
            transition: all 0.3s ease;
            cursor: pointer;
            border: 1px solid rgba(255,255,255,0.1);
        }}
        
        .quick-action:hover {{
            transform: translateY(-3px);
            border-color: {THEME_COLORS["primary"]};
        }}
        
        /* Disclaimer box */
        .disclaimer-box {{
            background: rgba(246, 173, 85, 0.1);
            border-left: 4px solid {THEME_COLORS["warning"]};
            padding: 15px;
            border-radius: 0 10px 10px 0;
            margin: 10px 0;
        }}
        
        /* Crisis helpline box */
        .crisis-box {{
            background: rgba(239, 68, 68, 0.1);
            border-left: 4px solid #EF4444;
            padding: 15px;
            border-radius: 0 10px 10px 0;
            margin: 10px 0;
        }}
        
        /* Mood selector buttons */
        .mood-btn {{
            display: inline-block;
            padding: 10px 15px;
            margin: 5px;
            border-radius: 20px;
            background: {THEME_COLORS["card_bg"]};
            border: 2px solid transparent;
            transition: all 0.3s ease;
        }}
        
        .mood-btn:hover {{
            border-color: {THEME_COLORS["primary"]};
        }}
        
        .mood-btn.selected {{
            border-color: {THEME_COLORS["secondary"]};
            background: rgba(72, 187, 120, 0.2);
        }}
        
        /* Technique cards */
        .technique-card {{
            background: {THEME_COLORS["card_bg"]};
            border-radius: 15px;
            padding: 20px;
            margin: 10px 0;
            border: 1px solid rgba(255,255,255,0.1);
        }}
        
        /* Breathing animation keyframes */
        @keyframes breathe {{
            0%, 100% {{ transform: scale(1); opacity: 0.8; }}
            50% {{ transform: scale(1.1); opacity: 1; }}
        }}
        
        .breathing-indicator {{
            animation: breathe 4s ease-in-out infinite;
        }}
        
        /* Smooth scrollbar */
        ::-webkit-scrollbar {{
            width: 8px;
        }}
        
        ::-webkit-scrollbar-track {{
            background: {THEME_COLORS["background"]};
        }}
        
        ::-webkit-scrollbar-thumb {{
            background: {THEME_COLORS["primary"]};
            border-radius: 4px;
        }}
        
        /* Header styling */
        h1 {{
            background: linear-gradient(135deg, {THEME_COLORS["primary"]} 0%, {THEME_COLORS["accent"]} 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
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
        "conversation_history": []  # Groq conversation history
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
    
    if mood_context:
        context_parts.append(f"[MOOD CONTEXT]\n{mood_context}")
    
    context_parts.append(sentiment_context)
    
    # Combine context with user message
    enhanced_message = "\n\n".join(context_parts) + f"\n\n[USER MESSAGE]: {user_message}"
    
    try:
        client = get_groq_client()
        if not client:
            return "⚠️ **API Key Required**: Please add your Groq API key to the `.env` file. You can get a free key at [Groq Console](https://console.groq.com). 💙"
        
        # Build messages with system prompt and conversation history
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        
        # Add conversation history for context
        for msg in st.session_state.conversation_history[-6:]:  # Keep last 6 messages for context
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
        
        # API Key status
        if not GROQ_API_KEY:
            st.warning("⚠️ Add your Groq API key to `.env` file")
            st.markdown("[Get free API key →](https://console.groq.com)")
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
        intro = TECHNIQUE_INTROS.get("breathing", "")
        st.session_state.messages.append({
            "role": "assistant",
            "content": f"{intro}\n\n{content}"
        })
    
    elif action == "grounding":
        exercise = get_grounding_exercise()
        content = format_grounding_exercise(exercise)
        intro = TECHNIQUE_INTROS.get("grounding", "")
        st.session_state.messages.append({
            "role": "assistant",
            "content": f"{intro}\n\n{content}"
        })
    
    elif action == "cbt":
        technique = get_cbt_technique()
        content = format_cbt_technique(technique)
        intro = TECHNIQUE_INTROS.get("cbt", "")
        st.session_state.messages.append({
            "role": "assistant",
            "content": f"{intro}\n\n{content}"
        })
    
    elif action == "journal":
        prompt = get_journal_prompt()
        content = format_journal_prompt(prompt)
        intro = TECHNIQUE_INTROS.get("journal", "")
        st.session_state.messages.append({
            "role": "assistant",
            "content": f"{intro}\n\n{content}"
        })
    
    elif action == "affirmation":
        affirmation = get_affirmation()
        intro = TECHNIQUE_INTROS.get("affirmation", "")
        st.session_state.messages.append({
            "role": "assistant",
            "content": f"{intro}\n\n✨ {affirmation}"
        })
    
    elif action == "meditation":
        meditation = get_meditation()
        content = format_meditation(meditation)
        intro = TECHNIQUE_INTROS.get("meditation", "")
        st.session_state.messages.append({
            "role": "assistant",
            "content": f"{intro}\n\n{content}"
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
        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"], avatar="🧘" if message["role"] == "assistant" else "👤"):
                st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Share what's on your mind... 💭"):
        # Mark conversation as started
        if not st.session_state.conversation_started:
            st.session_state.conversation_started = True
        
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)
        
        # Generate and display assistant response
        with st.chat_message("assistant", avatar="🧘"):
            with st.spinner("Thinking with care..."):
                # Get mood context if mood is selected
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
