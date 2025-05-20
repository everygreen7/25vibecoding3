
import streamlit as st
import pandas as pd
import plotly.express as px

# Load the data
@st.cache_data
def load_data():
    df_total = pd.read_csv("남여합계.csv", encoding="cp949")
    df_gender = pd.read_csv("남여구분.csv", encoding="cp949")
    return df_total, df_gender

df_total, df_gender = load_data()

# Select administrative district
districts = df_gender["행정구역"].unique()
selected_district = st.selectbox("행정구역을 선택하세요", districts)

# Filter data
row = df_gender[df_gender["행정구역"] == selected_district].iloc[0]

# Extract age columns
male_cols = [col for col in df_gender.columns if "남_" in col and "세" in col]
female_cols = [col for col in df_gender.columns if "여_" in col and "세" in col]

ages = [col.split("_")[-1].replace("세", "") for col in male_cols]
male_values = [int(str(row[col]).replace(",", "")) for col in male_cols]
female_values = [int(str(row[col]).replace(",", "")) for col in female_cols]

df_plot = pd.DataFrame({
    "연령": ages,
    "남자": male_values,
    "여자": female_values
})

# Melt for plotting
df_melted = df_plot.melt(id_vars="연령", var_name="성별", value_name="인구수")

# Plot
fig = px.bar(df_melted, x="연령", y="인구수", color="성별", barmode="group",
             title=f"{selected_district} 연령별 남녀 인구 분포")
st.plotly_chart(fig)
