import streamlit as st
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud, STOPWORDS

st.title("全国GDP对比分析")
st.sidebar.title("全国GDP对比分析")

st.markdown(" gdp and  人口️ ")
st.markdown("[点击跳转到地图](http://localhost:63342/%E5%8F%AF%E8%A7%86%E5%8C%96%E5%A4%A7%E4%BD%9C%E4%B8%9A/%E5%A4%A7%E4%BD%9C%E4%B8%9A/%E5%B1%95%E7%A4%BA.html?_ijt=o9d7dvljt5ikscarkthp5om2h7&_ij_reload=RELOAD_ON_SAVE)")

st.sidebar.markdown(" gdp️ ")

DATA_URL = r"D:\\pycharm\\可视化大作业\\大作业\\data1.csv"


data = pd.read_csv(DATA_URL,sep='\t')
city_name = data['地区']


st.sidebar.subheader("显示城市的GDP")

years = [str(year) + '年' for year in range(2012, 2023)]
provinces = ['北京市', '上海市', '天津市', '重庆市', '河北省', '山西省', '辽宁省', '吉林省', '黑龙江省', '江苏省', '浙江省', '安徽省', '福建省', '江西省', '山东省', '河南省', '湖北省', '湖南省', '广东省', '海南省', '四川省', '贵州省', '云南省', '陕西省', '甘肃省', '青海省', '台湾省', '内蒙古自治区', '广西壮族自治区', '西藏自治区', '宁夏回族自治区', '新疆维吾尔自治区', '香港特别行政区', '澳门特别行政区']
serise = ['GDP', '人口', '第一产业', '第二产业', '第三产业']
col1, col2 = st.sidebar.columns(2)
with col1:
    all_selected = st.checkbox('全选',key="地区")
    if all_selected:
        selected_cities = provinces  # 如果“全选”被选中，则将所有城市都选中
    else:
        selected_cities = st.multiselect('选择城市', provinces,key="地区1")
with col2:
    selected_years = st.radio('选择年份', years,key="地区2")


if selected_cities == [] or selected_years == []:
    selected_cities .append('北京市')
    selected_years ='2022年'

df = pd.DataFrame({
    '地区': pd.Series(dtype=str),
    'GDP': pd.Series(dtype=float),
    '颜色': pd.Series(dtype=str)  # 添加一个用于存储颜色的列
})


for index, row in data.iterrows():
    if row['年份'] == selected_years and row['地区'] in selected_cities:
        df = df._append({'地区': row['地区'], 'GDP': row['GDP'], '颜色': row['地区']}, ignore_index=True)

# 创建图表，并使用'颜色'列来映射颜色
fig = px.bar(df, x='地区', y='GDP', color='颜色', title='选定城市的GDP对比（人均地区生产总值（元/每人))')
st.plotly_chart(fig)



st.sidebar.subheader("显示城市的人口数")
col3, col4 = st.sidebar.columns(2)
with col3:
    all_selected1 = st.checkbox('全选',key="人口")
    if all_selected1:
        selected_cities = provinces  # 如果“全选”被选中，则将所有城市都选中
    else:
        selected_cities = st.multiselect('选择城市', provinces,key="人口1")
with col4:
    selected_years = st.radio('选择年份', years,key="人口2")


if selected_cities == [] or selected_years == []:
    selected_cities .append('北京市')
    selected_years ='2022年'

df1 = pd.DataFrame({
    '地区': pd.Series(dtype=str),
    '人口': pd.Series(dtype=float),
    '颜色': pd.Series(dtype=str)  # 添加一个用于存储颜色的列
})


for index, row in data.iterrows():
    if row['年份'] == selected_years and row['地区'] in selected_cities:
        df1 = df1._append({'地区': row['地区'], '人口': row['人口'], '颜色': row['地区']}, ignore_index=True)

# 创建图表，并使用'颜色'列来映射颜色
fig = px.bar(df1, x='地区', y='人口', color='颜色', title='选定城市的人口对比')
st.plotly_chart(fig)