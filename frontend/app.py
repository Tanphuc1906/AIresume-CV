import streamlit as st
import os
import sys
from PIL import Image
import pickle

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

import importlib
import core.ai_agent
importlib.reload(core.ai_agent)
from core.ai_agent import ResumeAgent

from core.pdf_parser import extract_text_from_pdf

@st.cache_data(show_spinner="Đang xử lý PDF...")
def cached_extract_text_from_pdf(pdf_bytes):
    return extract_text_from_pdf(pdf_bytes)

st.set_page_config(page_title="AI Resume Agent", page_icon="👔", layout="wide")

st.title("👔 Interactive AI Recruiter (Resume Builder)")
st.write("Phân tích khoảng trống CV của bạn -> Phỏng vấn khai thác kinh nghiệm -> Viết lại CV hoàn hảo!")

with st.sidebar:
    def on_mode_change():
        st.session_state.step = 1
        st.session_state.messages = []
        st.session_state.chat_session = None
        st.session_state.final_cv = ""
        for k in ["cv_content_cache", "jd_content_cache", "agent"]:
            if k in st.session_state:
                del st.session_state[k]

    st.header("🎯 Chọn Chế độ")
    app_mode = st.radio(
        "Chế độ hoạt động:", 
        options=[1, 2], 
        format_func=lambda x: "1. Tối ưu & Viết lại CV" if x == 1 else "2. Luyện tập Phỏng vấn (HR)",
        key="app_mode",
        on_change=on_mode_change
    )

    st.markdown("---")
    st.header("🔑 Cấu hình hệ thống")
    user_api_key = st.text_input("Nhập Gemini API Key của bạn:", type="password")
    
    model_choice = st.selectbox("🤖 Chọn AI Model:", ["gemini-2.5-flash (Khuyên dùng - Nhanh & Miễn phí cao)", "gemini-2.5-pro (Suy luận sâu - Giới hạn rất thấp)"])
    model_name = "gemini-2.5-pro" if "pro" in model_choice else "gemini-2.5-flash"
    
    st.markdown("""
    **🤔 Bạn chưa có API Key? Rất dễ!**
    1. Truy cập [Google AI Studio](https://aistudio.google.com/app/apikey).
    2. Đăng nhập bằng Gmail của bạn.
    3. Nhấp vào nút **Create API Key** màu xanh.
    4. Copy đoạn mã đó và dán vào ô bên trên là xong!
    
    *(Lưu ý: API Key của bạn hoàn toàn an toàn, nó chỉ tồn tại tạm thời trong phiên làm việc này và không bị lưu trữ lại ở bất cứ đâu).*
    """)
    
    if not user_api_key:
        st.warning("👈 Vui lòng nhập API Key để kích hoạt Nhà Tuyển Dụng AI.")
        st.stop()

    st.markdown("---")
    st.header("💾 Quản lý Phiên Phỏng vấn")
    
    if st.button("🔄 Tạo phiên mới"):
        st.session_state.step = 1
        st.session_state.messages = []
        st.session_state.chat_session = None
        st.session_state.final_cv = ""
        for k in ["cv_content_cache", "jd_content_cache", "agent"]:
            if k in st.session_state:
                del st.session_state[k]
        st.rerun()

    if st.session_state.get("step", 1) >= 2:
        session_data = {
            "app_mode": st.session_state.get("app_mode", 1),
            "step": st.session_state.get("step"),
            "messages": st.session_state.get("messages", []),
            "cv_content_cache": st.session_state.get("cv_content_cache"),
            "jd_content_cache": st.session_state.get("jd_content_cache"),
            "final_cv": st.session_state.get("final_cv", "")
        }
        try:
            pickled_data = pickle.dumps(session_data)
            st.download_button(
                label="⬇️ Tải xuống Phiên hiện tại",
                data=pickled_data,
                file_name="interview_session.pkl",
                mime="application/octet-stream"
            )
        except Exception as e:
            st.error(f"Lỗi khi tải xuống: {e}")
            
    uploaded_session = st.file_uploader("📂 Tải lên Phiên (File .pkl)", type=["pkl"])
    if uploaded_session is not None:
        if st.button("Tải phiên làm việc này"):
            try:
                session_data = pickle.loads(uploaded_session.read())
                st.session_state.app_mode = session_data.get("app_mode", 1)
                st.session_state.step = session_data["step"]
                st.session_state.messages = session_data["messages"]
                st.session_state.cv_content_cache = session_data["cv_content_cache"]
                st.session_state.jd_content_cache = session_data["jd_content_cache"]
                st.session_state.final_cv = session_data["final_cv"]
                
                if "agent" not in st.session_state:
                    st.session_state.agent = ResumeAgent(api_key=user_api_key, model_name=model_name)
                    st.session_state.current_key = user_api_key
                    st.session_state.current_model = model_name
                
                chat_session = st.session_state.agent.resume_interview_chat(
                    cv_content=session_data["cv_content_cache"],
                    jd_content=session_data["jd_content_cache"],
                    messages=session_data["messages"],
                    mode=st.session_state.app_mode
                )
                st.session_state.chat_session = chat_session
                st.success("Tải phiên thành công!")
                st.rerun()
            except Exception as e:
                st.error(f"Lỗi khi tải phiên: File không hợp lệ. {e}")

if "agent" not in st.session_state or st.session_state.get("current_key") != user_api_key or st.session_state.get("current_model") != model_name:
    st.session_state.agent = ResumeAgent(api_key=user_api_key, model_name=model_name)
    st.session_state.current_key = user_api_key
    st.session_state.current_model = model_name
    
if "step" not in st.session_state:
    st.session_state.step = 1
if "chat_session" not in st.session_state:
    st.session_state.chat_session = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "final_cv" not in st.session_state:
    st.session_state.final_cv = ""

col1, col2 = st.columns([1, 2])

with col1:
    cv_content = None
    if st.session_state.app_mode == 1:
        st.header("1. Nạp Dữ Liệu")
        
        st.subheader("CV Của Bạn")
        cv_file = st.file_uploader("Tải lên CV (PDF hoặc Ảnh - Nhấp vào đây và nhấn Ctrl+V để dán ảnh)", type=["pdf", "png", "jpg", "jpeg"])
        
        if cv_file:
            if cv_file.type == "application/pdf":
                cv_content = cached_extract_text_from_pdf(cv_file.read())
            else:
                cv_content = Image.open(cv_file)
            st.success("Đã nạp CV thành công!")
    else:
        st.header("1. Thông tin Công ty")
        st.info("💡 Ở chế độ này, bạn chỉ cần nhập JD. Trưởng phòng Nhân sự AI sẽ dùng nó làm cơ sở để phỏng vấn bạn.")

    st.subheader("Job Description (JD)")
    tab1, tab2 = st.tabs(["📝 Nhập Văn Bản", "🖼️ Dán Ảnh JD (Ctrl+V)"])
    with tab1:
        jd_text = st.text_area("Dán nội dung JD vào đây:", height=150)
    with tab2:
        jd_image_file = st.file_uploader("Tải hoặc Dán ảnh JD (Nhấp vào vùng này và Ctrl+V)", type=["png", "jpg", "jpeg"])
        if jd_image_file:
            st.image(jd_image_file, caption="Ảnh JD đã nạp", use_column_width=True)

    jd_content = None
    if jd_image_file:
        jd_content = Image.open(jd_image_file)
    elif jd_text:
        jd_content = jd_text
        
    if st.button("🚀 Bắt đầu Phỏng vấn" if st.session_state.app_mode == 2 else "🚀 Bắt đầu Phân tích & Phỏng vấn"):
        if st.session_state.app_mode == 1 and not cv_content:
            st.warning("Vui lòng nạp CV trước!")
        elif not jd_content:
            st.warning("Vui lòng nạp JD (Mô tả công việc) trước!")
        else:
            with st.spinner("AI đang chuẩn bị nội dung..."):
                try:
                    chat_session, first_msg = st.session_state.agent.start_interview_chat(cv_content, jd_content, mode=st.session_state.app_mode)
                    st.session_state.chat_session = chat_session
                    st.session_state.messages = [{"role": "assistant", "content": first_msg}]
                    st.session_state.cv_content_cache = cv_content
                    st.session_state.jd_content_cache = jd_content
                    st.session_state.step = 2
                except Exception as e:
                    if "429" in str(e) or "Quota" in str(e):
                        st.warning("⚠️ Nhắc nhở: API Key của bạn không có Token cho bản Pro, nên hãy đổi sang dùng bản Flash ở menu bên trái nhé!")
                    else:
                        st.error(f"Lỗi khi gọi AI: {e}")

with col2:
    if st.session_state.step == 1:
        if st.session_state.app_mode == 1:
            st.info("👈 Hãy tải CV và JD ở cột bên trái để bắt đầu.")
        else:
            st.info("👈 Hãy nạp Mô tả công việc (JD) ở cột bên trái để bắt đầu buổi phỏng vấn.")
        
    elif st.session_state.step >= 2:
        header_text = "2. AI Phỏng vấn (Tìm Gap)" if st.session_state.app_mode == 1 else "2. Giả lập Phỏng vấn (HR)"
        st.header(header_text)
        
        # Hiển thị lịch sử chat trong 1 ô vuông có thanh cuộn
        chat_container = st.container(height=450)
        with chat_container:
            for msg in st.session_state.messages:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])
                
        # Khung nhập chat (chỉ hiện khi chưa ở bước 3)
        if st.session_state.step == 2:
            user_msg = st.chat_input("Nhập câu trả lời của bạn (Enter để gửi)...")
            
            if user_msg:
                # Lưu tin nhắn user
                st.session_state.messages.append({"role": "user", "content": user_msg})
                # Hiển thị vào ô chat ngay
                with chat_container:
                    with st.chat_message("user"):
                        st.markdown(user_msg)
                        
                    # Gửi cho AI và hiện tin nhắn phản hồi
                    with st.chat_message("assistant"):
                        with st.spinner("Đang suy nghĩ..."):
                            try:
                                response = st.session_state.chat_session.send_message(user_msg)
                                st.markdown(response.text)
                                st.session_state.messages.append({"role": "assistant", "content": response.text})
                            except Exception as e:
                                if "429" in str(e) or "Quota" in str(e):
                                    st.warning("⚠️ Nhắc nhở: API Key của bạn không có Token cho bản Pro, nên hãy đổi sang dùng bản Flash ở menu bên trái nhé!")
                                else:
                                    st.error(f"Lỗi: {e}")
            
            if st.session_state.app_mode == 1:
                st.write("---")
                if st.button("✨ Hoàn tất phỏng vấn & Viết lại CV"):
                    with st.spinner("AI đang nhào nặn câu trả lời của bạn vào CV..."):
                        try:
                            # Gom toàn bộ lịch sử hội thoại thành văn bản
                            chat_history_text = "\n".join([f"{m['role'].upper()}: {m['content']}" for m in st.session_state.messages])
                            
                            final_cv = st.session_state.agent.write_cv_from_chat(
                                st.session_state.cv_content_cache, 
                                st.session_state.jd_content_cache, 
                                chat_history_text
                            )
                            st.session_state.final_cv = final_cv
                            st.session_state.step = 3
                            st.rerun()
                        except Exception as e:
                            if "429" in str(e) or "Quota" in str(e):
                                st.warning("⚠️ Nhắc nhở: API Key của bạn không có Token cho bản Pro, nên hãy đổi sang dùng bản Flash ở menu bên trái nhé!")
                            else:
                                st.error(f"Lỗi khi viết CV: {e}")
                
    if st.session_state.step == 3:
        st.header("3. Kết quả CV & Cover Letter")
        st.markdown(st.session_state.final_cv)
        
        st.download_button(
            label="⬇️ Tải xuống bản CV (Markdown)",
            data=st.session_state.final_cv,
            file_name="Tailored_CV.md",
            mime="text/markdown"
        )
