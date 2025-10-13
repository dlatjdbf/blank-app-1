import streamlit as st
import datetime
import calendar

# 한국 시간대 설정
KST = datetime.timezone(datetime.timedelta(hours=9))
today = datetime.datetime.now(KST).date()

# 페이지 설정
st.set_page_config(page_title="카페인 달력", layout="centered")

# 세션 상태 초기화
if "page" not in st.session_state:
    st.session_state.page = "home"
if "data" not in st.session_state:
    st.session_state.data = {}

# ------------------- 첫 화면 -------------------
if st.session_state.page == "home":
    st.title("☕ 카페인 관리 앱")
    st.write("기능을 선택하세요.")

    col1, col2, col3 = st.columns(3)
    with col2:
        if st.button("📅 카페인 달력 보기", use_container_width=True):
            st.session_state.page = "calendar"

# ------------------- 카페인 달력 -------------------
elif st.session_state.page == "calendar":
    st.title("📅 카페인 달력")
    st.write("목표 섭취량을 설정하고 달성 여부를 기록하세요.")

    # 현재 연도 / 월
    year = today.year
    month = st.selectbox("월 선택", range(1, 13), index=today.month - 1, format_func=lambda x: f"{x}월")

    # 달력 생성
    month_days = calendar.monthrange(year, month)[1]
    cols = st.columns(7)
    for i, day in enumerate(range(1, month_days + 1)):
        col = cols[i % 7]
        with col:
            key = f"{year}-{month:02d}-{day:02d}"
            entry = st.session_state.data.get(key)
            label = f"{day}일"
            if entry:
                label += f"\n{entry['intake']}mg {'✅' if entry['achieved'] else '❌'}"
            if st.button(label, key=f"btn_{key}"):
                st.session_state.selected_date = key

    # 날짜 클릭 시 입력창
    if "selected_date" in st.session_state:
        date = st.session_state.selected_date
        st.markdown("---")
        st.subheader(f"{date} 기록")
        goal = st.number_input("목표 섭취량 (mg)", min_value=0, step=10, key="goal_input"
        intake = st.number_input("총 섭취량 (mg)", min_value=0, step=10, key="intake_input")

        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("저장"):
                achieved = intake <= goal
                st.session_state.data[date] = {"goal": goal, "intake": intake, "achieved": achieved}
                del st.session_state.selected_date
                st.success(f"{date} 기록이 저장되었습니다!")
        with col2:
            if st.button("취소"):
                del st.session_state.selected_date
        with col3:
            if st.button("🏠 홈으로"):
                st.session_state.page = "home"
                if "selected_date" in st.session_state:
                    del st.session_state.selected_date

    # 홈으로 돌아가기 버튼
    st.markdown("---")
    if st.button("🏠 홈으로 돌아가기", use_container_width=True):
        st.session_state.page = "home"
