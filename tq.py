# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import plotly.express as px
import os

def get_dataframe_from_excel():
    """读取Excel销售数据，返回处理后的DataFrame（相对路径版）"""
    # 1. 相对路径：仅写文件名（前提：Excel和脚本在同一目录）
    excel_filename = "（商场销售数据）supermarket_sales.xlsx"  # Excel文件名（和脚本同目录）
    excel_path = os.path.join(os.path.dirname(__file__), excel_filename)  # 自动拼接脚本所在目录+文件名
    
    # 检查文件是否存在
    if not os.path.exists(excel_path):
        st.error(f"❌ 未找到Excel文件：{excel_path}")
        st.error("请确认：1.Excel文件和脚本在同一目录 2.文件名（包括括号/中文）完全匹配")
        # 打印脚本所在目录和目录下的文件，方便排查
        st.write(f"📌 脚本所在目录：{os.path.dirname(__file__)}")
        st.write(f"📂 目录下的文件：{os.listdir(os.path.dirname(__file__))}")
        st.stop()
    
    try:
        # 2. 读取Excel（适配不同sheet名/列名，跳过标题行）
        try:
            df = pd.read_excel(
                excel_path,
                sheet_name='销售数据',  # 若sheet名不对，改成Excel里的实际名称（如Sheet1）
                skiprows=1,            # 跳过第一行标题（2022年前3个月销售数据）
                engine='openpyxl'
            )
        except:
            df = pd.read_excel(
                excel_path,
                sheet_name=0,         # 读取第一个sheet
                skiprows=1,
                engine='openpyxl'
            )
        
        # 3. 去除列名首尾空格
        df.columns = [col.strip() for col in df.columns]
        
        # 调试：打印列名
        st.write("📌 Excel真实列名（跳过标题行后）：")
        st.write(df.columns.tolist())
        
        # 4. 核心列检查
        required_cols = ["订单号", "城市", "顾客类型", "性别", "产品类型", "总价", "评分", "时间"]
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            st.error(f"❌ Excel缺少关键列：{missing_cols}")
            st.stop()
        
        # 5. 处理订单号索引
        df = df.set_index("订单号", drop=False)
        
        # 6. 提取交易小时数（适配两种时间格式）
        df["小时数"] = pd.to_datetime(df["时间"], format="%H:%M:%S", errors="coerce").dt.hour
        if df["小时数"].isnull().all():
            df["小时数"] = pd.to_datetime(df["时间"], format="%H:%M", errors="coerce").dt.hour
        
        # 7. 处理缺失值
        df = df.dropna(subset=["总价", "评分", "小时数"])
        
        return df
    
    except Exception as e:
        st.error(f"❌ 读取Excel失败：{str(e)}")
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
        df_selection = df[
            (df["城市"].isin(city)) &
            (df["顾客类型"].isin(customer_type)) &
            (df["性别"].isin(gender))
        ]
        
        # 显示筛选后的数据量
        st.info(f"筛选后数据量：{len(df_selection)} 条")
    
    return df_selection

def product_line_chart(df):
    """生成按产品类型划分的销售额横向条形图"""
    sales_by_product_line = df.groupby(by=["产品类型"])["总价"].sum().sort_values()
    
    fig = px.bar(
        sales_by_product_line,
        x="总价",
        y=sales_by_product_line.index,
        orientation="h",
        title="<b>按产品类型划分的销售额</b>",
        color="总价",
        color_continuous_scale=px.colors.sequential.Blues,
        template="plotly_white"
    )
    
    fig.update_layout(
        xaxis_title="销售额（RMB）",
        yaxis_title="产品类型",
        height=400,
        margin=dict(l=10, r=10, t=30, b=10)
    )
    return fig

def hour_chart(df):
    """生成按小时数划分的销售额条形图"""
    sales_by_hour = df.groupby(by=["小时数"])["总价"].sum()
    
    fig = px.bar(
        sales_by_hour,
        x=sales_by_hour.index,
        y="总价",
        title="<b>按小时数划分的销售额</b>",
        color="总价",
        color_continuous_scale=px.colors.sequential.Oranges,
        template="plotly_white"
    )
    
    fig.update_layout(
        xaxis_title="交易小时（24小时制）",
        yaxis_title="销售额（RMB）",
        height=400,
        margin=dict(l=10, r=10, t=30, b=10)
    )
    return fig

def main_page_demo(df):
    """渲染主页面（关键指标+图表）"""
    st.title(':bar_chart: 超市销售数据分析仪表板')
    st.markdown("---")
    
    # 计算核心指标
    total_sales = int(df["总价"].sum())
    average_rating = round(df["评分"].mean(), 1)
    star_rating = ":star:" * int(round(average_rating, 0))
    avg_per_trans = round(df["总价"].mean(), 2)
    
    # 核心指标展示
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
    
    st.markdown("---")
    
    # 图表展示
    col_left, col_right = st.columns(2)
    with col_left:
        st.plotly_chart(hour_chart(df), use_container_width=True)
    with col_right:
        st.plotly_chart(product_line_chart(df), use_container_width=True)
    
    # 原始数据预览
    with st.expander("📋 查看筛选后原始数据"):
        st.dataframe(df, use_container_width=True)

def run_app():
    """应用入口函数"""
    st.set_page_config(
        page_title="销售仪表板",
        page_icon=":bar_chart:",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    df_raw = get_dataframe_from_excel()
    df_filtered = add_sidebar_func(df_raw)
    main_page_demo(df_filtered)

if __name__ == "__main__":
    run_app()
