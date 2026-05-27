<h1 align="center">👔 AI Resume Agent & Interviewer</h1>

<div align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/Google_Gemini-8E75B2?style=for-the-badge&logo=google&logoColor=white" alt="Gemini AI">
</div>

<p align="center">
  <b>Một ứng dụng AI thông minh giúp phân tích khoảng trống (Gap Analysis) giữa CV của bạn và Job Description, sau đó đóng vai nhà tuyển dụng để phỏng vấn khai thác kinh nghiệm, và cuối cùng tự động viết lại một bản CV hoàn hảo!</b>
</p>

---

## ✨ Tính năng nổi bật

- **Tự động phân tích PDF CV & Ảnh JD**: Ứng dụng hỗ trợ đọc văn bản từ file PDF hoặc trích xuất chữ trực tiếp từ hình ảnh (Multimodal OCR) bằng công nghệ Gemini.
- **Phỏng vấn giả định (Mock Interview)**: Giao diện Chatbot tương tác thời gian thực (như Messenger). AI sẽ đặt những câu hỏi hóc búa dựa trên những điểm yếu trong CV của bạn so với JD.
- **Auto-Rewrite CV**: Sau cuộc phỏng vấn, AI sẽ tự động "nhào nặn" các câu trả lời thực tế của bạn vào bản CV mới (định dạng Markdown), đảm bảo khớp 100% với yêu cầu của JD mà không bị "sáo rỗng".
- **Bring Your Own Key (BYOK)**: Tích hợp hệ thống bảo mật an toàn, người dùng tự nhập API Key để sử dụng mà không lo bị chia sẻ hạn mức.
- **Bắt lỗi thông minh**: Tự động cảnh báo giới hạn (Rate limit 429) và hướng dẫn người dùng chuyển đổi linh hoạt giữa `gemini-2.5-flash` và `gemini-2.5-pro`.

## 🚀 Hướng dẫn cài đặt (Chạy Local)

### 1. Clone repository
```bash
git clone https://github.com/your-username/ai-resume-agent.git
cd ai-resume-agent
```

### 2. Cài đặt thư viện
Đảm bảo bạn đã cài đặt Python 3.9+. Mở Terminal và chạy:
```bash
python -m venv venv
venv\Scripts\activate      # Dành cho Windows
pip install -r requirements.txt
```

### 3. Khởi chạy ứng dụng
Chạy lệnh sau hoặc nhấp đúp vào file `start.bat` (trên Windows):
```bash
streamlit run frontend/app.py
```

## 🎮 Cách sử dụng
1. Mở trình duyệt tại đường dẫn `http://localhost:8501`.
2. Lấy API Key miễn phí tại [Google AI Studio](https://aistudio.google.com/) và dán vào menu bên trái.
3. Tải CV của bạn (PDF/Ảnh) và dán nội dung/hình ảnh của JD.
4. Bấm **Bắt đầu Phân tích & Phỏng vấn**.
5. Trò chuyện với AI để cung cấp thêm kinh nghiệm thực tế.
6. Bấm **Viết lại CV** và tải xuống bản Markdown hoàn chỉnh!

## 🛡️ Bảo mật
- Tất cả API Key được nhập vào giao diện chỉ được lưu trên RAM (phiên làm việc hiện tại) và sẽ biến mất khi bạn tải lại trang.
- File `.env` chứa khóa cá nhân đã được loại bỏ an toàn thông qua `.gitignore`.

---
<p align="center"><i>Được xây dựng với ❤️ và sức mạnh của AI.</i></p>
