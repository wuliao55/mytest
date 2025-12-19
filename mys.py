import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import os  # 用于路径检查

# ===================== 全局配置 =====================
st.set_page_config(
    page_title="学生成绩分析与预测系统",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 【删除了所有CSS/JS/HTML注入代码】

# 加载数据（缓存避免重复读取）
@st.cache_data
def load_data():
    try:
        df = pd.read_excel("学生数据表.xlsx")
        # 数据预处理：确保数值字段格式正确
        numeric_cols = ["每周学习时长（小时）", "上课出勤率", "期中考试分数", "作业完成率", "期末考试分数"]
        df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors="coerce")
        return df
    except FileNotFoundError:
        st.error("❌ 未找到数据文件！请将「学生数据表.xlsx」放在代码同一目录下")
        st.stop()
    except Exception as e:
        st.error(f"❌ 数据加载失败：{str(e)}")
        st.stop()

df = load_data()

# ===================== 侧边栏导航 =====================
st.sidebar.title("📑 导航菜单")
page = st.sidebar.radio("选择功能模块", ["项目介绍", "专业数据分析", "成绩预测"])

# ===================== 1. 项目介绍界面 =====================
if page == "项目介绍":
    # 布局：左内容区 + 右示意图区（布局完全保留）
    col_left, col_right = st.columns([3, 1.2])

    with col_left:
        # 标题
        st.title("学生成绩分析与预测系统")

        # 项目概述
        st.header("一、项目概述")
        st.write("""
        本项目是一个基于Streamlit的学生成绩分析平台，通过机器学习技术，
        帮助教育工作者和学生深入了解学业表现，并预测期末考试成绩。
        """)

        # 主要特点（删除HTML标签，改为纯Markdown）
        st.subheader("主要特点：")
        st.write("""
        - 📊 **数据可视化**：多维度展示学生学业数据
        - 🔍 **专业分析**：多维度分析的详细统计分析
        - 🧠 **智能预测**：基于学习特征创建的成绩预测
        - 💡 **学习建议**：根据预测结果提供个性化反馈
        """)

        # 项目目标（布局保留，删除HTML标签）
        st.header("二、项目目标")
        goal_col1, goal_col2, goal_col3 = st.columns(3)
        
        with goal_col1:
            st.subheader("🎯 目标一")
            st.write("分析影响因素")
            st.write("""
            - 识别关键学习指标
            - 探索成绩相关因素
            - 辅助教学决策
            """)
        
        with goal_col2:
            st.subheader("✅ 目标二")
            st.write("可视化展示")
            st.write("""
            - 专业对比分析
            - 性别差异研究
            - 学习情况识别
            """)
        
        with goal_col3:
            st.subheader("🔮 目标三")
            st.write("成绩预测")
            st.write("""
            - 机器学习模型
            - 个性化成绩
            - 及时干预预警
            """)

        # 技术架构（布局保留，删除HTML标签）
        st.header("三、技术架构")
        tech_col1, tech_col2, tech_col3, tech_col4 = st.columns(4)
        
        with tech_col1:
            st.subheader("前端框架")
            st.write("Streamlit")
        
        with tech_col2:
            st.subheader("数据处理")
            st.write("Pandas\nNumPy")
        
        with tech_col3:
            st.subheader("可视化")
            st.write("Plotly\nMatplotlib")
        
        with tech_col4:
            st.subheader("机器学习")
            st.write("Scikit-Learn")

    # 右侧：系统界面示意图（容错逻辑完全保留）
    with col_right:
        st.subheader("系统界面预览")
        
        # 图片路径配置
        image_path = "system_demo.png"  # 相对路径（代码同目录）
        
        # 检查文件是否存在
        if os.path.exists(image_path):
            st.image(
                image_path,
                caption="专业数据分析界面",
                use_container_width=True
            )
        else:
            st.warning(f"""
            ⚠️ 未找到图片文件！请按以下步骤操作：
            1. 将系统界面示意图保存为「{image_path}」
            2. 放在代码文件的同一目录下
            3. 或修改代码中「image_path」为图片绝对路径
            """)

# ===================== 2. 专业数据分析界面 =====================
elif page == "专业数据分析":
    st.title("📚 专业数据分析")
    
    # 1. 按专业计算核心统计指标（逻辑完全保留）
    major_stats = df.groupby("专业").agg({
        "每周学习时长（小时）": "mean",
        "期中考试分数": "mean",
        "期末考试分数": "mean",
        "上课出勤率": "mean"
    }).round(2).reset_index()
    major_stats.columns = ["专业", "每周平均学时", "期中平均分", "期末平均分", "平均出勤率"]

    # 1.1 专业核心指标表格
    st.subheader("1. 各专业核心学习指标统计")
    st.table(major_stats[["专业", "每周平均学时", "期中平均分", "期末平均分"]])

    # 2. 专业性别比例（双层柱状图）
    st.subheader("2. 各专业男女性别比例")
    gender_dist = df.groupby(["专业", "性别"]).size().reset_index(name="人数")
    fig_gender = px.bar(
        gender_dist, x="专业", y="人数", color="性别",
        barmode="group", title="各专业男女生人数分布",
        color_discrete_map={"男": "#1f77b4", "女": "#ff7f0e"}
    )
    st.plotly_chart(fig_gender, use_container_width=True)

    # 3. 期中/期末分数对比（折线图）
    st.subheader("3. 各专业期中-期末分数趋势")
    score_long = major_stats.melt(
        id_vars="专业", value_vars=["期中平均分", "期末平均分"],
        var_name="考试类型", value_name="分数"
    )
    fig_score = px.line(
        score_long, x="专业", y="分数", color="考试类型",
        markers=True,
        title="各专业期中/期末分数对比"
    )
    st.plotly_chart(fig_score, use_container_width=True)

    # 4. 专业平均出勤率（单层柱状图）
    st.subheader("4. 各专业平均上课出勤率")
    fig_attendance = px.bar(
        major_stats, x="专业", y="平均出勤率",
        color="平均出勤率", color_continuous_scale="Blues",
        title="各专业平均上课出勤率",
        range_y=[0.6, 1.0]
    )
    st.plotly_chart(fig_attendance, use_container_width=True)

    # 5. 大数据管理专业专项分析
    st.subheader("5. 大数据管理专业专项分析")
    bd_major = major_stats[major_stats["专业"] == "大数据管理"]
    if not bd_major.empty:
        bd_att = bd_major["平均出勤率"].values[0]
        bd_final = bd_major["期末平均分"].values[0]
        # 显示数值（转换出勤率为百分比）
        st.write(f"""
        - 📋 平均上课出勤率：{bd_att:.2f}（{bd_att*100:.1f}%）
        - 📋 期末考试平均分：{bd_final:.2f} 分
        """)
        
        # 构建双Y轴组合图（逻辑完全保留）
        fig_bd = go.Figure()
        
        # 左侧Y轴：期末分数（柱状图）
        fig_bd.add_trace(go.Bar(
            x=["大数据管理专业"],
            y=[bd_final],
            name="期末考试平均分",
            yaxis="y1",
            marker_color="#3498db",
            text=[f"{bd_final:.2f}分"],
            textposition="auto"
        ))
        
        # 右侧Y轴：出勤率（折线+标记）
        fig_bd.add_trace(go.Scatter(
            x=["大数据管理专业"],
            y=[bd_att],
            name="平均上课出勤率",
            yaxis="y2",
            mode="markers+lines+text",
            marker=dict(size=15, color="#e74c3c"),
            text=[f"{bd_att:.2f}"],
            textposition="top center"
        ))
        
        # 双Y轴配置
        fig_bd.update_layout(
            title="大数据管理专业核心指标对比",
            yaxis=dict(
                title=dict(
                    text="期末考试平均分（分）",
                    font=dict(color="#3498db")
                ),
                tickfont=dict(color="#3498db"),
                range=[0, 100]
            ),
            yaxis2=dict(
                title=dict(
                    text="平均上课出勤率",
                    font=dict(color="#e74c3c")
                ),
                tickfont=dict(color="#e74c3c"),
                range=[0, 1],
                overlaying="y",
                side="right"
            ),
            legend=dict(x=0.01, y=0.99),
            width=800, height=400
        )
        
        st.plotly_chart(fig_bd, use_container_width=True)
    else:
        st.warning("⚠️ 当前数据中未包含「大数据管理」专业，可将代码中\"大数据管理\"替换为实际存在的专业（如\"人工智能\"）重新运行")

# ===================== 3. 成绩预测界面 =====================
elif page == "成绩预测":
    st.title("🔮 期末成绩预测")
    st.write("输入学生学习信息，系统将基于机器学习模型预测期末成绩并提供个性化建议")

    # 输入组件布局（完全保留）
    col1, col2 = st.columns(2)
    with col1:
        student_id = st.text_input("学号（选填）", placeholder="例如：2023000001")
        gender = st.selectbox("性别", df["性别"].unique())
        major = st.selectbox("专业", df["专业"].unique())
    with col2:
        study_hours = st.slider("每周学习时长（小时）", 5.0, 40.0, 20.0, 0.5)
        attendance = st.slider("上课出勤率", 0.6, 1.0, 0.8, 0.01)
        mid_score = st.slider("期中考试分数", 0.0, 100.0, 75.0, 0.5)
        homework_rate = st.slider("作业完成率", 0.7, 1.0, 0.85, 0.01)

    # 训练预测模型（逻辑完全保留）
    @st.cache_resource
    def train_pred_model():
        X = df[["每周学习时长（小时）", "上课出勤率", "期中考试分数", "作业完成率"]]
        y = df["期末考试分数"]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model = LinearRegression()
        model.fit(X_train, y_train)
        r2 = r2_score(y_test, model.predict(X_test))
        return model, r2

    model, model_r2 = train_pred_model()

    # 预测按钮
    if st.button("🚀 开始预测", type="primary"):
        input_feat = [[study_hours, attendance, mid_score, homework_rate]]
        pred_score = model.predict(input_feat)[0].round(2)
        
        # 展示预测结果
        st.subheader("📝 预测结果")
        st.success(f"该学生期末成绩预测为：{pred_score} 分")
        
        # 专属鼓励（保留逻辑，删除HTML相关）
        st.subheader("💖 专属鼓励")
        # 定义图片路径（需与代码放在同一目录）
        if pred_score >= 60:
            img_name = "perfect.png"  # 及格/优秀图
            img_caption = "太棒啦！继续保持这个好状态~"
        else:
            img_name = "cheerup.png"  # 不及格加油图
            img_caption = "别灰心，调整计划加油冲~"
        
        # 显示图片（容错处理完全保留）
        if os.path.exists(img_name):
            st.image(img_name, caption=img_caption, use_container_width=True)
        else:
            st.warning(f"请将「{img_name}」图片文件放在代码同一目录下，以显示鼓励图片~")
        
        # 个性化学习建议（完全保留）
        st.subheader("💡 个性化学习建议")
        if pred_score >= 85:
            st.info("🎉 你的学习状态优秀！建议保持当前学习节奏，可适当拓展知识深度，参与学科竞赛/科研项目提升综合能力~")
        elif 70 <= pred_score < 85:
            st.info(f"👍 成绩良好！建议将每周学习时长从{study_hours}小时提升至22+小时，重点巩固期中薄弱知识点，成绩可进一步提升~")
        elif 60 <= pred_score < 70:
            st.warning(f"⚠️ 成绩及格但需提升！建议提高上课出勤率（当前{attendance}）至0.9以上，增加作业完成质量检查，针对性补习期中低分模块~")
        else:
            st.error(f"❌ 成绩未达标！需紧急调整学习计划：保证出勤率≥0.95，每周学习时长≥25小时，重新梳理期中知识点，完成所有作业并错题复盘~")
        
        # 模型精度说明
        st.caption(f"📊 模型预测准确率（R²）：{model_r2:.2f}（数值越接近1，预测越准确）")
