"""
Core educational business logic and generation services for EduGenie.
"""

import io
import json
import re
from typing import List, Dict, Any, Optional
from gtts import gTTS
from backend.gemini_client import get_gemini_model, handle_gemini_error
from backend.parsers import clean_json_output, extract_text_from_pdf, process_image


def generate_explanation(
    api_key: str,
    model_name: str = "gemini-1.5-flash",
    topic: str = "",
    audience_level: str = "Beginner / High School",
    output_style: str = "Balanced & Structured",
    uploaded_file_bytes: Optional[bytes] = None,
    file_type: Optional[str] = None
) -> Dict[str, Any]:
    """Generates structured concept explanation with optional multimodal document/diagram intake."""
    try:
        model = get_gemini_model(api_key, model_name or "gemini-1.5-flash", temperature=0.6)
        if not model:
            return {"success": False, "error": "Model initialization failed. Please check your API key."}

        prompt_text = f"""
        You are an elite academic tutor and master explainer. Provide a deeply intuitive and comprehensive explanation.
        
        Topic/Subject: {topic if topic else 'Uploaded Study Document/Diagram'}
        Target Level: {audience_level}
        Focus Style: {output_style}

        Break your response down into the following structured sections:
        [SECTION: Core Intuition]
        A simple, jargon-free overview of the fundamental idea.

        [SECTION: Deep Breakdown]
        Step-by-step breakdown of how it works, mechanisms, and key components.

        [SECTION: Real-World Analogy]
        A vivid, relatable metaphor that connects abstract theory to everyday experience.

        [SECTION: Industry Applications]
        How this is actually used in research, engineering, biology, or modern industry.

        [SECTION: Self-Check Quiz]
        3 quick questions with answers to test understanding.
        """

        content_payload: List[Any] = [prompt_text]

        if uploaded_file_bytes and file_type:
            if "image" in file_type:
                img = process_image(uploaded_file_bytes)
                if img:
                    content_payload.append(img)
                    content_payload.append("Note: Analyze the uploaded visual image/diagram and incorporate its content into your explanation.")
            elif "pdf" in file_type:
                extracted_pdf = extract_text_from_pdf(uploaded_file_bytes)
                content_payload.append(f"\nEXTRACTED PDF CONTEXT:\n{extracted_pdf[:5000]}")
            elif "text" in file_type:
                text_str = uploaded_file_bytes.decode("utf-8", errors="ignore")
                content_payload.append(f"\nEXTRACTED TEXT CONTEXT:\n{text_str[:5000]}")

        response = model.generate_content(content_payload)
        return {"success": True, "content": response.text}
    except Exception as e:
        return {"success": False, "error": handle_gemini_error(e)}


def generate_quiz(
    api_key: str,
    model_name: str = "gemini-1.5-flash",
    topic: str = "",
    num_questions: int = 3,
    difficulty: str = "Medium",
    text_context: Optional[str] = None
) -> Dict[str, Any]:
    """Generates dynamic multiple-choice questions with 4 options each, stepwise guidance, and learning resources."""
    try:
        model = get_gemini_model(api_key, model_name or "gemini-1.5-flash", temperature=0.3)
        if not model:
            return {"success": False, "error": "Model initialization failed. Please check your API key."}

        context_clause = ""
        if text_context and text_context.strip():
            context_clause = f"\n\nBase the questions strictly on the following source material:\n\"\"\"{text_context[:10000]}\"\"\"\n"

        quiz_prompt = f"""
        You are an expert academic examiner. Generate a {num_questions}-question multiple choice quiz on '{topic if topic else 'the provided study material'}' with difficulty '{difficulty}'.{context_clause}
        Every question MUST have exactly 4 distinct options.
        Include detailed explanations, stepwise guidance on how to solve/arrive at the right answer, and curated resource recommendations where the student can learn more.
        
        You MUST respond ONLY with a valid JSON array of objects. Do not include markdown preamble or text outside JSON.
        Format:
        [
          {{
            "id": 1,
            "question": "Question text here?",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "correct_answer": "Option A",
            "explanation": "Why this answer is correct and why other options are wrong.",
            "stepwise_guidance": "Step 1: ..., Step 2: ...",
            "recommended_resources": "Recommended reading, textbook chapter, or documentation topic to master this concept."
          }}
        ]
        """
        response = model.generate_content(quiz_prompt)
        cleaned_json = clean_json_output(response.text)
        parsed_quiz = json.loads(cleaned_json)
        return {"success": True, "data": parsed_quiz}
    except Exception as e:
        return {"success": False, "error": handle_gemini_error(e)}


def generate_flashcards(
    api_key: str,
    model_name: str = "gemini-1.5-flash",
    topic: str = "",
    count: int = 5,
    text_context: Optional[str] = None
) -> Dict[str, Any]:
    """Generates active-recall study flashcards from topic or uploaded document context."""
    try:
        model = get_gemini_model(api_key, model_name or "gemini-1.5-flash", temperature=0.4)
        if not model:
            return {"success": False, "error": "Model initialization failed. Please check your API key."}

        context_clause = ""
        if text_context and text_context.strip():
            context_clause = f"\n\nExtract flashcards strictly from this source material:\n\"\"\"{text_context[:10000]}\"\"\"\n"

        fc_prompt = f"""
        Create {count} high-yield study flashcards for '{topic if topic else 'the provided material'}'.{context_clause}
        Return ONLY a valid JSON array of objects with keys 'front' (question or concept) and 'back' (concise, clear answer/definition).
        Format:
        [
          {{"front": "What is overfitting?", "back": "When a model learns training data noise too closely and fails to generalize to unseen data."}}
        ]
        """
        response = model.generate_content(fc_prompt)
        cleaned_json = clean_json_output(response.text)
        parsed_fc = json.loads(cleaned_json)
        return {"success": True, "data": parsed_fc}
    except Exception as e:
        return {"success": False, "error": handle_gemini_error(e)}


def generate_summary(
    api_key: str,
    model_name: str = "gemini-1.5-flash",
    text_content: str = "",
    summary_depth: str = "In-Depth Structured Notes"
) -> Dict[str, Any]:
    """Summarizes study notes and extracts cheat-sheets."""
    try:
        model = get_gemini_model(api_key, model_name or "gemini-1.5-flash", temperature=0.3)
        if not model:
            return {"success": False, "error": "Model initialization failed. Please check your API key."}

        prompt = f"""
        You are an expert academic summarizer. Process the provided study notes at detail level: '{summary_depth}'.

        STUDY NOTES:
        \"\"\"{text_content[:12000]}\"\"\"

        Organize your response with these exact delimiters:
        [SECTION: Overview]
        3-4 sentences giving the high-level executive summary.

        [SECTION: Key Glossary]
        Table or bullet list of core terms, formulas, and crisp definitions.

        [SECTION: Structured Notes]
        In-depth categorised bullet points covering all critical mechanisms.

        [SECTION: One-Page Cheat-Sheet]
        Formulas, laws, rules of thumb, and must-know exam takeaways.
        """
        response = model.generate_content(prompt)
        return {"success": True, "content": response.text}
    except Exception as e:
        return {"success": False, "error": handle_gemini_error(e)}


def chat_doubt_solver(
    api_key: str,
    model_name: str = "gemini-1.5-flash",
    conversation_history: List[Dict[str, Any]] = None,
    user_query: str = "",
    context_text: Optional[str] = None
) -> Dict[str, Any]:
    """Processes interactive Socratic doubt clarification with conversational history and optional context."""
    try:
        model = get_gemini_model(api_key, model_name or "gemini-1.5-flash", temperature=0.5)
        if not model:
            return {"success": False, "error": "Model initialization failed. Please check your API key."}

        gemini_history = []
        for msg in (conversation_history or []):
            role = "user" if msg.get("role") == "user" else "model"
            gemini_history.append({
                "role": role,
                "parts": [msg.get("content", "")]
            })

        chat = model.start_chat(history=gemini_history)
        
        system_prefix = "You are EduGenie, a supportive, patient, and world-class AI tutor. Answer questions clearly, provide step-by-step guidance, and format formulas or code cleanly with markdown."
        if context_text and context_text.strip():
            system_prefix += f"\n\nReference Material / Uploaded Context:\n\"\"\"{context_text[:8000]}\"\"\"\n"
        system_prefix += "\n\nStudent Query: "
        
        response = chat.send_message(system_prefix + user_query)
        return {"success": True, "reply": response.text}
    except Exception as e:
        return {"success": False, "error": handle_gemini_error(e)}


def generate_learning_plan(
    api_key: str,
    model_name: str = "gemini-1.5-flash",
    goal: str = "",
    current_level: str = "Beginner",
    timeframe_weeks: int = 4,
    daily_hours: float = 1.5,
    uploaded_context: Optional[str] = None
) -> Dict[str, Any]:
    """Generates a personalized step-by-step learning plan with curated resource recommendations."""
    try:
        model = get_gemini_model(api_key, model_name or "gemini-1.5-flash", temperature=0.4)
        if not model:
            return {"success": False, "error": "Model initialization failed. Please check your API key."}

        context_clause = ""
        if uploaded_context and uploaded_context.strip():
            context_clause = f"\n\nSyllabus / Reference Material:\n\"\"\"{uploaded_context[:10000]}\"\"\"\n"

        prompt = f"""
        You are an expert curriculum designer and master academic coach.
        Create a personalized, highly actionable step-by-step Learning Plan for the following goal:

        Target Subject / Skill Goal: {goal}
        Current Learner Proficiency: {current_level}
        Timeframe: {timeframe_weeks} Weeks
        Daily Available Study Time: {daily_hours} Hours/Day{context_clause}

        Structure your response with these exact delimiters:
        [SECTION: Executive Overview]
        A motivating summary of the learning trajectory, target mastery outcomes, and prerequisite check.

        [SECTION: Stepwise Milestone Roadmap]
        Numbered stages (Milestone 1 to Milestone N) with explicit checkpoints and mastery metrics.

        [SECTION: Week-by-Week Action Plan]
        Detailed weekly schedules breaking down daily topics, core concepts, and daily tasks.

        [SECTION: Curated Learning Resources]
        High-quality recommendations (official documentation, recommended textbooks, seminal papers, popular MOOC courses, YouTube channels, and practice platforms) from where to learn.

        [SECTION: Practice Projects & Assessment]
        Hands-on mini-projects, coding drills, or essay prompts to test practical application.
        """
        response = model.generate_content(prompt)
        return {"success": True, "content": response.text}
    except Exception as e:
        return {"success": False, "error": handle_gemini_error(e)}


def generate_tts_audio(text_content: str) -> io.BytesIO:
    """Generates MP3 audio stream using gTTS for auditory revision."""
    # Clean up markdown, section tags, formulas and links for clear voice synthesis
    cleaned = re.sub(r"\[SECTION:[^\]]*\]", " ", text_content, flags=re.IGNORECASE)
    cleaned = re.sub(r"https?://\S+", " ", cleaned)
    cleaned = re.sub(r"[`#*_\->~\[\]\(\)\{\}\$\|\\]", " ", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()[:2000]
    
    fp = io.BytesIO()
    tts = gTTS(text=cleaned, lang='en', slow=False)
    tts.write_to_fp(fp)
    fp.seek(0)
    return fp
