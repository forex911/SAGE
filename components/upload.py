# components/upload.py
# SAGE AI — Upload Panel Component

import streamlit as st
from utils.helpers import format_file_size


def render_upload():
    """Render the upload panel. Returns (uploaded_file, explain_clicked)."""
    st.markdown('<div class="panel-label"><span class="panel-label-num">01</span> Upload Target</div>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Drop screenshot here",
        type=["png", "jpg", "jpeg", "webp", "gif"],
        label_visibility="collapsed",
    )

    if uploaded_file:
        st.image(uploaded_file, use_column_width=True)

        file_size = format_file_size(len(uploaded_file.getvalue()))
        name_short = (uploaded_file.name[:24] + "…") if len(uploaded_file.name) > 24 else uploaded_file.name
        ftype = uploaded_file.type.split("/")[-1].upper()

        # Get image dimensions
        try:
            from PIL import Image
            import io
            img = Image.open(io.BytesIO(uploaded_file.getvalue()))
            dims = f"{img.width}×{img.height}"
        except Exception:
            dims = "N/A"

        st.markdown(f"""
        <div class="meta-row">
            <div class="meta-chip"><b>FILE</b> {name_short}</div>
            <div class="meta-chip"><b>SIZE</b> {file_size}</div>
            <div class="meta-chip"><b>TYPE</b> {ftype}</div>
            <div class="meta-chip"><b>DIM</b> {dims}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        explain_clicked = st.button(">> RUN ANALYSIS", use_container_width=True)
    else:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-icon">◈</div>
            <div>NO FILE SELECTED</div>
            <div class="empty-subtitle">drag & drop or click to browse</div>
            <div class="empty-subtitle">PNG · JPG · WEBP · GIF</div>
        </div>
        """, unsafe_allow_html=True)
        explain_clicked = False

    return uploaded_file, explain_clicked
