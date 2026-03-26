# components/results.py
# SAGE AI — Results Display + Chat Component

import html
import streamlit as st
from utils.helpers import md_to_html, extract_code_blocks


def render_results():
    """Render the analysis results panel with tabs, chat, and actions."""
    st.markdown('<div class="panel-label"><span class="panel-label-num">02</span> Analysis Output</div>', unsafe_allow_html=True)

    if not st.session_state.get("last_result"):
        st.markdown("""
        <div class="empty-state" style="min-height:300px;">
            <div class="empty-icon">◉</div>
            <div>AWAITING INPUT</div>
            <div class="empty-subtitle">upload a screenshot to begin analysis</div>
        </div>
        """, unsafe_allow_html=True)
        return

    result_text = st.session_state.last_result
    elapsed = st.session_state.analysis_time

    # Result header
    time_display = f"{elapsed}s" if elapsed else "--"
    st.markdown(f"""
    <div class="result-header">
        <div class="result-status">
            <div class="status-dot status-dot-static"></div>
            ANALYSIS COMPLETE
        </div>
        <div class="result-time">⏱ {time_display} · {st.session_state.last_filename or 'screenshot'}</div>
    </div>
    """, unsafe_allow_html=True)

    # Tabs
    code_blocks = extract_code_blocks(result_text)
    tab_names = ["FORMATTED", "RAW"]
    if code_blocks:
        tab_names.append("CODE")

    tabs = st.tabs(tab_names)

    # FORMATTED tab — render markdown as HTML inside .result-body
    with tabs[0]:
        result_html = md_to_html(result_text)
        st.markdown(f'<div class="result-body">{result_html}</div>', unsafe_allow_html=True)

    # RAW tab
    with tabs[1]:
        st.code(result_text, language="markdown")

    # CODE tab (if code blocks found)
    if code_blocks and len(tabs) > 2:
        with tabs[2]:
            for i, block in enumerate(code_blocks):
                lang = block["language"]
                code = block["code"]
                st.markdown(f'<div style="font-family:var(--mono);font-size:0.68rem;color:var(--text-3);margin-bottom:4px;text-transform:uppercase;letter-spacing:0.1em;">{lang}</div>', unsafe_allow_html=True)
                st.code(code, language=lang if lang != "text" else None)
                if i < len(code_blocks) - 1:
                    st.markdown("---")

    # Action bar
    st.markdown("<br>", unsafe_allow_html=True)
    _render_actions(result_text)


def _render_actions(result_text):
    """Render copy/download action buttons."""
    fname = st.session_state.get("last_filename", "screenshot")
    acol1, acol2, acol3, acol4, acol5 = st.columns([1, 1, 1, 1, 1])

    with acol1:
        escaped_text = html.escape(result_text).replace("\n", "\\n").replace("'", "\\'")
        copy_id = "copy-btn-main"
        st.markdown(f"""
        <button class="copy-btn" id="{copy_id}" onclick="
            navigator.clipboard.writeText('{escaped_text}'.replace(/\\\\n/g, '\\n')).then(function() {{
                var btn = document.getElementById('{copy_id}');
                btn.textContent = 'COPIED!';
                btn.classList.add('copied');
                setTimeout(function() {{
                    btn.textContent = 'COPY TEXT';
                    btn.classList.remove('copied');
                }}, 2000);
            }});
        ">COPY TEXT</button>
        """, unsafe_allow_html=True)

    with acol2:
        st.download_button(
            label="SAVE .TXT",
            data=result_text,
            file_name=f"analysis_{fname}.txt",
            mime="text/plain",
            use_container_width=True,
        )
    with acol3:
        st.download_button(
            label="SAVE .MD",
            data=result_text,
            file_name=f"analysis_{fname}.md",
            mime="text/markdown",
            use_container_width=True,
        )
    with acol4:
        word_count = len(result_text.split())
        st.markdown(f"""
        <div style="font-family:var(--mono);font-size:0.64rem;color:var(--text-4);padding:8px 0;text-align:center;letter-spacing:0.06em;">
            {word_count} WORDS
        </div>
        """, unsafe_allow_html=True)
    with acol5:
        if st.button("CLEAR", use_container_width=True):
            st.session_state.last_result = None
            st.session_state.last_filename = None
            st.session_state.analysis_time = None
            st.session_state.last_image_bytes = None
            st.session_state.chat_messages = []
            st.rerun()


def render_chat(api_key, model_choice):
    """Render the chat-with-screenshot interface."""
    if not st.session_state.get("last_result") or not st.session_state.get("last_image_bytes"):
        return

    st.markdown("---")
    st.markdown('<div class="panel-label"><span class="panel-label-num">03</span> Chat with Screenshot</div>', unsafe_allow_html=True)

    # Display chat history
    for msg in st.session_state.chat_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat input
    if question := st.chat_input("Ask a follow-up question about the screenshot..."):
        if not api_key:
            st.error("API key required for chat.")
            return

        # Display user message
        st.session_state.chat_messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)

        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    from services.vision import chat_followup
                    response = chat_followup(
                        image_bytes=st.session_state.last_image_bytes,
                        file_name=st.session_state.last_filename,
                        initial_analysis=st.session_state.last_result,
                        chat_history=st.session_state.chat_messages[:-1],
                        question=question,
                        api_key=api_key,
                        model=model_choice,
                    )
                    st.markdown(response)
                    st.session_state.chat_messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    st.error(f"Chat error: {str(e)}")
