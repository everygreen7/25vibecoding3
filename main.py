import streamlit as st
import folium
from streamlit_folium import st_folium

# Streamlit 앱의 제목 설정
st.set_page_config(layout="wide") # 전체 너비 사용
st.title("Streamlit + Folium 지도 앱")
st.write("아래 지도에서 서울의 특정 위치를 확인하고 줌 레벨을 조절해 보세요.")

# 지도의 중심 좌표 (예: 서울 시청)
initial_location = [37.5665, 126.9780]

# 초기 줌 레벨 설정
initial_zoom_start = 12

# Streamlit 슬라이더를 사용하여 줌 레벨 조절
zoom_level = st.slider(
    "지도의 줌 레벨을 선택하세요:",
    min_value=1,
    max_value=18,
    value=initial_zoom_start,
    step=1
)

# Folium 지도 생성
# tiles는 지도의 스타일을 결정합니다. 'OpenStreetMap', 'Stamen Terrain', 'Stamen Toner' 등이 있습니다.
m = folium.Map(location=initial_location, zoom_start=zoom_level, tiles="OpenStreetMap")

# 지도에 마커 추가 (예: 서울 시청)
folium.Marker(
    initial_location,
    popup="<b>서울 시청</b>",
    tooltip="서울 시청입니다."
).add_to(m)

# Streamlit에 Folium 지도 표시
# st_folium을 사용하여 지도를 렌더링합니다. 이 함수는 지도를 interactive하게 만들어줍니다.
st_folium(m, width=1000, height=600) # 지도의 너비와 높이 설정

st.markdown(
    """
    <div style="background-color: #f0f2f6; padding: 15px; border-radius: 10px; margin-top: 20px;">
        <h3>사용 방법:</h3>
        <ul>
            <li>위 슬라이더를 움직여 지도의 줌 레벨을 변경할 수 있습니다.</li>
            <li>지도를 드래그하여 이동하거나, 마우스 휠을 사용하여 줌 인/아웃 할 수 있습니다.</li>
            <li>마커를 클릭하면 팝업 메시지를 볼 수 있습니다.</li>
        </ul>
    </div>
    """,
    unsafe_allow_html=True
)

# 간단한 추가 정보
st.sidebar.header("추가 정보")
st.sidebar.write("이 앱은 Streamlit과 Folium 라이브러리를 사용하여 개발되었습니다.")
st.sidebar.write("더 많은 기능(예: 여러 마커, 원, 다각형 추가, 지도 스타일 변경)을 추가할 수 있습니다.")
