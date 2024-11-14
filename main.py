import streamlit as st
import utile 
import time
import os 
import random

st.set_page_config(initial_sidebar_state="collapsed")
st.title("커스텀 챗봇 만들기 실습")

st.session_state.messages = []
st.markdown(
    """
<style>
    [data-testid="collapsedControl"] {
        display: none
    }
</style>
""",
    unsafe_allow_html=True,
)
option = st.selectbox(
    "대화하고 싶은 캐릭터를 선택해주세요",
    ("해리포터", "슈퍼 마리오", "곰돌이 푸", "기타"),
    index=None
)
if option == "기타":
    st.session_state.character = st.text_input("대화하고 싶은 캐릭터를 입력해주세요")
else:
    st.session_state.character = option

details = st.text_area("캐릭터의 자세한 성격을 입력해주세요.")

if details:
    st.session_state.details = details

if st.session_state.character: 
    utile.set_config()
    st.page_link("pages/chat_page.py", label="대화 시작하기")
