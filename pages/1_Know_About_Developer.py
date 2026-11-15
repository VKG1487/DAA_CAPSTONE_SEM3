"""
Streamlit Multi-Page Entrypoint: Know About Developer
"""
import os
import sys

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

# Render Developer Page
render_know_about_developer_page()

# Sidebar profile snippet
st.sidebar.markdown("### Developer Profile")
if os.path.exists("assets/developer.jpg"):
    st.sidebar.image("assets/developer.jpg", width=120)
st.sidebar.markdown("""
**Vibhash Kumar Giri**  
[vibhash1487@gmail.com](mailto:vibhash1487@gmail.com)  

[LinkedIn](https://www.linkedin.com/in/vibhash-kumar-giri-8a7243381/) &bull; [GitHub](https://github.com/VKG1487) &bull; [LeetCode](https://leetcode.com/VKG1487)
""")
st.sidebar.caption("Design and Analysis of Algorithms (DAA) Capstone")

