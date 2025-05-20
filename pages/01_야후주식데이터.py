import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime, timedelta

# 주식 데이터를 가져오는 함수
def get_stock_data(ticker, period="1y"):
    """
    야후 파이낸스에서 지정된 티커의 주식 데이터를 가져옵니다.
    :param ticker: 주식 티커 (예: 'AAPL')
    :param period: 데이터 기간 (예: '1y' for 1 year)
    :return: pandas DataFrame 또는 None (데이터를 가져오는 데 실패한 경우)
    """
    try:
        data = yf.download(ticker, period=period)
        if data.empty:
            st.warning(f"'{ticker}'에 대한 데이터를 찾을 수 없습니다. 티커를 확인해주세요.")
            return None
        return data
    except Exception as e:
        st.error(f"'{ticker}' 데이터를 가져오는 데 실패했습니다: {e}")
        return None

# Streamlit 애플리케이션의 메인 함수
def main():
    # 페이지 설정 (넓은 레이아웃 사용)
    st.set_page_config(layout="wide")
    st.title("글로벌 시가총액 Top 10 기업 주가 변화 (최근 1년)")
    st.markdown("""
    이 애플리케이션은 야후 파이낸스 데이터를 사용하여 글로벌 시가총액 상위 10개 기업(가정)의
    지난 1년간 주가 변화를 시각화합니다.
    """)

    # 글로벌 시가총액 Top 10 기업 (가정, 티커 기준)
    # 실제 시가총액 순위는 변동될 수 있습니다.
    top_10_tickers = {
        "Apple": "AAPL",
        "Microsoft": "MSFT",
        "NVIDIA": "NVDA",
        "Alphabet (Class A)": "GOOGL",
        "Amazon": "AMZN",
        "Meta Platforms": "META",
        "Tesla": "TSLA",
        "Eli Lilly and Company": "LLY",
        "TSMC": "TSM",
        "Broadcom": "AVGO"
    }

    # 데이터 로딩 스피너
    with st.spinner("주식 데이터를 불러오는 중... 잠시만 기다려 주세요."):
        all_data = {}
        for company_name, ticker in top_10_tickers.items():
            data = get_stock_data(ticker, period="1y")
            if data is not None:
                all_data[company_name] = data

    if not all_data:
        st.error("데이터를 성공적으로 불러온 기업이 없습니다. 인터넷 연결을 확인하거나 나중에 다시 시도해주세요.")
        return

    # 각 기업의 주가 변화를 Plotly로 시각화
    st.subheader("개별 기업 주가 차트")
    for company_name, data in all_data.items():
        st.markdown(f"### {company_name} ({top_10_tickers[company_name]})")

        # Plotly Figure 생성
        fig = go.Figure()

        # 'Close' 가격을 라인 차트로 추가
        fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='종가'))

        # 차트 레이아웃 설정
        fig.update_layout(
            title=f'{company_name} ({top_10_tickers[company_name]}) 최근 1년 주가 변화',
            xaxis_title='날짜',
            yaxis_title='주가 (USD)',
            hovermode="x unified", # 마우스 오버 시 모든 트레이스에 대한 정보 표시
            template="plotly_white", # 깔끔한 화이트 테마
            margin=dict(l=20, r=20, t=50, b=20), # 여백 설정
            height=400, # 차트 높이
            xaxis_rangeslider_visible=True # 날짜 범위 슬라이더 표시
        )

        # Streamlit에 Plotly 차트 표시
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("모든 기업 주가 변화 (정규화)")
    st.markdown("""
    모든 기업의 주가 변화를 한 차트에 표시하기 위해,
    각 기업의 주가를 시작일 기준으로 정규화하여 상대적인 변화를 비교합니다.
    """)

    # 모든 기업의 정규화된 주가를 포함할 DataFrame 생성
    normalized_data = {}
    for company_name, data in all_data.items():
        if not data['Close'].empty:
            # 첫 번째 값을 기준으로 정규화 (첫 날의 주가를 1로 설정)
            first_close_price = data['Close'].iloc[0]
            normalized_data[company_name] = (data['Close'] / first_close_price) * 100 # 백분율로 표시

    if normalized_data:
        fig_normalized = go.Figure()
        for company_name, norm_series in normalized_data.items():
            fig_normalized.add_trace(go.Scatter(x=norm_series.index, y=norm_series, mode='lines', name=company_name))

        fig_normalized.update_layout(
            title='글로벌 시가총액 Top 10 기업 주가 변화 (정규화된 시작 가격 기준)',
            xaxis_title='날짜',
            yaxis_title='정규화된 주가 (%)',
            hovermode="x unified",
            template="plotly_white",
            margin=dict(l=20, r=20, t=50, b=20),
            height=600,
            xaxis_rangeslider_visible=True
        )
        st.plotly_chart(fig_normalized, use_container_width=True)
    else:
        st.warning("정규화된 주가를 표시할 데이터가 없습니다.")

    st.markdown("---")
    st.info("데이터는 야후 파이낸스에서 제공되며, 실시간 데이터가 아닐 수 있습니다.")

# 스크립트가 직접 실행될 때 main 함수 호출
if __name__ == "__main__":
    main()
# 데이터 로딩 스피너
    with st.spinner("주식 데이터를 불러오는 중... 잠시만 기다려 주세요."):
        all_data = {}
        for company_name, ticker in top_10_tickers.items():
            data = get_stock_data(ticker, period="1y")
            if data is not None:
                all_data[company_name] = data
                # 디버깅을 위해 데이터가 제대로 로드되었는지 확인
                # st.write(f"{company_name} ({ticker}) 데이터 미리보기:")
                # st.dataframe(data.head()) # 데이터의 상위 5행을 표시
