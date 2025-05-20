import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.io as pio
import os

# Set default Plotly template for better aesthetics
pio.templates.default = "plotly_white"

st.set_page_config(layout="wide") # Use wide layout for better visualization

st.title('인구 데이터 시각화 웹 앱 📊')
st.write('제공된 CSV 파일(`남여합계.csv`, `남여구분.csv`)을 기반으로 인구 데이터를 시각화합니다.')

# --- 남여합계.csv 시각화 (Total Male/Female) ---
st.header('1. 남여 전체 인구 추이 (Total Population Trend)')

if os.path.exists('남여합계.csv'):
    try:
        df_total = pd.read_csv('남여합계.csv')
        st.subheader('남여합계.csv 데이터 미리보기:')
        st.dataframe(df_total.head())

        fig_total = px.line(
            df_total,
            x=df_total.columns[0],
            y=df_total.columns[1],
            title='남여 전체 인구 추이',
            labels={
                df_total.columns[0]: '연도/항목',
                df_total.columns[1]: '인구수'
            }
        )
        st.plotly_chart(fig_total, use_container_width=True)

    except Exception as e:
        st.error(f"남여합계.csv 시각화 중 오류 발생: {e}")
        st.info("CSV 파일의 컬럼 이름이나 구조가 예상과 다를 수 있습니다. 파일을 확인해주세요.")
else:
    st.warning("경고: '남여합계.csv' 파일을 찾을 수 없습니다. 파일을 앱과 같은 경로에 두세요.")

# --- 남여구분.csv 시각화 (Male/Female Classification) ---
st.header('2. 남성 및 여성 인구 추이 (Male and Female Population Trend)')

if os.path.exists('남여구분.csv'):
    try:
        df_gender = pd.read_csv('남여구분.csv')
        st.subheader('남여구분.csv 데이터 미리보기:')
        st.dataframe(df_gender.head())

        # Create a single plot with both male and female lines for comparison
        fig_combined_gender = px.line(
            df_gender,
            x=df_gender.columns[0],
            y=[df_gender.columns[1], df_gender.columns[2]],
            title='남성 및 여성 인구 추이 비교',
            labels={
                df_gender.columns[0]: '연도/항목',
                'value': '인구수',
                'variable': '성별'
            }
        )
        # Update legend names to Korean
        new_names = {df_gender.columns[1]: '남성', df_gender.columns[2]: '여성'}
        fig_combined_gender.for_each_trace(lambda t: t.update(name = new_names[t.name]))
        fig_combined_gender.update_layout(legend_title_text='성별')


        st.plotly_chart(fig_combined_gender, use_container_width=True)

    except Exception as e:
        st.error(f"남여구분.csv 시각화 중 오류 발생: {e}")
        st.info("CSV 파일의 컬럼 이름이나 구조가 예상과 다를 수 있습니다. 파일을 확인해주세요.")
else:
    st.warning("경고: '남여구분.csv' 파일을 찾을 수 없습니다. 파일을 앱과 같은 경로에 두세요.")

st.markdown("---")
st.write("데이터 시각화 앱을 이용해 주셔서 감사합니다!")
