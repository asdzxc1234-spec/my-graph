import streamlit as st
import pandas as pd
import plotly.express as px


# ============================================================
# 기본 설정
# ============================================================

st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    page_icon="🎬",
    layout="wide",
)

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"


# ============================================================
# 데이터 불러오기
# ============================================================

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)

    # 날짜: YYYYMMDD 형태의 문자열 → 실제 날짜형
    df["날짜"] = pd.to_datetime(
        df["날짜"].astype(str),
        format="%Y%m%d"
    )

    # 숫자형 열 정리
    numeric_columns = [
        "순위",
        "영화코드",
        "일관객",
        "누적관객",
        "스크린수",
        "상영횟수",
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    return df


df = load_data()


# ============================================================
# 제목
# ============================================================

st.title("🎬 영화 데이터 그래프 도감 1 - 시간")

st.write(
    "영화의 일별 데이터를 시간의 흐름에 따라 살펴봅니다."
)


# ============================================================
# 그래프 1
# 영화별 날짜별 일관객 변화
# ============================================================

st.header("그래프 1. 영화별 날짜별 일관객 변화")

movie_list = sorted(df["영화명"].dropna().unique())

selected_movie = st.selectbox(
    "영화를 선택하세요.",
    movie_list,
)

movie_df = (
    df[df["영화명"] == selected_movie]
    .sort_values("날짜")
)


fig = px.line(
    movie_df,
    x="날짜",
    y="일관객",
    markers=True,
    title=f"{selected_movie}의 날짜별 일관객 변화",
    labels={
        "날짜": "날짜",
        "일관객": "일관객 수",
    },
)

# 마우스를 올렸을 때 날짜와 관객수가 표시되도록 설정
fig.update_traces(
    hovertemplate=(
        "날짜: %{x|%Y-%m-%d}"
        "<br>일관객: %{y:,}명"
        "<extra></extra>"
    )
)

fig.update_layout(
    hovermode="x unified",
    xaxis_title="날짜",
    yaxis_title="일관객 수",
)

st.plotly_chart(
    fig,
    width="stretch",
)

st.markdown("### 이 그래프로 알 수 있는 것")

# 사용자가 직접 문구를 작성할 자리
st.info("여기에 이 그래프로 알 수 있는 내용을 작성하세요.")


# ============================================================
# 그래프 2
# 앞으로 추가할 그래프
# ============================================================

st.header("그래프 2")

st.info("앞으로 추가할 그래프를 이 구역에 넣으세요.")


# ============================================================
# 그래프 3
# 앞으로 추가할 그래프
# ============================================================

st.header("그래프 3")

st.info("앞으로 추가할 그래프를 이 구역에 넣으세요.")
