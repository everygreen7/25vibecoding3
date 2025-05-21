import streamlit as st
import numpy as np

def get_trig_value(func, angle_rad):
    """주어진 함수와 라디안 각도에 대한 삼각함수 값을 반환합니다."""
    if func == "sin":
        return np.sin(angle_rad)
    elif func == "cos":
        return np.cos(angle_rad)
    elif func == "tan":
        # 탄젠트는 90도, 270도에서 정의되지 않으므로 처리
        if np.isclose(np.cos(angle_rad), 0):
            return "정의되지 않음"
        return np.tan(angle_rad)
    return None

def format_value_latex(value):
    """삼각함수 값을 LaTeX 형식으로 반환합니다."""
    if isinstance(value, str):
        return value  # '정의되지 않음'과 같은 문자열은 그대로 반환
    
    # 0, 1, -1, 0.5, -0.5와 같은 정수/반정수는 정확히 표시
    if np.isclose(value, 0):
        return r"$0$"
    elif np.isclose(value, 1):
        return r"$1$"
    elif np.isclose(value, -1):
        return r"$-1$"
    elif np.isclose(value, 0.5):
        return r"$\frac{1}{2}$"
    elif np.isclose(value, -0.5):
        return r"$-\frac{1}{2}$"
    elif np.isclose(value, np.sqrt(2)/2):
        return r"$\frac{\sqrt{2}}{2}$"
    elif np.isclose(value, -np.sqrt(2)/2):
        return r"$-\frac{\sqrt{2}}{2}$"
    elif np.isclose(value, np.sqrt(3)/2):
        return r"$\frac{\sqrt{3}}{2}$"
    elif np.isclose(value, -np.sqrt(3)/2):
        return r"$-\frac{\sqrt{3}}{2}$"
    elif np.isclose(value, np.sqrt(3)):
        return r"$\sqrt{3}$"
    elif np.isclose(value, -np.sqrt(3)):
        return r"$-\sqrt{3}$"
    elif np.isclose(value, 1/np.sqrt(3)):
        return r"$\frac{\sqrt{3}}{3}$" # 유리화
    elif np.isclose(value, -1/np.sqrt(3)):
        return r"$-\frac{\sqrt{3}}{3}$" # 유리화
    elif np.isclose(value, np.sqrt(2)):
        return r"$\sqrt{2}$"
    elif np.isclose(value, -np.sqrt(2)):
        return r"$-\sqrt{2}$"
    
    # 그 외의 값은 소수점 4째 자리까지 표시
    return rf"${value:.4f}$"

st.set_page_config(layout="centered")

st.title("📏 삼각함수 값 확인 앱")
st.markdown("고등학교 2학년 학생들을 위한 삼각함수 값 확인 도우미입니다.")

st.sidebar.header("설정")

# 1. 삼각함수 선택
selected_func = st.sidebar.radio(
    "삼각함수를 선택하세요:",
    ("sin", "cos", "tan"),
    index=0,
    format_func=lambda x: x.upper() # 'sin' -> 'SIN'으로 표시
)

# 2. 각도 단위 선택
angle_unit = st.sidebar.radio(
    "각도 단위를 선택하세요:",
    ("도 (Degrees)", "라디안 (Radians)"),
    index=0
)

# 3. 각도 선택 (30, 45, 60의 배수)
# 각도 리스트 생성
angles_deg = []
for i in range(0, 13): # 0도부터 360도까지 (0*30, 1*30, ..., 12*30)
    angles_deg.append(i * 30)
for i in range(1, 9): # 45도 배수 (45, 90, ..., 360)
    angles_deg.append(i * 45)
for i in range(1, 7): # 60도 배수 (60, 120, ..., 360)
    angles_deg.append(i * 60)

angles_deg = sorted(list(set(angles_deg))) # 중복 제거 및 정렬

# 0도와 360도를 포함하도록 수정
if 0 not in angles_deg:
    angles_deg.insert(0, 0)
if 360 not in angles_deg:
    angles_deg.append(360)

angles_deg = sorted(list(set(angles_deg))) # 최종 중복 제거 및 정렬

if angle_unit == "도 (Degrees)":
    selected_angle_deg = st.sidebar.selectbox(
        "각도를 선택하세요 (도):",
        angles_deg,
        index=angles_deg.index(30) if 30 in angles_deg else 0
    )
    angle_rad = np.deg2rad(selected_angle_deg)
    display_angle = rf"${selected_angle_deg}°$" # raw string 추가
else: # 라디안 선택 시
    angles_rad_display = []
    angle_to_rad = {} # 라디안 값에 해당하는 표시 문자열 매핑

    # 0부터 2파이까지 30, 45, 60도 배수에 해당하는 라디안 값 생성
    for angle_d in angles_deg:
        rad_val = np.deg2rad(angle_d)
        
        # 특수 라디안 값에 대한 LaTeX 표현 (r 접두사 추가)
        if np.isclose(rad_val, 0):
            display_str = r"$0$"
        elif np.isclose(rad_val, np.pi/6):
            display_str = r"$\frac{\pi}{6}$"
        elif np.isclose(rad_val, np.pi/4):
            display_str = r"$\frac{\pi}{4}$"
        elif np.isclose(rad_val, np.pi/3):
            display_str = r"$\frac{\pi}{3}$"
        elif np.isclose(rad_val, np.pi/2):
            display_str = r"$\frac{\pi}{2}$"
        elif np.isclose(rad_val, 2*np.pi/3):
            display_str = r"$\frac{2\pi}{3}$"
        elif np.isclose(rad_val, 3*np.pi/4):
            display_str = r"$\frac{3\pi}{4}$"
        elif np.isclose(rad_val, 5*np.pi/6):
            display_str = r"$\frac{5\pi}{6}$"
        elif np.isclose(rad_val, np.pi):
            display_str = r"$\pi$"
        elif np.isclose(rad_val, 7*np.pi/6):
            display_str = r"$\frac{7\pi}{6}$"
        elif np.isclose(rad_val, 5*np.pi/4):
            display_str = r"$\frac{5\pi}{4}$"
        elif np.isclose(rad_val, 4*np.pi/3):
            display_str = r"$\frac{4\pi}{3}$"
        elif np.isclose(rad_val, 3*np.pi/2):
            display_str = r"$\frac{3\pi}{2}$"
        elif np.isclose(rad_val, 5*np.pi/3):
            display_str = r"$\frac{5\pi}{3}$"
        elif np.isclose(rad_val, 7*np.pi/4):
            display_str = r"$\frac{7\pi}{4}$"
        elif np.isclose(rad_val, 11*np.pi/6):
            display_str = r"$\frac{11\pi}{6}$"
        elif np.isclose(rad_val, 2*np.pi):
            display_str = r"$2\pi$"
        else:
            display_str = rf"${rad_val:.4f} \text{{ rad}}$" # 그 외의 경우 소수점 표시에도 raw string

        angles_rad_display.append(display_str)
        angle_to_rad[display_str] = rad_val

    selected_angle_rad_display = st.sidebar.selectbox(
        "각도를 선택하세요 (라디안):",
        angles_rad_display,
        index=angles_rad_display.index(r"$\frac{\pi}{6}$") if r"$\frac{\pi}{6}$" in angles_rad_display else 0
    )
    angle_rad = angle_to_rad[selected_angle_rad_display]
    display_angle = selected_angle_rad_display

st.markdown("---")

st.header("계산 결과")

# 삼각함수 값 계산
trig_value = get_trig_value(selected_func, angle_rad)
formatted_trig_value = format_value_latex(trig_value)

# 결과 출력
st.markdown(rf"선택한 삼각함수: $\large\text{{{selected_func.upper()}}}$") # 여기도 raw string
st.markdown(rf"선택한 각도: $\large{display_angle}$") # 여기도 raw string
st.markdown(f"") # 간격 조절
st.markdown(rf"결과: $\huge\text{{{selected_func.upper()}}}(\large{display_angle}) = {formatted_trig_value}$") # 여기도 raw string

st.markdown("---")
st.markdown("궁금한 삼각함수 값을 선택하고 각도를 변경하여 확인해보세요!")
