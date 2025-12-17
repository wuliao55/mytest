# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import plotly.express as px
import os

def get_dataframe_from_excel():
    """读取Excel销售数据，返回处理后的DataFrame（全容错版）"""
    # 1. 配置Excel路径（确保和实际文件名完全一致）
    excel_path = r'D:\streamlit_env\（商场销售数据）supermarket_sales.xlsx'
    
    # 检查文件是否存在
    if not os.path.exists(excel_path):
        st.error(f"❌ 未找到Excel文件：{excel_path}")
        st.error("请确认：1.文件路径正确 2.文件名（包括括号/中文）完全匹配 3.文件在指定目录下")
        st.stop()
    
    try:
        # 2. 读取Excel（适配不同sheet名/列名，跳过标题行）
        # 先尝试读取指定sheet，失败则读取第一个sheet
        try:
            df = pd.read_excel(
                excel_path,
                sheet_name='销售数据',  # 若sheet名不是这个，改成Excel里的实际sheet名（比如Sheet1）
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
        
        # 3. 去除列名首尾空格（解决列名带空格的坑）
        df.columns = [col.strip() for col in df.columns]
        
        # 调试：打印列名（方便核对）
        st.write("📌 Excel真实列名（跳过标题行后）：")
        st.write(df.columns.tolist())
        
        # 4. 核心列检查（确保关键列存在）
        required_cols = ["订单号", "城市", "顾客类型", "性别", "产品类型", "总价", "评分", "时间"]
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            st.error(f"❌ Excel缺少关键列：{missing_cols}")
            st.stop()
        
        # 5. 处理订单号索引（避免索引错误）
        df = df.set_index("订单号", drop=False)  # 保留订单号列，同时设为索引
        
        # 6. 提取交易小时数（适配%H:%M和%H:%M:%S两种时间格式）
        df["小时数"] = pd.to_datetime(df["时间"], format="%H:%M:%S", errors="coerce").dt.hour
        # 若上面解析失败，尝试%H:%M格式
        if df["小时数"].isnull().all():
            df["小时数"] = pd.to_datetime(df["时间"], format="%H:%M", errors="coerce").dt.hour
        
        # 7. 处理缺失值
        df = df.dropna(subset=["总价", "评分", "小时数"])
        
        return df
    
    except Exception as e:
        st.error(f"❌ 读取Excel失败：{str(e)}")
        st.error("常见原因：1.sheet名错误 2.列名不匹配 3.跳过的标题行数不对 4.Excel文件损坏")
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
        
        # 应用筛选条件（容错版）
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
    # 按产品类型分组计算总销售额并排序
    sales_by_product_line = df.groupby(by=["产品类型"])["总价"].sum().sort_values()
    
    # 绘制横向条形图
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
    
    # 优化图表样式
    fig.update_layout(
        xaxis_title="销售额（RMB）",
        yaxis_title="产品类型",
        height=400,
        margin=dict(l=10, r=10, t=30, b=10)
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
        height=400,
        margin=dict(l=10, r=10, t=30, b=10)
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
