# Sukoon - Mental Wellness Companion

> *"Sukoon" means peace in Urdu. Everyone deserves a moment of calm.*

Hey there 👋

**Sukoon** is your AI companion for those moments when life feels heavy. Whether you're dealing with anxiety, stress, sadness, or just need someone to listen — Sukoon is here for you.

No judgment. No pressure. Just support.

---

## What Can Sukoon Do?

**Listen & Respond** — Have a real conversation about what's on your mind. Sukoon understands context and responds with genuine empathy.

**Match Your Mood** — Feeling anxious? Stressed? Sad? Select your mood and Sukoon adapts its approach to what you need most.

**Offer Quick Relief** — Sometimes you need something right away:
- 🌬️ Breathing exercises to calm your nerves
- 🌍 Grounding techniques to bring you back to the present
- 💭 Ways to reframe negative thoughts
- 📝 Journaling prompts to process emotions
- ✨ Affirmations when you need a reminder of your worth
- 🧘 Quick meditations for instant calm

---

## Getting Started

**1. Get your free API key**
→ Sign up at [console.groq.com](https://console.groq.com) (takes 2 minutes)

**2. Set up the project**
```bash
git clone https://github.com/moiz-mansoori/AI-Mental-Wellness-Chatbot.git
cd AI-Mental-Wellness-Chatbot
pip install -r requirements.txt
```

**3. Add your API key**
Create a `.env` file:
```
GROQ_API_KEY=your_key_here
```

**4. Run it**
```bash
streamlit run app.py
```

That's it. Open `localhost:8501` and start talking.

---

## How It Works

Sukoon uses **LLaMA 3.3** through Groq's ultra-fast infrastructure. Responses come back in milliseconds, not seconds — so conversations feel natural and fluid.

The app also includes:
- **Sentiment detection** to understand how you're feeling
- **Crisis awareness** to respond appropriately when things get tough
- **Conversation memory** so it remembers what you've shared

---

## A Note on Mental Health

Sukoon is a companion, not a replacement for professional help.

If you're going through something serious, please reach out to a therapist, counselor, or someone you trust. You deserve real support.

---

## Built With

- **Streamlit** — Clean, simple interface
- **Groq API** — Lightning-fast AI responses
- **LLaMA 3.3 70B** — Smart, empathetic conversations
- **TextBlob** — Understanding emotional context

---

## Project Structure

```
├── app.py                 # Main application
├── config/
│   └── settings.py        # Configuration & themes
├── prompts/
│   └── templates.py       # AI personality & responses
├── utils/
│   ├── sentiment.py       # Emotion detection
│   ├── crisis_detector.py # Safety responses
│   └── coping_techniques.py # Exercises & techniques
├── .env                   # Your API key
└── requirements.txt       # Dependencies
```

---

## Want to Contribute?

Pull requests are welcome! If you have ideas to make Sukoon better, feel free to open an issue or submit a PR.

---

## The Philosophy

Mental wellness isn't about "fixing" yourself. It's about finding moments of peace amidst the chaos. Sukoon is here to help you find those moments.

Take care of yourself. You matter. 💙

---

*Made with care by Moiz Mansoori*
