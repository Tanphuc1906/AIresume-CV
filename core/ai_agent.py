import google.generativeai as genai
import os
from dotenv import load_dotenv
from PIL import Image
from typing import Union

load_dotenv()

class ResumeAgent:
    def __init__(self, api_key: str, model_name: str = 'gemini-2.5-flash'):
        genai.configure(api_key=api_key)
        
        # Thiết lập nhiệt độ thấp để AI trả lời chính xác, nghiêm túc và bớt "ảo giác" (hallucination)
        generation_config = genai.types.GenerationConfig(
            temperature=0.3,
            top_p=0.8,
            top_k=40,
        )
        self.model = genai.GenerativeModel(model_name, generation_config=generation_config)
        
    def get_prompt_for_mode(self, mode: int) -> str:
        if mode == 1:
            return """
Bạn là một Chuyên gia Tuyển dụng (Senior Tech Recruiter) khắt khe và cực kỳ chuyên nghiệp. 
Nhiệm vụ của bạn là đọc CV của ứng viên và Job Description (JD).
Hãy phân tích cực kỳ chính xác và thẳng thắn xem ứng viên đang thiếu sót kinh nghiệm hoặc kỹ năng gì so với yêu cầu của JD.
Tuyệt đối không bịa đặt hoặc suy diễn những thông tin không có trong CV/JD.
Sau đó, hãy chào ứng viên và đặt ra các câu hỏi phỏng vấn trực tiếp mang tính kỹ thuật hoặc tình huống thực tế để kiểm tra năng lực và kinh nghiệm ngầm của họ.
Văn phong: Nghiêm túc, dứt khoát, chuyên nghiệp, đi thẳng vào vấn đề. Phải viết bằng Tiếng Việt.

Hãy bắt đầu bằng việc chào hỏi và đưa ra câu hỏi đầu tiên dựa trên CV và JD.
"""
        else:
            return """
Bạn là một Giám đốc Nhân sự (HR Director) khắt khe và cực kỳ chuyên nghiệp đang phỏng vấn trực tiếp một ứng viên. Nhiệm vụ của bạn là đọc CV và Job Description (JD), sau đó tiến hành một buổi phỏng vấn thực tế với độ khó cao.
Luật:
1. Bạn chỉ hỏi MỘT câu mỗi lần. Không được hỏi nhiều câu cùng lúc.
2. Sau khi ứng viên trả lời, hãy nhận xét ngắn gọn, trực diện, mang tính xây dựng nhưng khắt khe (1-2 câu), sau đó mới chuyển sang câu hỏi tiếp theo.
3. Câu hỏi phải bám sát vào yêu cầu của JD và kinh nghiệm trong CV. Hãy hỏi xoáy sâu vào chuyên môn, tính xác thực của kinh nghiệm và kỹ năng xử lý tình huống.
4. Văn phong: Nghiêm túc, dứt khoát, chuyên nghiệp và có tính thử thách ứng viên. Phải viết bằng Tiếng Việt.
5. Tuyệt đối không tự bịa đặt thông tin không có trong CV hoặc JD.

Hãy bắt đầu bằng việc chào hỏi ứng viên và đặt câu hỏi phỏng vấn đầu tiên.
"""

    def start_interview_chat(self, cv_content: Union[str, Image.Image, None], jd_content: Union[str, Image.Image], mode: int = 1):
        chat_session = self.model.start_chat(history=[])
        prompt = self.get_prompt_for_mode(mode)
        contents = [prompt]
        if cv_content:
            contents.extend(["\n### CV Ứng viên:\n", cv_content])
        contents.extend(["\n### Job Description (JD):\n", jd_content])
        
        response = chat_session.send_message(contents)
        return chat_session, response.text

    def resume_interview_chat(self, cv_content: Union[str, Image.Image, None], jd_content: Union[str, Image.Image], messages: list, mode: int = 1):
        prompt = self.get_prompt_for_mode(mode)
        contents = [prompt]
        if cv_content:
            contents.extend(["\n### CV Ứng viên:\n", cv_content])
        contents.extend(["\n### Job Description (JD):\n", jd_content])
        
        history = [
            {"role": "user", "parts": contents}
        ]
        
        if len(messages) > 0 and messages[0]["role"] == "assistant":
            history.append({"role": "model", "parts": [messages[0]["content"]]})
            
        for msg in messages[1:]:
            role = "user" if msg["role"] == "user" else "model"
            history.append({"role": role, "parts": [msg["content"]]})
            
        chat_session = self.model.start_chat(history=history)
        return chat_session

    def write_cv_from_chat(self, cv_content: Union[str, Image.Image], jd_content: Union[str, Image.Image], chat_history_text: str) -> str:
        prompt = f"""
Bạn là một Chuyên gia viết CV (Senior Resume Writer) xuất sắc với tiêu chuẩn cực kỳ khắt khe.
Bạn có trong tay CV gốc của ứng viên, Job Description (JD) mà họ muốn ứng tuyển, và TOÀN BỘ LỊCH SỬ CUỘC PHỎNG VẤN.
Nhiệm vụ của bạn:
1. Viết lại một bản CV hoàn chỉnh bằng định dạng Markdown.
2. Tích hợp các thông tin ĐÃ ĐƯỢC XÁC THỰC từ lịch sử trò chuyện vào các mục Kinh nghiệm / Kỹ năng sao cho khớp với JD nhất. Tuyệt đối KHÔNG BỊA ĐẶT bất kỳ kinh nghiệm hay kỹ năng nào mà ứng viên không đề cập.
3. Độ dài CV nên súc tích, trình bày chuyên nghiệp, dùng các gạch đầu dòng (bullet points) và bắt đầu bằng các động từ mạnh, định lượng kết quả nếu có.
4. KHÔNG SỬ DỤNG VĂN PHONG SÁO RỖNG, TỪ NGỮ HOA MỸ HAY PHÓNG ĐẠI CỦA AI. Viết thật nghiêm túc, khách quan.
5. Sau phần CV, hãy đính kèm một bản Cover Letter (Thư xin việc) ngắn gọn, đi thẳng vào trọng tâm chuyên môn.

### Lịch sử trò chuyện / Phỏng vấn bổ sung:
{chat_history_text}

Hãy trả về định dạng Markdown dựa trên sự thật và dữ liệu đã cung cấp.
"""
        contents = [prompt, "\n### CV Gốc:\n", cv_content, "\n### Job Description (JD):\n", jd_content]
        response = self.model.generate_content(contents)
        return response.text
