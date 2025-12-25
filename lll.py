import streamlit as st
import pandas as pd
import altair as alt
import joblib
import os
from PIL import Image
from sklearn.ensemble import RandomForestRegressor

# ====================== 全局配置（白色主题适配） ======================
st.set_page_config(
    page_title="学生成绩分析与预测系统",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义白色主题样式
st.markdown("""
    <style>
    .stApp {
        background-color: #ffffff;
        color: #000000;
    }
    .stSidebar {
        background-color: #f8f9fa;
        color: #000000;
    }
    .stButton>button {
        background-color: #3498db;
        color: white;
    }
    .stMetric {
        background-color: #f1f3f5;
        padding: 10px;
        border-radius: 5px;
        color: #000000;
    }
    </style>
""", unsafe_allow_html=True)

# 定义文件路径（已匹配当前目录）
FILE_PATH = "学生数据表.xlsx"
MODEL_PATH = "model.pkl"
CONGRATS_IMG_PATH = "congratulations.png"
ENCOURAGE_IMG_PATH = "encouragement.png"
PROJECT_INTRO_IMG_PATH = "project_intro.png"  # 已在当前目录的图片路径

# ====================== 工具函数 ======================
def check_file_exists(file_path):
    if not os.path.exists(file_path):
        st.error(f"错误：未找到文件 {file_path}")
        st.info("请确认：1.文件名称正确 2.文件和app.py在同一目录")
        return False
    return True

@st.cache_data
def load_data():
    if not check_file_exists(FILE_PATH):
        return None
    df = pd.read_excel(FILE_PATH)
    df = df.dropna()
    return df

@st.cache_resource
def train_and_load_model(df):
    if os.path.exists(MODEL_PATH):
        return joblib.load(MODEL_PATH)
    st.info("首次运行，正在训练预测模型...")
    df_train = df.copy()
    df_train["性别"] = df_train["性别"].map({"男": 1, "女": 0})
    df_train["专业"] = pd.factorize(df_train["专业"], sort=True)[0]
    X = df_train[["性别", "专业", "每周学习时长（小时）", "上课出勤率", "期中考试分数", "作业完成率"]]
    y = df_train["期末考试分数"]
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
    joblib.dump(model, MODEL_PATH)
    st.success("模型训练完成！")
    return model

# ====================== 加载资源 ======================
df = load_data()
if df is not None:
    model = train_and_load_model(df)

# ====================== 侧边栏导航 ======================
st.sidebar.title("导航菜单")
page = st.sidebar.radio("选择页面", ["项目介绍", "专业数据分析", "成绩预测"])

# ====================== 界面1：项目介绍（修复图片加载） ======================
if page == "项目介绍":
    st.title("学生成绩分析与预测系统")
    
    st.subheader("项目概述")
    st.write("""
    本项目是一个基于Streamlit的学生成绩分析平台，通过可视化展示学习数据，帮助教育工作者和学生深入了解学习表现，并预测期末考试成绩。
    """)
    
    st.subheader("主要特点")
    st.markdown("""
    - **数据可视化**：多维度展示学生学业数据
    - **专业分析**：多维度的专业课程成绩分析
    - **智能预测**：基于学习行为数据的成绩预测
    - **学习建议**：根据预测结果提供个性化建议
    """)
    
    st.subheader("项目目标")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("**目标一：分析影响因素**")
        st.write("- 识别关键学习指标\n- 探索成绩相关性\n- 提供数据决策支持")
    with col2:
        st.write("**目标二：可视化展示**")
        st.write("- 专业对比分析\n- 性别差异分析\n- 学习模式识别")
    with col3:
        st.write("**目标三：成绩预测**")
        st.write("- 机器学习模型\n- 个性化预测\n- 及时干预预警")
    
    st.subheader("技术架构")
    tech_cols = st.columns(4)
    with tech_cols[0]:
        st.write("**前端框架**")
        st.write("Streamlit")
    with tech_cols[1]:
        st.write("**数据处理**")
        st.write("Pandas\nNumPy")
    with tech_cols[2]:
        st.write("**可视化**")
        st.write("Altair\nMatplotlib")
    with tech_cols[3]:
        st.write("**机器学习**")
        st.write("Scikit-learn")
    
    # 核心修复：使用 'stretch' 参数替代 100%，实现图片占满列宽
    st.subheader("系统界面预览")
    try:
        intro_img = Image.open(PROJECT_INTRO_IMG_PATH)
        st.image(intro_img, caption="系统界面预览", width="stretch")  # 使用 stretch 实现占满列宽
    except Exception as e:
        st.info(f"加载图片失败：{str(e)}")

# ====================== 界面2：专业数据分析 ======================
elif page == "专业数据分析":
    if df is None:
        st.stop()
    st.title("专业数据分析")
    
    major_data = df.groupby("专业").agg({
        "每周学习时长（小时）": "mean",
        "期中考试分数": "mean",
        "期末考试分数": "mean",
        "上课出勤率": "mean",
        "性别": lambda x: x.value_counts().to_dict()
    }).reset_index()
    major_data["男生人数"] = major_data["性别"].apply(lambda x: x.get("男", 0))
    major_data["女生人数"] = major_data["性别"].apply(lambda x: x.get("女", 0))
    major_data = major_data.drop("性别", axis=1)
    
    st.subheader("1. 各专业核心指标统计")
    stats_table = major_data[["专业", "每周学习时长（小时）", "期中考试分数", "期末考试分数"]].round(2)
    st.dataframe(stats_table, use_container_width=True)
    
    st.subheader("2. 各专业男女性别比例")
    gender_data = major_data.melt(id_vars="专业", value_vars=["男生人数", "女生人数"], var_name="性别", value_name="人数")
    gender_chart = alt.Chart(gender_data).mark_bar().encode(
        x=alt.X("专业:N", title="专业", axis=alt.Axis(labelColor='#000000')),
        y=alt.Y("人数:Q", title="人数", axis=alt.Axis(labelColor='#000000')),
        color=alt.Color("性别:N", scale=alt.Scale(range=["#1f77b4", "#ff7f0e"])),
        xOffset="性别:N"
    ).properties(width=800, height=300).configure_view(strokeWidth=0)
    st.altair_chart(gender_chart, use_container_width=True)
    
    st.subheader("3. 各专业学习时长对比")
    study_chart = alt.Chart(major_data).mark_line(point=True).encode(
        x=alt.X("专业:N", axis=alt.Axis(labelColor='#000000')),
        y=alt.Y("每周学习时长（小时）:Q", axis=alt.Axis(labelColor='#000000')),
        color=alt.value("#2ca02c"),
        tooltip=["专业", "每周学习时长（小时）"]
    ).properties(width=800, height=300).configure_view(strokeWidth=0)
    st.altair_chart(study_chart, use_container_width=True)
    
    st.subheader("4. 各专业平均上课出勤率")
    attendance_chart = alt.Chart(major_data).mark_bar(color="#d62728").encode(
        x=alt.X("专业:N", axis=alt.Axis(labelColor='#000000')),
        y=alt.Y("上课出勤率:Q", axis=alt.Axis(labelColor='#000000')),
        tooltip=["专业", "上课出勤率"]
    ).properties(width=800, height=300).configure_view(strokeWidth=0)
    st.altair_chart(attendance_chart, use_container_width=True)
    
    st.subheader("5. 大数据管理专业详情")
    bigdata_data = major_data[major_data["专业"] == "大数据管理"]
    if not bigdata_data.empty:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("平均上课出勤率", f"{bigdata_data['上课出勤率'].values[0]:.2%}")
        with col2:
            st.metric("期末考试平均分", f"{bigdata_data['期末考试分数'].values[0]:.2f}")
        with col3:
            st.metric("平均学习时长", f"{bigdata_data['每周学习时长（小时）'].values[0]:.2f}小时")
        with col4:
            st.metric("期中考试平均分", f"{bigdata_data['期中考试分数'].values[0]:.2f}")
        detail_chart = alt.Chart(bigdata_data).mark_bar(color="#1abc9c").encode(
            x=alt.X("专业:N", axis=alt.Axis(labelColor='#000000')),
            y=alt.Y("期末考试分数:Q", axis=alt.Axis(labelColor='#000000'))
        ).properties(width=400, height=200).configure_view(strokeWidth=0)
        st.altair_chart(detail_chart)
    else:
        st.warning("未找到大数据管理专业数据")

# ====================== 界面3：成绩预测 ======================
elif page == "成绩预测":
    if df is None:
        st.stop()
    st.title("期末成绩预测")
    st.write("请输入学生的学习信息，系统将预测期末成绩并提供学习建议")
    
    major_list = df["专业"].unique().tolist()
    
    with st.form("prediction_form", clear_on_submit=True):
        st.subheader("学生信息输入")
        col1, col2 = st.columns(2)
        with col1:
            student_id = st.text_input("学号", placeholder="请输入学号")
            gender = st.selectbox("性别", ["男", "女"])
            major = st.selectbox("专业", major_list)
        with col2:
            study_hours = st.slider("每周学习时长（小时）", 5, 40, 20)
            attendance = st.slider("上课出勤率", 0.6, 1.0, 0.8, step=0.01)
            midterm_score = st.slider("期中考试分数", 0, 100, 75)
            homework_rate = st.slider("作业完成率", 0.7, 1.0, 0.85, step=0.01)
        
        submit_btn = st.form_submit_button("预测期末成绩", type="primary")
    
    if submit_btn:
        gender_enc = 1 if gender == "男" else 0
        major_enc = pd.factorize(major_list, sort=True)[0][major_list.index(major)]
        input_data = pd.DataFrame({
            "性别": [gender_enc], "专业": [major_enc], "每周学习时长（小时）": [study_hours],
            "上课出勤率": [attendance], "期中考试分数": [midterm_score], "作业完成率": [homework_rate]
        })
        pred_score = model.predict(input_data)[0]
        
        st.subheader(f"预测期末成绩：{pred_score:.2f}分")
        if pred_score >= 60:
            st.success("🎉 恭喜！预测成绩及格！")
            try:
                congrats_img = Image.open(CONGRATS_IMG_PATH)
                st.image(congrats_img, width=400)  # 固定像素值，合法参数
            except:
                st.info(f"可将恭喜图片命名为 {CONGRATS_IMG_PATH} 并放在当前目录")
        else:
            st.error("💪 需要努力！预测成绩不及格")
            try:
                encourage_img = Image.open(ENCOURAGE_IMG_PATH)
                st.image(encourage_img, width=400)  # 固定像素值，合法参数
            except:
                st.info(f"可将鼓励图片命名为 {ENCOURAGE_IMG_PATH} 并放在当前目录")
        
        st.subheader("📝 个性化学习建议")
        if study_hours < 15:
            st.warning("建议：增加每周学习时长至15小时以上，学习时长与成绩呈中等正相关")
        if attendance < 0.8:
            st.warning("建议：提高上课出勤率，按时上课有助于提升成绩")
        if homework_rate < 0.85:
            st.warning("建议：保证作业完成质量，按时完成作业能巩固知识点")
