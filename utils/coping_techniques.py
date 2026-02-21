import random
from typing import List, Dict

# BREATHING EXERCISES
# Guided breathing techniques for calming the nervous system

BREATHING_EXERCISES = {
    "4-7-8": {
        "name": "4-7-8 Relaxation Breath",
        "description": "A calming technique that activates your parasympathetic nervous system",
        "steps": [
            "🌬️ Find a comfortable position and relax your shoulders",
            "1️⃣ **Breathe IN** through your nose for **4 seconds**",
            "2️⃣ **HOLD** your breath for **7 seconds**",
            "3️⃣ **Breathe OUT** slowly through your mouth for **8 seconds**",
            "🔄 Repeat this cycle **3-4 times**",
            "✨ Notice how your body feels calmer with each breath"
        ]
    },
    "box": {
        "name": "Box Breathing",
        "description": "Used by Navy SEALs to stay calm under pressure",
        "steps": [
            "🌬️ Sit upright and exhale completely",
            "1️⃣ **Breathe IN** for **4 seconds** (imagine going UP one side of a box)",
            "2️⃣ **HOLD** for **4 seconds** (go ACROSS the top)",
            "3️⃣ **Breathe OUT** for **4 seconds** (go DOWN the other side)",
            "4️⃣ **HOLD** for **4 seconds** (go ACROSS the bottom)",
            "🔄 Repeat this cycle **4-6 times**",
            "✨ With practice, this becomes your instant calm button"
        ]
    },
    "belly": {
        "name": "Deep Belly Breathing",
        "description": "Simple but powerful technique to reduce anxiety",
        "steps": [
            "🌬️ Place one hand on your chest, one on your belly",
            "1️⃣ **Breathe IN** slowly through your nose, letting your belly rise",
            "💡 Your chest should stay relatively still, only belly moves",
            "2️⃣ **Breathe OUT** slowly, letting your belly fall naturally",
            "🔄 Continue for **1-2 minutes**",
            "✨ This activates your body's natural relaxation response"
        ]
    }
}


def get_breathing_exercise(exercise_type: str = None) -> Dict:
    """
    Get a breathing exercise.
    
    Args:
        exercise_type: Specific type ("4-7-8", "box", "belly") or None for random
        
    Returns:
        Dictionary with exercise details
    """
    if exercise_type and exercise_type in BREATHING_EXERCISES:
        return BREATHING_EXERCISES[exercise_type]
    return random.choice(list(BREATHING_EXERCISES.values()))


def format_breathing_exercise(exercise: Dict) -> str:
    """Format breathing exercise for display."""
    steps = "\n".join(exercise["steps"])
    return f"""### 🌬️ {exercise["name"]}

*{exercise["description"]}*

{steps}

---
Take your time. There's no rush. I'm here with you. 💙"""


# GROUNDING TECHNIQUES
# 5-4-3-2-1 and other sensory grounding methods

GROUNDING_54321 = {
    "name": "5-4-3-2-1 Grounding",
    "description": "Brings you back to the present using your senses",
    "steps": [
        "Take a slow, deep breath. Look around you and find:",
        "",
        "👁️ **5 things you can SEE**",
        "*Example: A window, your hands, a book, a light, a plant*",
        "",
        "✋ **4 things you can TOUCH**",
        "*Example: The chair beneath you, your clothes, the floor, your hair*",
        "",
        "👂 **3 things you can HEAR**",
        "*Example: Your breathing, distant traffic, a fan humming*",
        "",
        "👃 **2 things you can SMELL**",
        "*Example: Fresh air, coffee, your shampoo*",
        "",
        "👅 **1 thing you can TASTE**",
        "*Example: Toothpaste, coffee, the air*",
        "",
        "✨ Take another deep breath. You are here. You are safe."
    ]
}

OTHER_GROUNDING = [
    {
        "name": "Cold Water Reset",
        "steps": [
            "💧 Run cold water over your wrists for 30 seconds",
            "🧊 Or hold an ice cube in your palm",
            "🌡️ Focus on the sensation completely",
            "✨ This activates your dive reflex and calms your nervous system"
        ]
    },
    {
        "name": "Body Scan",
        "steps": [
            "🦶 Start at your toes. Notice any sensations there.",
            "🦵 Slowly move up: calves, knees, thighs...",
            "🫁 Notice your belly, chest, breathing...",
            "💪 Your hands, arms, shoulders...",
            "🧠 Finally, your neck, face, and head",
            "✨ You've just reconnected with your whole body"
        ]
    },
    {
        "name": "Object Focus",
        "steps": [
            "👐 Pick up any object near you",
            "🔍 Examine it like you've never seen it before",
            "❓ What color is it? What's the texture? Temperature?",
            "⚖️ How heavy is it? Does it make a sound?",
            "✨ This pulls your mind into the present moment"
        ]
    }
]


def get_grounding_exercise(include_54321: bool = True) -> Dict:
    """Get a grounding exercise."""
    if include_54321:
        return GROUNDING_54321
    return random.choice(OTHER_GROUNDING)


def format_grounding_exercise(exercise: Dict) -> str:
    """Format grounding exercise for display."""
    steps = "\n".join(exercise["steps"])
    return f"""### 🌍 {exercise["name"]}

*{exercise.get("description", "A technique to bring you back to the present moment")}*

{steps}

---
Take your time with each step. There's no rush. 💙"""


# CBT REFRAMING TECHNIQUES
# Cognitive Behavioral Therapy-inspired thought challenging

CBT_TECHNIQUES = [
    {
        "name": "Thought Challenge",
        "intro": "Let's gently examine that thought...",
        "questions": [
            "🤔 What evidence do I have **for** this thought?",
            "🤔 What evidence do I have **against** it?",
            "💭 If a friend had this thought, what would I tell them?",
            "🔮 What's the **worst** that could happen? Could I survive it?",
            "🌟 What's the **best** that could happen?",
            "⚖️ What's **most likely** to actually happen?",
            "💪 What can I do right now to feel a little better?"
        ]
    },
    {
        "name": "Thinking Traps",
        "intro": "Sometimes our minds fall into thinking traps. See if any of these fit:",
        "questions": [
            "🎯 **All-or-nothing**: Am I seeing things as only black or white?",
            "🔮 **Fortune-telling**: Am I predicting the worst without evidence?",
            "🧠 **Mind-reading**: Am I assuming I know what others think?",
            "🏷️ **Labeling**: Am I calling myself harsh names based on one thing?",
            "🔍 **Filtering**: Am I only focusing on the negatives?",
            "📍 **Catastrophizing**: Am I making a mountain out of a molehill?",
            "",
            "💡 Recognizing these traps is the first step to escaping them"
        ]
    },
    {
        "name": "Reframe Generator",
        "intro": "Let's find a more balanced way to look at this...",
        "questions": [
            "📝 The thought bothering me is: ___",
            "😰 This makes me feel: ___",
            "🔍 An alternative way to see this could be: ___",
            "💪 Even if the worst happens, I could cope by: ___",
            "🌱 One small thing I can do right now is: ___"
        ]
    }
]


def get_cbt_technique() -> Dict:
    """Get a random CBT technique."""
    return random.choice(CBT_TECHNIQUES)


def format_cbt_technique(technique: Dict) -> str:
    """Format CBT technique for display."""
    questions = "\n".join(technique["questions"])
    return f"""### 💭 {technique["name"]}

*{technique["intro"]}*

{questions}

---
Take your time. There's no right or wrong answer. 💙"""


# JOURNALING PROMPTS
# Guided writing exercises for emotional processing

JOURNAL_PROMPTS = [
    {
        "title": "Emotional Check-In",
        "prompt": "Right now, I'm feeling...",
        "follow_ups": [
            "I think this feeling started when...",
            "What I really need right now is...",
            "One small thing that might help is..."
        ]
    },
    {
        "title": "Gratitude Moment",
        "prompt": "Three small things I'm grateful for today:",
        "follow_ups": [
            "1. ...",
            "2. ...",
            "3. ...",
            "One of these I often take for granted is..."
        ]
    },
    {
        "title": "Letter to Myself",
        "prompt": "If I could send a message to my past self who felt like this before, I would say...",
        "follow_ups": [
            "I got through it by...",
            "What I learned was...",
            "What I want my future self to remember is..."
        ]
    },
    {
        "title": "The Worry Dump",
        "prompt": "Everything on my mind right now (no filter, just write):",
        "follow_ups": [
            "The biggest worry here is...",
            "Something I CAN control about this is...",
            "Something I CANNOT control is...",
            "One thing I will let go of for now is..."
        ]
    },
    {
        "title": "Tomorrow's Hope",
        "prompt": "Tomorrow, I hope to feel...",
        "follow_ups": [
            "One small thing I can do to help that happen is...",
            "I'll be kind to myself by...",
            "Even if tomorrow is hard, I'll remember that..."
        ]
    },
    {
        "title": "Self-Compassion",
        "prompt": "If my best friend was feeling exactly what I'm feeling, I would tell them...",
        "follow_ups": [
            "I deserve the same kindness because...",
            "One thing I'm doing well right now is...",
            "I forgive myself for..."
        ]
    }
]


def get_journal_prompt() -> Dict:
    """Get a random journal prompt."""
    return random.choice(JOURNAL_PROMPTS)


def format_journal_prompt(prompt: Dict) -> str:
    """Format journal prompt for display."""
    follow_ups = "\n".join(f"• {f}" for f in prompt["follow_ups"])
    return f"""### 📝 {prompt["title"]}

**{prompt["prompt"]}**

{follow_ups}

---
Write freely. This is just for you. There are no wrong answers. 💙"""


# AFFIRMATIONS
# Positive, supportive reminders

AFFIRMATIONS = [
    "You are doing the best you can with what you have right now. And that's enough. 💙",
    "It's okay to not be okay. Healing isn't linear, and every step counts.",
    "Your feelings are valid. You don't have to justify or explain them.",
    "You've survived 100% of your worst days so far. That takes strength.",
    "It's okay to rest. You don't have to earn your right to take a break.",
    "You are not a burden. The people who love you want to be there for you.",
    "Progress isn't always visible. Sometimes just getting through the day is a victory.",
    "You are worthy of love and kindness — especially from yourself.",
    "This moment is hard, but it won't last forever. Nothing does.",
    "You are more resilient than you know. You've proven that before.",
    "Taking care of yourself isn't selfish. It's necessary.",
    "You don't have to have everything figured out. It's okay to take life one day at a time.",
    "Your struggles don't define you. They're just one chapter, not the whole story.",
    "It's okay to ask for help. Strength isn't about doing it all alone.",
    "You matter. Your presence in this world makes a difference.",
]


def get_affirmation() -> str:
    """Get a random affirmation."""
    return random.choice(AFFIRMATIONS)


# QUICK MEDITATION SCRIPT
# Simple guided relaxation

MEDITATION_SCRIPTS = [
    {
        "title": "1-Minute Calm",
        "script": """### 🧘 1-Minute Calm

Find a comfortable position. You can close your eyes if that feels right.

**Breathe in slowly...** 

Let your shoulders drop. Release any tension in your jaw.

**Breathe out slowly...**

Notice the weight of your body. You don't have to hold anything right now.

**Breathe in...**

Imagine a warm, golden light filling your chest.

**Breathe out...**

Let anything heavy leave your body with your breath.

**One more deep breath in... and slowly out.**

When you're ready, gently open your eyes.

You just gave yourself the gift of a moment of peace. 💙"""
    },
    {
        "title": "Safe Place Visualization",
        "script": """### 🧘 Safe Place Visualization

Close your eyes and take three slow, deep breaths.

Imagine a place where you feel completely safe and at peace. It could be:
- A beach at sunset
- A cozy room with soft lights
- A quiet forest clearing
- Anywhere that feels like home

**See it clearly.** Notice the colors, the light, the details.

**Feel it.** What's the temperature? What textures surround you?

**Hear it.** What sounds fill this peaceful place?

You can return to this place anytime you need. It's always here, inside you.

Take one more deep breath... and when you're ready, slowly open your eyes.

You carry this peace with you. 💙"""
    }
]


def get_meditation() -> Dict:
    """Get a random meditation script."""
    return random.choice(MEDITATION_SCRIPTS)


def format_meditation(meditation: Dict) -> str:
    """Format meditation for display."""
    return meditation["script"]
