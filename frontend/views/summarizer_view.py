"""
View controller for Module 3: Multimodal Notes Summarizer & Cheat-Sheet Generator.
Condenses uploaded PDF/TXT files or pasted study notes into executive overviews,
glossaries, structured deep notes, and exam cheat-sheets with audio recaps.
"""

import streamlit as st
from backend.services import generate_summary, generate_tts_audio
from backend.parsers import extract_text_from_upload, extract_delimited_section
from frontend.components import render_export_buttons


def render_summarizer_view(api_key: str, model_name: str):
    """Renders the study notes summarizer and cheat-sheet module."""
    st.markdown("""
    <div style="margin-bottom: 20px;">
        <h2 style="margin: 0; display: flex; align-items: center; gap: 10px; font-size: 1.5rem;">
            <span>📝</span> Notes Summarizer & Exam Cheat-Sheet
        </h2>
        <div style="color: #94a3b8; font-size: 0.92rem; margin-top: 4px;">
            Upload your lecture notes, textbook chapters, or paste study materials to generate structured cheat-sheets and audio recaps.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Initialize session state if empty
    if "summarizer_text_input_field" not in st.session_state:
        st.session_state["summarizer_text_input_field"] = ""

    col_input, col_output = st.columns([1, 1.3], gap="large")

    with col_input:
        with st.container(border=True):
            st.markdown("<div style='font-weight: 700; font-size: 0.95rem; color: #f8fafc; margin-bottom: 10px;'>📥 Study Material Input</div>", unsafe_allow_html=True)

            uploaded_doc = st.file_uploader(
                "📎 Upload document to summarize (.pdf, .txt):",
                type=["pdf", "txt"],
                key="summarizer_doc_uploader"
            )

            notes_text = st.text_area(
                "Or paste study notes / lecture text:",
                height=160,
                placeholder="Paste lecture transcript, reading material, or bullet notes here...",
                key="summarizer_text_input_field"
            )

            # Determine Active Text Content
            active_text = ""
            if uploaded_doc is not None:
                active_text = extract_text_from_upload(uploaded_doc) or ""
            elif notes_text.strip():
                active_text = notes_text.strip()

            word_count = len(active_text.split()) if active_text.strip() else 0
            char_count = len(active_text)
            st.markdown(f'<div style="margin-bottom: 12px;"><span class="badge-tag badge-cyan">📊 {word_count} words | {char_count} chars</span></div>', unsafe_allow_html=True)

            summary_depth = st.radio(
                "Summary Detail Level:",
                ["Executive Overview (Fast Revision)", "In-Depth Structured Notes", "High-Yield Exam Cheat-Sheet"],
                index=1,
                key="summarizer_depth_radio"
            )

            summarize_btn = st.button("⚡ Condense & Extract Cheat-Sheet", type="primary", use_container_width=True, key="summarizer_submit_btn")

        if summarize_btn:
            if not api_key:
                st.error("🔑 Please enter a valid Gemini API Key in the sidebar or `.env` file.")
            elif not active_text.strip():
                st.warning("Please upload a document (.pdf, .txt) or paste study notes to summarize.")
            else:
                with st.spinner("Analyzing and condensing your uploaded notes with Gemini..."):
                    result = generate_summary(
                        api_key=api_key,
                        model_name=model_name,
                        text_content=active_text,
                        summary_depth=summary_depth
                    )

                    if result["success"]:
                        st.session_state.summarizer_output = result["content"]
                        # Pre-generate Audio Stream
                        try:
                            audio_stream = generate_tts_audio(result["content"])
                            st.session_state.summarizer_audio = audio_stream.getvalue()
                        except Exception:
                            st.session_state.summarizer_audio = None
                        st.rerun()
                    else:
                        st.error(result["error"])

    with col_output:
        if st.session_state.get("summarizer_output"):
            raw_summary = st.session_state.summarizer_output

            # Audio Player Bar
            if st.session_state.get("summarizer_audio"):
                st.audio(st.session_state.summarizer_audio, format="audio/mp3")
            else:
                if st.button("🔊 Generate Summary Audio Recap", key="play_summary_tts", use_container_width=True):
                    with st.spinner("Synthesizing audio recap..."):
                        try:
                            audio_stream = generate_tts_audio(raw_summary)
                            st.session_state.summarizer_audio = audio_stream.getvalue()
                            st.rerun()
                        except Exception as err:
                            st.warning(f"Audio generation unavailable: {str(err)}")

            # Tabbed Sections
            tab_sum1, tab_sum2, tab_sum3, tab_sum4 = st.tabs([
                "📌 Overview", "🔑 Glossary", "📑 Structured Notes", "🚀 1-Page Cheat Sheet"
            ])

            with tab_sum1:
                st.markdown(extract_delimited_section(raw_summary, "Overview") or raw_summary)
            with tab_sum2:
                st.markdown(extract_delimited_section(raw_summary, "Key Glossary") or "See Structured Notes tab.")
            with tab_sum3:
                st.markdown(extract_delimited_section(raw_summary, "Structured Notes") or "See Overview tab.")
            with tab_sum4:
                st.markdown(extract_delimited_section(raw_summary, "One-Page Cheat-Sheet") or "See Overview tab.")

            # Export Buttons
            render_export_buttons("Study Notes & Cheat-Sheet", raw_summary, key_prefix="summary_export")
        else:
            # Empty state placeholder
            st.markdown("""
            <div style="background: rgba(18, 26, 48, 0.4); border: 1px dashed rgba(255, 255, 255, 0.12); border-radius: 14px; padding: 46px 20px; text-align: center; color: #64748b;">
                <div style="font-size: 2.4rem; margin-bottom: 8px;">📑</div>
                <div style="font-size: 1.05rem; font-weight: 600; color: #94a3b8; margin-bottom: 4px;">Summarizer Workspace Ready</div>
                <div style="font-size: 0.86rem; color: #64748b;">Upload your study document (.pdf, .txt) or paste lecture text on the left and click <b>Condense & Extract Cheat-Sheet</b>.</div>
            </div>
            """, unsafe_allow_html=True)
