"""
Reusable Streamlit UI components and widgets for EduGenie.
Featuring an interactive, functional sidebar equipped with:
- Module Navigation (Home, Explainer, Quiz, Summarizer, Doubt Clarifier, Learning Plan)
- User Profile & Session Logout
- One-Click Quick Launchers
- Live Study Session Activity Metrics
- Polished Export & Download Hub
"""

from typing import Tuple
import streamlit as st
from backend.gemini_client import resolve_api_key
from backend.parsers import generate_export_document


def render_hero_banner():
    """Renders the flagship subtle glass hero header."""
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-top-row">
            <h1 class="hero-title">
                <span>🎓 EduGenie</span>
                <span style="font-size: 0.74rem; color: #38bdf8; font-weight: 600; padding: 3px 10px; background: rgba(56, 189, 248, 0.12); border-radius: 20px; border: 1px solid rgba(56, 189, 248, 0.35);">Autonomous Academic Assistant</span>
            </h1>
            <div class="pill-container">
                <span class="feature-pill">💬 Socratic Doubts</span>
                <span class="feature-pill">🎓 Deep Explanations</span>
                <span class="feature-pill">❓ 3-MCQ Engine</span>
                <span class="feature-pill">📝 Exam Digests</span>
                <span class="feature-pill">🗺️ Roadmaps</span>
            </div>
        </div>
        <div class="hero-subtitle">
            Autonomous academic assistant: Asking questions, topic explanations, long paragraph condensing, 3-question MCQ drills with corrective guidance, and personalized learning roadmaps.
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_sidebar() -> Tuple[str, str, str]:
    """
    Renders a fully interactive, functional sidebar:
    1. App Identity & Authenticated User Card
    2. Primary Study Tool Navigation
    3. Quick Subject Presets
    4. Live Study Progress & Session Metrics
    5. Action toolbar (Reset Session, Sign Out)
    """
    api_key = resolve_api_key()
    model_name = "gemini-1.5-flash"

    # Initialize study session counters
    if "concepts_explored" not in st.session_state:
        st.session_state.concepts_explored = 0
    if "quizzes_completed" not in st.session_state:
        st.session_state.quizzes_completed = 0
    if "doubts_resolved" not in st.session_state:
        st.session_state.doubts_resolved = 0

    with st.sidebar:
        # 1. App Identity & User Profile Card
        user_info = st.session_state.get("authenticated_user", {"name": "Scholar", "email": "student@edugenie.ai"})
        st.markdown(f"""
        <div class="sidebar-brand-card">
            <div class="brand-icon">🎓</div>
            <div>
                <div class="brand-title">EduGenie</div>
                <div class="brand-subtitle">👤 {user_info.get('name', 'Scholar')}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 2. Primary Navigation
        with st.container(border=True):
            st.markdown("<div style='font-weight: 700; font-size: 0.88rem; color: #f1f5f9; margin-bottom: 8px;'>📚 Study Tools</div>", unsafe_allow_html=True)
            
            nav_options = [
                "🏠 Home & Overview",
                "🎓 Concept Explainer",
                "❓ Quiz & Flashcards",
                "📝 Notes Summarizer",
                "💬 Doubt Clarifier",
                "🗺️ Learning Plan"
            ]

            if "sidebar_module_nav" not in st.session_state or st.session_state.sidebar_module_nav not in nav_options:
                st.session_state.sidebar_module_nav = nav_options[0]

            selected_module = st.radio(
                "Navigation:",
                options=nav_options,
                key="sidebar_module_nav",
                label_visibility="collapsed"
            )

        # 3. Interactive Quick Subject Presets
        with st.container(border=True):
            st.markdown("<div style='font-weight: 700; font-size: 0.88rem; color: #f1f5f9; margin-bottom: 6px;'>⚡ Quick Subject Presets</div>", unsafe_allow_html=True)
            st.caption("Click to load a topic into your active tool:")

            col_q1, col_q2 = st.columns(2)
            with col_q1:
                if st.button("🧬 Biology", key="side_preset_bio", use_container_width=True):
                    st.session_state["concept_topic_input"] = "Photosynthesis & Cellular Respiration"
                    st.session_state["quiz_topic_input"] = "Cellular Biology & Genetics"
                    st.session_state["plan_goal_input"] = "Master AP Biology in 4 Weeks"
                    st.rerun()
                if st.button("⚛️ Physics", key="side_preset_phy", use_container_width=True):
                    st.session_state["concept_topic_input"] = "Quantum Mechanics & Superposition"
                    st.session_state["quiz_topic_input"] = "Newtonian Mechanics & Laws of Motion"
                    st.session_state["plan_goal_input"] = "Understand Modern Quantum Physics"
                    st.rerun()
            with col_q2:
                if st.button("💻 CompSci", key="side_preset_cs", use_container_width=True):
                    st.session_state["concept_topic_input"] = "Transformer Neural Networks"
                    st.session_state["quiz_topic_input"] = "Data Structures & Algorithms"
                    st.session_state["plan_goal_input"] = "Full Stack AI Engineering Roadmap"
                    st.rerun()
                if st.button("📐 Math", key="side_preset_math", use_container_width=True):
                    st.session_state["concept_topic_input"] = "Bayes' Theorem & Conditional Probability"
                    st.session_state["quiz_topic_input"] = "Calculus & Linear Algebra"
                    st.session_state["plan_goal_input"] = "Linear Algebra for Machine Learning"
                    st.rerun()

        # 4. Live Session Activity Tracker
        with st.container(border=True):
            st.markdown("<div style='font-weight: 700; font-size: 0.88rem; color: #f1f5f9; margin-bottom: 6px;'>📊 Live Session Metrics</div>", unsafe_allow_html=True)
            
            c_count = 1 if st.session_state.get("explainer_output") else 0
            quiz_list = st.session_state.get("quiz_data")
            q_count = len(quiz_list) if isinstance(quiz_list, list) else 0
            chat_list = st.session_state.get("chat_messages")
            d_count = (len(chat_list) // 2) if isinstance(chat_list, list) else 0
            p_count = 1 if st.session_state.get("learning_plan_output") else 0

            st.markdown(f"""
            <div style="font-size: 0.82rem; color: #94a3b8; line-height: 1.8;">
                <div>• 💡 Concepts Explained: <b style="color: #38bdf8;">{c_count}</b></div>
                <div>• ✍️ Active Questions: <b style="color: #c084fc;">{q_count}</b></div>
                <div>• 💬 Doubts Discussed: <b style="color: #34d399;">{d_count}</b></div>
                <div>• 🗺️ Learning Plans: <b style="color: #fbbf24;">{p_count}</b></div>
            </div>
            """, unsafe_allow_html=True)

        # 5. Session Actions & Sign Out
        st.markdown("<div style='margin-top: 6px;'></div>", unsafe_allow_html=True)
        col_side_rst, col_side_out = st.columns(2)
        with col_side_rst:
            if st.button("🔄 Reset Data", key="side_clear_all", use_container_width=True):
                st.session_state.explainer_output = None
                st.session_state.explainer_audio = None
                st.session_state.quiz_data = None
                st.session_state.user_quiz_answers = {}
                st.session_state.quiz_submitted = False
                st.session_state.flashcards_data = None
                st.session_state.summarizer_output = None
                st.session_state.summarizer_audio = None
                st.session_state.chat_messages = []
                st.session_state.learning_plan_output = None
                st.session_state.learning_plan_audio = None
                st.rerun()

        with col_side_out:
            if st.button("🚪 Sign Out", key="side_logout_btn", use_container_width=True):
                st.session_state.authenticated_user = None
                st.rerun()

        # Connection Status
        if api_key:
            st.markdown('<div style="text-align: center; margin-top: 10px;"><span class="badge-tag badge-green">🟢 Gemini AI Connected</span></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div style="text-align: center; margin-top: 10px;"><span class="badge-tag badge-amber">⚠️ No Gemini Key (.env / secrets)</span></div>', unsafe_allow_html=True)

    return api_key, model_name, selected_module


def render_export_buttons(title: str, markdown_content: str, key_prefix: str = "export"):
    """Renders 3-column export download buttons (.md, .txt, .html)."""
    st.markdown("<div style='margin-top: 18px;'></div>", unsafe_allow_html=True)
    st.markdown("<div style='font-weight: 700; font-size: 0.92rem; color: #f1f5f9; margin-bottom: 8px;'>📥 Export Study Package:</div>", unsafe_allow_html=True)
    col_d1, col_d2, col_d3 = st.columns(3)
    
    file_slug = title.lower().replace(" ", "_")[:30]

    with col_d1:
        st.download_button(
            label="📄 Markdown Note (.md)",
            data=markdown_content,
            file_name=f"{file_slug}_notes.md",
            mime="text/markdown",
            key=f"{key_prefix}_md",
            use_container_width=True
        )
    with col_d2:
        plain_text = generate_export_document(title, markdown_content, doc_format="txt")
        st.download_button(
            label="📝 Text File (.txt)",
            data=plain_text,
            file_name=f"{file_slug}_notes.txt",
            mime="text/plain",
            key=f"{key_prefix}_txt",
            use_container_width=True
        )
    with col_d3:
        html_doc = generate_export_document(title, markdown_content, doc_format="html")
        st.download_button(
            label="🌐 Printable HTML (.html)",
            data=html_doc,
            file_name=f"{file_slug}_notes.html",
            mime="text/html",
            key=f"{key_prefix}_html",
            use_container_width=True
        )
