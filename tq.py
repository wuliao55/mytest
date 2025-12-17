# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import plotly.express as px
import os

def get_dataframe_from_excel():
    """读取Excel销售数据，返回处理后的DataFrame"""
    # 替换为你的Excel文件实际路径（比如D:\data\supermarket_sales.xlsx）
    excel_path = r'D:\streamlit_env\（商场销售数据）supermarket_sales.xlsx'  # r表示原始字符串，避免路径转义
    if not os.path.exists(excel_path):
        st.error(f"未找到Excel文件：{excel_path}")
        st.stop()  # 停止程序运行
    
    try:
        # 读取Excel数据（跳过首行标题，以订单号为索引）
        df = pd.read_excel(
            excel_path,
            sheet_name='销售数据',
            skiprows=1,
            index_col='订单号',
            engine='openpyxl'  # 指定引擎，避免Excel读取警告
        )
        
        # 提取交易小时数（新增列）
        df['小时数'] = pd.to_datetime(df["时间"], format="%H:%M:%S").dt.hour
        return df
    except Exception as e:
        st.error(f"读取Excel失败：{str(e)}")
        st.stop()

def add_sidebar_func(df):
    """创建侧边栏筛选器，返回筛选后的数据"""
    with st.sidebar:
        st.header("🔍 数据筛选条件")
        
        # 城市筛选
        city_unique = df["城市"].unique()
        city = st.multiselect(
            "选择城市：",
            options=city_unique,
            default=city_unique,
            key="city_select"
        )
        
        # 顾客类型筛选
        customer_type_unique = df["顾客类型"].unique()
        customer_type = st.multiselect(
            "选择顾客类型：",
            options=customer_type_unique,
            default=customer_type_unique,
            key="customer_type_select"
        )
        
        # 性别筛选
        gender_unique = df["性别"].unique()
        gender = st.multiselect(
            "选择性别：",
            options=gender_unique,
            default=gender_unique,
            key="gender_select"
        )
        
        # 应用筛选条件
        df_selection = df.query(
            "城市 == @city & 顾客类型 ==@customer_type & 性别 == @gender"
        )
        
        # 显示筛选后的数据量
        st.info(f"筛选后数据量：{len(df_selection)} 条")
    
    return df_selection

def product_line_chart(df):
    """生成按产品类型划分的销售额横向条形图"""
    # 按产品类型分组计算总销售额并排序
    sales_by_product_line = df.groupby(by=["产品类型"])["总价"].sum().sort_values()
    
    # 绘制横向条形图
    fig = px.bar(
        sales_by_product_line,
        x="总价",
        y=sales_by_product_line.index,
        orientation="h",
        title="<b>按产品类型划分的销售额</b>",
        color="总价",  # 增加颜色渐变
        color_continuous_scale=px.colors.sequential.Blues,
        template="plotly_white"  # 简洁风格
    )
    
    # 优化图表样式
    fig.update_layout(
        xaxis_title="销售额（RMB）",
        yaxis_title="产品类型",
        height=400
    )
    return fig

def hour_chart(df):
    """生成按小时数划分的销售额条形图"""
    # 按小时数分组计算总销售额
    sales_by_hour = df.groupby(by=["小时数"])["总价"].sum()
    
    # 绘制纵向条形图
    fig = px.bar(
        sales_by_hour,
        x=sales_by_hour.index,
        y="总价",
        title="<b>按小时数划分的销售额</b>",
        color="总价",
        color_continuous_scale=px.colors.sequential.Oranges,
        template="plotly_white"
    )
    
    # 优化图表样式
    fig.update_layout(
        xaxis_title="交易小时（24小时制）",
        yaxis_title="销售额（RMB）",
        height=400
    )
    return fig

def main_page_demo(df):
    """渲染主页面（关键指标+图表）"""
    # 页面标题
    st.title(':bar_chart: 超市销售数据分析仪表板')
    st.markdown("---")  # 分割线
    
    # 计算核心指标
    total_sales = int(df["总价"].sum())  # 总销售额
    average_rating = round(df["评分"].mean(), 1)  # 平均评分
    star_rating = ":star:" * int(round(average_rating, 0))  # 星级展示
    avg_per_trans = round(df["总价"].mean(), 2)  # 单笔平均销售额
    
    # 核心指标展示（三列布局）
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("总销售额")
        st.metric(label="", value=f"¥ {total_sales:,}", delta="本月累计")
    with col2:
        st.subheader("平均评分")
        st.metric(label="", value=f"{average_rating} {star_rating}", delta="顾客满意度")
    with col3:
        st.subheader("单笔平均销售额")
        st.metric(label="", value=f"¥ {avg_per_trans}", delta="交易均值")
    
    st.markdown("---")  # 分割线
    
    # 图表展示（两列布局）
    col_left, col_right = st.columns(2)
    with col_left:
        st.plotly_chart(hour_chart(df), use_container_width=True)
    with col_right:
        st.plotly_chart(product_line_chart(df), use_container_width=True)
    
    # 可选：展示原始数据（折叠面板）
    with st.expander("📋 查看筛选后原始数据"):
        st.dataframe(df, use_container_width=True)

def run_app():
    """应用入口函数"""
    # 页面基础配置
    st.set_page_config(
        page_title="销售仪表板",
        page_icon=":bar_chart:",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # 读取数据 → 筛选数据 → 渲染页面
    df_raw = get_dataframe_from_excel()
    df_filtered = add_sidebar_func(df_raw)
    main_page_demo(df_filtered)

if __name__ == "__main__":
    run_app()
