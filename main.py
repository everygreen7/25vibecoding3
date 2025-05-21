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
        if abs(np.cos(angle_rad)) < 1e-9: # 1e-9는 매우 작은 값으로, 부동 소수점 오차 처리
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
    return f"{value:.4f}"

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
    else: return rf"{rad_val:.4f} \text{{ rad}}" # 일반적인 라디안 값

st.set_page_config(layout="centered")

st.title("📏 삼각함수 값 확인 앱")
st.markdown("고등학교 2학년 학생들을 위한 삼각함수 값 확인 도우미입니다.")

st.sidebar.header("설정")

# 1. 삼각함수 선택
selected_func = st.sidebar.radio(
    "삼각함수를 선택하세요:",
    ("sin", "cos", "tan"),
    index=0,
    format_func=lambda x: x.upper()
)

# 2. 각도 단위 선택
angle_unit = st.sidebar.radio(
    "각도 단위를 선택하세요:",
    ("도 (Degrees)", "라디안 (Radians)"),
    index=0
)

st.markdown("---")
st.header("각도 선택")

# 3. 각도 리스트 생성 (30, 45, 60의 배수)
angles_deg_values = []
for i in range(0, 13):
    angles_deg_values.append(i * 30)
for i in range(1, 9):
    angles_deg_values.append(i * 45)
for i in range(1, 7):
    angles_deg_values.append(i * 60)

angles_deg_values = sorted(list(set(angles_deg_values)))

# 세션 상태를 사용하여 선택된 각도 저장
if 'selected_angle_rad' not in st.session_state:
    st.session_state.selected_angle_rad = np.deg2rad(30) # 초기값 설정 (30도)
    st.session_state.display_angle_latex = r"30^\circ" # 초기값 LaTeX 표시

# 각도 버튼 생성
cols = st.columns(6) # 6개의 열로 버튼 정렬

current_col_idx = 0
for deg_val in angles_deg_values:
    with cols[current_col_idx]:
        if angle_unit == "도 (Degrees)":
            button_label = rf"${deg_val}^\circ$"
            button_rad_value = np.deg2rad(deg_val)
            button_latex_display = rf"{deg_val}^\circ"
        else: # 라디안 선택 시
            rad_val = np.deg2rad(deg_val)
            button_label = rf"${get_latex_rad_display(rad_val)}$" # 버튼에 LaTeX 표시
            button_rad_value = rad_val
            button_latex_display = get_latex_rad_display(rad_val)
        
        # 버튼을 누르면 세션 상태 업데이트
        if st.button(button_label, key=f"angle_{deg_val}_{angle_unit}"):
            st.session_state.selected_angle_rad = button_rad_value
            st.session_state.display_angle_latex = button_latex_display
    
    current_col_idx = (current_col_idx + 1) % 6 # 다음 열로 이동

st.markdown("---")
st.header("계산 결과")

# 삼각함수 값 계산
trig_value = get_trig_value(selected_func, st.session_state.selected_angle_rad)
formatted_trig_value_latex = format_value_latex(trig_value)

# 결과 출력 - st.latex 사용
st.markdown(f"선택한 삼각함수: **{selected_func.upper()}**")

st.markdown(f"선택된 각도: ")
st.latex(st.session_state.display_angle_latex)

st.markdown(f"") # 간격 조절
st.markdown("결과:")
st.latex(rf"\text{{{selected_func.upper()}}}({st.session_state.display_angle_latex}) = {formatted_trig_value_latex}")

st.markdown("---")
st.markdown("궁금한 삼각함수 값을 선택하고 각도를 변경하여 확인해보세요!")
