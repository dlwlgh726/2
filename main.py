import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="배송 데이터 대시보드", layout="wide")

st.title("🚚 배송 데이터 시각화 대시보드")

# CSV 데이터 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv("Delivery.csv")
    return df

df = load_data()

# 날짜 컬럼 자동 처리
if 'Date' in df.columns:
    df['Date'] = pd.to_datetime(df['Date'])

# 데이터 미리보기
st.subheader("📄 데이터 미리보기")
st.dataframe(df.head(), use_container_width=True)

# 사이드바 필터
st.sidebar.header("🔍 필터")
if 'City' in df.columns:
    city_list = df['City'].dropna().unique()
    selected_city = st.sidebar.selectbox("도시 선택", city_list)
    df = df[df['City'] == selected_city]

# 시각화 1: 날짜별 배송 수량
if 'Date' in df.columns and 'Delivery Count' in df.columns:
    st.subheader("📊 날짜별 배송 횟수")
    fig1 = px.bar(df, x="Date", y="Delivery Count", title="날짜별 배송 횟수", color='Delivery Count')
    st.plotly_chart(fig1, use_container_width=True)

# 시각화 2: 배송 상태 비율
if 'Status' in df.columns:
    st.subheader("📈 배송 상태 비율")
    status_df = df['Status'].value_counts().reset_index()
    status_df.columns = ['Status', 'Count']
    fig2 = px.pie(status_df, names='Status', values='Count', title="배송 상태 비율")
    st.plotly_chart(fig2, use_container_width=True)

# 시각화 3: 거리 vs 소요 시간
if 'Distance' in df.columns and 'Time Taken' in df.columns:
    st.subheader("📌 거리 vs 소요 시간")
    fig3 = px.scatter(df, x='Distance', y='Time Taken', color='Status', title="거리와 소요 시간 관계")
    st.plotly_chart(fig3, use_container_width=True)
