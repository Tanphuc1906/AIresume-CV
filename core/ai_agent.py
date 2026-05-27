import google.generativeai as genai
import os
from dotenv import load_dotenv
from PIL import Image
from typing import Union

load_dotenv()

class ResumeAgent:
    def __init__(self, api_key: str, model_name: str = 'gemini-2.5-flash'):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)
        
    def start_interview_chat(self, cv_content: Union[str, Image.Image], jd_content: Union[str, Image.Image]):
        chat_session = self.model.start_chat(history=[])
        prompt = """
Bạn là một Chuyên gia Tuyển dụng (Recruiter) cấp cao. Nhiệm vụ của bạn là đọc CV của ứng viên và Job Description (JD).
Hãy phân tích xem ứng viên đang thiếu sót kinh nghiệm hoặc kỹ năng gì so với yêu cầu của JD.
Sau đó, hãy chào ứng viên và đặt ra các câu hỏi phỏng vấn trực tiếp cho ứng viên để khai thác xem liệu họ có kinh nghiệm ngầm nào liên quan đến những kỹ năng còn thiếu đó không.
Văn phong: Chuyên nghiệp nhưng thân thiện, đóng vai trò như người đang phỏng vấn trực tiếp. Phải viết bằng Tiếng Việt.

Hãy bắt đầu bằng việc chào hỏi và đưa ra câu hỏi đầu tiên dựa trên CV và JD.
"""
        contents = [prompt, "\n### CV Ứng viên:\n", cv_content, "\n### Job Description (JD):\n", jd_content]
        response = chat_session.send_message(contents)
        return chat_session, response.text

    def write_cv_from_chat(self, cv_content: Union[str, Image.Image], jd_content: Union[str, Image.Image], chat_history_text: str) -> str:
        prompt = f"""
Bạn là một Chuyên gia viết CV (Resume Writer) xuất sắc.
Bạn có trong tay CV gốc của ứng viên, Job Description (JD) mà họ muốn ứng tuyển, và TOÀN BỘ LỊCH SỬ CUỘC PHỎNG VẤN.
Nhiệm vụ của bạn:
1. Viết lại một bản CV hoàn chỉnh bằng Markdown.
2. Tích hợp khéo léo những câu trả lời/kinh nghiệm thật của ứng viên (từ lịch sử chat) vào các mục Kinh nghiệm / Kỹ năng trong CV sao cho tự nhiên, chuyên nghiệp và KHỚP VỚI JD NHẤT.
3. Độ dài CV nên vừa vặn, không quá dài dòng, dùng các gạch đầu dòng (bullet points) bắt đầu bằng các động từ mạnh.
4. KHÔNG SỬ DỤNG VĂN PHONG SÁO RỖNG HAY TỪ NGỮ ĐAO TO BÚA LỚN CỦA AI. Hãy viết thật tự nhiên.
5. Sau phần CV, hãy đính kèm một bản Cover Letter (Thư xin việc) ngắn gọn, súc tích.

### Lịch sử trò chuyện / Phỏng vấn bổ sung:
{chat_history_text}

Hãy trả về định dạng Markdown dựa trên CV và JD được cung cấp.
"""
        contents = [prompt, "\n### CV Gốc:\n", cv_content, "\n### Job Description (JD):\n", jd_content]
        response = self.model.generate_content(contents)
        return response.text
