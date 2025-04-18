# chatbot_web.py
import streamlit as st
import os
from openai import OpenAI
from io import StringIO

openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    st.error("🚫 Hệ thống chưa cấu hình API Key. Vui lòng liên hệ quản trị viên để thiết lập biến môi trường OPENAI_API_KEY.")
    st.stop()

client = OpenAI(api_key=openai_api_key)

st.set_page_config(
    page_title="Trợ lý Kiểm toán viên | ECOVIS AFA VIETNAM",
    page_icon="💼",
    layout="wide",
)

password = st.text_input("🔐 Nhập mật khẩu để truy cập:", type="password")
if password != "ecovis2025":
    st.warning("Vui lòng nhập đúng mật khẩu.")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "Bạn là chuyên gia cao cấp về Kiểm toán, kế toán, thuế và Thẩm định giá của công ty ECOVIS AFA VIETNAM. Nhiệm vụ của bạn là hỗ trợ trả lời câu hỏi liên quan đến: - Kiểm toán tài chính, kiểm toán nội bộ, kiểm toán dự án đầu tư, Thẩm định giá - Kế toán doanh nghiệp - Thuế GTGT, TNDN, TNCN - Hóa đơn điện tử, quy định đầu tư công Trả lời chính xác, ngắn gọn, lịch sự. Nếu không chắc chắn, hãy xin phép người dùng cung cấp thêm thông tin hoặc từ chối trả lời."}
    ]

st.markdown("""
<style>
.chat-box {
    height: 75vh;
    overflow-y: auto;
    padding: 1rem;
    border: 1px solid #ddd;
    border-radius: 10px;
    background-color: #f8f9fa;
}
.message.user {
    background-color: #DCF8C6;
    padding: 10px;
    border-radius: 10px;
    margin-bottom: 10px;
    text-align: right;
}
.message.assistant {
    background-color: #F1F0F0;
    padding: 10px;
    border-radius: 10px;
    margin-bottom: 10px;
    text-align: left;
}
.input-container {
    padding-top: 1rem;
}
</style>
<script>
window.scrollTo(0, document.body.scrollHeight);
</script>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 10])
with col1:
    st.image("LOGO ECOVIS AFA VIETNAM.jpg", width=80)
with col2:
    st.title("Trợ lý Kiểm toán viên | ECOVIS AFA VIETNAM")

st.markdown("---")




st.markdown("<div class='chat-box'>", unsafe_allow_html=True)
for msg in st.session_state.messages[1:]:
    role = msg["role"]
    content = msg["content"]
    st.markdown(f"<div class='message {role}'>{content}</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='input-container'>", unsafe_allow_html=True)
user_input = st.text_input("Nhập câu hỏi và nhấn Enter:", key="input")
st.markdown("</div>", unsafe_allow_html=True)

if user_input:
    with st.spinner("💬 Đang xử lý..."):
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Tự động chuyển model nếu câu đơn giản
        simple_keywords = ["là gì", "là ai", "định nghĩa", "viết tắt", "mẫu", "ví dụ"]
        is_simple = any(kw in user_input.lower() for kw in simple_keywords) and len(user_input) < 80

        model_to_use = "gpt-3.5-turbo" if is_simple else "gpt-4o"

        response = client.chat.completions.create(
            model=model_to_use,
            messages=[
                st.session_state.messages[0],
                {"role": "user", "content": user_input}
            ],
            max_tokens=512,
            temperature=0.7
        )

        bot_reply = response.choices[0].message.content
        model_info = f"<br><sub><i>🤖 Mô hình sử dụng: {model_to_use}</i></sub>"
        bot_reply += model_info
        st.session_state.messages.append({"role": "assistant", "content": bot_reply})
        # Xoá nội dung ô nhập liệu (nếu đã tồn tại khoá)
        if "input" in st.session_state:
            del st.session_state["input"]
        st.rerun()

if st.button("🧹 Xoá hội thoại"):
    st.session_state.messages = st.session_state.messages[:1]
    st.rerun()
