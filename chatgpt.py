# chatbot_web.py
import streamlit as st
import os
from openai import OpenAI

# ================== CẤU HÌNH CƠ BẢN ==================
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ================== MÀU & LOGO ==================
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

# ================== HEADER & GIAO DIỆN ==================
col1, col2 = st.columns([1, 5])
with col1:
    st.image("LOGO ECOVIS AFA VIETNAM.jpg", width=90)
with col2:
    st.markdown("""
    <h3 style='margin-bottom:0;'>Trợ lý Kiểm toán viên</h3>
    <p style='margin-top:0;color:gray;'>ECOVIS AFA VIETNAM</p>
    """, unsafe_allow_html=True)

st.markdown("---")
st.write("📍 Địa chỉ: 142 Xô Viết Nghệ Tĩnh, TP. Đà Nẵng")
st.write("📧 Email: info@ecovis.com.vn | ☎️ 02363.633.333")
st.markdown("---")

# ================== Ô NHẬP CÂU HỎI ==================
user_input = st.text_area("✏️ Nhập câu hỏi cần hỗ trợ:", height=100)

if st.button("💬 Gửi câu hỏi"):
    if user_input.strip() == "":
        st.warning("Vui lòng nhập nội dung câu hỏi.")
    else:
        with st.spinner("🔎 Đang xử lý câu trả lời từ Trợ lý Kiểm toán viên..."):
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Bạn là Trợ lý Kiểm toán viên của công ty ECOVIS AFA VIETNAM, luôn tư vấn chính xác, thân thiện và ngắn gọn."},
                    {"role": "user", "content": user_input}
                ]
            )
            st.success("✅ Phản hồi từ Trợ lý:")
            st.write(response.choices[0].message.content)
