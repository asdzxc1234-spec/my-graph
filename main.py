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

    # 날짜: YYYYMMDD → 실제 날짜형
    df["날짜"] = pd.to_datetime(
        df["날짜"].astype(str),
        format="%Y%m%d",
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

fig1 = px.line(
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

fig1.update_traces(
    hovertemplate=(
        "날짜: %{x|%Y-%m-%d}"
        "<br>일관객: %{y:,}명"
        "<extra></extra>"
    )
)

fig1.update_layout(
    hovermode="x unified",
    xaxis_title="날짜",
    yaxis_title="일관객 수",
)

st.plotly_chart(
    fig1,
    width="stretch",
)

st.markdown("### 이 그래프로 알 수 있는 것")

st.info("여기에 이 그래프로 알 수 있는 내용을 작성하세요.")


# ============================================================
# 그래프 2
# 일관객 합계 상위 5편의 날짜별 일관객 변화
# ============================================================

st.header("그래프 2. 일관객 합계 상위 5편의 날짜별 일관객 변화")

# 영화별 전체 기간 일관객 합계
top5_movies = (
    df.groupby("영화명", as_index=False)["일관객"]
    .sum()
    .sort_values("일관객", ascending=False)
    .head(5)["영화명"]
    .tolist()
)

top5_df = (
    df[df["영화명"].isin(top5_movies)]
    .sort_values(["영화명", "날짜"])
)

fig2 = px.line(
    top5_df,
    x="날짜",
    y="일관객",
    color="영화명",
    markers=True,
    title="이 기간 일관객 합계 상위 5편",
    labels={
        "날짜": "날짜",
        "일관객": "일관객 수",
        "영화명": "영화",
    },
)

fig2.update_traces(
    hovertemplate=(
        "영화: %{fullData.name}"
        "<br>날짜: %{x|%Y-%m-%d}"
        "<br>일관객: %{y:,}명"
        "<extra></extra>"
    )
)

fig2.update_layout(
    hovermode="closest",
    xaxis_title="날짜",
    yaxis_title="일관객 수",
    legend_title="영화",
)

st.plotly_chart(
    fig2,
    width="stretch",
)

st.markdown("### 이 그래프로 알 수 있는 것")

st.info("여기에 이 그래프로 알 수 있는 내용을 작성하세요.")


# ============================================================
# 그래프 3
# 날짜별 10위권 전체 일관객 합계
# ============================================================

st.header("그래프 3. 날짜별 10위권 전체 일관객 합계")

# 날짜별로 그날 10위권 영화들의 일관객 합계 계산
daily_total = (
    df.groupby("날짜", as_index=False)["일관객"]
    .sum()
    .sort_values("날짜")
)

# 일관객 합계가 가장 큰 날 3일
top3_days = (
    daily_total
    .nlargest(3, "일관객")
    .sort_values("날짜")
)

fig3 = px.area(
    daily_total,
    x="날짜",
    y="일관객",
    title="날짜별 영화 10위권 일관객 합계",
    labels={
        "날짜": "날짜",
        "일관객": "10위권 일관객 합계",
    },
)

# 전체 영역 그래프의 마우스 오버
fig3.update_traces(
    hovertemplate=(
        "날짜: %{x|%Y-%m-%d}"
        "<br>10위권 일관객 합계: %{y:,}명"
        "<extra></extra>"
    )
)

# 가장 큰 3일을 그래프 위에 표시
for _, row in top3_days.iterrows():
    fig3.add_annotation(
        x=row["날짜"],
        y=row["일관객"],
        text=(
            f"{row['날짜'].strftime('%Y-%m-%d')}"
            f"<br>{row['일관객']:,}명"
        ),
        showarrow=True,
        arrowhead=2,
        ax=0,
        ay=-50,
        bgcolor="white",
        bordercolor="#555",
        borderwidth=1,
    )

fig3.update_layout(
    xaxis_title="날짜",
    yaxis_title="10위권 일관객 합계",
)

st.plotly_chart(
    fig3,
    width="stretch",
)

st.markdown("### 이 그래프로 알 수 있는 것")

st.info("여기에 이 그래프로 알 수 있는 내용을 작성하세요.")


# ============================================================
# 그래프 4
# 영화별 일관객 합계 TOP 10
# ============================================================

st.header("그래프 4. 영화별 일관객 합계 TOP 10")

# 영화별 일관객 합계
movie_summary = (
    df.groupby("영화명")
    .agg(
        일관객합계=("일관객", "sum"),
        상영일수=("날짜", "nunique"),
    )
    .reset_index()
)

# 일관객 합계가 큰 순서로 TOP 10
top10_movies = (
    movie_summary
    .sort_values("일관객합계", ascending=False)
    .head(10)
    .sort_values("일관객합계", ascending=True)
)

fig4 = px.bar(
    top10_movies,
    x="일관객합계",
    y="영화명",
    orientation="h",
    title="이 기간 영화별 일관객 합계 TOP 10",
    labels={
        "영화명": "영화",
        "일관객합계": "일관객 합계",
    },
)

# 마우스를 올리면 일관객 합계와 10위권에 든 날수가 표시됨
fig4.update_traces(
    customdata=top10_movies[["상영일수"]].values,
    hovertemplate=(
        "영화: %{y}"
        "<br>일관객 합계: %{x:,}명"
        "<br>10위권에 든 날수: %{customdata[0]}일"
        "<extra></extra>"
    )
)

fig4.update_layout(
    xaxis_title="일관객 합계",
    yaxis_title="영화",
)

st.plotly_chart(
    fig4,
    width="stretch",
)

st.markdown("### 이 그래프로 알 수 있는 것")

st.info("여기에 이 그래프로 알 수 있는 내용을 작성하세요.")


# ============================================================
# 그래프 5
# 앞으로 추가할 그래프
# ============================================================

st.header("그래프 5")

st.info("앞으로 추가할 그래프를 이 구역에 넣으세요.")


# ============================================================
# 그래프 6
# 앞으로 추가할 그래프
# ============================================================

st.header("그래프 6")

st.info("앞으로 추가할 그래프를 이 구역에 넣으세요.")
# ============================================================
# 그래프 5
# 월 × 요일별 일관객 합계 히트맵
# ============================================================

st.header("그래프 5. 월 × 요일별 일관객 합계")

# 날짜에서 월과 요일 추출
heatmap_df = df.copy()

heatmap_df["월"] = heatmap_df["날짜"].dt.month
heatmap_df["요일번호"] = heatmap_df["날짜"].dt.dayofweek

# 월요일부터 일요일까지 표시하기 위한 요일 이름
weekday_names = [
    "월요일",
    "화요일",
    "수요일",
    "목요일",
    "금요일",
    "토요일",
    "일요일",
]

heatmap_df["요일"] = heatmap_df["요일번호"].map(
    dict(enumerate(weekday_names))
)

# 월 × 요일별 일관객 합계
monthly_weekday = (
    heatmap_df
    .groupby(["월", "요일번호", "요일"], as_index=False)["일관객"]
    .sum()
)

# 히트맵용 형태로 변환
heatmap_pivot = (
    monthly_weekday
    .pivot(
        index="월",
        columns="요일번호",
        values="일관객",
    )
    .reindex(columns=range(7))
)

# 히트맵에 표시할 요일 이름
heatmap_pivot.columns = weekday_names

# Plotly 히트맵
fig5 = px.imshow(
    heatmap_pivot,
    labels={
        "x": "요일",
        "y": "월",
        "color": "일관객 합계",
    },
    x=weekday_names,
    y=[f"{month}월" for month in heatmap_pivot.index],
    color_continuous_scale="Blues",
    text_auto=False,
    aspect="auto",
    title="월 × 요일별 10위권 일관객 합계",
)

# 마우스를 올리면 정확한 합계 표시
fig5.update_traces(
    hovertemplate=(
        "월: %{y}"
        "<br>요일: %{x}"
        "<br>일관객 합계: %{z:,}명"
        "<extra></extra>"
    )
)

fig5.update_layout(
    xaxis_title="요일",
    yaxis_title="월",
    coloraxis_colorbar_title="일관객 합계",
)

st.plotly_chart(
    fig5,
    width="stretch",
)

st.markdown("### 이 그래프로 알 수 있는 것")

st.info("여기에 이 그래프로 알 수 있는 내용을 작성하세요.")
