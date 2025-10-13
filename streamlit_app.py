import streamlit as st
import datetime

st.set_page_config(page_title="카페인 달력", layout="centered")

# 데이터 저장용 딕셔너리 (세션 상태)
if "data" not in st.session_state:
    st.session_state.data = {}

# 제목
st.title("☕ 카페인 달력")

# 현재 달 표시
today = datetime.date.today()
month_days = [datetime.date(today.year, today.month, day) for day in range(1, 31)]

# 날짜 선택 UI
cols = st.columns(7)
for i, day in enumerate(month_days):
    col = cols[i % 7]
    with col:
        key = str(day.day)
        entry = st.session_state.data.get(key)
        label = f"{day.day}일"
        if entry:
            label += f"\n{entry['intake']}mg {'✅' if entry['achieved'] else '❌'}"
        if st.button(label, key=f"btn_{day.day}"):
            st.session_state.selected_date = key

# 선택된 날짜 입력 창
if "selected_date" in st.session_state:
    date = st.session_state.selected_date
    st.write(f"### {date}일 기록")
    goal = st.number_input("목표 섭취량 (mg)", min_value=0, step=10, key="goal_input")

    st.write("제품 선택 (아직 항목 없음)")
    st.button("제품 선택", disabled=True)

    intake = st.number_input("총 섭취량 (현재는 0으로 고정)", min_value=0, value=0, step=10, key="intake_input")

    save, cancel = st.columns(2)
    with save:
        if st.button("저장"):
            achieved = intake <= goal
            st.session_state.data[date] = {"goal": goal, "intake": intake, "achieved": achieved}
            del st.session_state.selected_date
            st.success(f"{date}일 기록 저장 완료!")
    with cancel:
        if st.button("취소"):
            del st.session_state.selected_date
