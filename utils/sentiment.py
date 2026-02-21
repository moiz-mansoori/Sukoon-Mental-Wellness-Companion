# SENTIMENT ANALYSIS UTILITY
"""
Simple sentiment analysis to understand user's emotional state.
Uses TextBlob for basic analysis and custom keywords for mental health context.
"""

from textblob import TextBlob
from typing import Dict, Tuple

# EMOTIONAL KEYWORDS
# Custom keywords for mental health context
NEGATIVE_INDICATORS = {
    # Sadness
    "sad", "depressed", "hopeless", "empty", "worthless", "crying", "tears",
    "lonely", "alone", "miserable", "broken", "hurt", "pain", "suffering",
    
    # Anxiety
    "anxious", "worried", "scared", "fearful", "panicking", "nervous",
    "terrified", "dread", "overwhelmed", "restless", "uneasy",
    
    # Stress
    "stressed", "exhausted", "burnout", "tired", "drained", "pressure",
    "overworked", "struggling", "can't cope", "falling apart",
    
    # Overthinking
    "overthinking", "ruminating", "can't stop thinking", "racing thoughts",
    "spiraling", "obsessing", "intrusive", "what if", "worst case"
}

POSITIVE_INDICATORS = {
    "happy", "grateful", "thankful", "blessed", "peaceful", "calm",
    "hopeful", "better", "improving", "good", "great", "fine", "okay",
    "relaxed", "content", "proud", "accomplished", "strong"
}

INTENSITY_MODIFIERS = {
    "very", "really", "extremely", "so", "incredibly", "absolutely",
    "completely", "totally", "truly", "deeply", "seriously"
}


def analyze_sentiment(text: str) -> Dict:
    """
    Analyze the sentiment and emotional content of user's message.
    
    Args:
        text: User's message text
        
    Returns:
        Dictionary containing:
        - polarity: Float from -1 (negative) to 1 (positive)
        - subjectivity: Float from 0 (objective) to 1 (subjective)
        - emotional_intensity: "mild", "moderate", or "severe"
        - detected_emotions: List of detected emotional keywords
        - needs_support: Boolean indicating if user needs extra support
    """
    text_lower = text.lower()
    
    # Basic TextBlob sentiment analysis
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity  # -1 to 1
    subjectivity = blob.sentiment.subjectivity  # 0 to 1
    
    # Detect emotional keywords
    words = set(text_lower.split())
    
    negative_found = words.intersection(NEGATIVE_INDICATORS)
    positive_found = words.intersection(POSITIVE_INDICATORS)
    modifiers_found = words.intersection(INTENSITY_MODIFIERS)
    
    # Calculate emotional intensity
    intensity = "mild"
    if len(negative_found) >= 2 or len(modifiers_found) >= 1:
        intensity = "moderate"
    if len(negative_found) >= 3 or (len(modifiers_found) >= 1 and len(negative_found) >= 2):
        intensity = "severe"
    
    # Check for phrases that indicate intensity
    intense_phrases = [
        "can't cope", "can't handle", "falling apart", "breaking down",
        "can't take it", "too much", "end it all", "give up"
    ]
    for phrase in intense_phrases:
        if phrase in text_lower:
            intensity = "severe"
            break
    
    # Determine if user needs extra support
    needs_support = (
        polarity < -0.3 or 
        intensity in ["moderate", "severe"] or
        len(negative_found) >= 2
    )
    
    return {
        "polarity": round(polarity, 2),
        "subjectivity": round(subjectivity, 2),
        "emotional_intensity": intensity,
        "detected_emotions": list(negative_found | positive_found),
        "negative_indicators": list(negative_found),
        "positive_indicators": list(positive_found),
        "needs_support": needs_support
    }


def get_empathy_level(sentiment_result: Dict) -> str:
    """
    Determine appropriate empathy level based on sentiment analysis.
    
    Returns:
        "high" - User is struggling, needs maximum warmth
        "medium" - User has some concerns, be supportive
        "low" - User seems okay, maintain friendly presence
    """
    if sentiment_result["emotional_intensity"] == "severe":
        return "high"
    elif sentiment_result["emotional_intensity"] == "moderate" or sentiment_result["needs_support"]:
        return "medium"
    else:
        return "low"


def format_sentiment_for_prompt(sentiment_result: Dict) -> str:
    """
    Format sentiment analysis into a prompt modifier for the AI.
    
    This helps the AI understand the user's emotional state and respond appropriately.
    Framed as gentle guidance, not clinical labels.
    """
    intensity = sentiment_result["emotional_intensity"]
    emotions = sentiment_result.get("negative_indicators", [])
    
    if intensity == "severe":
        return f"""[EMOTIONAL AWARENESS]
The user is carrying something very heavy right now. 
What you're sensing: {', '.join(emotions) if emotions else 'deep pain'}
Be fully present. Sit with them before offering anything. Maximum warmth, maximum gentleness. Let them feel heard first."""
    
    elif intensity == "moderate":
        return f"""[EMOTIONAL AWARENESS]
The user is going through a difficult moment.
What you're sensing: {', '.join(emotions) if emotions else 'emotional weight'}
Be warm and present. Validate what they're feeling. Only offer gentle support if it feels natural."""
    
    else:
        return """[EMOTIONAL AWARENESS]
The user seems relatively steady right now.
Stay warm, be present, maintain a safe and gentle space for whatever they want to share."""
