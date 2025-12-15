import streamlit as st

# 页面基础配置
st.set_page_config(
    page_title="个人简历生成器",
    page_icon="✨",
    layout="wide"
)

# 页面标题
st.title("个人简历生成器")
st.caption("使用Streamlit创建你的个性化简历")

# 分栏布局：左侧表单栏 + 右侧预览栏
form_col, preview_col = st.columns((1, 2))

# ---------------------- 左侧表单区域（完全清空所有默认值） ----------------------
with form_col:
    st.subheader("📝 个人信息填写")
    
    # 基础信息（无默认值）
    user_name = st.text_input("姓名")
    user_position = st.text_input("应聘职位")
    user_phone = st.text_input("联系电话")
    user_email = st.text_input("电子邮箱")
    
    # 日期/时间类（完全清空默认值，必须手动选择）
    user_birth = st.date_input("出生日期", value=None)  # 清空默认日期
    user_time = st.time_input("最佳联系时间", value=None)  # 清空默认时间
    
    # 单选类（默认无选中状态）
    user_gender = st.radio("性别", ["男", "女", "其他"], index=None)
    user_edu = st.selectbox("最高学历", ["本科", "专科", "硕士", "博士"], index=None)
    
    # 多选类（默认空列表）
    user_lang = st.multiselect("掌握语言", ["英语", "中文", "德语", "日语", "法语"])
    user_skill = st.multiselect("专业技能", ["Python", "项目管理", "数据分析", "SQL", "PPT"])
    
    # 数值类（默认0/空范围）
    user_exp = st.number_input("工作经验（年）", min_value=0, step=1)
    user_salary = st.slider(
        "期望薪资（元/月）", 
        min_value=30000, 
        max_value=50000, 
        value=None,  # 清空滑块默认值
        format="%d元"  # 显示格式优化
    )
    
    # 文本域（无默认值）
    user_intro = st.text_area("个人简介（可选）")

# ---------------------- 右侧预览区域（仅显示已填写的内容） ----------------------
with preview_col:
    st.subheader("🖥️ 简历实时预览")
    
    # 只有填写姓名后才显示预览内容
    if user_name:
        with st.container(border=True):  # 带边框的预览卡片
            # 姓名+头像区域
            st.markdown(f"### {user_name}")
            avatar_col, info_col = st.columns((1, 2))
            
            with avatar_col:
                # 基于姓名生成专属头像（刷新不改变）
                avatar_url = f"https://api.dicebear.com/7.x/bottts-neutral/svg?seed={user_name}"
                st.image(avatar_url, width=150)
            
            with info_col:
                # 仅显示已填写的信息，未填写则不展示
                if user_gender: st.write(f"性别: {user_gender}")
                if user_edu: st.write(f"学历: {user_edu}")
                if user_exp > 0: st.write(f"工作经验: {user_exp}年")
                if user_salary: st.write(f"期望薪资: {user_salary}元/月")  # 仅选中后显示
                if user_time: st.write(f"最佳联系时间: {user_time}")  # 仅选择后显示
                if user_lang: st.write(f"语言能力: {', '.join(user_lang)}")
        
        # 详细信息区域
        st.divider()  # 分隔线
        if user_position: st.write(f"**应聘职位**: {user_position}")
        if user_phone: st.write(f"**联系电话**: {user_phone}")
        if user_email: st.write(f"**电子邮箱**: {user_email}")
        if user_birth: st.write(f"**出生日期**: {user_birth.strftime('%Y年%m月%d日')}")  # 仅选择后显示
        
        # 技能与简介区域
        if user_skill:
            st.subheader("📌 专业技能")
            st.write(", ".join(user_skill))
        if user_intro:
            st.subheader("✍️ 个人简介")
            st.write(user_intro)
    else:
        # 未填写姓名时的提示
        st.info("请先在左侧填写姓名，预览内容会实时更新～", icon="ℹ️")
