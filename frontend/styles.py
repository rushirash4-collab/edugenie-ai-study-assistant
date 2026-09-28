"""
Lumina Obsidian & Cyber Luxe Design System for EduGenie.
Engineered with multi-layer glassmorphic containers, ambient mesh gradients,
refined typography, glowing micro-interactions, responsive tabs, and dynamic components.
"""

import streamlit as st


def apply_custom_styles():
    """Injects the Lumina Obsidian design system into the Streamlit app."""
    st.markdown("""
    <style>
        /* 1. Google Fonts Import */
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Outfit:wght@500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600&display=swap');

        /* 2. Global CSS Variables */
        :root {
            --bg-canvas: #070913;
            --bg-surface: rgba(14, 21, 38, 0.75);
            --bg-card: rgba(18, 26, 48, 0.65);
            --bg-card-hover: rgba(26, 38, 70, 0.8);
            --border-glass: rgba(255, 255, 255, 0.09);
            --border-glow: rgba(99, 102, 241, 0.4);
            --border-accent: rgba(6, 182, 212, 0.5);
            --primary: #6366f1;
            --primary-glow: rgba(99, 102, 241, 0.35);
            --accent-cyan: #06b6d4;
            --accent-violet: #a855f7;
            --accent-emerald: #10b981;
            --accent-amber: #f59e0b;
            --text-main: #f8fafc;
            --text-sub: #94a3b8;
            --text-dim: #64748b;
            --grad-brand: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #06b6d4 100%);
            --grad-btn: linear-gradient(135deg, #4f46e5 0%, #7c3aed 50%, #06b6d4 100%);
            --grad-card: linear-gradient(145deg, rgba(22, 33, 62, 0.7) 0%, rgba(13, 19, 36, 0.8) 100%);
            --radius-sm: 8px;
            --radius-md: 14px;
            --radius-lg: 20px;
        }

        /* 3. Global Canvas Background with Ambient Radial Glows */
        html, body, [class*="css"], .stApp {
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
            background: #070913 !important;
            background-image: 
                radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.12) 0px, transparent 55%),
                radial-gradient(at 100% 0%, rgba(6, 182, 212, 0.1) 0px, transparent 50%),
                radial-gradient(at 50% 100%, rgba(168, 85, 247, 0.08) 0px, transparent 60%) !important;
            background-attachment: fixed !important;
            color: var(--text-main) !important;
        }

        h1, h2, h3, h4, h5, h6, .brand-title, .hero-title {
            font-family: 'Outfit', -apple-system, sans-serif !important;
            letter-spacing: -0.02em !important;
        }

        code, pre {
            font-family: 'JetBrains Mono', monospace !important;
        }

        /* 4. Canvas Container Polish */
        .block-container {
            padding-top: 1.2rem !important;
            padding-bottom: 3rem !important;
            max-width: 1320px !important;
        }

        /* 5. Sleek Ambient Top Hero Banner */
        .hero-banner {
            background: linear-gradient(135deg, rgba(18, 26, 48, 0.8) 0%, rgba(10, 16, 30, 0.9) 100%);
            border: 1px solid var(--border-glass);
            border-radius: var(--radius-lg);
            padding: 22px 28px;
            margin-bottom: 24px;
            backdrop-filter: blur(20px);
            box-shadow: 0 12px 35px -10px rgba(0, 0, 0, 0.6), inset 0 1px 1px rgba(255, 255, 255, 0.12);
            transition: all 0.3s ease;
        }

        .hero-banner:hover {
            border-color: rgba(99, 102, 241, 0.35);
            box-shadow: 0 16px 40px -10px rgba(99, 102, 241, 0.25);
        }

        .hero-top-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 12px;
            margin-bottom: 8px;
        }

        .hero-title {
            font-size: 1.65rem;
            font-weight: 800;
            background: linear-gradient(90deg, #ffffff 0%, #cbd5e1 45%, #38bdf8 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 0;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .hero-subtitle {
            color: #94a3b8;
            font-size: 0.9rem;
            line-height: 1.5;
            max-width: 900px;
        }

        .pill-container {
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
            align-items: center;
        }

        .feature-pill {
            display: inline-flex;
            align-items: center;
            gap: 5px;
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.08);
            color: #cbd5e1;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.78rem;
            font-weight: 600;
            transition: all 0.25s ease;
        }

        .feature-pill:hover {
            background: rgba(99, 102, 241, 0.2);
            border-color: rgba(99, 102, 241, 0.4);
            color: #ffffff;
            transform: translateY(-2px);
        }

        /* 6. Redesigned Sidebar Styling */
        [data-testid="stSidebar"] {
            background: #090e1c !important;
            border-right: 1px solid rgba(255, 255, 255, 0.07) !important;
            box-shadow: 4px 0 24px rgba(0, 0, 0, 0.4);
        }

        .sidebar-brand-card {
            background: linear-gradient(135deg, rgba(22, 33, 62, 0.6) 0%, rgba(13, 19, 36, 0.8) 100%);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: var(--radius-md);
            padding: 14px 16px;
            margin-bottom: 16px;
            display: flex;
            align-items: center;
            gap: 12px;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.25);
        }

        .brand-icon {
            font-size: 1.5rem;
            display: flex;
            align-items: center;
            justify-content: center;
            width: 42px;
            height: 42px;
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.3), rgba(6, 182, 212, 0.25));
            border: 1px solid rgba(99, 102, 241, 0.45);
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(99, 102, 241, 0.25);
        }

        .brand-title {
            font-size: 1.3rem;
            font-weight: 800;
            color: #f8fafc;
            margin: 0;
            line-height: 1.1;
            letter-spacing: -0.02em;
        }

        .brand-subtitle {
            font-size: 0.76rem;
            color: #94a3b8;
            font-weight: 500;
            margin-top: 2px;
        }

        /* Sidebar Navigation Radios */
        [data-testid="stSidebar"] .stRadio [role="radiogroup"] {
            gap: 6px;
        }

        [data-testid="stSidebar"] .stRadio [role="radiogroup"] label {
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: 10px;
            padding: 9px 14px;
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
            margin: 0;
            cursor: pointer;
        }

        [data-testid="stSidebar"] .stRadio [role="radiogroup"] label:hover {
            background: rgba(99, 102, 241, 0.15);
            border-color: rgba(99, 102, 241, 0.4);
            transform: translateX(4px);
            box-shadow: 0 2px 10px rgba(99, 102, 241, 0.15);
        }

        [data-testid="stSidebar"] .stRadio [role="radiogroup"] label[data-checked="true"] {
            background: linear-gradient(90deg, rgba(99, 102, 241, 0.3) 0%, rgba(6, 182, 212, 0.15) 100%) !important;
            border-color: rgba(129, 140, 248, 0.6) !important;
            box-shadow: 0 4px 14px rgba(99, 102, 241, 0.25) !important;
        }

        /* 7. Glass Card Containers */
        .glass-card {
            background: var(--grad-card);
            border: 1px solid var(--border-glass);
            border-radius: var(--radius-md);
            padding: 20px 24px;
            margin-bottom: 16px;
            backdrop-filter: blur(16px);
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .glass-card:hover {
            border-color: rgba(255, 255, 255, 0.16);
            transform: translateY(-2px);
            box-shadow: 0 12px 30px rgba(0, 0, 0, 0.4);
        }

        .glass-card-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 10px;
            flex-wrap: wrap;
            gap: 8px;
        }

        /* 8. Modern Buttons with Smooth Gradients & Elevating Shadows */
        .stButton>button {
            border-radius: 11px !important;
            font-weight: 600 !important;
            font-size: 0.92rem !important;
            padding: 0.58rem 1.35rem !important;
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            background: rgba(22, 33, 62, 0.6) !important;
            color: #f1f5f9 !important;
        }

        .stButton>button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 20px rgba(99, 102, 241, 0.3) !important;
            border-color: #818cf8 !important;
            color: #ffffff !important;
            background: rgba(30, 44, 82, 0.8) !important;
        }

        .stButton>button[kind="primary"] {
            background: var(--grad-btn) !important;
            border: none !important;
            color: #ffffff !important;
            box-shadow: 0 4px 18px rgba(79, 70, 229, 0.45) !important;
        }

        .stButton>button[kind="primary"]:hover {
            box-shadow: 0 8px 28px rgba(79, 70, 229, 0.65) !important;
            transform: translateY(-2px) !important;
        }

        /* 9. Segmented Modern Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 6px;
            background: rgba(14, 21, 38, 0.7);
            padding: 6px;
            border-radius: 14px;
            border: 1px solid rgba(255, 255, 255, 0.07);
        }

        .stTabs [data-baseweb="tab"] {
            border-radius: 9px !important;
            padding: 7px 16px !important;
            font-weight: 600 !important;
            font-size: 0.88rem !important;
            color: #94a3b8 !important;
            transition: all 0.2s ease !important;
        }

        .stTabs [aria-selected="true"] {
            background: rgba(99, 102, 241, 0.28) !important;
            color: #ffffff !important;
            border: 1px solid rgba(99, 102, 241, 0.45) !important;
            box-shadow: 0 3px 10px rgba(99, 102, 241, 0.2) !important;
        }

        /* 10. Flashcard Box & 3D Cards */
        .flashcard-box {
            background: linear-gradient(145deg, #12192b 0%, #0a0f1c 100%);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-left: 4px solid #6366f1;
            border-radius: var(--radius-md);
            padding: 22px 26px;
            margin-bottom: 14px;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35);
            transition: all 0.25s ease;
        }

        .flashcard-box:hover {
            transform: translateY(-2px);
            border-left-color: #06b6d4;
            box-shadow: 0 10px 28px rgba(6, 182, 212, 0.25);
        }

        .flashcard-front {
            font-size: 0.82rem;
            color: #38bdf8;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 6px;
        }

        .flashcard-back {
            color: #cbd5e1;
            font-size: 0.95rem;
            line-height: 1.6;
            margin-top: 10px;
            padding-top: 10px;
            border-top: 1px dashed rgba(255, 255, 255, 0.1);
        }

        /* 11. Custom Dropzones */
        [data-testid="stFileUploader"] section {
            padding: 12px 16px !important;
            background: rgba(14, 21, 38, 0.6) !important;
            border: 1px dashed rgba(255, 255, 255, 0.15) !important;
            border-radius: 12px !important;
            transition: all 0.2s ease !important;
        }

        [data-testid="stFileUploader"] section:hover {
            border-color: rgba(99, 102, 241, 0.5) !important;
            background: rgba(22, 33, 62, 0.5) !important;
        }

        /* 12. Inputs & Glowing Focus Rings */
        .stTextInput input, .stTextArea textarea, .stSelectbox select {
            border-radius: 10px !important;
            background: rgba(14, 21, 38, 0.75) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            color: #f8fafc !important;
            font-size: 0.92rem !important;
            transition: all 0.2s ease !important;
        }

        .stTextInput input:focus, .stTextArea textarea:focus {
            border-color: #06b6d4 !important;
            box-shadow: 0 0 0 2px rgba(6, 182, 212, 0.25) !important;
        }

        /* 13. Badges & Pill Tags */
        .badge-tag {
            display: inline-flex;
            align-items: center;
            gap: 5px;
            padding: 4px 12px;
            border-radius: 10px;
            font-size: 0.76rem;
            font-weight: 600;
            letter-spacing: 0.2px;
        }
        .badge-cyan { background: rgba(6, 182, 212, 0.14); color: #67e8f9; border: 1px solid rgba(6, 182, 212, 0.35); }
        .badge-blue { background: rgba(56, 189, 248, 0.14); color: #7dd3fc; border: 1px solid rgba(56, 189, 248, 0.35); }
        .badge-purple { background: rgba(168, 85, 247, 0.14); color: #d8b4fe; border: 1px solid rgba(168, 85, 247, 0.35); }
        .badge-green { background: rgba(16, 185, 129, 0.14); color: #6ee7b7; border: 1px solid rgba(16, 185, 129, 0.35); }
        .badge-amber { background: rgba(245, 158, 11, 0.14); color: #fde68a; border: 1px solid rgba(245, 158, 11, 0.35); }

        /* 14. Custom Progress Bars & Dividers */
        .stProgress > div > div > div > div {
            background: var(--grad-btn) !important;
            border-radius: 10px !important;
        }

        hr {
            border-color: rgba(255, 255, 255, 0.08) !important;
            margin: 24px 0 !important;
        }
    </style>
    """, unsafe_allow_html=True)
