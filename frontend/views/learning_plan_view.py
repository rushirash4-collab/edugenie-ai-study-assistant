"""
View controller for Module 5: Personalized Learning Plan & Curriculum Roadmap.
Implements custom goal intake, level selection, timeframe scheduling,
curated resource directories, and stepwise milestone tracking.
"""

import streamlit as st
from backend.services import generate_learning_plan, generate_tts_audio
from backend.parsers import extract_delimited_section, extract_text_from_upload
from frontend.components import render_export_buttons


def render_learning_plan_view(api_key: str, model_name: str):
    """Renders the personalized learning plan generator."""
    st.markdown("""
    <div style="margin-bottom: 20px;">
        <h2 style="margin: 0; display: flex; align-items: center; gap: 10px; font-size: 1.5rem;">
            <span>🗺️</span> Personalized Learning Plan & Roadmap
        </h2>
        <div style="color: #94a3b8; font-size: 0.92rem; margin-top: 4px;">
            Set your target skill or exam goal, define your timeframe, and receive a customized week-by-week curriculum with curated learning resources and step-by-step guidance.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Preset Goal Suggestions
    st.markdown("""
    <div style="margin-bottom: 12px; display: flex; align-items: center; gap: 6px; flex-wrap: wrap;">
        <span style="font-size: 0.82rem; color: #94a3b8; font-weight: 600;">⚡ Popular Roadmap Goals:</span>
    </div>
    """, unsafe_allow_html=True)

    col_g1, col_g2, col_g3, col_g4 = st.columns(4)
    sample_goals = [
        "Master Machine Learning in Python",
        "Ace Data Structures & Algorithms",
        "AP Biology Exam Prep in 4 Weeks",
        "Full-Stack Web Dev with React & Node"
    ]
    for idx, (c, goal_text) in enumerate(zip([col_g1, col_g2, col_g3, col_g4], sample_goals)):
        with c:
            if st.button(f"🎯 {goal_text[:25]}...", key=f"plan_preset_{idx}", use_container_width=True, help=goal_text):
                st.session_state["plan_goal_input"] = goal_text
                st.rerun()

    col_input, col_output = st.columns([1, 1.4], gap="large")

    with col_input:
        with st.container(border=True):
            st.markdown("<div style='font-weight: 700; font-size: 0.95rem; color: #f8fafc; margin-bottom: 10px;'>⚙️ Learning Plan Parameters</div>", unsafe_allow_html=True)

            goal = st.text_input(
                "Learning Goal / Target Subject:",
                value=st.session_state.get("plan_goal_input", ""),
                placeholder="e.g., Master Calculus 1, Learn Rust from scratch, Prepare for AWS Cloud Cert",
                key="plan_goal_input_field"
            )

            col_sub1, col_sub2 = st.columns(2)
            with col_sub1:
                level = st.selectbox(
                    "Current Level:",
                    ["Complete Beginner", "Intermediate", "Advanced"],
                    index=0,
                    key="plan_level_select"
                )
            with col_sub2:
                timeframe = st.selectbox(
                    "Timeframe:",
                    ["2 Weeks (Sprint)", "4 Weeks (1 Month)", "8 Weeks (2 Months)", "12 Weeks (Full Semester)"],
                    index=1,
                    key="plan_timeframe_select"
                )

            daily_hours = st.slider("Daily Study Commitment (Hours/Day):", min_value=0.5, max_value=8.0, value=1.5, step=0.5, key="plan_hours_slider")

            uploaded_syllabus = st.file_uploader(
                "📎 Optional: Upload Course Syllabus / Exam Outline (.pdf, .txt):",
                type=["pdf", "txt"],
                key="plan_syllabus_uploader"
            )

            generate_plan_btn = st.button("🚀 Generate My Personalized Plan", type="primary", use_container_width=True, key="plan_submit_btn")

        if generate_plan_btn:
            active_goal = goal.strip() or st.session_state.get("plan_goal_input", "").strip()
            if not api_key:
                st.error("🔑 Please enter a valid Gemini API Key in the sidebar or `.env` file.")
            elif not active_goal and not uploaded_syllabus:
                st.warning("Please specify your learning goal or attach a syllabus outline.")
            else:
                syllabus_text = extract_text_from_upload(uploaded_syllabus)

                weeks_map = {
                    "2 Weeks (Sprint)": 2,
                    "4 Weeks (1 Month)": 4,
                    "8 Weeks (2 Months)": 8,
                    "12 Weeks (Full Semester)": 12
                }
                weeks_num = weeks_map.get(timeframe, 4)

                with st.spinner("Synthesizing tailored curriculum, weekly milestones, and resource directory..."):
                    result = generate_learning_plan(
                        api_key=api_key,
                        model_name=model_name,
                        goal=active_goal if active_goal else (uploaded_syllabus.name if uploaded_syllabus else "Target Curriculum"),
                        current_level=level,
                        timeframe_weeks=weeks_num,
                        daily_hours=daily_hours,
                        uploaded_context=syllabus_text
                    )

                    if result["success"]:
                        st.session_state.learning_plan_output = {
                            "goal": active_goal if active_goal else (uploaded_syllabus.name if uploaded_syllabus else "Syllabus Study Plan"),
                            "content": result["content"],
                            "level": level,
                            "timeframe": timeframe,
                            "hours": daily_hours
                        }
                        # Pre-generate Audio Stream
                        try:
                            audio_stream = generate_tts_audio(result["content"])
                            st.session_state.learning_plan_audio = audio_stream.getvalue()
                        except Exception:
                            st.session_state.learning_plan_audio = None
                        st.rerun()
                    else:
                        st.error(result["error"])

    with col_output:
        if st.session_state.get("learning_plan_output"):
            plan_data = st.session_state.learning_plan_output
            raw_plan = plan_data["content"]

            st.markdown(f"""
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px; flex-wrap: wrap; gap: 8px;">
                <div style="display: flex; gap: 6px; align-items: center;">
                    <span class="badge-tag badge-purple">🎯 Goal: {plan_data['goal']}</span>
                    <span class="badge-tag badge-blue">{plan_data['level']}</span>
                    <span class="badge-tag badge-cyan">⏱️ {plan_data['timeframe']} ({plan_data['hours']} hrs/day)</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            if st.session_state.get("learning_plan_audio"):
                st.audio(st.session_state.learning_plan_audio, format="audio/mp3")

            tab_p1, tab_p2, tab_p3, tab_p4, tab_p5, tab_p_all = st.tabs([
                "📌 Overview", "🚩 Milestones", "📅 Weekly Plan", "📚 Resources", "🛠️ Projects", "📑 Full Plan"
            ])

            with tab_p1:
                st.markdown(extract_delimited_section(raw_plan, "Executive Overview") or raw_plan)
            with tab_p2:
                st.markdown(extract_delimited_section(raw_plan, "Stepwise Milestone Roadmap") or "See Weekly Plan tab.")
            with tab_p3:
                st.markdown(extract_delimited_section(raw_plan, "Week-by-Week Action Plan") or "See Full Plan tab.")
            with tab_p4:
                st.markdown(extract_delimited_section(raw_plan, "Curated Learning Resources") or "See Full Plan tab.")
            with tab_p5:
                st.markdown(extract_delimited_section(raw_plan, "Practice Projects & Assessment") or "See Full Plan tab.")
            with tab_p_all:
                st.markdown(raw_plan)

            render_export_buttons(f"{plan_data['goal']}_learning_plan", raw_plan, key_prefix="plan_export")
        else:
            st.markdown("""
            <div style="background: rgba(18, 26, 48, 0.4); border: 1px dashed rgba(255, 255, 255, 0.12); border-radius: 14px; padding: 46px 20px; text-align: center; color: #64748b;">
                <div style="font-size: 2.4rem; margin-bottom: 8px;">🗺️</div>
                <div style="font-size: 1.05rem; font-weight: 600; color: #94a3b8; margin-bottom: 4px;">Learning Plan Generator Ready</div>
                <div style="font-size: 0.86rem; color: #64748b;">Enter your target goal or attach a syllabus on the left and click <b>Generate My Personalized Plan</b>.</div>
            </div>
            """, unsafe_allow_html=True)
