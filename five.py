import streamlit as st

# ---------------------- 页面基础配置 ----------------------
st.set_page_config(
    page_title="还珠格格第一部 - 经典播放页",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"  # 隐藏侧边栏，聚焦主内容
)

# ---------------------- 全局数据定义 ----------------------
# 视频列表（含标题、集数、播放地址）
video_arr = [
    {
        'url': 'https://upos-sz-mirrorcosov.bilivideo.com/upgcxcode/55/22/34578302255/34578302255-1-192.mp4?e=ig8euxZM2rNcNbRBnwdVhwdlhWU3hwdVhoNvNC8BqJIzNbfq9rVEuxTEnE8L5F6VnEsSTx0vkX8fqJeYTj_lta53NCM=&mid=3546763107502921&nbs=1&os=cosovbv&og=hw&platform=html5&oi=1804878521&deadline=1765768710&uipk=5&trid=f6c6c76fe5cc432daec777568fe1174T&gen=playurlv3&upsig=f92713098c187bfeb596053f86d1ffd3&uparams=e,mid,nbs,os,og,platform,oi,deadline,uipk,trid,gen&bvc=vod&nettype=0&bw=1269037&agrr=1&buvid=&build=0&dl=0&f=T_0_0&mobi_app=&orderid=0,1',
        'title': '还珠格格第一部',
        'episode_name': '第1集：阴差阳错入皇宫',
        'episode': 1
    },{
        'url': 'https://upos-sz-mirrorcosov.bilivideo.com/upgcxcode/17/33/34578303317/34578303317-1-192.mp4?e=ig8euxZM2rNcNbRz7zdVhwdlhWhahwdVhoNvNC8BqJIzNbfq9rVEuxTEnE8L5F6VnEsSTx0vkX8fqJeYTj_lta53NCM=&og=cos&deadline=1765768923&uipk=5&gen=playurlv3&platform=html5&mid=3546763107502921&oi=1804878521&nbs=1&trid=1a26a4d19f464299b65bdd1ebc1070dT&os=cosovbv&upsig=474bc515fbe7d752d6443a177700af87&uparams=e,og,deadline,uipk,gen,platform,mid,oi,nbs,trid,os&bvc=vod&nettype=0&bw=1100998&mobi_app=&agrr=1&buvid=&build=0&dl=0&f=T_0_0&orderid=0,1',
        'title': '还珠格格第一部',
        'episode_name': '第2集：紫薇初遇福尔康',
        'episode': 2
    },{
        'url': 'https://upos-sz-mirrorcosov.bilivideo.com/upgcxcode/93/43/34578304393/34578304393-1-192.mp4?e=ig8euxZM2rNcNbRVnwdVhwdlhWd3hwdVhoNvNC8BqJIzNbfq9rVEuxTEnE8L5F6VnEsSTx0vkX8fqJeYTj_lta53NCM=&trid=3748a5d634f8497c908cfcd07dfdd56T&mid=3546763107502921&uipk=5&gen=playurlv3&os=cosovbv&platform=html5&deadline=1765768981&nbs=1&oi=1804878521&og=cos&upsig=e95d93af01c29bd4b4b5c0d904e8b7be&uparams=e,trid,mid,uipk,gen,os,platform,deadline,nbs,oi,og&bvc=vod&nettype=0&bw=866304&mobi_app=&agrr=1&buvid=&build=0&dl=0&f=T_0_0&orderid=0,1',
        'title': '还珠格格第一部',
        'episode_name': '第3集：乾隆认女起风波',
        'episode': 3
    }
]

# 演职人员数据（图文结合：头像、角色、演员、简介）
actors = [
    {
        "avatar": "https://ts1.tc.mm.bing.net/th/id/OIP-C.Jo-g8zQohrzztjZmPKiErAAAAA?w=229&h=211&c=8&rs=1&qlt=90&o=6&cb=ucfimg1&pid=3.1&rm=2&ucfimg=1",  # 赵薇头像（示例链接）
        "role": "小燕子",
        "actor": "赵薇",
        "intro": "性格活泼开朗、古灵精怪，本是民间卖艺的孤女，误打误撞进入皇宫成为格格，是全剧的喜剧担当，敢爱敢恨的性格深受观众喜爱。"
    },
    {
        "avatar": "https://ts1.tc.mm.bing.net/th/id/OIP-C.P7KtVHOrggHw6DSmrypqMQHaNK?w=149&h=211&c=8&rs=1&qlt=90&o=6&cb=ucfimg1&pid=3.1&rm=2&ucfimg=1",  # 林心如头像（示例链接）
        "role": "夏紫薇",
        "actor": "林心如",
        "intro": "乾隆与夏雨荷的私生女，温柔善良、知书达理、琴棋书画样样精通，千里迢迢到京城寻父，与小燕子结下生死与共的深厚情谊。"
    },
    {
        "avatar": "https://ts1.tc.mm.bing.net/th/id/OIP-C.fJMGGlo8Zyx2STV-2yi94wAAAA?w=160&h=211&c=8&rs=1&qlt=90&o=6&cb=ucfimg1&pid=3.1&rm=2&ucfimg=1",  # 苏有朋头像（示例链接）
        "role": "五阿哥永琪",
        "actor": "苏有朋",
        "intro": "乾隆的第五子，才华横溢、重情重义，对小燕子一往情深，为了爱情甘愿放弃皇子身份，是全剧的核心男性角色之一。"
    },
    {
        "avatar": "https://tse3-mm.cn.bing.net/th/id/OIP-C.9PNvx2FgizXHgT9-lze7PgHaFR?w=245&h=180&c=7&r=0&o=7&cb=ucfimg2&pid=1.7&rm=3&ucfimg=1",  # 周杰头像（示例链接）
        "role": "福尔康",
        "actor": "周杰",
        "intro": "大学士傅恒之子，御前侍卫，文武双全、沉稳可靠，与紫薇相知相爱，是紫薇在皇宫中最坚实的依靠和保护者。"
    }
]

# 剧集详细介绍
drama_intro = {
    "title": "还珠格格第一部",
    "year": "1998年",
    "type": "古装 / 喜剧 / 爱情",
    "director": "孙树培",
    "writer": "琼瑶",
    "content": """
    《还珠格格》第一部改编自琼瑶同名小说，1998年播出后迅速风靡两岸三地，创下万人空巷的收视奇迹。
    该剧以清朝乾隆年间为背景，讲述了民间女子小燕子阴差阳错被封为“还珠格格”，而真正的格格紫薇则历经波折认父，
    两个性格迥异的女孩在皇宫中携手面对重重考验，与永琪、尔康等人谱写了一段段动人的爱情与友情故事。
    剧集凭借轻松诙谐的剧情、鲜明的人物形象和真挚的情感，成为一代观众的经典童年回忆。
    """
}

# ---------------------- 初始化会话状态 ----------------------
if 'ind' not in st.session_state:
    st.session_state['ind'] = 0  # 默认播放第1集

# ---------------------- 集数切换函数 ----------------------
def switch_episode(index):
    st.session_state['ind'] = index

# ---------------------- 核心CSS样式（适配+美观） ----------------------
st.markdown("""
    <style>
    /* 视频容器：自适应+居中+16:9比例 */
    div[data-testid="stVideo"] {
        width: 100% !important;
        max-width: 1200px !important;
        max-height: 450px !important;
        margin: 0 auto !important;
        aspect-ratio: 16/9 !important;
    }
    /* 视频播放器适配 */
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
    /* 标题样式优化 */
    .main-title {
        font-size: 2.5rem;
        color: #d4a017;
        text-align: center;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------- 页面内容布局 ----------------------
# 1. 主标题
st.markdown(f'<h1 class="main-title">{drama_intro["title"]}</h1>', unsafe_allow_html=True)

# 2. 剧集简介区（带边框+多维度信息）- 修正divider为yellow（替代gold）
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
        # 剧集封面图（示例链接）
        st.image(
            "https://ts1.tc.mm.bing.net/th/id/OIP-C.Vl1xkEUOGJJoBZUZUR-_-gHaEC?w=240&h=211&c=8&rs=1&qlt=90&o=6&cb=ucfimg1&pid=3.1&rm=2&ucfimg=1",
            caption=f"{drama_intro['title']} 官方海报",
            use_container_width=True
        )

# 3. 视频播放区（含当前集数标题）- divider=red（合法）
st.subheader("🎥 正片播放", divider="red")
# 视频父容器：三列布局居中
col_video_1, col_video_2, col_video_3 = st.columns([0.1, 0.8, 0.1])
with col_video_2:
    # 当前播放集数标题
    current_video = video_arr[st.session_state['ind']]
    st.markdown(f"<h4>当前播放：{current_video['episode_name']}</h4>", unsafe_allow_html=True)
    # 视频播放（兼容旧版：width传1200，CSS强制自适应）
    st.video(current_video['url'], width=1200)

# 4. 集数选择区（横向按钮+居中）- divider=gray（合法）
st.subheader("📽️ 选择集数", divider="gray")
col_ep_1, col_ep_2, col_ep_3 = st.columns([0.1, 0.8, 0.1])
with col_ep_2:
    episode_cols = st.columns(len(video_arr))
    for idx, video in enumerate(video_arr):
        with episode_cols[idx]:
            # 选中集数按钮高亮（增加视觉反馈）
            is_selected = idx == st.session_state['ind']
            st.button(
                label=f"第{video['episode']}集\n{video['episode_name'].split('：')[1]}",
                use_container_width=True,
                on_click=switch_episode,
                args=(idx,),
                type="primary" if is_selected else "secondary"  # 选中的按钮为蓝色主按钮
            )

# 5. 演职人员图文介绍区 - 修正divider为violet（替代purple）
st.subheader("🎭 主要演职人员", divider="violet")
actor_cols = st.columns(len(actors))  # 按演员数量分栏
for idx, actor in enumerate(actors):
    with actor_cols[idx]:
        st.markdown('<div class="actor-card">', unsafe_allow_html=True)
        # 演员头像
        st.image(
            actor["avatar"],
            caption=f"{actor['role']} - {actor['actor']}",
            use_container_width=True,
            clamp=True,
            output_format="JPEG"
        )
        # 演员信息
        st.markdown(f"**角色**：{actor['role']}")
        st.markdown(f"**演员**：{actor['actor']}")
        st.markdown(f"**角色简介**：{actor['intro']}")
        st.markdown('</div>', unsafe_allow_html=True)

# 6. 页脚（可选，增强完整性）
st.markdown("---")
st.markdown("<center>© 1998 琼瑶工作室 版权所有</center>", unsafe_allow_html=True)
