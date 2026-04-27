import streamlit as st
import time

# --- [조건 3] 캐싱 기능 적용 ---
# @st.cache_data를 써서 퀴즈 데이터를 캐싱합니다. (매번 새로고침할 때마다 느려지는 걸 방지)
@st.cache_data
def load_quiz_data():
    time.sleep(1) # 데이터를 가져오는 중이라고 가정 (1초 딜레이)
    return [
        {"문제": "NBA 단일 경기 최고 득점(100점)을 기록한 선수는?", "보기": ["마이클 조던", "윌트 체임벌린", "코비 브라이언트"], "정답": "윌트 체임벌린"},
        {"문제": "스테픈 커리의 소속 팀으로, 3점슛의 시대를 연 팀은?", "보기": ["골든스테이트 워리어스", "LA 레이커스", "시카고 불스"], "정답": "골든스테이트 워리어스"},
        {"문제": "현재 NBA 로고의 실제 모델이 된 선수는?", "보기": ["제리 웨스트", "매직 존슨", "르브론 제임스"], "정답": "제리 웨스트"}
    ]

# --- [조건 1] 첫 화면 조건 (학번/이름) ---
st.sidebar.title("제작자 정보")
st.sidebar.info("학번: 2024404091\n\n이름: 문창현")

st.title("NBA 마스터 퀴즈 앱")

# 세션 상태(로그인 여부) 초기화
if 'login' not in st.session_state:
    st.session_state['login'] = False

# --- [조건 2] 로그인 기능 ---
if not st.session_state['login']:
    st.subheader("로그인이 필요합니다.")
    st.caption("테스트 계정 - 아이디: nba / 비밀번호: 1234")
    
    user_id = st.text_input("아이디")
    user_pw = st.text_input("비밀번호", type="password")
    
    if st.button("로그인"):
        if user_id == "nba" and user_pw == "1234":
            st.session_state['login'] = True
            st.success("로그인 성공! 퀴즈를 불러옵니다...")
            time.sleep(1)
            st.rerun()
        else:
            st.error("정보가 틀렸습니다. 다시 시도해주세요.")

# --- [조건 4] 퀴즈 기능 (로그인 성공 시 화면) ---
else:
    st.write("환영합니다! NBA 지식을 테스트해보세요.")
    
    # 퀴즈 데이터 불러오기 (위에서 만든 캐싱 함수 사용)
    quiz_list = load_quiz_data()
    st.caption("@st.cache_data를 사용해 퀴즈 데이터를 빠르게 불러왔습니다.")
    
    answers = []
    for i, q in enumerate(quiz_list):
        st.write(f"**Q{i+1}. {q['문제']}**")
        # 라디오 버튼 (선택 안 된 상태로 시작)
        ans = st.radio(f"{i}번 문제", q['보기'], key=f"q{i}", index=None, label_visibility="collapsed")
        answers.append(ans)
        st.write("---")
        
    if st.button("결과 확인하기"):
        if None in answers:
            st.warning("아직 안 푼 문제가 있습니다. 모두 선택해주세요!")
        else:
            score = 0
            for i, q in enumerate(quiz_list):
                if answers[i] == q['정답']:
                    score += 1
            
            st.balloons() # 풍선 이펙트!
            st.success(f"당신의 점수는 {score} / {len(quiz_list)} 점입니다!")
            
            if score == len(quiz_list):
                st.info("NBA 진성 팬 인정합니다! MVP ")
            else:
                st.info("조금 아쉽네요! 다음 시즌을 기약해 봅시다.")
                
    # 로그아웃 기능
    st.write("")
    if st.button("로그아웃"):
        st.session_state['login'] = False
        st.rerun()