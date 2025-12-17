import streamlit as st
import pandas as pd
import numpy as np

# ===================== 核心规则：set_page_config 必须放在所有Streamlit操作最前面（仅调用一次） =====================
st.set_page_config(
    page_title="学生小莫-数字档案",
    layout="wide",
    initial_sidebar_state="collapsed",
    page_icon="📜"
)

# ---------------------- 全局CSS样式（整合所有页面的样式，避免重复定义） ----------------------
st.markdown("""
<style>
/* 全局样式：暖橙色层次+轻微纹理背景+柔和文字 */
.stApp {
    background-color: #fdf2e9;
    background-image: url("https://www.transparenttextures.com/patterns/old-paper.png");
    background-blend-mode: overlay;
    color: #5c3b30;
    padding: 0 2rem;
}
/* 标题层级样式 */
h1 {
    background: linear-gradient(90deg, #e67e22, #d35400);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    font-size: 2.8rem;
    font-weight: 800;
    text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    margin-bottom: 1.5rem;
}
h2 {
    color: #e67e22;
    font-size: 1.8rem;
    font-weight: 700;
    border-left: 4px solid #d35400;
    padding-left: 0.8rem;
    margin-top: 2rem;
    margin-bottom: 1rem;
}
/* Metric卡片样式 */
.stMetric {
    background: linear-gradient(135deg, #f8e0c8 0%, #f5d0a8 100%);
    padding: 1.2rem;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    transition: transform 0.2s ease;
}
.stMetric:hover {
    transform: translateY(-3px);
    box-shadow: 0 6px 16px rgba(0,0,0,0.15);
}
.stMetric label {
    color: #d35400 !important;
    font-size: 1.1rem;
    font-weight: 600;
}
.stMetric value {
    font-size: 2rem !important;
    font-weight: 700;
}
/* 表格美化 */
.stTable {
    --st-table-row-hover-color: #f5d0a8;
    border-collapse: separate;
    border-spacing: 0;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}
.stTable th {
    background-color: #f5a65b !important;
    color: #fff !important;
    font-weight: 700;
    padding: 0.8rem !important;
    border: none !important;
}
.stTable td {
    background-color: #f8e8d8 !important;
    color: #5c3b30 !important;
    padding: 0.8rem !important;
    border: none !important;
    border-bottom: 1px solid #f5d0a8 !important;
}
/* 进度条样式 */
.stProgress > div > div {
    background: linear-gradient(90deg, #e67e22, #d35400) !important;
    border-radius: 8px;
}
/* 视频容器样式 */
div[data-testid="stVideo"] {
    width: 100% !important;
    max-width: 1200px !important;
    max-height: 450px !important;
    margin: 0 auto !important;
    aspect-ratio: 16/9 !important;
}
div[data-testid="stVideo"] video {
    width: 100% !important;
    height: 100% !important;
    object-fit: contain !important;
}
/* 演职人员卡片样式 */
.actor-card {
    border-radius: 10px;
    padding: 15px;
    background-color: #f8f9fa;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
.main-title {
    font-size: 2.5rem;
    color: #d4a017;
    text-align: center;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# ===================== 顶部标题和选项卡 =====================
st.title("顶部栏")
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["选项卡1", "选项卡2", "选项卡3", "选项卡4", "选项卡5", "选项卡6"])

# ===================== 选项卡1：学生数字档案 =====================
with tab1:
    st.header("这是第一个选项卡")
    st.markdown("#### 第一个选项卡的内容")
    
    # 主容器：包裹所有内容
    with st.container():
        st.title("📜 学生 小莫 - 数字档案")
        st.divider()
        
        # 基础信息模块
        with st.container(border=True):
            st.header("👤 基础信息")
            info_col1, info_col2 = st.columns(2)
            with info_col1:
                st.markdown("**学生ID:** NEO-2023-001")
                st.markdown("**注册时间:** 2023-10-01 08:30:17")
            with info_col2:
                st.markdown("**当前教室:** 实训楼301")
                st.markdown("**安全等级:** 🛡️ 绝密")
            st.markdown("**精神状态:** ✅ 正常 | **学习模式:** 🚀 高效")
        
        # 技能矩阵模块
        with st.container(border=True):
            st.header("🎯 技能矩阵")
            skill_col1, skill_col2, skill_col3 = st.columns([1,1,1], gap="medium")
            with skill_col1:
                st.metric(label="C语言", value="95%", delta="+2%")
            with skill_col2:
                st.metric(label="Python", value="87%", delta="-1%")
            with skill_col3:
                st.metric(label="Java", value="68%", delta="-10%")
        
        # 课程进度模块
        with st.container(border=True):
            st.header("📚 Streamlit课程进度")
            st.markdown("**当前完成度:** 65%（目标：100% | 剩余课时：12节）")
            st.progress(65)
        
        # 任务日志模块
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
        
        # 最新代码成果模块
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
        
        # 系统消息模块
        st.divider()
        st.header("📢 系统通知")
        st.markdown("> **SYSTEM MESSAGE:** 下一个任务目标已解锁...")
        st.markdown("> **TARGET:** 课程管理系统（暖色系界面适配版）")
        st.markdown("> **COUNTDOWN:** 2025-06-03 15:24:58 | **优先级:** 🔴 高")
        st.markdown("**系统状态:** 🟢 在线 | **数据加密:** 🔒 AES-256")

# ===================== 选项卡2：餐厅数据分析 =====================
with tab2:
    st.header("这是第二个选项卡")
    st.markdown("#### 第二个选项卡的内容")
    
    # 1. 定义基础餐厅数据
    restaurants_data = {
        "餐厅": ["星艺会尝不忘", "高峰柠檬鸭", "复记老友粉", "好友缘", "西冷牛排店"],
        "类型": ["中餐", "中餐", "快餐", "自助餐", "西餐"],
        "评分": [4.2, 4.5, 4.0, 4.7, 4.3],
        "人均消费(元)": [15, 20, 25, 35, 50],
        "latitude": [22.853838, 22.965046, 22.812200, 22.809105, 22.839699],
        "longitude": [108.222177, 108.353921, 108.266629, 108.378664, 108.245804]
    }
    
    # 2. 转换为DataFrame（调整索引为“餐厅”）
    df = pd.DataFrame(restaurants_data).set_index("餐厅")
    
    # 3. 提取需要可视化的数值列（评分、人均消费）
    visual_df = df[["评分", "人均消费(元)"]]
    map_df = df[["latitude", "longitude"]]
    
    # 4. 生成12个月价格走势数据
    np.random.seed(42)
    months = ["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月"]
    price_trend_data = {}
    base_prices = df["人均消费(元)"].values
    
    for i, restaurant in enumerate(df.index):
        monthly_prices = base_prices[i] + np.random.randint(-1, 4, size=12)
        monthly_prices = np.maximum(monthly_prices, 8)
        price_trend_data[restaurant] = monthly_prices
    
    price_trend_df = pd.DataFrame(price_trend_data, index=months)
    
    # 5. Streamlit展示布局
    st.title("餐厅数据分析")
    
    # 基础信息表格
    st.subheader("餐厅基础信息")
    st.dataframe(visual_df)
    
    # 评分&人均消费可视化
    st.subheader("评分 vs 人均消费")
    st.line_chart(visual_df)
    st.bar_chart(visual_df)
    
    # 12个月价格走势折线图
    st.subheader("各餐厅12个月人均消费价格走势")
    st.line_chart(
        price_trend_df,
        x_label="月份",
        y_label="人均消费(元)",
        height=400
    )
    
    # 餐厅位置地图
    st.subheader("餐厅地理位置分布")
    st.map(map_df)
    
    # 价格走势数据详情
    with st.expander("查看价格走势详细数据"):
        st.dataframe(price_trend_df)

# ===================== 选项卡3：相册 =====================
with tab3:
    st.header("这是第三个选项卡")
    st.markdown("#### 第三个选项卡的内容")
    
    st.title("我的相册")
    
    # 初始化图片索引
    if 'img_ind' not in st.session_state:
        st.session_state['img_ind'] = 0
    
    # 图片列表
    images = [
        {
            'url': "https://www.baltana.com/files/wallpapers-2/Cute-Cat-Images-07756.jpg",
            'text': '猫'
        },
        {
            'url': "https://cdn.britannica.com/82/232782-050-8062ACFA/Black-labrador-retriever-dog.jpg",
            'text': 'dog'
        },
        {
            'url': "https://live.staticflickr.com/2686/4497672316_d283310530_3k.jpg",
            'text': 'lion'
        }
    ]
    
    # 显示当前图片
    st.image(images[st.session_state['img_ind']]['url'], caption=images[st.session_state['img_ind']]['text'])
    
    # 切换图片函数
    def nextImg():
        st.session_state['img_ind'] = (st.session_state['img_ind'] + 1) % len(images)
    
    def prevImg():
        st.session_state['img_ind'] = (st.session_state['img_ind'] - 1) % len(images)
    
    # 切换按钮
    col1, col2 = st.columns(2)
    with col1:
        st.button("上一张", on_click=prevImg)
    with col2:
        st.button("下一张", on_click=nextImg)

# ===================== 选项卡4：简易音乐播放器 =====================
with tab4:
    st.header("这是第四个选项卡")
    st.markdown("#### 第四个选项卡的内容")
    
    st.title("简易音乐播放器")
    
    # 初始化歌曲索引
    if 'current_song_idx' not in st.session_state:
        st.session_state.current_song_idx = 0
    
    # 切换歌曲函数
    def prev_song():
        st.session_state.current_song_idx = (st.session_state.current_song_idx - 1) % len(music_list)
    
    def next_song():
        st.session_state.current_song_idx = (st.session_state.current_song_idx + 1) % len(music_list)
    
    # 音乐列表
    music_list = [
        {
            "album_img": "http://p2.music.126.net/QsebYbDgQtKelH6r1iE2Fg==/109951167129280730.jpg?param=130y130",
            "singer": "郑润泽",
            "song_name": "小胡同",
            "audio_url": "https://music.163.com/song/media/outer/url?id=1926623288.mp3"
        },
        {
            "album_img": "http://p2.music.126.net/-xMsNLpquZTmMZlIztTgHg==/109951165953469081.jpg?param=130y130",
            "singer": "郑润泽",
            "song_name": "如果呢",
            "audio_url": "https://music.163.com/song/media/outer/url?id=1842728629.mp3"
        },
        {
            "album_img": "http://p2.music.126.net/Oz62EqsdMUQhQnGz5sLfdA==/109951165835998589.jpg?param=130y130",
            "singer": "夏日入侵企划",
            "song_name": "回不去的夏天",
            "audio_url": "https://music.163.com/song/media/outer/url?id=1832684671.mp3"
        }
    ]
    
    # 当前歌曲
    current_song = music_list[st.session_state.current_song_idx]
    
    # 布局：专辑图 + 歌曲信息
    col_img, col_info = st.columns([1, 3], gap="small")
    with col_img:
        st.image(current_song["album_img"], width=130)
    with col_info:
        st.markdown(f"### {current_song['song_name']}")
        st.write(f"**歌手**：{current_song['singer']}")
    
    # 音频播放
    st.audio(current_song["audio_url"], format="audio/mp3")
    
    # 切换按钮
    col_prev, col_next = st.columns(2, gap="small")
    with col_prev:
        st.button("上一首", on_click=prev_song, use_container_width=True)
    with col_next:
        st.button("下一首", on_click=next_song, use_container_width=True)

# ===================== 选项卡5：还珠格格播放页 =====================
with tab5:
    st.header("这是第五个选项卡")
    st.markdown("#### 第五个选项卡的内容")
    
    # 视频列表
    video_arr = [
        {
            'url': 'https://upos-sz-mirrorcosov.bilivideo.com/upgcxcode/55/22/34578302255/34578302255-1-192.mp4?e=ig8euxZM2rNcNbRBnwdVhwdlhWU3hwdVhoNvNC8BqJIzNbfq9rVEuxTEnE8L5F6VnEsSTx0vkX8fqJeYTj_lta53NCM=&mid=3546763107502921&nbs=1&os=cosovbv&og=hw&platform=html5&oi=1804878521&deadline=1765768710&uipk=5&trid=f6c6c76fe5cc432daec777568fe1174T&gen=playurlv3&upsig=f92713098c187bfeb596053f86d1ffd3&uparams=e,mid,nbs,os,og,platform,oi,deadline,uipk,trid,gen&bvc=vod&nettype=0&bw=1269037&agrr=1&buvid=&build=0&dl=0&f=T_0_0&mobi_app=&orderid=0,1',
            'title': '还珠格格第一部',
            'episode_name': '第1集：阴差阳错入皇宫',
            'episode': 1
        },
        {
            'url': 'https://upos-sz-mirrorcosov.bilivideo.com/upgcxcode/17/33/34578303317/34578303317-1-192.mp4?e=ig8euxZM2rNcNbRz7zdVhwdlhWhahwdVhoNvNC8BqJIzNbfq9rVEuxTEnE8L5F6VnEsSTx0vkX8fqJeYTj_lta53NCM=&og=cos&deadline=1765768923&uipk=5&gen=playurlv3&platform=html5&mid=3546763107502921&oi=1804878521&nbs=1&trid=1a26a4d19f464299b65bdd1ebc1070dT&os=cosovbv&upsig=474bc515fbe7d752d6443a177700af87&uparams=e,og,deadline,uipk,gen,platform,mid,oi,nbs,trid,os&bvc=vod&nettype=0&bw=1100998&mobi_app=&agrr=1&buvid=&build=0&dl=0&f=T_0_0&orderid=0,1',
            'title': '还珠格格第一部',
            'episode_name': '第2集：紫薇初遇福尔康',
            'episode': 2
        },
        {
            'url': 'https://upos-sz-mirrorcosov.bilivideo.com/upgcxcode/93/43/34578304393/34578304393-1-192.mp4?e=ig8euxZM2rNcNbRVnwdVhwdlhWd3hwdVhoNvNC8BqJIzNbfq9rVEuxTEnE8L5F6VnEsSTx0vkX8fqJeYTj_lta53NCM=&trid=3748a5d634f8497c908cfcd07dfdd56T&mid=3546763107502921&uipk=5&gen=playurlv3&os=cosovbv&platform=html5&deadline=1765768981&nbs=1&oi=1804878521&og=cos&upsig=e95d93af01c29bd4b4b5c0d904e8b7be&uparams=e,trid,mid,uipk,gen,os,platform,deadline,nbs,oi,og&bvc=vod&nettype=0&bw=866304&mobi_app=&agrr=1&buvid=&build=0&dl=0&f=T_0_0&orderid=0,1',
            'title': '还珠格格第一部',
            'episode_name': '第3集：乾隆认女起风波',
            'episode': 3
        }
    ]
    
    # 演职人员数据
    actors = [
        {
            "avatar": "https://ts1.tc.mm.bing.net/th/id/OIP-C.Jo-g8zQohrzztjZmPKiErAAAAA?w=229&h=211&c=8&rs=1&qlt=90&o=6&cb=ucfimg1&pid=3.1&rm=2&ucfimg=1",
            "role": "小燕子",
            "actor": "赵薇",
            "intro": "性格活泼开朗、古灵精怪，本是民间卖艺的孤女，误打误撞进入皇宫成为格格，是全剧的喜剧担当。"
        },
        {
            "avatar": "https://ts1.tc.mm.bing.net/th/id/OIP-C.P7KtVHOrggHw6DSmrypqMQHaNK?w=149&h=211&c=8&rs=1&qlt=90&o=6&cb=ucfimg1&pid=3.1&rm=2&ucfimg=1",
            "role": "夏紫薇",
            "actor": "林心如",
            "intro": "乾隆与夏雨荷的私生女，温柔善良、知书达理，千里迢迢到京城寻父，与小燕子结下生死与共的情谊。"
        },
        {
            "avatar": "https://ts1.tc.mm.bing.net/th/id/OIP-C.fJMGGlo8Zyx2STV-2yi94wAAAA?w=160&h=211&c=8&rs=1&qlt=90&o=6&cb=ucfimg1&pid=3.1&rm=2&ucfimg=1",
            "role": "五阿哥永琪",
            "actor": "苏有朋",
            "intro": "乾隆的第五子，才华横溢、重情重义，对小燕子一往情深，为了爱情甘愿放弃皇子身份。"
        },
        {
            "avatar": "https://tse3-mm.cn.bing.net/th/id/OIP-C.9PNvx2FgizXHgT9-lze7PgHaFR?w=245&h=180&c=7&r=0&o=7&cb=ucfimg2&pid=1.7&rm=3&ucfimg=1",
            "role": "福尔康",
            "actor": "周杰",
            "intro": "大学士傅恒之子，御前侍卫，文武双全、沉稳可靠，与紫薇相知相爱，是紫薇最坚实的依靠。"
        }
    ]
    
    # 剧集介绍
    drama_intro = {
        "title": "还珠格格第一部",
        "year": "1998年",
        "type": "古装 / 喜剧 / 爱情",
        "director": "孙树培",
        "writer": "琼瑶",
        "content": """
        《还珠格格》第一部改编自琼瑶同名小说，1998年播出后风靡两岸三地。
        该剧以清朝乾隆年间为背景，讲述了小燕子阴差阳错成格格，紫薇历经波折认父，
        两个女孩在皇宫中携手面对考验，与永琪、尔康谱写爱情与友情的故事。
        """
    }
    
    # 初始化视频索引
    if 'video_ind' not in st.session_state:
        st.session_state['video_ind'] = 0
    
    # 切换集数函数
    def switch_episode(index):
        st.session_state['video_ind'] = index
    
    # 主标题
    st.markdown(f'<h1 class="main-title">{drama_intro["title"]}</h1>', unsafe_allow_html=True)
    
    # 剧集简介
    with st.container(border=True):
        st.subheader("📖 剧集档案", divider="yellow")
        col_intro_1, col_intro_2 = st.columns([2, 1])
        with col_intro_1:
            st.write(f"**播出年份**：{drama_intro['year']}")
            st.write(f"**剧集类型**：{drama_intro['type']}")
            st.write(f"**导演**：{drama_intro['director']}")
            st.write(f"**编剧**：{drama_intro['writer']}")
            st.subheader("剧情简介")
            st.write(drama_intro['content'])
        with col_intro_2:
            st.image(
                "https://ts1.tc.mm.bing.net/th/id/OIP-C.Vl1xkEUOGJJoBZUZUR-_-gHaEC?w=240&h=211&c=8&rs=1&qlt=90&o=6&cb=ucfimg1&pid=3.1&rm=2&ucfimg=1",
                caption=f"{drama_intro['title']} 官方海报",
                use_container_width=True
            )
    
    # 视频播放区
    st.subheader("🎥 正片播放", divider="red")
    col_video_1, col_video_2, col_video_3 = st.columns([0.1, 0.8, 0.1])
    with col_video_2:
        current_video = video_arr[st.session_state['video_ind']]
        st.markdown(f"<h4>当前播放：{current_video['episode_name']}</h4>", unsafe_allow_html=True)
        st.video(current_video['url'], width=1200)
    
    # 集数选择区
    st.subheader("📽️ 选择集数", divider="gray")
    col_ep_1, col_ep_2, col_ep_3 = st.columns([0.1, 0.8, 0.1])
    with col_ep_2:
        episode_cols = st.columns(len(video_arr))
        for idx, video in enumerate(video_arr):
            with episode_cols[idx]:
                is_selected = idx == st.session_state['video_ind']
                st.button(
                    label=f"第{video['episode']}集\n{video['episode_name'].split('：')[1]}",
                    use_container_width=True,
                    on_click=switch_episode,
                    args=(idx,),
                    type="primary" if is_selected else "secondary"
                )
    
    # 演职人员区
    st.subheader("🎭 主要演职人员", divider="violet")
    actor_cols = st.columns(len(actors))
    for idx, actor in enumerate(actors):
        with actor_cols[idx]:
            st.markdown('<div class="actor-card">', unsafe_allow_html=True)
            st.image(
                actor["avatar"],
                caption=f"{actor['role']} - {actor['actor']}",
                use_container_width=True,
                clamp=True,
                output_format="JPEG"
            )
            st.markdown(f"**角色**：{actor['role']}")
            st.markdown(f"**演员**：{actor['actor']}")
            st.markdown(f"**角色简介**：{actor['intro']}")
            st.markdown('</div>', unsafe_allow_html=True)
    
    # 页脚
    st.markdown("---")
    st.markdown("<center>© 1998 琼瑶工作室 版权所有</center>", unsafe_allow_html=True)

# ===================== 选项卡6：个人简历生成器 =====================
with tab6:
    st.header("这是第六个选项卡")
    st.markdown("#### 第六个选项卡的内容")
    
    st.title("个人简历生成器")
    st.caption("使用Streamlit创建你的个性化简历")
    
    # 分栏布局
    form_col, preview_col = st.columns((1, 2))
    
    # 左侧表单
    with form_col:
        st.subheader("📝 个人信息填写")
        
        # 基础信息
        user_name = st.text_input("姓名")
        user_position = st.text_input("应聘职位")
        user_phone = st.text_input("联系电话")
        user_email = st.text_input("电子邮箱")
        
        # 日期/时间
        user_birth = st.date_input("出生日期", value=None)
        user_time = st.time_input("最佳联系时间", value=None)
        
        # 单选
        user_gender = st.radio("性别", ["男", "女", "其他"], index=None)
        user_edu = st.selectbox("最高学历", ["本科", "专科", "硕士", "博士"], index=None)
        
        # 多选
        user_lang = st.multiselect("掌握语言", ["英语", "中文", "德语", "日语", "法语"])
        user_skill = st.multiselect("专业技能", ["Python", "项目管理", "数据分析", "SQL", "PPT"])
        
        # 数值
        user_exp = st.number_input("工作经验（年）", min_value=0, step=1)
        user_salary = st.slider(
            "期望薪资（元/月）",
            min_value=30000,
            max_value=50000,
            value=None,
            format="%d元"
        )
        
        # 文本域
        user_intro = st.text_area("个人简介（可选）")
    
    # 右侧预览
    with preview_col:
        st.subheader("🖥️ 简历实时预览")
        
        if user_name:
            with st.container(border=True):
                st.markdown(f"### {user_name}")
                avatar_col, info_col = st.columns((1, 2))
                
                with avatar_col:
                    avatar_url = f"https://api.dicebear.com/7.x/bottts-neutral/svg?seed={user_name}"
                    st.image(avatar_url, width=150)
                
                with info_col:
                    if user_gender: st.write(f"性别: {user_gender}")
                    if user_edu: st.write(f"学历: {user_edu}")
                    if user_exp > 0: st.write(f"工作经验: {user_exp}年")
                    if user_salary: st.write(f"期望薪资: {user_salary}元/月")
                    if user_time: st.write(f"最佳联系时间: {user_time}")
                    if user_lang: st.write(f"语言能力: {', '.join(user_lang)}")
            
            # 详细信息
            st.divider()
            if user_position: st.write(f"**应聘职位**: {user_position}")
            if user_phone: st.write(f"**联系电话**: {user_phone}")
            if user_email: st.write(f"**电子邮箱**: {user_email}")
            if user_birth: st.write(f"**出生日期**: {user_birth.strftime('%Y年%m月%d日')}")
            
            # 技能与简介
            if user_skill:
                st.subheader("📌 专业技能")
                st.write(", ".join(user_skill))
            if user_intro:
                st.subheader("✍️ 个人简介")
                st.write(user_intro)
        else:
            st.info("请先在左侧填写姓名，预览内容会实时更新～", icon="ℹ️")
