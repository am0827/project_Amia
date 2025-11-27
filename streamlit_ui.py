import streamlit as st
import requests
import time

st.set_page_config(page_title="내아내임", layout="wide")

col1, col2 = st.columns([4, 6], gap="large")

with col1:
    st.image("C:/Users/User/Downloads/mzk_img.png", 
             caption="아키야마 미즈키",
             use_container_width=True) # 컬럼 너비에 이미지를 꽉 채움



with col2:
    
    BOT_AVATAR_PATH = "C:/Users/User/Downloads/amia_icon.png"

    # 제목 + 아이콘 
    icon_col, title_col = st.columns([1, 9], gap="small")
    
    with icon_col:
        st.image(BOT_AVATAR_PATH, width=60) 

    with title_col:
        st.title("Amia님과의 채팅")

    # 세션 상태 초기화
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 백엔드 모델 준비 상태 확인
    @st.cache_resource
    def check_backend_status():
        """백엔드 서버의 상태를 확인하고 'ready'가 될 때까지 대기합니다."""
        status = "loading"
        spinner_placeholder = st.empty() 

        while status != "ready":
            try:
                res = requests.get("http://127.0.0.1:8000/health", timeout=5)
                res.raise_for_status() 
                status = res.json().get("status", "loading")
                
                if status != "ready":
                    with spinner_placeholder.container():
                        with st.spinner("모델 로딩 중... 잠시만 기다려주세요"):
                            time.sleep(2)
            except requests.exceptions.ConnectionError:
                with spinner_placeholder.container():
                    with st.spinner("서버 연결을 시도 중..."):
                        time.sleep(2)
            except Exception as e:
                st.error(f"서버 연결 중 심각한 오류 발생: {e}")
                st.stop() 
        
        spinner_placeholder.empty()
        return True

    # 백엔드 상태 확인 실행
    if check_backend_status():
        st.success("모델 준비 완료!")

    # 이전 대화 내용 화면에 출력
    # 'messages' 세션에 저장된 내용을 루프를 돌며 "우측 컬럼(col2)"에 출력
    for message in st.session_state.messages:
        
        if message["role"] == "assistant":
            # 봇(assistant)의 메시지일 경우, avatar 파라미터에 아이콘 경로를 지정
            with st.chat_message(message["role"], avatar=BOT_AVATAR_PATH):
                st.markdown(message["content"])
        else:
            # 사용자(user) 메시지는 기본 아이콘을 사용
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

# 새 사용자 입력 페이지 하단 고정
if prompt := st.chat_input("메시지를 입력하세요:"):
    
    # 사용자 메시지를 세션 상태에 추가
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # 봇 응답 생성
    try:
        res = requests.post("http://127.0.0.1:8000/chat", json={"message": prompt})
        res.raise_for_status() # HTTP 오류 검사
        
        reply = res.json().get("reply", "서버에서 올바른 응답이 오지 않았습니다.")
    
    except requests.exceptions.RequestException as e:
        reply = f"서버 오류: {e}"
    except Exception as e:
        reply = f"예상치 못한 오류 발생: {e}"
    
    # 봇 응답을 세션 상태에 추가
    st.session_state.messages.append({"role": "assistant", "content": reply})

    # 앱을 즉시 새로고침하여 col2에 새 메시지(사용자 + 봇)가 표시되도록 함
    st.rerun()