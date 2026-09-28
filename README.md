# 🎓 EduGenie: Autonomous Google Gemini Powered Learning Assistant

EduGenie is a full-featured, multimodal AI study companion designed to enhance personalized learning using Google's state-of-the-art **Gemini Large Language Models** (`gemini-1.5-flash`, `gemini-2.0-flash`, `gemini-1.5-pro`), **Streamlit**, **PyPDF**, and **gTTS**.

---

## 🚀 Key Modules & Capabilities

1. 🔐 **Authentication & Student Accounts:**
   - Dedicated, elegant glassmorphic Sign In and Sign Up portals with persistent account sessions.

2. 🏠 **Home & System Exploration Dashboard:**
   - Interactive feature matrix with quick navigation launchers and the complete FIG. EDUGENIE system pipeline architecture visualizer.

3. 🎓 **Adaptive Concept Explainer & Multimodal Tutor:**
   - Calibrated explanations across 4 audience tiers (*ELI5*, *High School*, *Undergraduate*, *Professional*).
   - Ingests textbook pages, diagrams (`.png`, `.jpg`), and PDFs (`.pdf`).
   - 🔊 Built-in **Text-to-Speech (TTS)** for auditory learning.
   - Multi-format exports: Markdown (`.md`), Plain Text (`.txt`), and Printable HTML (`.html`).

4. ❓ **Smart 3-MCQ Quiz & Flashcard Engine:**
   - Dynamic Multiple-Choice Questions (3 MCQs with 4 options each) with automatic evaluation, corrective feedback, stepwise solutions, and recommended resources.
   - 2-sided active recall flashcards with question front & answer back.

5. 📝 **Multimodal Notes Summarizer & Cheat-Sheet:**
   - Digests lecture transcripts, articles, or uploaded documents up to 12,000+ characters.
   - Extracts Executive Overviews, Key Glossaries, Structured Notes, and 1-Page Exam Cheat Sheets.
   - Audio recap synthesis and multi-format file downloads.

6. 💬 **Instant Socratic Doubt Clarifier:**
   - 24/7 personalized AI tutor interface with persistent multi-turn conversational context, document attachment, and starter chips.

7. 🗺️ **Personalized Learning Plan & Roadmap:**
   - Tailored week-by-week curriculum roadmaps, milestones, daily commitment tracking, and curated resource directories.

---

## 🛠️ Project Structure

```
.
├── app.py                      # Main Streamlit application entry point
├── requirements.txt            # Python dependencies (Streamlit, Google GenAI, PyPDF, gTTS, Pillow)
├── test_app.py                 # Automated unit test suite
├── PROJECT_REPORT.md           # Engineering, architecture & evaluation report
├── .env.example                # Environment variable template
├── .gitignore                  # Git exclusion rules
├── .streamlit/
│   ├── config.toml             # Custom Lumina Obsidian theme & server settings
│   └── secrets.toml.example    # Cloud secrets configuration example
├── backend/
│   ├── auth.py                 # User authentication & session management
│   ├── gemini_client.py        # Gemini API client & error handling
│   ├── parsers.py              # File extractors (PDF/images), clean JSON & exports
│   ├── services.py             # Core educational AI generation logic
│   └── users.json              # Local user credentials store
├── frontend/
│   ├── styles.py               # Lumina Obsidian design system & CSS
│   ├── components.py           # Sidebar, navigation, metrics & export buttons
│   └── views/
│       ├── auth_view.py        # Sign In & Sign Up pages
│       ├── home_view.py        # Overview & architecture dashboard
│       ├── explainer_view.py   # Concept explainer module
│       ├── quiz_view.py        # 3-MCQ quiz & flashcard deck
│       ├── summarizer_view.py  # Notes digest & cheat-sheet
│       ├── chat_view.py        # Socratic chat doubt solver
│       └── learning_plan_view.py # Personalized learning plan
└── README.md                   # Setup & deployment documentation
```

---

## 📦 Local Installation & Setup

### 1. Prerequisites
- Python 3.9+ installed on your system.
- A **Google Gemini API Key** (Obtain a free key from [Google AI Studio](https://aistudio.google.com/app/apikey)).

### 2. Activate Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure API Key
Create a `.env` file in the root directory:
```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
```

### 5. Run Automated Tests
```bash
python -m unittest test_app.py
```

### 6. Run the Application
```bash
streamlit run app.py
```

The app will launch in your browser at `http://localhost:8501`.

---

## 🌐 Deploying to Streamlit Community Cloud

1. Push your repository to **GitHub**.
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in.
3. Select your repository and set `app.py` as the main file.
4. Under **Advanced Settings** -> **Secrets**, provide:
   ```toml
   GEMINI_API_KEY = "your_actual_gemini_api_key"
   ```
5. Deploy!
