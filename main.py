import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
from sklearn.cluster import KMeans

# 데이터 로딩
df = pd.read_csv("Delivery - Delivery.csv")

st.title("🗺️ 위치 기반 배송 군집 분석")

# 결측치 제거
df = df.dropna(subset=['Latitude', 'Longitude'])

# 클러스터 수 선택
k = st.slider("군집 수 (K)", min_value=2, max_value=10, value=3)

# KMeans 적용
kmeans = KMeans(n_clusters=k, random_state=42, n_init='auto')
df['Cluster'] = kmeans.fit_predict(df[['Latitude', 'Longitude']])

# 지도 생성
st.subheader("📍 Folium 지도 시각화")
m = folium.Map(location=[df['Latitude'].mean(), df['Longitude'].mean()], zoom_start=12)
marker_cluster = MarkerCluster().add_to(m)

# 마커 표시
colors = ['red', 'blue', 'green', 'purple', 'orange', 'darkred', 'lightblue', 'beige', 'pink', 'gray']
for _, row in df.iterrows():
    folium.Marker(
        location=[row['Latitude'], row['Longitude']],
        popup=f"Cluster {row['Cluster']}",
        icon=folium.Icon(color=colors[row['Cluster'] % len(colors)])
    ).add_to(marker_cluster)

folium_static(m)
