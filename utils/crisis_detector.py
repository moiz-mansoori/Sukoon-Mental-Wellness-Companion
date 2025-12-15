# CRISIS DETECTION MODULE

import re
from typing import Dict, Tuple

# CRISIS INDICATORS
# Keywords and phrases that may indicate crisis

# HIGH PRIORITY - Immediate concern patterns
HIGH_RISK_PATTERNS = [
    r"kill\s*(my)?self",
    r"end\s*(my)?\s*life",
    r"want\s*to\s*die",
    r"wanting\s*to\s*die",
    r"don'?t\s*want\s*to\s*(be\s*here|live|exist)",
    r"better\s*off\s*(dead|without\s*me)",
    r"no\s*reason\s*to\s*live",
    r"suicide",
    r"suicidal",
    r"take\s*my\s*(own\s*)?life",
    r"end\s*it\s*all",
    r"can'?t\s*go\s*on",
    r"not\s*worth\s*living",
    r"wish\s*i\s*was\s*dead",
    r"wish\s*i\s*wasn'?t\s*(alive|here|born)",
]

# MEDIUM PRIORITY - Self-harm indicators
SELF_HARM_PATTERNS = [
    r"hurt\s*(my)?self",
    r"hurting\s*(my)?self",
    r"cutting",
    r"self[- ]?harm",
    r"harm\s*(my)?self",
    r"punish\s*(my)?self",
]

# LOWER PRIORITY - Concerning but less immediate
CONCERNING_PATTERNS = [
    r"hopeless",
    r"worthless",
    r"no\s*point",
    r"give\s*up",
    r"can'?t\s*take\s*(it|this)\s*(anymore)?",
    r"falling\s*apart",
    r"nobody\s*(cares|would\s*miss\s*me)",
    r"burden\s*(to|on)\s*(everyone|others|people)",
    r"everyone\s*would\s*be\s*better\s*off",
]


def detect_crisis(text: str) -> Dict:
    """
    Analyze text for crisis indicators.
    
    Args:
        text: User's message text
        
    Returns:
        Dictionary containing:
        - is_crisis: Boolean indicating if crisis was detected
        - severity: "high", "medium", "low", or "none"
        - matched_patterns: List of concerning patterns found
        - response_needed: Boolean indicating if special response is needed
    """
    text_lower = text.lower().strip()
    
    matched = []
    severity = "none"
    
    # Check high-risk patterns first
    for pattern in HIGH_RISK_PATTERNS:
        if re.search(pattern, text_lower):
            matched.append(pattern)
            severity = "high"
    
    # Check self-harm patterns
    if severity != "high":
        for pattern in SELF_HARM_PATTERNS:
            if re.search(pattern, text_lower):
                matched.append(pattern)
                severity = "medium" if severity == "none" else severity
    
    # Check concerning patterns (only if nothing higher found)
    if severity == "none":
        for pattern in CONCERNING_PATTERNS:
            if re.search(pattern, text_lower):
                matched.append(pattern)
                severity = "low"
    
    is_crisis = severity in ["high", "medium"]
    
    return {
        "is_crisis": is_crisis,
        "severity": severity,
        "matched_patterns": matched,
        "response_needed": severity in ["high", "medium", "low"]
    }


def get_crisis_response(severity: str) -> str:
    """
    Get appropriate response based on crisis severity.
    
    Args:
        severity: "high", "medium", "low", or "none"
        
    Returns:
        Supportive response message
    """
    
    if severity == "high":
        return """I'm really glad you reached out, and I want you to know that what you're feeling matters deeply. Thank you for trusting me with something so important. 💙

What you've shared tells me you're going through an incredibly difficult time, and I'm genuinely concerned about you. **You deserve support from someone who can really help.**

**You are not alone in this.** There are people who care about you and want to help. Would you be willing to reach out to one of these resources? I'm also here to keep talking with you."""

    elif severity == "medium":
        return """I hear that you're in a really tough place right now, and I want you to know that I take what you've shared seriously. 💙

What you're describing sounds really painful, and you deserve support. I'm here for you.

You don't have to face this alone. Is there someone in your life you trust that you could reach out to?

I'm still here with you. Would you like to talk more about what you're going through?"""

    elif severity == "low":
        return """I can hear that things feel really heavy right now, and I want you to know that your feelings are valid. 💙

It takes courage to share when you're struggling. I'm here to listen and support you however I can.

For now, I'm here. Would you like to talk more about what's been on your mind?"""
    
    else:
        return ""


def should_continue_conversation(crisis_result: Dict) -> bool:
    """
    Determine if the chatbot should continue normal conversation
    or focus on crisis support.
    
    Args:
        crisis_result: Result from detect_crisis()
        
    Returns:
        True if normal conversation can continue,
        False if crisis support should take priority
    """
    return not crisis_result["is_crisis"]


def format_crisis_for_prompt(crisis_result: Dict) -> str:
    """
    Format crisis detection result for inclusion in AI prompt.
    
    This helps the AI understand the context and respond appropriately.
    """
    if crisis_result["severity"] == "high":
        return """[CRISIS ALERT: HIGH PRIORITY]
User has expressed language indicating potential immediate crisis.
Response requirements:
- Lead with compassion and validation
- Prioritize safety resources
- Encourage professional help
- Do NOT attempt to 'solve' or minimize
- Stay calm and non-judgmental"""
    
    elif crisis_result["severity"] == "medium":
        return """[CONCERN ALERT: MEDIUM PRIORITY]
User has expressed concerning language about self-harm.
Response requirements:
- Be extra gentle and caring
- Mention resources naturally
- Check in about their safety
- Encourage speaking to someone they trust"""
    
    elif crisis_result["severity"] == "low":
        return """[CONCERN ALERT: LOW PRIORITY]
User has expressed some concerning language.
Response requirements:
- Be extra supportive and validating
- Monitor for escalation
- Gently remind them help is available"""
    
    return ""
