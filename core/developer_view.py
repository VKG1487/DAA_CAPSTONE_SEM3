"""
Know About Developer Module
Renders an attractive, professional, and classic portfolio page for Vibhash Kumar Giri.
Features:
- Professional biography
- Technical skills & programming languages:
  Python, Java, HTML, CSS, JAVASCRIPT, REACT AND EXPRESS JS, SQL, Plpg SQL, MONGO DB
- Dedicated cards for developer social media handles (LinkedIn, GitHub, LeetCode) with heading and developer.jpg embedded in each link.
"""

import os
import base64
import streamlit as st


def get_image_base64(image_path: str) -> str:
    """Reads a local image and encodes it to a base64 string."""
    if os.path.exists(image_path):
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    return ""


def render_know_about_developer_page():
    """Renders the comprehensive 'Know About Developer' page."""
    img_b64 = get_image_base64("assets/developer.jpg")
    img_src = f"data:image/jpeg;base64,{img_b64}" if img_b64 else ""

    # Classic, formal, and attractive CSS
    st.markdown("""
    <style>
        .dev-hero-box {
            background-color: #F8F9FA;
            border: 1px solid #E2E8F0;
            border-left: 5px solid #1B365D;
            padding: 24px 28px;
            margin-bottom: 24px;
            border-radius: 4px;
        }
        .dev-hero-title {
            font-size: 26px;
            font-weight: 700;
            color: #1B365D;
            font-family: 'Merriweather', Georgia, serif;
            margin: 0 0 6px 0;
        }
        .dev-hero-sub {
            font-size: 13.5px;
            color: #4A5568;
            margin: 0;
            line-height: 1.5;
        }
        .profile-bio-card {
            background-color: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 6px;
            padding: 24px 26px;
            box-shadow: 0 1px 4px rgba(0,0,0,0.03);
            margin-bottom: 22px;
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
            transition: transform 0.15s ease, box-shadow 0.15s ease, border-color 0.15s ease;
        }
        .social-link-card:hover {
            border-color: #1B365D;
            box-shadow: 0 4px 12px rgba(27, 54, 93, 0.09);
        }
        .social-photo-circle {
            width: 90px;
            height: 90px;
            border-radius: 50%;
            object-fit: cover;
            border: 3px solid #1B365D;
            margin: 10px auto 14px auto;
            display: block;
            box-shadow: 0 2px 6px rgba(0,0,0,0.1);
            transition: transform 0.15s ease;
        }
        .social-photo-circle:hover {
            transform: scale(1.04);
        }
        .social-btn {
            display: inline-block;
            background-color: #1B365D;
            color: #FFFFFF !important;
            padding: 8px 20px;
            border-radius: 4px;
            font-size: 13px;
            font-weight: 600;
            text-decoration: none !important;
            margin-top: 14px;
            box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        }
        .social-btn:hover {
            background-color: #0E2240;
            color: #FFFFFF !important;
        }
        .skill-group-box {
            background-color: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 6px;
            padding: 20px 22px;
            margin-bottom: 18px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.02);
        }
        .lang-pill {
            display: inline-block;
            background-color: #F1F5F9;
            color: #0F172A;
            border: 1px solid #CBD5E1;
            padding: 6px 14px;
            border-radius: 4px;
            font-size: 12.5px;
            font-weight: 700;
            font-family: 'Source Code Pro', monospace;
            margin: 4px 6px 4px 0;
            letter-spacing: 0.02em;
        }
        .lang-pill-primary {
            background-color: #EBF3FC;
            color: #1B365D;
            border: 1px solid #BFDBFE;
        }
    </style>
    """, unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # TOP HEADER BANNER
    # -------------------------------------------------------------------------
    st.markdown("""
    <div class="dev-hero-box">
        <div class="dev-hero-title">Know About the Developer</div>
        <div class="dev-hero-sub">
            Engineering Profile &bull; Core Competencies &bull; Technical Languages &bull; Professional Connect
        </div>
    </div>
    """, unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # MAIN DEVELOPER SHOWCASE & BIOGRAPHY
    # -------------------------------------------------------------------------
    col_photo, col_info = st.columns([1.1, 3])

    with col_photo:
        if os.path.exists("assets/developer.jpg"):
            st.image("assets/developer.jpg", width=225, caption="Vibhash Kumar Giri")
        else:
            st.info("Developer photo asset at assets/developer.jpg")

    with col_info:
        st.markdown("""
        <div class="profile-bio-card">
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
                I am a passionate software engineer and computer science researcher dedicated to building robust, high-performance algorithmic systems, scalable full-stack web applications, and resilient data architectures. With a solid grounding in theoretical computer science, discrete mathematics, and applied systems engineering, I excel at transforming mathematically complex computational and optimization problems into clean, modular, and production-grade software solutions.
            </div>
            <div style="margin-top: 12px; font-size: 13.5px; color: #2D3748; line-height: 1.6; text-align: justify;">
                As the lead developer of this <strong>Intelligent Courier Route & Packing Planning System</strong>, I designed and implemented an integrated computational framework combining multi-key divide-and-conquer sorting, 0/1 Knapsack dynamic programming with strict feasibility guarantees, Dijkstra's algorithm with min-heap priority queues for road network metric closures, and TSP nearest-neighbor approximation enhanced with 2-Opt local search refinement.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    # -------------------------------------------------------------------------
    # TECHNICAL EXPERTISE & LANGUAGES I KNOW
    # -------------------------------------------------------------------------
    st.markdown("### Programming Languages & Technical Proficiencies")
    st.markdown("The complete suite of programming languages, frameworks, and database technologies I specialize in:")

    # High-visibility pill overview of the exact languages requested
    st.markdown("""
    <div style="background-color: #FFFFFF; border: 1px solid #E2E8F0; padding: 16px 20px; border-radius: 6px; margin-bottom: 18px; box-shadow: 0 1px 3px rgba(0,0,0,0.02);">
        <div style="font-size: 12px; text-transform: uppercase; letter-spacing: 0.05em; color: #718096; font-weight: 700; margin-bottom: 10px;">
            Core Languages & Stacks
        </div>
        <div style="display: flex; flex-wrap: wrap; gap: 6px;">
            <span class="lang-pill lang-pill-primary">Python</span>
            <span class="lang-pill lang-pill-primary">Java</span>
            <span class="lang-pill lang-pill-primary">HTML</span>
            <span class="lang-pill lang-pill-primary">CSS</span>
            <span class="lang-pill lang-pill-primary">JAVASCRIPT</span>
            <span class="lang-pill lang-pill-primary">REACT AND EXPRESS JS</span>
            <span class="lang-pill lang-pill-primary">SQL</span>
            <span class="lang-pill lang-pill-primary">Plpg SQL</span>
            <span class="lang-pill lang-pill-primary">MONGO DB</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_t1, col_t2 = st.columns(2)

    with col_t1:
        st.markdown("""
        <div class="skill-group-box">
            <h4 style="margin: 0 0 10px 0; color: #1B365D; font-family: 'Merriweather', serif; font-size: 15px;">
                Systems Programming & Algorithmic Problem Solving
            </h4>
            <div style="margin-bottom: 10px;">
                <span class="lang-pill">Python</span>
                <span class="lang-pill">Java</span>
            </div>
            <p style="font-size: 12.5px; color: #4A5568; margin: 0; line-height: 1.55;">
                &bull; <strong>Python:</strong> Dynamic programming, asymptotic complexity analysis, graph optimization (NetworkX), scientific computing (NumPy, Pandas), and high-throughput application frameworks.<br>
                &bull; <strong>Java:</strong> Object-oriented architecture, strong type systems, multithreaded concurrency, collection hierarchies, and robust enterprise backend engineering.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="skill-group-box">
            <h4 style="margin: 0 0 10px 0; color: #1B365D; font-family: 'Merriweather', serif; font-size: 15px;">
                Full-Stack Web Development
            </h4>
            <div style="margin-bottom: 10px;">
                <span class="lang-pill">HTML</span>
                <span class="lang-pill">CSS</span>
                <span class="lang-pill">JAVASCRIPT</span>
                <span class="lang-pill">REACT AND EXPRESS JS</span>
            </div>
            <p style="font-size: 12.5px; color: #4A5568; margin: 0; line-height: 1.55;">
                &bull; <strong>Frontend (HTML, CSS, JavaScript, React):</strong> Clean semantic DOM, CSS Grid/Flexbox responsive styling, modern asynchronous JavaScript (ES6+), reusable React component state management.<br>
                &bull; <strong>Backend (Express JS):</strong> Scalable RESTful microservices, middleware pipelines, routing, authentication, and non-blocking I/O operations.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col_t2:
        st.markdown("""
        <div class="skill-group-box">
            <h4 style="margin: 0 0 10px 0; color: #1B365D; font-family: 'Merriweather', serif; font-size: 15px;">
                Database Engineering & Management
            </h4>
            <div style="margin-bottom: 10px;">
                <span class="lang-pill">SQL</span>
                <span class="lang-pill">Plpg SQL</span>
                <span class="lang-pill">MONGO DB</span>
            </div>
            <p style="font-size: 12.5px; color: #4A5568; margin: 0; line-height: 1.55;">
                &bull; <strong>Relational Databases (SQL & Plpg SQL):</strong> Relational schema design, third normal form (3NF), ACID transactions, PostgreSQL stored procedures, user-defined functions, triggers, and query execution plan optimization.<br>
                &bull; <strong>NoSQL Databases (MONGO DB):</strong> Document-oriented data modeling, indexing strategies, replication, sharding, and aggregation pipelines for unstructured data.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="skill-group-box">
            <h4 style="margin: 0 0 10px 0; color: #1B365D; font-family: 'Merriweather', serif; font-size: 15px;">
                Design & Analysis of Algorithms Core Focus
            </h4>
            <div style="margin-bottom: 10px;">
                <span class="lang-pill">Dynamic Programming</span>
                <span class="lang-pill">Graph Algorithms</span>
                <span class="lang-pill">TSP Heuristics</span>
            </div>
            <p style="font-size: 12.5px; color: #4A5568; margin: 0; line-height: 1.55;">
                Formal mathematical modeling of optimization problems, recurrence equations, min-heap priority queues, shortest path tree formulation, 2-opt edge-exchange heuristics, and empirical scalability benchmarking.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    # -------------------------------------------------------------------------
    # SOCIAL MEDIA HANDLES (ONLY THESE THREE, WITH PHOTO EMBEDDED IN EACH)
    # -------------------------------------------------------------------------
    st.markdown("### Professional Profiles & Social Media Handles")
    st.markdown("Connect directly via my official professional networks and code repositories:")

    col_l1, col_l2, col_l3 = st.columns(3)

    # 1. LinkedIn Card
    with col_l1:
        st.markdown(f"""
        <div class="social-link-card">
            <div>
                <h4 style="margin: 0 0 6px 0; color: #0A66C2; font-family: 'Merriweather', Georgia, serif; font-size: 16px;">
                    LinkedIn Profile
                </h4>
                <div style="font-size: 12px; color: #718096; margin-bottom: 6px;">Professional Network & Experience</div>
                <a href="https://www.linkedin.com/in/vibhash-kumar-giri-8a7243381/" target="_blank">
                    <img src="{img_src}" class="social-photo-circle" alt="Vibhash Kumar Giri - LinkedIn" />
                </a>
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
                <h4 style="margin: 0 0 6px 0; color: #24292E; font-family: 'Merriweather', Georgia, serif; font-size: 16px;">
                    GitHub Profile & Code
                </h4>
                <div style="font-size: 12px; color: #718096; margin-bottom: 6px;">Open-Source Code & Systems</div>
                <a href="https://github.com/VKG1487" target="_blank">
                    <img src="{img_src}" class="social-photo-circle" alt="Vibhash Kumar Giri - GitHub" />
                </a>
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
                <h4 style="margin: 0 0 6px 0; color: #B25E00; font-family: 'Merriweather', Georgia, serif; font-size: 16px;">
                    LeetCode Profile
                </h4>
                <div style="font-size: 12px; color: #718096; margin-bottom: 6px;">Algorithmic Problem Solving</div>
                <a href="https://leetcode.com/VKG1487" target="_blank">
                    <img src="{img_src}" class="social-photo-circle" alt="Vibhash Kumar Giri - LeetCode" />
                </a>
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
