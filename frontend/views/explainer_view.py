"""
View controller for Module 1: Adaptive Concept Explainer & Multimodal Tutor.
Implements unified glassmorphic input cards, instant sample topic chips,
persistent audio lesson player, and responsive tabbed output.
"""

import time
import streamlit as st
from backend.services import generate_explanation, generate_tts_audio
from backend.parsers import extract_delimited_section
from frontend.components import render_export_buttons


def render_explainer_view(api_key: str, model_name: str):
    """Renders the concept explainer module with clean SaaS layout."""
    st.markdown("""
    <div style="margin-bottom: 20px;">
        <h2 style="margin: 0; display: flex; align-items: center; gap: 10px; font-size: 1.5rem;">
            <span>🎓</span> Adaptive Concept Explainer
        </h2>
        <div style="color: #94a3b8; font-size: 0.92rem; margin-top: 4px;">
            Deconstruct difficult STEM and humanities topics with calibrated depth, real-world analogies, and audio playback.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Preset Sample Topic Chips
    st.markdown("""
    <div style="margin-bottom: 12px; display: flex; align-items: center; gap: 6px; flex-wrap: wrap;">
        <span style="font-size: 0.82rem; color: #94a3b8; font-weight: 600;">⚡ Quick Sample Topics:</span>
    </div>
    """, unsafe_allow_html=True)

    chip_cols = st.columns(4)
    sample_topics = [
        "Quantum Superposition",
        "Transformer Neural Networks",
        "Photosynthesis & Light Reactions",
        "Dijkstra's Shortest Path"
    ]
    for idx, (c, topic_name) in enumerate(zip(chip_cols, sample_topics)):
        with c:
            if st.button(f"💡 {topic_name}", key=f"explainer_sample_{idx}", use_container_width=True):
                st.session_state["concept_topic_input"] = topic_name
                st.rerun()

    col_input, col_output = st.columns([1, 1.4], gap="large")

    with col_input:
        with st.container(border=True):
            st.markdown("<div style='font-weight: 700; font-size: 0.95rem; color: #f8fafc; margin-bottom: 10px;'>⚙️ Learning Parameters</div>", unsafe_allow_html=True)

            topic = st.text_input(
                "Concept / Topic Name",
                value=st.session_state.get("concept_topic_input", ""),
                placeholder="e.g., Backpropagation, Photosynthesis, Bayes Theorem",
                key="concept_topic_input_field"
            )

            col_sub1, col_sub2 = st.columns(2)
            with col_sub1:
                audience_level = st.selectbox(
                    "Audience Depth",
                    [
                        "Explain Like I'm 5 (ELI5)",
                        "Beginner / High School",
                        "Undergraduate / University",
                        "Advanced / Industry Professional"
                    ],
                    index=1,
                    key="concept_audience_select"
                )
            with col_sub2:
                output_style = st.selectbox(
                    "Learning Focus",
                    [
                        "Balanced & Structured",
                        "Story & Analogy Driven",
                        "Real-World Applications",
                        "Concise Bullet Cheatsheet"
                    ],
                    index=0,
                    key="concept_style_select"
                )

            uploaded_file = st.file_uploader(
                "📎 Optional: Attach Diagram or Document (.png, .jpg, .pdf, .txt)",
                type=["png", "jpg", "jpeg", "pdf", "txt"],
                key="explainer_file_uploader"
            )

            generate_btn = st.button("🚀 Explain Concept", type="primary", use_container_width=True, key="explainer_submit_btn")

        if generate_btn:
            active_topic = topic.strip() or st.session_state.get("concept_topic_input", "").strip()
            if not api_key:
                st.error("🔑 Please provide a valid Gemini API Key in the sidebar or `.env` file.")
            elif not active_topic and not uploaded_file:
                st.warning("Please enter a concept name or upload a document/diagram.")
            else:
                start_time = time.time()
                with st.spinner("Analyzing concept and synthesizing structured explanation..."):
                    file_bytes = uploaded_file.getvalue() if uploaded_file else None
                    file_type = uploaded_file.type if uploaded_file else None

                    result = generate_explanation(
                        api_key=api_key,
                        model_name=model_name,
                        topic=active_topic,
                        audience_level=audience_level,
                        output_style=output_style,
                        uploaded_file_bytes=file_bytes,
                        file_type=file_type
                    )

                    if result["success"]:
                        elapsed = round(time.time() - start_time, 2)
                        st.session_state.explainer_output = {
                            "topic": active_topic if active_topic else (uploaded_file.name if uploaded_file else "Concept Analysis"),
                            "content": result["content"],
                            "time": elapsed,
                            "level": audience_level
                        }
                        # Pre-generate Audio Stream
                        try:
                            audio_stream = generate_tts_audio(result["content"])
                            st.session_state.explainer_audio = audio_stream.getvalue()
                        except Exception:
                            st.session_state.explainer_audio = None
                        st.rerun()
                    else:
                        st.error(result["error"])

    with col_output:
        if st.session_state.get("explainer_output"):
            exp_data = st.session_state.explainer_output
            raw_text = exp_data["content"]

            # Output Header Toolbar
            st.markdown(f"""
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px; flex-wrap: wrap; gap: 8px;">
                <div style="display: flex; gap: 6px; align-items: center;">
                    <span class="badge-tag badge-purple">Topic: {exp_data['topic']}</span>
                    <span class="badge-tag badge-blue">{exp_data['level']}</span>
                </div>
                <span class="badge-tag badge-cyan">⏱️ Generated in {exp_data['time']}s</span>
            </div>
            """, unsafe_allow_html=True)

            # Persistent Audio Player Bar
            if st.session_state.get("explainer_audio"):
                st.audio(st.session_state.explainer_audio, format="audio/mp3")
            else:
                if st.button("🔊 Generate Audio Lesson", key="play_explainer_tts_btn", use_container_width=True):
                    with st.spinner("Synthesizing audio lesson..."):
                        try:
                            audio_stream = generate_tts_audio(raw_text)
                            st.session_state.explainer_audio = audio_stream.getvalue()
                            st.rerun()
                        except Exception as err:
                            st.warning(f"Audio generation unavailable: {str(err)}")

            # Structured Tabs
            tab_intuition, tab_deep, tab_analogy, tab_apps, tab_quiz, tab_full = st.tabs([
                "💡 Intuition", "🔍 Deep Dive", "🌟 Analogy", "🛠️ Applications", "❓ Self-Check", "📑 Full Note"
            ])

            with tab_intuition:
                content = extract_delimited_section(raw_text, "Core Intuition") or raw_text
                st.markdown(content)
            with tab_deep:
                content = extract_delimited_section(raw_text, "Deep Breakdown") or "See Full Note tab."
                st.markdown(content)
            with tab_analogy:
                content = extract_delimited_section(raw_text, "Real-World Analogy") or "See Full Note tab."
                st.markdown(content)
            with tab_apps:
                content = extract_delimited_section(raw_text, "Industry Applications") or "See Full Note tab."
                st.markdown(content)
            with tab_quiz:
                content = extract_delimited_section(raw_text, "Self-Check Quiz") or "See Full Note tab."
                st.markdown(content)
            with tab_full:
                st.markdown(raw_text)

            # Export Buttons
            render_export_buttons(exp_data["topic"], raw_text, key_prefix="explainer_export")
        else:
            # Empty state with interactive prompt
            st.markdown("""
            <div style="background: rgba(18, 26, 48, 0.4); border: 1px dashed rgba(255, 255, 255, 0.12); border-radius: 14px; padding: 46px 20px; text-align: center; color: #64748b;">
                <div style="font-size: 2.4rem; margin-bottom: 8px;">📖</div>
                <div style="font-size: 1.05rem; font-weight: 600; color: #94a3b8; margin-bottom: 4px;">Explanation Workspace Ready</div>
                <div style="font-size: 0.86rem; color: #64748b;">Select a quick sample topic above or type your own concept on the left and click <b>Explain Concept</b>.</div>
            </div>
            """, unsafe_allow_html=True)
