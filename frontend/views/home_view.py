"""
View controller for the Home / Exploring EduGenie Dashboard.
Features:
- "Exploring EduGenie" feature matrix (Asking questions, Explanations, Summarising, Quizzes, Learning plans)
- Fig. EDUGENIE System Architecture & Workflow Diagram
- Quick Action Launchers linking directly to each study module.
"""

import streamlit as st


def render_home_view():
    """Renders the comprehensive EduGenie Home and Exploration portal."""
    st.markdown("""
    <div style="margin-bottom: 24px;">
        <div style="background: linear-gradient(135deg, rgba(22, 33, 62, 0.7) 0%, rgba(13, 19, 36, 0.9) 100%); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 16px; padding: 26px 26px; position: relative; overflow: hidden; box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);">
            <div style="position: absolute; top: -30px; right: -30px; width: 150px; height: 150px; background: radial-gradient(circle, rgba(6, 182, 212, 0.25) 0%, transparent 70%); border-radius: 50%;"></div>
            <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 12px;">
                <div>
                    <span class="badge-tag badge-cyan" style="margin-bottom: 8px;">🚀 AI Study Assistant v2.0</span>
                    <h2 style="margin: 6px 0; font-size: 1.85rem; font-weight: 800; color: #f8fafc;">
                        Exploring EduGenie: Autonomous Academic Suite
                    </h2>
                    <div style="color: #94a3b8; font-size: 0.95rem; max-width: 720px; line-height: 1.6;">
                        Master difficult subjects faster with calibrated multi-level explanations, interactive 3-question MCQ drills with corrective guidance, long paragraph condensing, and personalized learning plans.
                    </div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 1. Core Capabilities Grid
    st.markdown("### 🌟 Exploring EduGenie: Core Capabilities")
    
    col_f1, col_f2 = st.columns(2, gap="medium")
    
    with col_f1:
        st.markdown("""
        <div class="glass-card" style="margin-bottom: 14px; min-height: 180px;">
            <div class="glass-card-header">
                <span class="badge-tag badge-cyan">a. Asking Questions</span>
                <span style="font-weight: 700; color: #f8fafc; font-size: 1.05rem;">💬 Instant Socratic Tutor</span>
            </div>
            <div style="color: #94a3b8; font-size: 0.88rem; line-height: 1.6;">
                Clear academic doubts 24/7 with a conversational Socratic AI tutor. Debug coding logic, ask follow-up questions, or attach lecture notes for highly accurate contextual explanations.
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("👉 Launch Doubt Clarifier", key="home_nav_doubt", use_container_width=True):
            st.session_state.sidebar_module_nav = "💬 Doubt Clarifier"
            st.rerun()

        st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)

        st.markdown("""
        <div class="glass-card" style="margin-bottom: 14px; min-height: 180px;">
            <div class="glass-card-header">
                <span class="badge-tag badge-purple">b. Topic Explanations</span>
                <span style="font-weight: 700; color: #f8fafc; font-size: 1.05rem;">🎓 Adaptive Concept Explainer</span>
            </div>
            <div style="color: #94a3b8; font-size: 0.88rem; line-height: 1.6;">
                Deconstruct abstract STEM and humanities topics across 4 calibrated cognitive depths (ELI5 to Industry Pro) with vivid real-world analogies, deep mechanics, and text-to-speech audio lessons.
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("👉 Launch Concept Explainer", key="home_nav_explain", use_container_width=True):
            st.session_state.sidebar_module_nav = "🎓 Concept Explainer"
            st.rerun()

    with col_f2:
        st.markdown("""
        <div class="glass-card" style="margin-bottom: 14px; min-height: 180px;">
            <div class="glass-card-header">
                <span class="badge-tag badge-green">c. Summarising Content</span>
                <span style="font-weight: 700; color: #f8fafc; font-size: 1.05rem;">📝 Notes Summarizer & Cheat-Sheet</span>
            </div>
            <div style="color: #94a3b8; font-size: 0.88rem; line-height: 1.6;">
                Condense lengthy textbook chapters, PDFs, and lecture transcripts into executive overviews, core glossaries, structured bullet notes, and 1-page high-yield exam cheat-sheets.
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("👉 Launch Notes Summarizer", key="home_nav_summary", use_container_width=True):
            st.session_state.sidebar_module_nav = "📝 Notes Summarizer"
            st.rerun()

        st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)

        st.markdown("""
        <div class="glass-card" style="margin-bottom: 14px; min-height: 180px;">
            <div class="glass-card-header">
                <span class="badge-tag badge-amber">d. Generating Quizzes</span>
                <span style="font-weight: 700; color: #f8fafc; font-size: 1.05rem;">❓ Smart 3-MCQ Engine & Flashcards</span>
            </div>
            <div style="color: #94a3b8; font-size: 0.88rem; line-height: 1.6;">
                Synthesizes <b>3 targeted questions with 4 options each</b>. Evaluates choices, corrects wrong selections with detailed rationale, provides stepwise solution guidance, and recommends learning resources.
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("👉 Launch Smart Quiz Suite", key="home_nav_quiz", use_container_width=True):
            st.session_state.sidebar_module_nav = "❓ Quiz & Flashcards"
            st.rerun()

    # 2. Personalized Learning Plan Highlight Card
    st.markdown("<div style='margin-top: 24px;'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(168, 85, 247, 0.15) 100%); border: 1px solid rgba(168, 85, 247, 0.35); border-radius: 14px; padding: 22px; margin-bottom: 18px; box-shadow: 0 8px 24px rgba(0, 0, 0, 0.25);">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
            <div>
                <span class="badge-tag badge-purple">e. Personalized Roadmaps</span>
                <h4 style="margin: 6px 0 2px 0; color: #f8fafc; font-size: 1.2rem;">🗺️ Get a Personalized Learning Plan</h4>
                <div style="color: #94a3b8; font-size: 0.9rem; line-height: 1.5;">
                    Input your target skill, timeframe, and daily hours to receive a week-by-week roadmap with curated textbooks, courses, and practice drills.
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("🚀 Create My Personalized Learning Plan", key="home_nav_plan", type="primary", use_container_width=True):
        st.session_state.sidebar_module_nav = "🗺️ Learning Plan"
        st.rerun()

    # 3. System Architecture Diagram: Fig. EDUGENIE
    st.markdown("---")
    st.markdown("### 📐 Fig. EDUGENIE: AI Study Assistant Architecture")
    
    st.markdown("""
    <div style="background: #090e1c; border: 1px solid rgba(255, 255, 255, 0.09); border-radius: 14px; padding: 24px; margin-bottom: 20px; box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35);">
        <div style="text-align: center; color: #38bdf8; font-weight: 700; font-size: 0.95rem; margin-bottom: 16px; letter-spacing: 0.5px;">
            FIG. EDUGENIE: END-TO-END MULTIMODAL INTELLIGENCE PIPELINE
        </div>
        <div style="display: flex; justify-content: space-around; align-items: center; flex-wrap: wrap; gap: 12px; text-align: center;">
            <div style="background: rgba(22, 33, 62, 0.7); border: 1px solid rgba(56, 189, 248, 0.35); border-radius: 12px; padding: 16px; flex: 1; min-width: 140px; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);">
                <div style="font-size: 1.6rem;">📥</div>
                <div style="font-weight: 700; color: #f1f5f9; font-size: 0.88rem; margin-top: 4px;">User Inputs</div>
                <div style="font-size: 0.74rem; color: #94a3b8;">Topic • Text • PDF • Notes</div>
            </div>
            <div style="color: #38bdf8; font-size: 1.4rem; font-weight: 700;">➔</div>
            <div style="background: rgba(22, 33, 62, 0.7); border: 1px solid rgba(168, 85, 247, 0.35); border-radius: 12px; padding: 16px; flex: 1; min-width: 140px; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);">
                <div style="font-size: 1.6rem;">🧠</div>
                <div style="font-weight: 700; color: #f1f5f9; font-size: 0.88rem; margin-top: 4px;">Gemini LLM Engine</div>
                <div style="font-size: 0.74rem; color: #94a3b8;">gemini-1.5-flash & Prompts</div>
            </div>
            <div style="color: #38bdf8; font-size: 1.4rem; font-weight: 700;">➔</div>
            <div style="background: rgba(22, 33, 62, 0.7); border: 1px solid rgba(16, 185, 129, 0.35); border-radius: 12px; padding: 16px; flex: 1; min-width: 140px; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);">
                <div style="font-size: 1.6rem;">⚡</div>
                <div style="font-weight: 700; color: #f1f5f9; font-size: 0.88rem; margin-top: 4px;">Structured Parsers</div>
                <div style="font-size: 0.74rem; color: #94a3b8;">JSON • Markdown • gTTS Audio</div>
            </div>
            <div style="color: #38bdf8; font-size: 1.4rem; font-weight: 700;">➔</div>
            <div style="background: rgba(22, 33, 62, 0.7); border: 1px solid rgba(245, 158, 11, 0.35); border-radius: 12px; padding: 16px; flex: 1; min-width: 140px; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);">
                <div style="font-size: 1.6rem;">📊</div>
                <div style="font-weight: 700; color: #f1f5f9; font-size: 0.88rem; margin-top: 4px;">Smart Outputs</div>
                <div style="font-size: 0.74rem; color: #94a3b8;">3-MCQ Drill • Cheat-Sheet • Plan</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
