"""
View controller for Login & Registration screens in EduGenie.
Provides dedicated, elegant glassmorphic authentication pages for both
Login (Sign In) and Registration (Sign Up).
"""

import streamlit as st
from backend.auth import authenticate_user, register_user


def render_auth_view():
    """Renders clean dedicated Login and Registration pages."""
    st.markdown("""
    <div style="text-align: center; margin-top: 20px; margin-bottom: 28px;">
        <div style="font-size: 3.2rem; margin-bottom: 8px; filter: drop-shadow(0 4px 12px rgba(99, 102, 241, 0.4));">🎓</div>
        <h1 style="font-size: 2.3rem; font-weight: 800; background: linear-gradient(135deg, #38bdf8 0%, #818cf8 50%, #c084fc 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 6px;">
            EduGenie AI Study Suite
        </h1>
        <div style="color: #94a3b8; font-size: 0.96rem; max-width: 540px; margin: 0 auto; line-height: 1.6;">
            Empowering students with adaptive concept explanations, 3-MCQ practice drills, high-yield summarization, and personalized learning roadmaps.
        </div>
    </div>
    """, unsafe_allow_html=True)

    if "auth_mode" not in st.session_state:
        st.session_state.auth_mode = "login"

    col_center1, col_center2, col_center3 = st.columns([1, 1.7, 1])

    with col_center2:
        # Toggle Segmented Buttons between Login and Sign Up
        col_nav1, col_nav2 = st.columns(2)
        with col_nav1:
            if st.button("🔐 Sign In (Login)", type="primary" if st.session_state.auth_mode == "login" else "secondary", use_container_width=True, key="switch_to_login_btn"):
                st.session_state.auth_mode = "login"
                st.rerun()
        with col_nav2:
            if st.button("📝 Sign Up (Register)", type="primary" if st.session_state.auth_mode == "register" else "secondary", use_container_width=True, key="switch_to_register_btn"):
                st.session_state.auth_mode = "register"
                st.rerun()

        st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)

        # 1. Dedicated Login View
        if st.session_state.auth_mode == "login":
            with st.container(border=True):
                st.markdown("<h3 style='margin: 0 0 6px 0; color: #f8fafc; font-size: 1.3rem;'>Student Sign In</h3>", unsafe_allow_html=True)
                st.markdown("<div style='color: #94a3b8; font-size: 0.86rem; margin-bottom: 16px;'>Enter your registered email and password to access your study portal.</div>", unsafe_allow_html=True)
                
                login_email = st.text_input("Email Address", placeholder="e.g., student@edugenie.ai", key="auth_login_email")
                login_pwd = st.text_input("Password", type="password", placeholder="Enter your password", key="auth_login_pwd")

                st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
                if st.button("🚀 Sign In to Account", type="primary", use_container_width=True, key="auth_submit_login"):
                    success, user_data, msg = authenticate_user(login_email, login_pwd)
                    if success:
                        st.session_state.authenticated_user = user_data
                        st.success(f"Welcome back, {user_data['name']}!")
                        st.rerun()
                    else:
                        st.error(msg)

                st.markdown("""
                <div style="margin-top: 18px; text-align: center; color: #94a3b8; font-size: 0.86rem;">
                    Don't have an account yet? Click <b>Sign Up (Register)</b> above to create one.
                </div>
                """, unsafe_allow_html=True)

        # 2. Dedicated Registration / Sign Up View
        else:
            with st.container(border=True):
                st.markdown("<h3 style='margin: 0 0 6px 0; color: #f8fafc; font-size: 1.3rem;'>New Student Registration</h3>", unsafe_allow_html=True)
                st.markdown("<div style='color: #94a3b8; font-size: 0.86rem; margin-bottom: 16px;'>Create your free EduGenie study account to start learning.</div>", unsafe_allow_html=True)
                
                reg_name = st.text_input("Full Name", placeholder="e.g., Alex Johnson", key="auth_reg_name")
                reg_email = st.text_input("Email Address", placeholder="e.g., alex@university.edu", key="auth_reg_email")
                reg_pwd = st.text_input("Create Password", type="password", placeholder="Minimum 6 characters", key="auth_reg_pwd")

                st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
                if st.button("✨ Complete Registration", type="primary", use_container_width=True, key="auth_submit_register"):
                    success, msg = register_user(reg_email, reg_name, reg_pwd)
                    if success:
                        st.success(f"Account created successfully for {reg_name}! Redirecting to Sign In...")
                        st.session_state.auth_mode = "login"
                        st.rerun()
                    else:
                        st.error(msg)

                st.markdown("""
                <div style="margin-top: 18px; text-align: center; color: #94a3b8; font-size: 0.86rem;">
                    Already have an account? Click <b>Sign In (Login)</b> above to access your workspace.
                </div>
                """, unsafe_allow_html=True)
