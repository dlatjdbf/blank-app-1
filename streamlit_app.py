import streamlit as st
import datetime
import calendar
import json
import os

# ------------------- 기본 설정 -------------------
KST = datetime.timezone(datetime.timedelta(hours=9))
today = datetime.datetime.now(KST).date()
st.set_page_config(page_title="카페인 달력", layout="centered")

# ------------------- 데이터 불러오기 -------------------
DATA_FILE = "data.json"
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        st.session_state.data = json.load(f)
else:
    st.session_state.data = {}

# ------------------- 상태 초기화 -------------------
if "page" not in st.session_state:
    st.session_state.page = "home"
if "intake_input" not in st.session_state:
    st.session_state.intake_input = 0
if "selected_products" not in st.session_state:
    st.session_state.selected_products = []

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
                st.session_state.intake_input = 0
                st.session_state.selected_products = []

    # 날짜 클릭 시 입력창
    if "selected_date" in st.session_state:
        date = st.session_state.selected_date
        st.markdown("---")
        st.subheader(f"{date} 기록")

        # 목표 섭취량 입력
        goal = st.number_input("목표 섭취량 (mg)", min_value=0, step=10, key="goal_input")

        # 제품 목록
        products = {
            "몬스터 에너지 355ml": 100,
            "레드불 에너지 드링크 355ml": 88.75,
            "핫식스 더킹 파워 355ml": 100,
            "핫식스 더킹 크러쉬피치 355ml": 100,
            "핫식스 더킹 퍼플그레이프 355ml": 100,
            "핫식스 더킹 제로 355ml": 100,
            "핫식스 더킹 러쉬 355ml": 100,
            "핫식스 더킹 포스 355ml": 100
        }

        # 제품 선택 및 추가
        selected_product = st.selectbox("제품 선택", ["선택 안 함"] + list(products.keys()), key="product_select")
        if selected_product != "선택 안 함":
            if st.button("선택한 제품 추가"):
                caffeine_value = products[selected_product]
                st.session_state.selected_products.append((selected_product, caffeine_value))
                st.session_state.intake_input += caffeine_value
                st.success(f"{selected_product} 추가됨 (+{caffeine_value}mg)")

        # 추가된 제품 목록 및 총 섭취량 자동 표시
        if st.session_state.selected_products:
            st.write("### 오늘 추가한 제품 목록")
            for name, mg in st.session_state.selected_products:
                st.write(f"- {name}: {mg}mg")
