# CONFIGURATION SETTINGS
"""
Central configuration file containing all settings, constants,
and configurable parameters for the Mental Wellness Chatbot.
"""

import os
import streamlit as st
from dotenv import load_dotenv

# Load environment variables (for local development)
load_dotenv()

# LLM MODEL CONFIGURATION
# Try Streamlit secrets first (for cloud), then fall back to .env (for local)
def get_api_key():
    # First try Streamlit secrets (cloud deployment)
    try:
        if "GROQ_API_KEY" in st.secrets:
            return st.secrets["GROQ_API_KEY"]
    except:
        pass
    # Fall back to environment variable (local development)
    return os.getenv("GROQ_API_KEY", "")

GROQ_API_KEY = get_api_key()

# Groq model settings - LLaMA 3.3 70B for high-quality empathetic responses
GROQ_MODEL = "llama-3.3-70b-versatile"

# Response generation settings
MAX_TOKENS = 600
TEMPERATURE = 0.8  # More natural, human-sounding variation

# RAG CONFIGURATION
CHROMA_PERSIST_DIR = "./chroma_db"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
RAG_TOP_K = 2
RAG_SIMILARITY_THRESHOLD = 0.5

# MOOD OPTIONS
# Each mood affects how the AI responds to the user
MOOD_OPTIONS = {
    "😔 Sad": {
        "key": "sad",
        "description": "Feeling down, low energy, or hopeless",
        "prompt_modifier": "The user is feeling sad and low. Be extra gentle, validating, and warm."
    },
    "😰 Anxious": {
        "key": "anxious", 
        "description": "Feeling worried, nervous, or on edge",
        "prompt_modifier": "The user is experiencing anxiety. Offer calming presence and grounding techniques."
    },
    "😤 Stressed": {
        "key": "stressed",
        "description": "Feeling overwhelmed by responsibilities",
        "prompt_modifier": "The user is stressed. Help them prioritize and find moments of calm."
    },
    "🌀 Overthinking": {
        "key": "overthinking",
        "description": "Mind racing with endless thoughts",
        "prompt_modifier": "The user is overthinking. Help them break the thought loop gently."
    },
    "😌 Calm": {
        "key": "calm",
        "description": "Feeling okay, just want to chat",
        "prompt_modifier": "The user is feeling calm. Maintain this positive state and be supportive."
    }
}

# SAFETY DISCLAIMER
SAFETY_DISCLAIMER = """
⚠️ **Important Disclaimer**

This chatbot is designed for **emotional support only** and is **NOT a substitute for professional mental health care**.

- I cannot diagnose mental health conditions
- I am not a licensed therapist or counselor
- In case of emergency, please contact professional help

**If you're having thoughts of self-harm, please reach out to a crisis helpline immediately.**
"""

# UI THEME COLORS (Calming palette)
THEME_COLORS = {
    "primary": "#6B73FF",      # Soft purple-blue
    "secondary": "#48BB78",     # Calming green
    "background": "#1A1D29",    # Dark background
    "card_bg": "#252836",       # Card background
    "text": "#E8E8E8",          # Light text
    "accent": "#F687B3",        # Soft pink accent
    "warning": "#F6AD55"        # Warm orange for warnings
}

# QUICK ACTIONS CONFIGURATION
QUICK_ACTIONS = [
    {
        "icon": "🌬️",
        "label": "Breathing Exercise",
        "action": "breathing"
    },
    {
        "icon": "🌍",
        "label": "Grounding (5-4-3-2-1)",
        "action": "grounding"
    },
    {
        "icon": "💭",
        "label": "Reframe Thoughts",
        "action": "cbt"
    },
    {
        "icon": "📝",
        "label": "Journal Prompt",
        "action": "journal"
    },
    {
        "icon": "✨",
        "label": "Affirmation",
        "action": "affirmation"
    },
    {
        "icon": "🧘",
        "label": "Quick Meditation",
        "action": "meditation"
    }
]
