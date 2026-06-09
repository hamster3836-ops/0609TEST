import streamlit as st
import yfinance as yf
import plotly.express as px
import pandas as pd
from datetime import datetime

# 페이지 기본 설정
st.set_page_config(page_title="글로벌 Top 10 주식 대시보드", page_icon="📈", layout="wide")

st.title("🌐 글로벌 시가총액 Top 10 주식 대시보드")
st.markdown("야후 파이낸스(Yahoo Finance) 데이터를 활용하여 글로벌 시가총액 상위 10개 기업의 **최근 1년 주가 변화**를 시각화합니다.")

# 시가총액 Top 10 기업 티커 딕셔너리 (미국 상장 기준)
top10_tickers = {
    'Microsoft': 'MSFT',
    'Apple': 'AAPL',
    'NVIDIA': 'NVDA',
    'Alphabet (Google)': 'GOOGL',
    'Amazon': 'AMZN',
    'Meta': 'META',
    'Berkshire Hathaway': 'BRK-B',
    'Eli Lilly': 'LLY',
    'TSMC': 'TSM',
    'Broadcom': 'AVGO'
}

# 데이터 로드 함수 (캐싱을 통해 속도 향상)
@st.cache_data(ttl=86400) # 24시간(86400초)마다 데이터 갱신
def load_stock_data():
    df_list = []
    for company_name, ticker in top10_tickers.items():
        try:
            # yfinance로 1년치 데이터 가져오기
            stock = yf.Ticker(ticker)
            hist = stock.history(period="1y")
            
            if not hist.empty:
                # 데이터프레임 정리
                hist = hist.reset_index()
                # 시간대(timezone) 정보 제거 (Plotly 호환성)
                hist['Date'] = hist['Date'].dt.tz_localize(None)
                hist['Company'] = company_name
                hist['Ticker'] = ticker
                df_list.append(hist)
        except Exception as e:
            st.error(f"{company_name} 데이터를 가져오는 중 오류가 발생했습니다: {e}")
            
    # 리스트에 있는 모든 데이터프레임을 하나로 합치기
    if df_list:
        return pd.concat(df_list, ignore_index=True)
    return pd.DataFrame()

# 데이터 로딩 상태 표시
with st.spinner('야후 파이낸스에서 데이터를 불러오는 중입니다...'):
    df = load_stock_data()

if not df.empty:
    st.success("데이터 로드 완료!")
    
    # 사이드바: 회사 필터링 옵션
    st.sidebar.header("설정")
    selected_companies = st.sidebar.multiselect(
        "비교할 기업을 선택하세요",
        options=list(top10_tickers.keys()),
        default=list(top10_tickers.keys()) # 기본으로 모두 선택
    )
    
    # 선택된 기업만 필터링
    filtered_df = df[df['Company'].isin(selected_companies)]
    
    if not filtered_df.empty:
        # Plotly를 이용한 시각화
        fig = px.line(
            filtered_df, 
            x='Date', 
            y='Close', 
            color='Company',
            title='최근 1년 주가 추이 (종가 기준)',
            labels={'Close': '주가 (USD)', 'Date': '날짜', 'Company': '기업명'}
        )
        
        # 차트 레이아웃 디자인 개선
        fig.update_layout(
            hovermode='x unified', # 마우스를 올렸을 때 같은 날짜의 모든 주가 표시
            xaxis_title="",
            yaxis_title="주가 (USD)",
            legend_title="기업",
            template="plotly_white"
        )
        
        # Streamlit에 차트 출력
        st.plotly_chart(fig, use_container_width=True)
        
        # 원본 데이터 확인 탭 (옵션)
        with st.expander("📊 원본 데이터 확인하기"):
            st.dataframe(filtered_df[['Date', 'Company', 'Ticker', 'Open', 'High', 'Low', 'Close', 'Volume']].sort_values(['Date', 'Company'], ascending=[False, True]))
    else:
        st.warning("선택된 기업이 없습니다. 사이드바에서 기업을 선택해 주세요.")
else:
    st.error("데이터를 불러오지 못했습니다.")
