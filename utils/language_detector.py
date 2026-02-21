# LANGUAGE DETECTION MODULE
"""
Detects whether user input is in English, Urdu, or Roman Urdu.
"""

import re
from typing import Tuple

# Common Roman Urdu words and patterns
ROMAN_URDU_WORDS = {
    # Pronouns
    "mera", "meri", "mere", "tera", "teri", "tere", "uska", "uski", "uske",
    "hamara", "hamari", "hamare", "tumhara", "tumhari", "tumhare",
    "mujhe", "tujhe", "aap", "aapka", "aapki", "aapko", "hum", "tum",
    "woh", "wo", "yeh", "ye", "kya", "kaun", "kahan", "kab", "kyun", "kaise",
    
    # Common verbs
    "hai", "hain", "ho", "tha", "thi", "the", "hoga", "hogi", "hoge",
    "kar", "karo", "karna", "karta", "karti", "karte", "karein", "karunga", "karungi",
    "bol", "bolo", "bolna", "bolta", "bolti", "bolte", "batao", "batana", "bata",
    "sun", "suno", "sunna", "sunta", "sunti", "sunte", "sunao",
    "dekh", "dekho", "dekhna", "dekhta", "dekhti", "dekhte",
    "ja", "jao", "jana", "jata", "jati", "jate", "jaana", "jayega", "jayegi",
    "aa", "aao", "aana", "aata", "aati", "aate", "aaonga", "aaongi",
    "le", "lo", "lena", "leta", "leti", "lete", "liya", "liye",
    "de", "do", "dena", "deta", "deti", "dete", "diya", "diye",
    "raha", "rahi", "rahe", "raho", "rehna", "rehta", "rehti",
    "sakta", "sakti", "sakte", "sakein",
    "chahiye", "chahte", "chahti", "chaahta", "chaahti",
    "laga", "lagi", "lage", "lagta", "lagti", "lagte",
    "pata", "pati", "maloom", "samajh", "samjha", "samjho",
    "horha", "horhi", "horhe", "horai", "hora",
    "karha", "karhi", "karhe",
    
    # Common nouns
    "dil", "dimagh", "sir", "sar", "dard", "drd", "takleef", "taklif",
    "zindagi", "zindgi", "maut", "pyar", "mohabbat", "ishq",
    "ghar", "kaam", "kam", "paisa", "paise", "waqt", "time",
    "raat", "din", "subah", "shaam", "kal", "aaj", "parso",
    "dost", "bhai", "behen", "behan", "maa", "baap", "abbu", "ammi",
    "log", "banda", "bande", "insaan", "aadmi", "aurat", "larki", "larka",
    "khushi", "gham", "udaas", "udasi", "tension", "fikar", "fikr",
    "neend", "nind", "thakan", "thakawat", "aram", "sukoon",
    
    # Feelings and emotions
    "udas", "udaas", "pareshan", "preshan", "ghabra", "ghabrahat",
    "akela", "akeli", "akele", "tanha", "tanhai",
    "dar", "darr", "khauf", "khof", "stress",
    "thak", "thaka", "thaki", "thake", "thakgaya", "thakgayi",
    "rona", "roya", "royi", "roye", "ro", "aansu", "aansoo",
    "hasna", "hasa", "hasi", "hanse", "muskurana", "muskura",
    "gussa", "ghussa", "naraz", "upset",
    
    # Common phrases and expressions
    "kuch", "koi", "sab", "bohot", "bahut", "bohat", "zyada", "ziada",
    "thoda", "thodi", "thore", "kam", "bilkul", "bilkool",
    "acha", "achi", "ache", "bura", "buri", "bure",
    "theek", "thik", "sahi", "galat", "mushkil", "aasan", "asan",
    "pehle", "baad", "abhi", "ab", "phir", "fir",
    "lekin", "magar", "par", "kyunke", "kyonke", "isliye", "islye",
    "shayad", "zaroor", "zarur", "hamesha", "kabhi", "kabho",
    "sirf", "bas", "bhi", "aur", "ya", "nahi", "nhi", "na", "mat", "haan", "han", "ji",
    "please", "plz", "pls", "shukriya", "shukria", "meherbani",
    
    # Common shorthand
    "kr", "kro", "krna", "krta", "krti", "krte",
    "h", "hn", "ni", "shi", "toh", "to",
    "bs", "bss", "aur", "or",
    "pta", "btao", "btana", "smjh", "smjha",
    "ap", "apko", "apka", "apki",
    "mjhe", "mjh", "hmara", "hmari", "tmhara", "tmhari",
    "kbi", "kbhi", "hmesa", "phle", "bd",
    
    # Question words shorthand
    "q", "kyu", "kya", "kn", "kb", "kha", "kese", "kaise",
    
    # Greetings
    "salam", "assalam", "walaikum", "alikum", "slm",
    "khuda", "allah", "hafiz", "janab",
}

# Common English words to help differentiate
COMMON_ENGLISH_WORDS = {
    "the", "is", "are", "was", "were", "been", "being",
    "have", "has", "had", "having", "do", "does", "did",
    "will", "would", "could", "should", "may", "might",
    "must", "shall", "can", "need", "dare", "ought",
    "i", "me", "my", "myself", "we", "our", "ours",
    "you", "your", "yours", "he", "him", "his", "she", "her",
    "it", "its", "they", "them", "their", "what", "which",
    "who", "whom", "this", "that", "these", "those",
    "am", "been", "being", "because", "but", "and", "or",
    "feeling", "feel", "felt", "think", "thought", "know",
    "help", "want", "need", "like", "love", "hate",
    "happy", "sad", "angry", "scared", "worried", "anxious",
    "depressed", "stressed", "tired", "exhausted", "overwhelmed",
    "today", "yesterday", "tomorrow", "now", "always", "never",
    "sometimes", "often", "usually", "really", "very", "much",
    # Greetings (prevent misclassification)
    "hi", "hello", "hey", "good", "morning", "evening", "night",
    "thanks", "thank", "please", "sorry", "okay", "ok", "yes", "no",
    "how", "are", "doing", "going", "fine", "well", "great",
}


def detect_language(text: str) -> Tuple[str, float]:
    """
    Detect if text is in Roman Urdu, English, or mixed.
    
    Returns:
        Tuple of (language, confidence)
        language: "roman_urdu", "english", or "mixed"
        confidence: float from 0 to 1
    """
    if not text or not text.strip():
        return "english", 0.0
    
    text_lower = text.lower().strip()
    
    # Remove punctuation for word matching
    clean_text = re.sub(r'[^\w\s]', '', text_lower)
    words = clean_text.split()
    
    if not words:
        return "english", 0.0
    
    # Short messages (1-2 words): default to English unless clearly Roman Urdu
    # This prevents greetings like "Hi", "Hello", "Hey" from being misclassified
    if len(words) <= 2:
        english_greetings = {"hi", "hello", "hey", "yo", "sup", "thanks", "ok", "okay", "yes", "no", "good", "fine", "great", "help", "please"}
        if any(w in english_greetings for w in words):
            return "english", 0.9
        # Only classify as Roman Urdu if the word is clearly Urdu (not ambiguous)
        clear_urdu = {"salam", "assalam", "walaikum", "kaise", "kya", "mujhe", "batao", "haan", "nahi", "bohot", "bhai", "yaar"}
        if any(w in clear_urdu for w in words):
            return "roman_urdu", 0.8
        # Default short messages to English
        return "english", 0.7
    
    roman_urdu_count = 0
    english_count = 0
    
    for word in words:
        if word in ROMAN_URDU_WORDS:
            roman_urdu_count += 1
        elif word in COMMON_ENGLISH_WORDS:
            english_count += 1
    
    total_matched = roman_urdu_count + english_count
    total_words = len(words)
    
    # If very few words matched, try pattern-based detection
    if total_matched < total_words * 0.3:
        # Check for Roman Urdu patterns
        roman_urdu_patterns = [
            r'\b(kya|kaise|kyun|kahan|kab)\b',  # Question words
            r'\b(hai|hain|tha|thi|ho)\b',       # Common verbs
            r'\b(mera|meri|tera|teri|aap)\b',   # Pronouns
            r'\b(nahi|nhi|mat|haan|han)\b',     # Yes/No
            r'\b(bohot|bahut|bohat|zyada)\b',   # Intensifiers
        ]
        
        for pattern in roman_urdu_patterns:
            if re.search(pattern, text_lower):
                roman_urdu_count += 1
    
    # Calculate confidence
    if total_words == 0:
        return "english", 0.0
    
    roman_urdu_ratio = roman_urdu_count / total_words
    english_ratio = english_count / total_words
    
    # Decision logic
    # Mixed language: both have significant presence
    if roman_urdu_count >= 2 and english_count >= 2 and roman_urdu_ratio >= 0.2 and english_ratio >= 0.2:
        confidence = min((roman_urdu_ratio + english_ratio) / 2 + 0.3, 1.0)
        return "mixed", confidence
    elif roman_urdu_ratio >= 0.3 or roman_urdu_count >= 2:
        confidence = min(roman_urdu_ratio + 0.3, 1.0)
        return "roman_urdu", confidence
    elif english_ratio >= 0.5:
        return "english", english_ratio
    elif roman_urdu_count > english_count:
        return "roman_urdu", roman_urdu_ratio + 0.2
    else:
        return "english", 0.5


def get_language_instruction(detected_language: str) -> str:
    """
    Get language-specific instruction for the LLM.
    """
    if detected_language == "roman_urdu":
        return """
────────────────────────────────
LANGUAGE INSTRUCTION (CRITICAL)
────────────────────────────────

The user is speaking in ROMAN URDU. You MUST respond ENTIRELY in ROMAN URDU.

Rules:
- Write in Roman Urdu (Urdu written in English letters)
- Use PAKISTANI Roman Urdu vocabulary ONLY
- Be natural, soft, conversational, culturally grounded, emotionally expressive
- Do NOT respond in English
- Do NOT use Urdu script (Arabic letters)
- Do NOT use formal or textbook Urdu
- Do NOT use Hindi words. You are Pakistani, not Indian.
- FORBIDDEN Hindi words: samay, samajhna, prayas, samay, sochiye, koshish kijiye, dhyan, sahara, vishwas, himmat, umeed (use instead: waqt, seekhna, koshish, socho, mehnat, tawajju, sahara, bharosa, himmat, umeed)
- Sound like a real Pakistani person having a heartfelt conversation

Tone examples:
"Main samajh sakta hoon tum kya mehsoos kar rahe ho."
"Yeh feeling bohat bhari hoti hai."
"Har takleef ka hal foran nahi milta, kabhi sirf sun lena hi kaafi hota hai."
"""
    elif detected_language == "mixed":
        return """
────────────────────────────────
LANGUAGE INSTRUCTION (CRITICAL)
────────────────────────────────

The user is mixing ROMAN URDU and ENGLISH together naturally. You MUST mirror this EXACT style.

Rules:
- Respond in the same mixed Roman Urdu + English style the user is using
- Let the language flow naturally between both, just like the user does
- Don't force either language — blend them the way Pakistani friends talk
- Keep your warm, emotionally present tone in whatever mix feels natural
- Do NOT use Hindi words. Use Pakistani Roman Urdu vocabulary.

Tone examples:
"Yeh feeling bohat overwhelming hoti hai, especially jab sab kuch ek saath hit kare."
"I can feel ke tum bohat drain ho rahe ho. That's completely valid."
"Sometimes bas kisi ko sunne ki zaroorat hoti hai, and I'm here for that."
"""
    else:
        return """
────────────────────────────────
LANGUAGE INSTRUCTION (CRITICAL)
────────────────────────────────

The user is speaking in ENGLISH. You MUST respond ENTIRELY in ENGLISH.

Rules:
- Respond ONLY in English
- Do NOT use Roman Urdu, Urdu, or Hindi words
- Do NOT mix languages
- Be warm, natural, and emotionally present — in English only
"""


def format_language_context(text: str) -> str:
    """
    Analyze text and return language context for the prompt.
    Always returns a language instruction to enforce strict language mirroring.
    """
    language, confidence = detect_language(text)
    
    if language == "roman_urdu" and confidence >= 0.3:
        return get_language_instruction("roman_urdu")
    elif language == "mixed" and confidence >= 0.3:
        return get_language_instruction("mixed")
    
    # Always return English instruction for English input
    return get_language_instruction("english")
