# -*- coding: utf-8 -*-
"""
企鹅分类器 - 相对路径版
特点：所有路径改为相对路径，无需依赖绝对路径D:/streamlit_env
"""

import streamlit as st
import pickle
import pandas as pd
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# ============================ 全局配置（全相对路径，无绝对路径依赖） ============================
st.set_page_config(page_title="企鹅分类器", page_icon="🐧", layout="wide")

# 核心修改：所有路径改为相对路径（代码文件与数据集/图片在同一目录）
# 数据集相对路径：直接写文件名（因数据集在D:/streamlit_env，代码也在该目录）
DATA_PATH = "(企鹅识别数据)penguins-chinese.csv"
# 模型文件相对路径
MODEL_PATH = "rfc_model.pkl"
SPECIES_MAP_PATH = "output_uniques.pkl"
# 物种图片相对路径（图片与代码在同一目录）
SPECIES_IMG_MAP = {
    "阿德利企鹅": "ADELIE.png",
    "帽带企鹅": "CHINSTRAP.png",
    "巴布亚企鹅": "GENTOO.png"
}
# Logo和合集图相对路径
LOGO_IMG = "right_logo.png"
PENGUINS_ALL_IMG = "penguins_all.png"

# 数据中实际岛屿
ACTUAL_ISLANDS = ["比斯科群岛", "德里姆岛", "托尔森岛"]
predict_result_species = None
predict_result_img = None

# ============================ 工具函数（适配相对路径） ============================
def check_file_exists(file_path, file_type="文件"):
    """检查文件是否存在（相对路径）"""
    if not os.path.exists(file_path):
        st.error(f"❌ 未找到{file_type}：{file_path}")
        st.info(f"💡 请确保{file_type}与代码文件（qwq.py）在同一目录！")
        return False
    return True

def check_species_images():
    """检查物种图片是否存在（相对路径）"""
    missing = []
    for species, img_path in SPECIES_IMG_MAP.items():
        if not os.path.exists(img_path):
            missing.append(f"{species}的图片：{img_path}")
    if missing:
        st.warning("⚠️ 以下图片与代码不在同一目录（不影响预测，仅影响显示）：")
        for img in missing:
            st.write(f"- {img}")
    return missing

def get_correct_image(species_name):
    """获取物种图片（相对路径）"""
    if species_name not in SPECIES_IMG_MAP:
        default_img = f"https://picsum.photos/300/300?{species_name}"
        return default_img, f"未识别物种：{species_name}（用默认图替代）"
    
    img_path = SPECIES_IMG_MAP[species_name]
    if os.path.exists(img_path):
        return img_path, f"成功加载{species_name}图片（相对路径）"
    else:
        default_img = f"https://picsum.photos/300/300?{species_name}"
        return default_img, f"缺失{species_name}图片：{img_path}（用默认图替代）"

# ============================ 核心功能函数（适配相对路径） ============================
def load_and_preprocess_data():
    """加载数据集（相对路径）"""
    global ACTUAL_ISLANDS
    # 先检查数据集是否存在（相对路径）
    if not check_file_exists(DATA_PATH, "数据集"):
        return None, None, None
    
    # 读取数据集（gbk编码）
    try:
        df = pd.read_csv(DATA_PATH, encoding="gbk")
        st.success(f"✅ 成功读取数据集（相对路径：{DATA_PATH}）")
    except Exception as e:
        st.error(f"❌ 读取数据集失败：{str(e)}")
        return None, None, None
    
    # 数据清洗
    df = df.dropna(subset=["企鹅的种类", "企鹅栖息的岛屿", "喙的长度", "喙的深度", "翅膀的长度", "身体质量", "性别"])
    df = df.reset_index(drop=True)
    
    # 同步岛屿名称
    data_islands = df["企鹅栖息的岛屿"].unique()
    if not set(data_islands).issubset(set(ACTUAL_ISLANDS)):
        ACTUAL_ISLANDS = list(data_islands)
        st.info(f"ℹ️ 数据集包含岛屿：{ACTUAL_ISLANDS}")
    
    # 列名映射
    df.rename(columns={
        "企鹅的种类": "物种",
        "企鹅栖息的岛屿": "岛屿",
        "喙的长度": "喙长度(mm)",
        "喙的深度": "喙深度(mm)",
        "翅膀的长度": "鳍长(mm)",
        "身体质量": "体重(g)"
    }, inplace=True)
    
    # 特征编码
    X = pd.get_dummies(df[["喙长度(mm)", "喙深度(mm)", "鳍长(mm)", "体重(g)", "岛屿", "性别"]], 
                      columns=["岛屿", "性别"], drop_first=False)
    le = LabelEncoder()
    y = le.fit_transform(df["物种"])
    species_map = {idx: name for idx, name in enumerate(le.classes_)}
    
    return X, y, species_map

def train_or_load_model():
    """加载/训练模型（相对路径）"""
    # 先检查模型文件是否存在（相对路径）
    model_exists = os.path.exists(MODEL_PATH) and os.path.exists(SPECIES_MAP_PATH)
    if model_exists:
        try:
            with open(MODEL_PATH, "rb") as f:
                model = pickle.load(f)
            with open(SPECIES_MAP_PATH, "rb") as f:
                species_map = pickle.load(f)
            st.success(f"✅ 加载预训练模型（相对路径：{MODEL_PATH}）")
            return model, species_map
        except Exception as e:
            st.warning(f"⚠️ 加载模型失败：{str(e)}，将重新训练")
    
    # 重新训练模型
    X, y, species_map = load_and_preprocess_data()
    if X is None:
        return None, None
    model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    model.fit(X, y)
    
    # 保存模型（相对路径）
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)
    with open(SPECIES_MAP_PATH, "wb") as f:
        pickle.dump(species_map, f)
    st.success(f"✅ 模型训练完成并保存（相对路径：{MODEL_PATH}）")
    return model, species_map

# ============================ 页面逻辑（适配相对路径） ============================
def render_predict_page():
    global predict_result_species, predict_result_img
    st.header("企鹅物种预测 📊")
    
    # 检查图片是否存在（相对路径）
    check_species_images()
    
    # 布局
    col_logo, col_form = st.columns([1, 2.5])
    with col_form:
        # 输入表单
        with st.form("predict_form"):
            island = st.selectbox("栖息岛屿", ACTUAL_ISLANDS)
            sex = st.selectbox("性别", ["雌性", "雄性"])
            bill_length = st.number_input("喙长度（mm）", 32.0, 60.0, 45.0)
            bill_depth = st.number_input("喙深度（mm）", 13.0, 22.0, 17.0)
            flipper_length = st.number_input("翅膀长度（mm）", 170.0, 240.0, 200.0)
            body_mass = st.number_input("体重（g）", 2700.0, 6300.0, 4200.0)
            submit = st.form_submit_button("预测", type="primary")
        
        # 加载模型并预测
        model, species_map = train_or_load_model()
        if submit and model:
            # 构造输入特征
            input_data = {
                "喙长度(mm)": bill_length,
                "喙深度(mm)": bill_depth,
                "鳍长(mm)": flipper_length,
                "体重(g)": body_mass
            }
            # 补充分类特征one-hot编码
            for feat in model.feature_names_in_:
                if feat.startswith("岛屿_"):
                    input_data[feat] = 1 if feat == f"岛屿_{island}" else 0
                elif feat.startswith("性别_"):
                    input_data[feat] = 1 if feat == f"性别_{sex}" else 0
            
            # 执行预测
            input_df = pd.DataFrame([[input_data[f] for f in model.feature_names_in_]], 
                                   columns=model.feature_names_in_)
            predict_code = model.predict(input_df)[0]
            predict_result_species = species_map[predict_code]
            predict_result_img, img_msg = get_correct_image(predict_result_species)
            
            # 显示结果
            st.success(f"🎉 预测结果：{predict_result_species}")
            st.info(f"🖼️ {img_msg}")

    # 显示图片（相对路径）
    with col_logo:
        if not submit or not predict_result_img:
            # 未预测时显示Logo（相对路径）
            if os.path.exists(LOGO_IMG):
                st.image(LOGO_IMG, width=300, caption="企鹅分类器（相对路径图片）")
            else:
                st.image("https://picsum.photos/300/300?penguinlogo", width=300, caption="企鹅分类器（默认图）")
        else:
            # 预测后显示物种图片（相对路径）
            st.image(predict_result_img, width=300, caption=f"预测物种：{predict_result_species}")

def render_intro_page():
    st.header("企鹅分类器 🐧")
    st.subheader("数据集简介（相对路径版）")
    
    # 数据集基本信息（相对路径）
    st.write(f"- 数据集相对路径：{DATA_PATH}")
    st.write(f"- 代码与数据集位置要求：必须在同一目录（如D:/streamlit_env）")
    st.write(f"- 包含岛屿：{', '.join(ACTUAL_ISLANDS)}")
    st.write("- 预测物种：阿德利企鹅、帽带企鹅、巴布亚企鹅")
    
    # 显示数据集样本（相对路径）
    if check_file_exists(DATA_PATH, "数据集"):
        try:
            df_sample = pd.read_csv(DATA_PATH, encoding="gbk").head(5)
            st.dataframe(df_sample, use_container_width=True)
        except:
            st.warning("⚠️ 无法加载数据集样本")
    
    # 物种图鉴（相对路径）
    st.subheader("物种图鉴（相对路径图片）")
    col1, col2, col3 = st.columns(3)
    for (species, img_path), col in zip(SPECIES_IMG_MAP.items(), [col1, col2, col3]):
        with col:
            if os.path.exists(img_path):
                st.image(img_path, use_container_width=True)
                st.caption(f"{species}（相对路径）")
            else:
                st.image(f"https://picsum.photos/200/200?{species}", use_container_width=True)
                st.caption(f"{species}（默认图）")

# ============================ 主程序 ============================
if __name__ == "__main__":
    # 初始化检查：代码与数据集是否在同一目录
    st.markdown("### 📌 初始化检查（相对路径版）")
    if check_file_exists(DATA_PATH, "数据集"):
        st.success("✅ 数据集与代码在同一目录，可正常运行")
    else:
        st.error("❌ 数据集与代码不在同一目录，无法运行")
    
    # 渲染侧边栏
    st.sidebar.title("功能导航")
    page = st.sidebar.selectbox("选择页面", ["数据集简介", "物种预测"], label_visibility="collapsed")
    
    # 渲染对应页面
    if page == "数据集简介":
        render_intro_page()
    else:
        render_predict_page()
    
    st.markdown("---")
    st.caption("© 2025 企鹅分类器（全相对路径版）")
