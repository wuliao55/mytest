# 导入核心库
import streamlit as st
import pandas as pd

# ---------------------- 1. 页面基础配置（优化：增加页面图标） ----------------------
st.set_page_config(
    page_title="学生小莫-数字档案",
    layout="wide",
    initial_sidebar_state="collapsed",
    page_icon="📜"  # 增加档案类图标，强化主题
)

# ---------------------- 2. 精细化暖橙色系CSS（核心美观优化） ----------------------
st.markdown("""
<style>
/* 全局样式：暖橙色层次+轻微纹理背景+柔和文字 */
.stApp {
    background-color: #fdf2e9;  /* 主背景：暖橙米色（温馨柔和） */
    background-image: url("https://www.transparenttextures.com/patterns/old-paper.png");  /* 旧纸张纹理，增加暖感质感 */
    background-blend-mode: overlay;  /* 纹理与背景融合，不突兀 */
    color: #5c3b30;  /* 文字：暖深棕（高对比度，易阅读） */
    padding: 0 2rem;  /* 全局左右边距，避免内容贴边 */
}

/* 标题层级：暖橙渐变+加粗+阴影，区分层级 */
h1 {
    background: linear-gradient(90deg, #e67e22, #d35400);  /* 暖橙→深橙渐变 */
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;  /* 文字渐变效果 */
    font-size: 2.8rem;
    font-weight: 800;
    text-shadow: 0 2px 4px rgba(0,0,0,0.1);  /* 轻微文字阴影，增加立体感 */
    margin-bottom: 1.5rem;
}
h2 {
    color: #e67e22;  /* 暖橙色标题，与h1区分 */
    font-size: 1.8rem;
    font-weight: 700;
    border-left: 4px solid #d35400;  /* 左侧深橙竖线，强化视觉焦点 */
    padding-left: 0.8rem;
    margin-top: 2rem;
    margin-bottom: 1rem;
}

/* Metric卡片：暖橙渐变背景+圆角+阴影+hover效果 */
.stMetric {
    background: linear-gradient(135deg, #f8e0c8 0%, #f5d0a8 100%);  /* 暖橙渐变卡片 */
    padding: 1.2rem;
    border-radius: 12px;  /* 更大圆角，更柔和 */
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);  /* 轻微阴影，增加层次感 */
    transition: transform 0.2s ease;  /* hover过渡动画 */
}
.stMetric:hover {
    transform: translateY(-3px);  /* hover轻微上移，增加交互感 */
    box-shadow: 0 6px 16px rgba(0,0,0,0.15);
}
.stMetric label {
    color: #d35400 !important;  /* Metric标签深橙色 */
    font-size: 1.1rem;
    font-weight: 600;
}
.stMetric value {
    font-size: 2rem !important;
    font-weight: 700;
}
.stMetric delta {
    font-size: 1rem !important;
}

/* 表格美化：边框+圆角+hover行变色 */
.stTable {
    --st-table-row-hover-color: #f5d0a8;  /* 行hover暖橙背景 */
    border-collapse: separate;
    border-spacing: 0;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}
.stTable th {
    background-color: #f5a65b !important;  /* 表头暖橙背景 */
    color: #fff !important;  /* 表头文字白色 */
    font-weight: 700;
    padding: 0.8rem !important;
    border: none !important;
}
.stTable td {
    background-color: #f8e8d8 !important;  /* 单元格浅暖橙 */
    color: #5c3b30 !important;
    padding: 0.8rem !important;
    border: none !important;
    border-bottom: 1px solid #f5d0a8 !important;
}

/* 进度条美化：暖橙色渐变 */
.stProgress > div > div {
    background: linear-gradient(90deg, #e67e22, #d35400) !important;
    border-radius: 8px;
}

/* 代码块美化：暖色系适配 */
.stCodeBlock {
    background-color: #f8e8d8 !important;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    padding: 1rem !important;
}

/* 系统消息：引用框美化 */
blockquote {
    background-color: #f8e8d8;
    border-left: 4px solid #e67e22;
    padding: 1rem;
    border-radius: 0 8px 8px 0;
    box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    margin: 1rem 0;
}

/* 模块分隔：增加间距，避免拥挤 */
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* 带边框容器的样式适配 */
[data-testid="stVerticalBlock"] > [data-testid="stVerticalBlockBorderWrapper"] {
    border: 1px solid #f5d0a8 !important;
    border-radius: 12px;
    padding: 1.5rem;
    background-color: #fff8f0 !important;
}
</style>
""", unsafe_allow_html=True)

# ---------------------- 3. 布局优化：模块封装+呼吸感 ----------------------
# 主容器：包裹所有内容，增加内边距
with st.container():
    # 标题（增加emoji装饰，强化科幻+暖感）
    st.title("📜 学生 小莫 - 数字档案")
    
    # 分割线：视觉分隔，增加层次
    st.divider()

    # 基础信息模块（卡片化+图标）
    with st.container(border=True):  # 带边框的容器，包裹模块
        st.header("👤 基础信息")
        # 两列布局，避免文字过长拥挤
        info_col1, info_col2 = st.columns(2)
        with info_col1:
            st.markdown("**学生ID:** NEO-2023-001")
            st.markdown("**注册时间:** 2023-10-01 08:30:17")
        with info_col2:
            st.markdown("**当前教室:** 实训楼301")
            st.markdown("**安全等级:** 🛡️ 绝密")
        st.markdown("**精神状态:** ✅ 正常 | **学习模式:** 🚀 高效")

    # 技能矩阵模块（优化列间距+图标）
    with st.container(border=True):
        st.header("🎯 技能矩阵")
        # 列之间增加间距（gap参数）
        skill_col1, skill_col2, skill_col3 = st.columns([1,1,1], gap="medium")
        with skill_col1:
            st.metric(label="C语言", value="95%", delta="+2%")
        with skill_col2:
            st.metric(label="Python", value="87%", delta="-1%")
        with skill_col3:
            st.metric(label="Java", value="68%", delta="-10%")

    # 课程进度模块（增加说明文字，更清晰）
    with st.container(border=True):
        st.header("📚 Streamlit课程进度")
        st.markdown("**当前完成度:** 65%（目标：100% | 剩余课时：12节）")
        st.progress(65)

    # 任务日志模块（表格优化+说明）
    with st.container(border=True):
        st.header("📋 任务日志")
        task_data = {
            "日期": ["2023-10-01", "2023-10-05", "2023-10-12"],
            "任务名称": ["学生数字档案开发", "课程管理系统搭建", "数据图表可视化"],
            "完成状态": ["✅ 已完成", "🔴 进行中", "❌ 未开始"],
            "难度评级": ["⭐⭐⭐⭐⭐", "⭐⭐⭐⭐☆", "⭐⭐⭐☆☆"],
            "耗时(h)": ["8.5", "12.2", "预估6.0"]
        }
        task_df = pd.DataFrame(task_data)
        st.table(task_df)
        st.markdown("*注：难度评级5星为最高，耗时统计含调试时间*")

    # 最新代码成果模块（代码注释更清晰）
    with st.container(border=True):
        st.header("💻 最新代码成果")
        code_content = '''def student_archive_analysis():  # 学生档案数据分析函数
    # 初始化技能评分字典
    skill_scores = {"C语言": 95, "Python": 87, "Java": 68}
    # 遍历技能，计算提升建议
    for skill, score in skill_scores.items():
        if score < 70:  # 低于70分的技能标记为重点提升
            print(f"⚠️ 重点提升：{skill}（当前{score}分）")
        else:
            print(f"✅ {skill}：熟练度良好（{score}分）")
    return "分析完成 - 生成学习报告"'''
        st.code(code_content, language="python")

    # 系统消息模块（视觉强化）
    st.divider()  # 分割线
    st.header("📢 系统通知")
    st.markdown("> **SYSTEM MESSAGE:** 下一个任务目标已解锁...")
    st.markdown("> **TARGET:** 课程管理系统（暖色系界面适配版）")
    st.markdown("> **COUNTDOWN:** 2025-06-03 15:24:58 | **优先级:** 🔴 高")
    st.markdown("**系统状态:** 🟢 在线 | **数据加密:** 🔒 AES-256")
