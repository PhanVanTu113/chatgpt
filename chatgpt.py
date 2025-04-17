# chatbot_web.py
import streamlit as st
import os
from openai import OpenAI
from io import StringIO

# ================== CẤU HÌNH CƠ BẢN ==================
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ================== PAGE CONFIG ==================
st.set_page_config(
    page_title="Trợ lý Kiểm toán viên | ECOVIS AFA VIETNAM",
    page_icon="💼",
    layout="centered",
)

# ================== MẬT KHẨU ==================
password = st.text_input("🔐 Nhập mật khẩu để truy cập:", type="password")
if password != "ecovis2025":
    st.warning("Vui lòng nhập đúng mật khẩu.")
    st.stop()

# ================== KHỞI TẠO SESSION STATE ==================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": """
Bạn là chuyên gia cao cấp về Kiểm toán, kế toán, thuế và Thẩm định giá của công ty ECOVIS AFA VIETNAM.
Nhiệm vụ của bạn là hỗ trợ trả lời câu hỏi liên quan đến:
- Kiểm toán tài chính, kiểm toán nội bộ, kiểm toán dự án đầu tư, Thẩm định giá
- Kế toán doanh nghiệp
- Thuế GTGT, TNDN, TNCN
- Hóa đơn điện tử, quy định đầu tư công
Trả lời chính xác, ngắn gọn, lịch sự. Nếu không chắc chắn, hãy xin phép người dùng cung cấp thêm thông tin hoặc từ chối trả lời.
"""}
    ]
if "confirm_clear" not in st.session_state:
    st.session_state.confirm_clear = False

# ================== GIAO DIỆN HEADER ==================
st.markdown("""
    <style>
        .chat-bubble {
            padding: 10px;
            border-radius: 10px;
            margin-bottom: 10px;
        }
        .user-msg {
            background-color: #DCF8C6;
            text-align: right;
        }
        .bot-msg {
            background-color: #F1F0F0;
            text-align: left;
        }
        .input-box textarea {
            background-color: #fff !important;
        }
    </style>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 5])
with col1:
    st.image("LOGO ECOVIS AFA VIETNAM.jpg", width=90)
with col2:
    st.markdown("""
    <h3 style='margin-bottom:0;'>Trợ lý Kiểm toán viên</h3>
    <p style='margin-top:0;color:gray;'>ECOVIS AFA VIETNAM</p>
    """, unsafe_allow_html=True)

st.markdown("---")

# ================== NÚT XÓA & TẢI LỊCH SỬ ==================
col3, col4 = st.columns([1, 1])
with col3:
    if not st.session_state.confirm_clear:
        if st.button("🧹 Xoá hội thoại"):
            st.session_state.confirm_clear = True
    else:
        st.warning("Bạn có chắc chắn muốn xoá? Hành động này không thể hoàn tác.")
        confirm = st.columns([1, 1])
        with confirm[0]:
            if st.button("✅ Xác nhận xoá"):
                st.session_state.messages = st.session_state.messages[:1]
                st.session_state.confirm_clear = False
                st.rerun()
        with confirm[1]:
            if st.button("❌ Huỷ"):
                st.session_state.confirm_clear = False

with col4:
    if st.download_button(
        label="📥 Tải hội thoại (.txt)",
        data="\n\n".join([
            f"Người dùng: {m['content']}" if m['role'] == 'user' else f"Trợ lý: {m['content']}"
            for m in st.session_state.messages[1:]
        ]),
        file_name="hoi_thoai_ecovis.txt",
        mime="text/plain"
    ):
        pass

# ================== HIỂN THỊ LỊCH SỬ CHAT ==================
for msg in st.session_state.messages[1:]:
    if msg["role"] == "user":
        st.markdown(f"<div class='chat-bubble user-msg'>{msg['content']}</div>", unsafe_allow_html=True)
    elif msg["role"] == "assistant":
        st.markdown(f"<div class='chat-bubble bot-msg'>{msg['content']}</div>", unsafe_allow_html=True)

# ================== NHẬP CÂU HỎI ==================
with st.container():
    user_input = st.text_input("✏️ Nhập câu hỏi của bạn và nhấn Enter:", key="input")

if user_input:
    with st.spinner("💬 Đang xử lý..."):
        st.session_state.messages.append({"role": "user", "content": user_input})

        response = client.chat.completions.create(
            model="gpt-4",
            messages=st.session_state.messages
        )

        bot_reply = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": bot_reply})
