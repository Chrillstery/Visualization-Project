import pandas as pd
import plotly.express as px
import streamlit as st
import streamlit.components.v1 as components
import pyecharts.options as opts
from pyecharts.charts import Line, Bar, Pie


def create_rose_chart(label, values):
    c = (
        Pie()
        .add(
            "",
            [list(z) for z in zip(label, values)],
            radius=["30%", "75%"],
            center=["50%", "50%"],
            rosetype="radius",
            label_opts=opts.LabelOpts(is_show=False),
        )
        .set_global_opts(title_opts=opts.TitleOpts(title="玫瑰图"))
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}:{c} {d}%"))
    )

    # 将图表渲染为 HTML 字符串
    return c.render_embed()


st.set_page_config(layout="wide")
st.title("全国经济相关数据对比分析")
st.sidebar.title("全国经济相关数据对比分析")
st.markdown(
    "[点击跳转到地图](http://localhost:63342/%E5%A4%A7%E4%BD%9C%E4%B8%9A%E9%98%B6%E6%AE%B52/%E5%B1%95%E7%A4%BA.html?_ijt=rvfolou16u984hv547t5l174cf&_ij_reload=RELOAD_ON_SAVE)")
st.markdown(
    "[点击跳转到主题河流](http://localhost:63342/%E5%A4%A7%E4%BD%9C%E4%B8%9A%E9%98%B6%E6%AE%B52/demo.html?_ijt=q58bkq60o6s1bdg18hsml044p9&_ij_reload=RELOAD_ON_SAVE)")
DATA_URL = "data1.csv"


def load_data(url):
    data = pd.read_csv(url, sep='\t')
    return data


data = load_data(DATA_URL)


def create_chart(data, category, chart_type, title):
    if chart_type == 'Bar':
        fig = px.bar(data, x='地区', y=category, color='地区', title=title)
    elif chart_type == 'Pie':
        fig = px.pie(data, names='地区', values=category, title=title)
    return fig


# 创建一个用于选择年份和城市的辅助函数
def selection_ui(key_prefix):
    col1, col2 = st.sidebar.columns(2)
    with col1:
        all_selected = st.checkbox('全选', key=f"{key_prefix}_all")
        if all_selected:
            selected_cities = data['地区'].unique().tolist()
        else:
            selected_cities = st.multiselect('选择城市', data['地区'].unique(), key=f"{key_prefix}_cities")
    with col2:
        selected_year = st.radio('选择年份', [f'{year}年' for year in range(2012, 2023)], key=f"{key_prefix}_year")
    return selected_cities, selected_year


# 创建一个用于生成图表的辅助函数
def generate_chart(category, key_prefix):
    selected_cities, selected_year = selection_ui(key_prefix)
    if not selected_cities:
        selected_cities = ['北京市']
    if not selected_year:
        selected_year = '2012年'

    filtered_data = data[(data['年份'] == selected_year) & (data['地区'].isin(selected_cities))]

    chart_type = st.sidebar.selectbox('选择图表类型', ['Bar', 'Pie'], key=f"{key_prefix}_chart_type")
    if chart_type == 'Bar':
        fig = create_chart(filtered_data, category, chart_type, f'选定城市的{category}对比')
        st.plotly_chart(fig)
    else:
        label = filtered_data['地区']
        values = filtered_data[category]
        rose_chart_html = create_rose_chart(label, values)
        components.html(rose_chart_html, height=500)


# 为每个类别生成图表
# 2002 - 2011 年的数据
html_file = open('finance_indices_2002.html', 'r', encoding='utf-8')
source_code = html_file.read()
components.html(source_code, width=1000, height=600)
html_file = open('demo.html', 'r', encoding='utf-8')
source_code = html_file.read()
st.components.v1.html(source_code,width=1000,height=600)
generate_chart('GDP', 'gdp')
generate_chart('人口', 'population')
generate_chart('第一产业', 'primary_industry')
generate_chart('第二产业', 'secondary_industry')
generate_chart('第三产业', 'tertiary_industry')
