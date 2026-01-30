# Sukoon - Advanced RAG Mental Wellness Companion

> *"Sukoon" means peace in Urdu. Everyone deserves a moment of calm.*

**Sukoon** is an advanced, RAG-based AI companion designed to respond like a grounded, emotionally intelligent human — not a chatbot. It's built for those moments when life feels heavy and you need a supportive, non-judgmental presence to sit with you.

---

## What Makes Sukoon Different?

**🧠 RAG-Based Intelligence** — Sukoon is grounded in a curated knowledge base of wellness wisdom. It retrieves "lived insights" and weaves them naturally into your conversation.

**❤️ Human-First Responses** — Every response follows a mandatory emotional flow: *Acknowledgment → Validation → Gentle Support → Soft Invitation*. It treats you like a person, not a user.

**🕊️ Calm & Grounded** — No bullet points, no instructional tone, and no clinical terminology. Sukoon uses gentle pauses and thoughtful language to create a safe space.

**🌬️ Integrated Wellness Exercises** — Access breathing techniques, grounding practices, and reflective journaling prompts, all humanized and offered with care.

---

## How It Works

Sukoon uses a **Retrieval-Augmented Generation (RAG)** pipeline to ensure its support is grounded in meaningful wellness practices:

1. **Context Retrieval**: Your message is embedded and matched against a local vector database (**ChromaDB**) containing humanized wellness wisdom.
2. **Emotional Analysis**: Sukoon analyzes your sentiment and detects emotional intensity behind the scenes.
3. **LLM Generation**: Using **LLaMA 3.3 70B** (via Groq), Sukoon weaves the retrieved wisdom into a human-first response that prioritizes your safety and emotional state.
4. **Crisis Guardrails**: Built-in safety detection monitors for high distress and gently encourages real-world support when needed.

---

## Getting Started

**1. Get your free API key**
→ Sign up at [console.groq.com](https://console.groq.com) (takes 2 minutes)

**1. Clone the repository**
```bash
git clone https://github.com/moiz-mansoori/Sukoon-Mental-Wellness-Companion.git
cd Sukoon-Mental-Wellness-Companion
```

**2. Set up a virtual environment (Recommended)**
```bash
python -m venv venv
.\venv\Scripts\activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Configure your environment**
Create a `.env` file in the root directory:
```text
GROQ_API_KEY=your_groq_key_here
```

**5. Launch Sukoon**
```bash
streamlit run app.py
```

---

## Built With

- **Streamlit** — Calming, premium dark-themed interface
- **Groq API** — Ultra-fast inference with LLaMA 3.3 70B (Core Brain)
- **ChromaDB** — Local vector storage for wellness wisdom
- **Sentence Transformers** — Local embedding generation (No API key needed)
- **TextBlob** — Emotional sentiment context detection

---

## Project Structure

```text
├── app.py                 # Main application & UI
├── rag/                   # RAG Architecture Module
│   ├── embeddings.py      # Local Embedding Service
│   ├── vector_store.py    # ChromaDB integration
│   ├── retriever.py       # Context retrieval logic
│   └── knowledge_loader.py # KB indexer
├── knowledge_base/        # Curated Wellness Wisdom (JSON)
├── prompts/
│   └── templates.py       # Human-first behavior definition
├── config/
│   └── settings.py        # Configuration & themes
├── utils/
│   ├── sentiment.py       # Emotion detection
│   ├── crisis_detector.py # Safety guardrails
│   └── coping_techniques.py # Core wellness exercises
├── .env                   # Your API keys
└── requirements.txt       # Dependencies
```

---

## A Note on Mental Health

Sukoon is a companion, not a replacement for professional help. If you're going through something serious, please reach out to a therapist, counselor, or a crisis helpline. You deserve real support. 💙

---

## The Philosophy

Mental wellness isn't about "fixing" yourself. It's about finding moments of peace amidst the chaos. Sukoon is here to help you find those moments by listening deeply and being truly present.

Take care of yourself. You matter. 💙

---

*Made by Moiz Ahmed Mansoori*
