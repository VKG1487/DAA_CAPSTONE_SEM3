"""
Streamlit Multi-Page Entrypoint: Know About Developer
"""
import os
import sys
import base64

# Ensure root directory is in sys.path
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import streamlit as st
from core.developer_view import render_know_about_developer_page

st.set_page_config(
    page_title="Know About Developer | Vibhash Kumar Giri",
    page_icon="👨‍💻",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Render Developer Page Content
render_know_about_developer_page()


# =============================================================================
# GLOBAL APPLICATION FOOTER: DEVELOPER PROFILE ON FOOTER
# =============================================================================
def get_footer_image_b64(path: str) -> str:
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    return ""

_dev_b64 = get_footer_image_b64("assets/developer.jpg")
_img_markup = f'<img src="data:image/jpeg;base64,{_dev_b64}" style="width: 64px; height: 64px; border-radius: 50%; border: 2.5px solid #1B365D; object-fit: cover; box-shadow: 0 1px 4px rgba(0,0,0,0.08);" alt="Vibhash Kumar Giri" />' if _dev_b64 else ''

st.markdown(f"""
<div style="margin-top: 55px; padding: 22px 28px; background-color: #F8F9FA; border: 1px solid #CBD5E1; border-top: 3px solid #1B365D; border-radius: 6px; box-shadow: 0 1px 4px rgba(0,0,0,0.03);">
    <div style="font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em; color: #718096; margin-bottom: 12px;">
        Developer Profile
    </div>
    <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 16px;">
        <div style="display: flex; align-items: center; gap: 18px;">
            {_img_markup}
            <div>
                <div style="font-size: 16px; font-weight: 700; color: #1B365D; font-family: 'Merriweather', Georgia, serif; margin-bottom: 2px;">
                    Vibhash Kumar Giri
                </div>
                <div style="font-size: 12.5px; font-weight: 600; color: #4A5568; margin-bottom: 4px;">
                    Lead Algorithm Developer & Full-Stack Engineer
                </div>
                <div style="font-size: 12px; color: #4A5568;">
                    <strong>Email:</strong> <a href="mailto:vibhash1487@gmail.com" style="color: #1B365D; font-weight: 600; text-decoration: underline;">vibhash1487@gmail.com</a>
                    &bull; <a href="https://www.linkedin.com/in/vibhash-kumar-giri-8a7243381/" target="_blank" style="color: #0A66C2; text-decoration: none; font-weight: 600;">LinkedIn</a>
                    &bull; <a href="https://github.com/VKG1487" target="_blank" style="color: #24292E; text-decoration: none; font-weight: 600;">GitHub</a>
                    &bull; <a href="https://leetcode.com/VKG1487" target="_blank" style="color: #B25E00; text-decoration: none; font-weight: 600;">LeetCode</a>
                </div>
            </div>
        </div>
        <div style="text-align: right; font-size: 12px; color: #718096; line-height: 1.55;">
            <div style="font-weight: 700; color: #1B365D;">Design and Analysis of Algorithms (DAA) Capstone Project</div>
            <div>Department of Computer Science & Engineering</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
