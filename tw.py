import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os  # 新增：用于检查文件是否存在

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# 自定义CSS样式（匹配目标筛选器/布局风格）
st.markdown("""
<style>
/* 筛选器标签样式（红色背景+白色文字） */
.stMultiSelect div[data-baseweb="tag"] {
    background-color: #dc3545 !important;
    color: white !important;
}
.stMultiSelect div[data-baseweb="tag"] span[data-baseweb="tag-close"] {
    color: white !important;
}
/* 标题/指标样式优化 */
h1 {
    font-size: 28px !important;
    font-weight: bold !important;
}
h3 {
    font-size: 18px !important;
    color: #6c757d !important;
    margin-bottom: 5px !important;
}
.big-value {
    font-size: 24px !important;
    font-weight: bold !important;
}
</style>
""", unsafe_allow_html=True)

# 1. 数据加载（适配Cloud环境：相对路径+文件存在性检查）
def load_data():
    # 关键修改：使用Cloud项目根目录的相对路径（仅文件名）
    file_name = "supermarket_sales.xlsx"
    file_path = file_name  # 直接读取根目录下的文件
    
    # 检查文件是否存在（帮助排查问题）
    st.write("当前目录下的文件：", os.listdir('.'))  # 部署后可删除此行
    if file_name not in os.listdir('.'):
        st.error(f"错误：未找到 {file_name} 文件！请确认文件已上传到项目根目录，且文件名完全一致（区分大小写）。")
        st.stop()  # 终止程序，避免后续报错
    
    # 读取Excel（header=1保持不变，第2行为列名）
    df = pd.read_excel(file_path, header=1)
    
    # 时间列处理（适配带秒格式）
    df['时间_小时'] = pd.to_datetime(df['时间'], format='%H:%M:%S').dt.hour
    df['日期'] = pd.to_datetime(df['日期'], format='%Y/%m/%d')
    
    # 提取维度分类
    cities = df['城市'].unique().tolist()
    customer_types = df['顾客类型'].unique().tolist()
    genders = df['性别'].unique().tolist()
    product_types = df['产品类型'].unique().tolist()
    
    return df, cities, customer_types, genders, product_types

# 加载数据
df, cities, customer_types, genders, product_types = load_data()

# 2. 页面布局：左侧筛选栏 + 右侧内容区
left_col, main_col = st.columns([1, 3])  # 左侧占1份，右侧占3份

# 左侧筛选栏
with left_col:
    st.markdown("### 请筛选数据:")
    
    # 城市筛选
    st.markdown("#### 请选择城市:")
    selected_cities = st.multiselect(
        label="城市选项",
        options=cities,
        default=cities,
        key="city_select"
    )
    
    # 顾客类型筛选
    st.markdown("#### 请选择顾客类型:")
    selected_customers = st.multiselect(
        label="顾客类型选项",
        options=customer_types,
        default=customer_types,
        key="customer_select"
    )
    
    # 性别筛选
    st.markdown("#### 请选择性别:")
    selected_genders = st.multiselect(
        label="性别选项",
        options=genders,
        default=genders,
        key="gender_select"
    )

# 3. 数据筛选
filtered_df = df[
    (df['城市'].isin(selected_cities)) &
    (df['顾客类型'].isin(selected_customers)) &
    (df['性别'].isin(selected_genders))
].copy()

# 4. 核心指标计算
total_sales = filtered_df['总价'].sum()
avg_rating = filtered_df['评分'].mean()
avg_order_sales = filtered_df['总价'].mean()

# 右侧内容区（仪表板主体）
with main_col:
    # 标题
    st.markdown("# 📊 销售仪表板")
    
    # 核心指标展示（3列布局）
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 总销售额:")
        st.markdown(f'<p class="big-value">RMB ¥{total_sales:,.0f}</p>', unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 顾客评分的平均值:")
        # 生成对应数量的星星（取整）
        star_count = int(round(avg_rating, 0))
        stars = "★" * star_count
        st.markdown(f'<p class="big-value">{avg_rating:.1f} {stars}</p>', unsafe_allow_html=True)
    
    with col3:
        st.markdown("### 每单的平均销售额:")
        st.markdown(f'<p class="big-value">RMB ¥{avg_order_sales:.2f}</p>', unsafe_allow_html=True)
    
    st.markdown("---")  # 分隔线
    
    # 可视化图表区域
    st.markdown("### 销售数据分布")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    # 子图1：按小时划分的销售额（柱状图）
    hourly_sales = filtered_df.groupby('时间_小时')['总价'].sum().reset_index()
    ax1.bar(
        x=hourly_sales['时间_小时'],
        height=hourly_sales['总价'],
        color='#1f77b4',
        edgecolor='white'
    )
    ax1.set_title("按小时划分的销售额", fontweight='bold', fontsize=12)
    ax1.set_xlabel("小时数")
    ax1.set_ylabel("总价")
    ax1.grid(alpha=0.3, axis='y')
    ax1.set_xticks(hourly_sales['时间_小时'])  # 显示所有存在的小时

    # 子图2：按产品类型划分的销售额（水平条形图）
    product_sales = filtered_df.groupby('产品类型')['总价'].sum().sort_values(ascending=True)  # 升序排列（大值在上方）
    ax2.barh(
        y=product_sales.index,
        width=product_sales.values,
        color='#ff7f0e',
        edgecolor='white'
    )
    ax2.set_title("按产品类型划分的销售额", fontweight='bold', fontsize=12)
    ax2.set_xlabel("总价")
    ax2.set_ylabel("产品类型")
    ax2.grid(alpha=0.3, axis='x')

    plt.tight_layout()
    st.pyplot(fig)
