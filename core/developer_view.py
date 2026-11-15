"""
Know About Developer Module
Renders an attractive, professional, and classic portfolio page for Vibhash Kumar Giri.
Features:
- Professional biography
- Technical skills & programming languages (Python, Java, HTML, CSS, JavaScript, React & Express JS, SQL, PL/pgSQL, MongoDB)
- Dedicated cards for developer social media handles (LinkedIn, GitHub, LeetCode) with developer.jpg embedded in each link.
"""

import os
import base64
import streamlit as st

try:
    from core.dev_img_data import DEV_PHOTO_B64
except ImportError:
    DEV_PHOTO_B64 = ""


def get_image_base64(image_path: str) -> str:
    """Reads a local image and encodes it to base64 string, falling back to DEV_PHOTO_B64."""
    if os.path.exists(image_path):
        try:
            with open(image_path, "rb") as f:
                return base64.b64encode(f.read()).decode("utf-8")
        except Exception:
            pass
    return DEV_PHOTO_B64


def render_know_about_developer_page():
    """Renders the comprehensive 'Know About Developer' page."""
    img_b64 = get_image_base64("assets/developer.jpg")
    img_src = f"data:image/jpeg;base64,{img_b64}" if img_b64 else ""

    # Custom styling specific to developer profile
    st.markdown("""
    <style>
        .dev-header-box {
            background-color: #F8F9FA;
            border: 1px solid #E2E8F0;
            border-left: 5px solid #1B365D;
            padding: 22px 28px;
            margin-bottom: 24px;
            border-radius: 4px;
        }
        .dev-header-title {
            font-size: 26px;
            font-weight: 700;
            color: #1B365D;
            font-family: 'Merriweather', Georgia, serif;
            margin: 0 0 6px 0;
        }
        .dev-header-sub {
            font-size: 14px;
            color: #4A5568;
            margin: 0;
        }
        .profile-card {
            background-color: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 6px;
            padding: 24px;
            box-shadow: 0 1px 4px rgba(0,0,0,0.03);
            margin-bottom: 24px;
        }
        .social-link-card {
            background-color: #FFFFFF;
            border: 1px solid #CBD5E1;
            border-radius: 6px;
            padding: 22px 20px;
            text-align: center;
            box-shadow: 0 1px 3px rgba(0,0,0,0.03);
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            align-items: center;
        }
        .social-link-card:hover {
            border-color: #1B365D;
            box-shadow: 0 4px 12px rgba(27, 54, 93, 0.08);
        }
        .social-photo-circle {
            width: 84px;
            height: 84px;
            border-radius: 50%;
            object-fit: cover;
            border: 2px solid #1B365D;
            margin: 10px auto 14px auto;
            display: block;
            box-shadow: 0 2px 6px rgba(0,0,0,0.08);
        }
        .social-btn {
            display: inline-block;
            background-color: #1B365D;
            color: #FFFFFF !important;
            padding: 8px 18px;
            border-radius: 4px;
            font-size: 13px;
            font-weight: 600;
            text-decoration: none !important;
            margin-top: 12px;
            transition: background-color 0.15s ease;
        }
        .social-btn:hover {
            background-color: #0E2240;
            color: #FFFFFF !important;
        }
        .skill-box {
            background-color: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 6px;
            padding: 18px 22px;
            margin-bottom: 16px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.02);
        }
        .skill-badge-item {
            display: inline-block;
            background-color: #F1F5F9;
            color: #1E293B;
            border: 1px solid #CBD5E1;
            padding: 5px 12px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: 600;
            font-family: 'Source Code Pro', monospace;
            margin: 4px 6px 4px 0;
        }
    </style>
    """, unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # HEADER BANNER
    # -------------------------------------------------------------------------
    st.markdown("""
    <div class="dev-header-box">
        <div class="dev-header-title">Know About the Developer</div>
        <div class="dev-header-sub">
            Engineering Profile &bull; Core Competencies &bull; Algorithmic Architecture &bull; Professional Connect
        </div>
    </div>
    """, unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # MAIN DEVELOPER SHOWCASE
    # -------------------------------------------------------------------------
    col_photo, col_info = st.columns([1.2, 3])

    with col_photo:
        if os.path.exists("assets/developer.jpg"):
            st.image("assets/developer.jpg", width=220)
        else:
            st.info("Photo asset available in assets/developer.jpg")

    with col_info:
        st.markdown("""
        <div class="profile-card">
            <h2 style="margin: 0 0 6px 0; color: #1B365D; font-family: 'Merriweather', Georgia, serif; font-size: 24px;">
                Vibhash Kumar Giri
            </h2>
            <div style="font-size: 14px; font-weight: 600; color: #4A5568; margin-bottom: 8px;">
                Full-Stack Software Engineer & Algorithm Architect
            </div>
            <div style="font-size: 13px; color: #4A5568; margin-bottom: 14px;">
                <strong>Contact Email:</strong> <a href="mailto:vibhash1487@gmail.com" style="color: #1B365D; text-decoration: underline; font-weight: 600;">vibhash1487@gmail.com</a>
            </div>
            <div style="font-size: 13.5px; color: #2D3748; line-height: 1.6; text-align: justify;">
                I am a passionate software engineer and computer science researcher dedicated to building robust, high-performance algorithmic systems, scalable full-stack applications, and resilient data architectures. With a strong foundation in theoretical computer science, discrete mathematics, and applied engineering, I specialize in transforming mathematically complex optimization problems into clean, production-grade software solutions.
            </div>
            <div style="margin-top: 12px; font-size: 13.5px; color: #2D3748; line-height: 1.6; text-align: justify;">
                As the sole developer of this <strong>Intelligent Courier Planning System</strong>, I engineered an integrated logistics framework combining multi-key divide-and-conquer sorting, dynamic programming for 0/1 knapsack vehicle packing, Dijkstra's min-heap algorithm for road network metric closures, and TSP nearest neighbor approximation with 2-opt local search refinement.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    # -------------------------------------------------------------------------
    # TECHNICAL SKILLS & LANGUAGES
    # -------------------------------------------------------------------------
    st.markdown("### Technical Expertise & Programming Languages")
    st.markdown("Languages, frameworks, and database management systems mastered and applied in engineering projects:")

    col_s1, col_s2 = st.columns(2)

    with col_s1:
        st.markdown("""
        <div class="skill-box">
            <h4 style="margin: 0 0 10px 0; color: #1B365D; font-family: 'Merriweather', serif; font-size: 15px;">
                Core Programming & Algorithmic Problem Solving
            </h4>
            <div style="margin-bottom: 10px;">
                <span class="skill-badge-item">Python</span>
                <span class="skill-badge-item">Java</span>
            </div>
            <p style="font-size: 12.5px; color: #4A5568; margin: 0; line-height: 1.5;">
                <strong>Python:</strong> Advanced algorithmic modeling, dynamic programming, scientific computing, graph algorithms (NetworkX), data processing (Pandas, NumPy), and dashboard engineering (Streamlit).<br>
                <strong>Java:</strong> Object-oriented design patterns, robust data structures, concurrency, multithreaded systems, and enterprise application architectures.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="skill-box">
            <h4 style="margin: 0 0 10px 0; color: #1B365D; font-family: 'Merriweather', serif; font-size: 15px;">
                Full-Stack Web Development & Frameworks
            </h4>
            <div style="margin-bottom: 10px;">
                <span class="skill-badge-item">HTML5</span>
                <span class="skill-badge-item">CSS3</span>
                <span class="skill-badge-item">JavaScript (ES6+)</span>
                <span class="skill-badge-item">React.js</span>
                <span class="skill-badge-item">Express.js</span>
            </div>
            <p style="font-size: 12.5px; color: #4A5568; margin: 0; line-height: 1.5;">
                <strong>Frontend:</strong> Semantic HTML5 markup, responsive CSS3 styling (Flexbox/Grid), modern JavaScript (ES6+), component-driven single-page interfaces with React.js.<br>
                <strong>Backend:</strong> High-throughput RESTful API architectures, Node.js runtime, Express.js middleware, routing, and asynchronous service design.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col_s2:
        st.markdown("""
        <div class="skill-box">
            <h4 style="margin: 0 0 10px 0; color: #1B365D; font-family: 'Merriweather', serif; font-size: 15px;">
                Databases & Data Management Systems
            </h4>
            <div style="margin-bottom: 10px;">
                <span class="skill-badge-item">SQL</span>
                <span class="skill-badge-item">PL/pgSQL</span>
                <span class="skill-badge-item">MongoDB</span>
            </div>
            <p style="font-size: 12.5px; color: #4A5568; margin: 0; line-height: 1.5;">
                <strong>Relational Databases (SQL & PL/pgSQL):</strong> Relational schema modeling, normalization, ACID compliance, complex multi-table joins, PostgreSQL procedural stored procedures, triggers, and query indexing.<br>
                <strong>NoSQL Databases (MongoDB):</strong> Document-oriented data modeling, aggregation pipelines, JSON/BSON storage, flexible schema design for high-scale applications.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="skill-box">
            <h4 style="margin: 0 0 10px 0; color: #1B365D; font-family: 'Merriweather', serif; font-size: 15px;">
                Algorithmic & Engineering Principles
            </h4>
            <div style="margin-bottom: 10px;">
                <span class="skill-badge-item">Dynamic Programming</span>
                <span class="skill-badge-item">Graph Theory</span>
                <span class="skill-badge-item">NP-Hard Approximations</span>
                <span class="skill-badge-item">Clean Architecture</span>
            </div>
            <p style="font-size: 12.5px; color: #4A5568; margin: 0; line-height: 1.5;">
                Expertise in asymptotic complexity analysis (Big-O, Omega, Theta), divide-and-conquer algorithms, state-space recurrence formulation, shortest-path algorithms, and local search heuristics.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    # -------------------------------------------------------------------------
    # SOCIAL MEDIA HANDLES (ONLY THESE THREE, WITH PHOTO EMBEDDED IN EACH)
    # -------------------------------------------------------------------------
    st.markdown("### Professional Profiles & Connect")
    st.markdown("Connect and explore my open-source projects, professional background, and algorithmic solutions:")

    col_l1, col_l2, col_l3 = st.columns(3)

    # 1. LinkedIn Card
    with col_l1:
        st.markdown(f"""
        <div class="social-link-card">
            <div>
                <h4 style="margin: 0 0 8px 0; color: #0A66C2; font-family: 'Merriweather', Georgia, serif; font-size: 16px;">
                    LinkedIn Profile
                </h4>
                <div style="font-size: 12px; color: #718096; margin-bottom: 4px;">Professional Network & Experience</div>
                <img src="{img_src}" class="social-photo-circle" alt="Vibhash Kumar Giri - LinkedIn" />
                <div style="font-size: 14px; font-weight: 700; color: #1B365D; margin-bottom: 6px;">Vibhash Kumar Giri</div>
                <p style="font-size: 12px; color: #4A5568; margin: 0 0 12px 0; line-height: 1.45;">
                    Connect for career opportunities, technical collaborations, algorithm architecture, and professional networking.
                </p>
            </div>
            <a href="https://www.linkedin.com/in/vibhash-kumar-giri-8a7243381/" target="_blank" class="social-btn">
                Connect on LinkedIn &rarr;
            </a>
        </div>
        """, unsafe_allow_html=True)

    # 2. GitHub Card
    with col_l2:
        st.markdown(f"""
        <div class="social-link-card">
            <div>
                <h4 style="margin: 0 0 8px 0; color: #24292E; font-family: 'Merriweather', Georgia, serif; font-size: 16px;">
                    GitHub Repositories
                </h4>
                <div style="font-size: 12px; color: #718096; margin-bottom: 4px;">Open-Source Code & Systems</div>
                <img src="{img_src}" class="social-photo-circle" alt="Vibhash Kumar Giri - GitHub" />
                <div style="font-size: 14px; font-weight: 700; color: #1B365D; margin-bottom: 6px;">@VKG1487</div>
                <p style="font-size: 12px; color: #4A5568; margin: 0 0 12px 0; line-height: 1.45;">
                    Explore complete repositories, algorithmic implementations, data structure utilities, and full-stack software codebases.
                </p>
            </div>
            <a href="https://github.com/VKG1487" target="_blank" class="social-btn">
                Explore GitHub &rarr;
            </a>
        </div>
        """, unsafe_allow_html=True)

    # 3. LeetCode Card
    with col_l3:
        st.markdown(f"""
        <div class="social-link-card">
            <div>
                <h4 style="margin: 0 0 8px 0; color: #B25E00; font-family: 'Merriweather', Georgia, serif; font-size: 16px;">
                    LeetCode Profile
                </h4>
                <div style="font-size: 12px; color: #718096; margin-bottom: 4px;">Algorithmic Problem Solving</div>
                <img src="{img_src}" class="social-photo-circle" alt="Vibhash Kumar Giri - LeetCode" />
                <div style="font-size: 14px; font-weight: 700; color: #1B365D; margin-bottom: 6px;">@VKG1487</div>
                <p style="font-size: 12px; color: #4A5568; margin: 0 0 12px 0; line-height: 1.45;">
                    Review algorithmic problem solutions, competitive coding achievements, data structures mastery, and contest rankings.
                </p>
            </div>
            <a href="https://leetcode.com/VKG1487" target="_blank" class="social-btn">
                View LeetCode Profile &rarr;
            </a>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

