import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta

# -----------------------------------------------------------------------------
# 1. 페이지 기본 설정 및 제목
# -----------------------------------------------------------------------------
st.set_page_config(page_title="AI 수학: 트렌드 예측 시뮬레이터", layout="wide")

st.title("📈 AI 수학: 먹거리 트렌드 추세선과 예측")
st.markdown("### 내가 좋아하는 음식의 인기는 앞으로 어떻게 될까? 데이터를 통해 트렌드의 추세선을 그리고 미래를 예측해 보자!")

# -----------------------------------------------------------------------------
# 2. 사이드바: 사용자 입력 (검색어, 기간 설정)
# -----------------------------------------------------------------------------
st.sidebar.header("🔍 데이터 탐색 설정")
keyword = st.sidebar.text_input("검색어를 입력하세요 (예: 탕후루, 마라탕, 소금빵)", value="탕후루")

# 기본 날짜 설정: 2023년 1월 1일 ~ 2023년 12월 31일
start_date = st.sidebar.date_input("시작일", datetime(2023, 1, 1))
end_date = st.sidebar.date_input("종료일", datetime(2023, 12, 31))

st.sidebar.markdown("---")
show_residuals = st.sidebar.checkbox("📐 오차(잔차) 시각화 켜기", value=False)

# -----------------------------------------------------------------------------
# 3. 데이터 수집 함수 (위키백과 API)
# -----------------------------------------------------------------------------
@st.cache_data
def fetch_wiki_data(query, start, end):
    # API가 요구하는 YYYYMMDD 형식으로 날짜 변환
    start_str = start.strftime("%Y%m%d")
    end_str = end.strftime("%Y%m%d")
    
    url = f"https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/ko.wikipedia.org/all-access/user/{query}/daily/{start_str}/{end_str}"
    
    headers = {"User-Agent": "AI-Math-Education-App/1.0"}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        items = data.get("items", [])
        
        # 데이터프레임으로 변환
        df = pd.DataFrame(items)
        if not df.empty:
            df['date'] = pd.to_datetime(df['timestamp'], format="%Y%m%d00")
            df = df[['date', 'views']]
            return df
    return pd.DataFrame() # 실패하거나 데이터가 없으면 빈 데이터프레임 반환

# -----------------------------------------------------------------------------
# 4. 데이터 전처리 및 수학적 모델링 (최소제곱법)
# -----------------------------------------------------------------------------
if start_date > end_date:
    st.error("시작일이 종료일보다 늦을 수 없습니다.")
else:
    df = fetch_wiki_data(keyword, start_date, end_date)
    
    if df.empty:
        st.warning(f"'{keyword}'에 대한 해당 기간의 데이터가 없습니다. 다른 검색어나 기간을 시도해 보세요.")
    else:
        # X축을 '시작일로부터 지난 날짜 수(0, 1, 2...)'로 변환하여 계산하기 쉽게 만듦
        df['x_days'] = (df['date'] - df['date'].min()).dt.days
        x = df['x_days'].values
        y = df['views'].values
        
        # 선형 회귀 (최소제곱법 적용: y = ax + b의 a와 b를 구함)
        # np.polyfit을 사용하면 오차를 최소화하는 기울기(a)와 절편(b)을 자동으로 찾아줍니다.
        a, b = np.polyfit(x, y, 1)
        
        # 구한 식을 바탕으로 예측된 추세선 Y값 계산
        df['predicted_y'] = a * x + b
        
        # 잔차(실제값 - 예측값) 및 SSE(오차의 제곱합) 계산
        df['residual'] = y - df['predicted_y']
        sse = np.sum(df['residual']**2)
        
        # -----------------------------------------------------------------------------
        # 5. 메인 화면 시각화 및 수식 표시
        # -----------------------------------------------------------------------------
        col1, col2 = st.columns([2, 1])
        
        with col2:
            st.markdown("### 🧮 수학적 모델링 결과")
            st.info("데이터를 가장 잘 설명하는 **최적의 직선(추세선)**")
            # 도출된 일차함수 수식 표시 (소수점 2자리까지)
            st.latex(f"y = {a:.2f}x + {b:.2f}")
            
            st.markdown("### 🎯 오차 분석")
            # SSE 값을 천 단위 콤마를 찍어 직관적으로 보여줌
            st.metric(label="현재 추세선의 총 오차 (SSE: 오차들의 제곱합)", value=f"{sse:,.0f}")
            st.caption("※ 인공지능은 이 SSE 값을 가장 작게 만드는 a와 b를 찾아냅니다.")
            
        with col1:
            # Plotly를 이용한 동적 그래프 그리기
            fig = go.Figure()

            # 1. 실제 데이터 산점도
            fig.add_trace(go.Scatter(
                x=df['date'], y=df['views'], 
                mode='markers', name='실제 조회수(데이터)',
                marker=dict(color='royalblue', size=5, opacity=0.6)
            ))

            # 2. 선형 추세선
            fig.add_trace(go.Scatter(
                x=df['date'], y=df['predicted_y'], 
                mode='lines', name='추세선 (예측 모델)',
                line=dict(color='red', width=3)
            ))

            # 3. 오차(잔차) 시각화: 체크박스가 켜져 있을 때만 점선으로 그림
            if show_residuals:
                # Plotly에서 여러 선분을 빠르게 그리기 위해 x, x, None 형태로 리스트 생성
                res_x = []
                res_y = []
                for idx, row in df.iterrows():
                    res_x.extend([row['date'], row['date'], None])
                    res_y.extend([row['views'], row['predicted_y'], None])
                
                fig.add_trace(go.Scatter(
                    x=res_x, y=res_y, 
                    mode='lines', name='오차 (잔차)',
                    line=dict(color='gray', width=1, dash='dot'),
                    hoverinfo='skip'
                ))

            fig.update_layout(
                title=f"'{keyword}' 위키백과 조회수 트렌드 및 추세선",
                xaxis_title="날짜",
                yaxis_title="조회수",
                template="plotly_white",
                height=500
            )
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")
        
        # -----------------------------------------------------------------------------
        # 6. 미래 예측 기능
        # -----------------------------------------------------------------------------
        st.subheader("🔮 추세선을 이용한 미래 예측")
        predict_date = st.date_input("예측해보고 싶은 미래의 날짜를 선택하세요:", datetime.today() + timedelta(days=30))
        
        if predict_date:
            # 선택한 날짜가 시작일로부터 며칠째인지 계산 (X값)
            target_x_days = (pd.to_datetime(predict_date) - df['date'].min()).days
            
            # 수식에 대입하여 Y값 예측
            predicted_views = a * target_x_days + b
            
            # 결과 출력
            if predicted_views < 0:
                pred_result = 0 # 조회수가 음수가 될 수는 없으므로 0으로 보정
                st.warning("예측 결과가 음수입니다. 이 추세대로라면 대중의 관심이 완전히 사라질 것으로 예측됩니다.")
            else:
                pred_result = predicted_views
            
            st.success(f"선택하신 **{predict_date.strftime('%Y년 %m월 %d일')}**의 '{keyword}' 예상 조회수는 **약 {pred_result:,.0f}회** 입니다.")

# -----------------------------------------------------------------------------
# 7. 학생 탐구 질문 (수업 맥락)
# -----------------------------------------------------------------------------
st.markdown("---")
st.header("💡 스스로 탐구해 봅시다")

st.markdown("""
**1. 트렌드 분석 (기울기의 의미)**
> 다른 음식(예: 마라탕)도 검색해 보고 추세선의 기울기($a$)가 더 가파른 것은 무엇인지 비교해 보세요. 이 일차함수의 기울기가 실제 사회에서 대중들의 관심도가 변하는 속도와 어떻게 연결될까요?

**2. 최적화의 원리 (최소제곱법)**
> 왼쪽 사이드바에서 **'오차(잔차) 시각화 켜기'**를 눌러보세요. 수많은 데이터 점들 사이를 관통하는 최적의 직선($y = ax + b$)은 어떻게 결정될까요? 실제 데이터(점)와 예측된 추세선(직선) 사이의 수직 거리(잔차)를 최소화한다는 것은 수학적으로 어떤 의미를 가질까요? (화면에 표시된 '총 오차(SSE)' 수치를 참고해 보세요.)

**3. 예측의 수학적 원리와 한계**
> 위에서 6개월 뒤의 날짜를 대입하여 인기도를 예측해 보았습니다. 하지만 특정 음식의 인기가 영원히 일직선으로만 증가하거나 감소할까요? 선형 모델을 활용한 예측이 가지는 수학적, 현실적 한계점은 무엇일지 친구들과 토론해 봅시다.
""")
