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
        # np.isclose 대신 절대값이 매우 작은지 확인하여 부동 소수점 오차를 더 잘 처리
        if abs(np.cos(angle_rad)) < 1e-9: # 1e-9는 매우 작은 값
            return "정의되지 않음"
        return np.tan(angle_rad)
    return None

def format_value_latex(value):
    """삼각함수 값을 LaTeX 형식으로 반환합니다."""
    if isinstance(value, str):
        return value  # '정의되지 않음'과 같은 문자열은 그대로 반환
    
    # 정수 및 특정 분수/무리수 값은 정확한 LaTeX 표현 사용
    if np.isclose(value, 0):
        return r"0"
    elif np.isclose(value, 1):
        return r"1"
    elif np.isclose(value, -1):
        return r"-1"
    elif np.isclose(value, 0.5):
        return r"\frac{1}{2}"
    elif np.isclose(value, -0.5):
        return r"-\frac{1}{2}"
    elif np.isclose(value, np.sqrt(2)/2):
        return r"\frac{\sqrt{2}}{2}"
    elif np.isclose(value, -np.sqrt(2)/2):
        return r"-\frac{\sqrt{2}}{2}"
    elif np.isclose(value, np.sqrt(3)/2):
        return r"\frac{\sqrt{3}}{2}"
    elif np.isclose(value, -np.sqrt(3)/2):
        return r"-\frac{\sqrt{3}}{2}"
    elif np.isclose(value, np.sqrt(3)):
        return r"\sqrt{3}"
    elif np.isclose(value, -np.sqrt(3)):
        return r"-\sqrt{3}"
    elif np.isclose(value, 1/np.sqrt(3)):
        return r"\frac{\sqrt{3}}{3}" # 유리화된 형태로
    elif np.isclose(value, -1/np.sqrt(3)):
        return r"-\frac{\sqrt{3}}{3}" # 유리화된 형태로
    
    # 그 외의 값은 소수점 4째 자리까지 표시
    return f"{value:.4f}" # 소수점 표현은 굳이 LaTeX로 감싸지 않아도 됨

# 라디안 값을 LaTeX 문자열로 변환하는 헬퍼 함수
def get_latex_rad_display(rad_val):
    if np.isclose(rad_val, 0): return r"0"
    elif np.isclose(rad_val, np.pi/6): return r"\frac{\pi}{6}"
    elif np.isclose(rad_val, np.pi/4): return r"\frac{\pi}{4}"
    elif np.isclose(rad_val, np.pi/3): return r"\frac{\pi}{3}"
    elif np.isclose(rad_val, np.pi/2): return r"\frac{\pi}{2}"
    elif np.isclose(rad_val, 2*np.pi/3): return r"\frac{2\pi}{3}"
    elif np.isclose(rad_val, 3*np.pi/4): return r"\frac{3\pi}{4}"
    elif np.isclose(rad_val, 5*np.pi/6): return r"\frac{5\pi}{6}"
    elif np.isclose(rad_val, np.pi): return r"\pi"
    elif np.isclose(rad_val, 7*np.pi/6): return r"\frac{7\pi}{6}"
    elif np.isclose(rad_val, 5*np.pi/4): return r"\frac{5\pi}{4}"
    elif np.isclose(rad_val, 4*np.pi/3): return r"\frac{4\pi}{3}"
    elif np.isclose(rad_val, 3*np.pi/2): return r"\frac{3\pi}{2}"
    elif np.isclose(rad_val, 5*np.pi/3): return r"\frac{5\pi}{3}"
    elif np.isclose(rad_val, 7*np.pi/4): return r"\frac{7\pi}{4}"
    elif np.isclose(rad_val, 11*np.pi/6): return r"\frac{11\pi}{6}"
    elif np.isclose(rad_val, 2*np.pi): return r"2\pi"
    else: return f"{rad_val:.4f} \\text{{ rad}}" # 일반적인 라디안 값

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

# 3. 각도 리스트 생성 (30, 45, 60의 배수)
angles_deg_raw = []
for i in range(0, 13): # 0도부터 360도까지 (0*30, 1*30, ..., 12*30)
    angles_deg_raw.append(i * 30)
for i in range(1, 9): # 45도 배수 (45, 90, ..., 360)
    angles_deg_raw.append(i * 45)
for i in range(1, 7): # 60도 배수 (60, 120, ..., 360)
    angles_deg_raw.append(i * 60)

angles_deg_raw = sorted(list(set(angles_deg_raw))) # 중복 제거 및 정렬

if angle_unit == "도 (Degrees)":
    selected_angle_deg = st.sidebar.selectbox(
        "각도를 선택하세요 (도):",
        angles_deg_raw,
        index=angles_deg_raw.index(30) if 30 in angles_deg_raw else 0
    )
    angle_rad = np.deg2rad(selected_angle_deg)
    display_angle_latex = rf"{selected_angle_deg}^\circ" # LaTeX 표기용 문자열
    display_angle_plain = f"{selected_angle_deg}°" # 일반 텍스트 표기용
else: # 라디안 선택 시
    # 드롭다운에는 일반적인 텍스트 라벨을 사용하고, 내부적으로 실제 라디안 값을 매핑
    rad_options_plain = []
    angle_rad_map = {} # 일반 텍스트 -> 라디안 값 매핑

    for angle_d in angles_deg_raw:
        rad_val = np.deg2rad(angle_d)
        
        # 일반 텍스트 표시 (드롭다운 메뉴용)
        if np.isclose(rad_val, 0): plain_str = "0"
        elif np.isclose(rad_val, np.pi/6): plain_str = "pi/6"
        elif np.isclose(rad_val, np.pi/4): plain_str = "pi/4"
        elif np.isclose(rad_val, np.pi/3): plain_str = "pi/3"
        elif np.isclose(rad_val, np.pi/2): plain_str = "pi/2"
        elif np.isclose(rad_val, np.pi): plain_str = "pi"
        elif np.isclose(rad_val, 2*np.pi): plain_str = "2pi"
        else: plain_str = f"{rad_val:.4f} rad"

        rad_options_plain.append(plain_str)
        angle_rad_map[plain_str] = rad_val

    selected_angle_plain = st.sidebar.selectbox(
        "각도를 선택하세요 (라디안):",
        rad_options_plain,
        index=rad_options_plain.index("pi/6") if "pi/6" in rad_options_plain else 0
    )
    angle_rad = angle_rad_map[selected_angle_plain]
    
    # 선택된 라디안 값에 대한 LaTeX 표현을 가져옴
    display_angle_latex = get_latex_rad_display(angle_rad)
    display_angle_plain = selected_angle_plain # 사이드바의 텍스트 그대로 사용

st.markdown("---")

st.header("계산 결과")

# 삼각함수 값 계산
trig_value = get_trig_value(selected_func, angle_rad)
formatted_trig_value_latex = format_value_latex(trig_value)

# 결과 출력 - st.latex 사용
# st.markdown(f"선택한 삼각함수: $\large\text{{{selected_func.upper()}}}$")
st.markdown(f"선택한 삼각함수: **{selected_func.upper()}**") # 일반 텍스트로 변경

# 각도 표시
st.markdown(f"선택한 각도: ")
st.latex(display_angle_latex) # 각도 LaTeX 표시

# 최종 결과 수식
st.markdown(f"") # 간격 조절
st.markdown("결과:")
st.latex(rf"\text{{{selected_func.upper()}}}({display_angle_latex}) = {formatted_trig_value_latex}")

st.markdown("---")
st.markdown("궁금한 삼각함수 값을 선택하고 각도를 변경하여 확인해보세요!")
