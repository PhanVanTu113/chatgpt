# chatbot_web.py
import streamlit as st
import os
from openai import OpenAI
from io import StringIO

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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
if "input_text" not in st.session_state:
    st.session_state.input_text = ""

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
user_input = st.text_input("Nhập câu hỏi và nhấn Enter:", value=st.session_state.input_text, key="input")
st.markdown("</div>", unsafe_allow_html=True)

if user_input and user_input != st.session_state.input_text:
    st.session_state.input_text = user_input
    with st.spinner("💬 Đang xử lý..."):
        st.session_state.messages.append({"role": "user", "content": user_input})

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                st.session_state.messages[0],
                {"role": "user", "content": user_input}
            ]
        )

        bot_reply = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": bot_reply})
        st.session_state.input_text = ""
        st.rerun()

if st.button("🧹 Xoá hội thoại"):
    st.session_state.messages = st.session_state.messages[:1]
    st.session_state.input_text = ""
    st.rerun()
