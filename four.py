import streamlit as st

# 页面配置
st.set_page_config(page_title="还珠格格播放", page_icon="🎬", layout="wide")

# 标题 + 电视剧介绍
st.title('还珠格格第一部')
with st.container(border=True):
    st.subheader("📺 剧集简介")
    st.write("""
    《还珠格格》是中国台湾作家琼瑶创作的古装爱情喜剧，第一部于1998年播出。
    该剧以清朝乾隆年间为背景，讲述了民间女子小燕子误闯皇宫，与紫薇、尔康、永琪等发生的一系列啼笑皆非又感人至深的故事，
    是一代人的经典童年回忆，曾创下超高收视率。
    """)

# 视频列表数据
video_arr = [
    {
        'url': 'https://upos-sz-mirrorcosov.bilivideo.com/upgcxcode/55/22/34578302255/34578302255-1-192.mp4?e=ig8euxZM2rNcNbRBnwdVhwdlhWU3hwdVhoNvNC8BqJIzNbfq9rVEuxTEnE8L5F6VnEsSTx0vkX8fqJeYTj_lta53NCM=&mid=3546763107502921&nbs=1&os=cosovbv&og=hw&platform=html5&oi=1804878521&deadline=1765768710&uipk=5&trid=f6c6c76fe5cc432daec777568fe1174T&gen=playurlv3&upsig=f92713098c187bfeb596053f86d1ffd3&uparams=e,mid,nbs,os,og,platform,oi,deadline,uipk,trid,gen&bvc=vod&nettype=0&bw=1269037&agrr=1&buvid=&build=0&dl=0&f=T_0_0&mobi_app=&orderid=0,1',
        'title': '第1集',
        'episode': 1
    },{
        'url': 'https://upos-sz-mirrorcosov.bilivideo.com/upgcxcode/17/33/34578303317/34578303317-1-192.mp4?e=ig8euxZM2rNcNbRz7zdVhwdlhWhahwdVhoNvNC8BqJIzNbfq9rVEuxTEnE8L5F6VnEsSTx0vkX8fqJeYTj_lta53NCM=&og=cos&deadline=1765768923&uipk=5&gen=playurlv3&platform=html5&mid=3546763107502921&oi=1804878521&nbs=1&trid=1a26a4d19f464299b65bdd1ebc1070dT&os=cosovbv&upsig=474bc515fbe7d752d6443a177700af87&uparams=e,og,deadline,uipk,gen,platform,mid,oi,nbs,trid,os&bvc=vod&nettype=0&bw=1100998&mobi_app=&agrr=1&buvid=&build=0&dl=0&f=T_0_0&orderid=0,1',
        'title': '第2集',
        'episode': 2
    },{
        'url': 'https://upos-sz-mirrorcosov.bilivideo.com/upgcxcode/93/43/34578304393/34578304393-1-192.mp4?e=ig8euxZM2rNcNbRVnwdVhwdlhWd3hwdVhoNvNC8BqJIzNbfq9rVEuxTEnE8L5F6VnEsSTx0vkX8fqJeYTj_lta53NCM=&trid=3748a5d634f8497c908cfcd07dfdd56T&mid=3546763107502921&uipk=5&gen=playurlv3&os=cosovbv&platform=html5&deadline=1765768981&nbs=1&oi=1804878521&og=cos&upsig=e95d93af01c29bd4b4b5c0d904e8b7be&uparams=e,trid,mid,uipk,gen,os,platform,deadline,nbs,oi,og&bvc=vod&nettype=0&bw=866304&mobi_app=&agrr=1&buvid=&build=0&dl=0&f=T_0_0&orderid=0,1',
        'title': '第3集',
        'episode': 3
    }
]

# 初始化会话状态
if 'ind' not in st.session_state:
    st.session_state['ind'] = 0

# 集数切换函数
def switch_episode(index):
    st.session_state['ind'] = index

# 核心CSS：强制自适应+居中+16:9比例（覆盖width参数的固定值）
st.markdown("""
    <style>
    /* 视频容器：自适应宽度 + 16:9比例 + 居中 + 限制最大高度 */
    div[data-testid="stVideo"] {
        width: 100% !important;       /* 强制自适应父容器，覆盖width参数 */
        max-width: 1200px !important; /* 限制最大宽度，避免太宽 */
        max-height: 450px !important; /* 限制最大高度 */
        margin: 0 auto !important;    /* 水平居中 */
        aspect-ratio: 16/9 !important;/* 16:9比例，高度自动适配 */
    }
    /* 视频播放器：填满容器 + 保持比例 */
    div[data-testid="stVideo"] video {
        width: 100% !important;
        height: 100% !important;
        object-fit: contain !important; /* 不拉伸、不裁剪 */
    }
    /* 集数按钮容器：自适应居中 */
    .episode-btn-container {
        max-width: 1200px !important; /* 和视频最大宽度对齐 */
        margin: 0 auto !important;
    }
    </style>
""", unsafe_allow_html=True)

# 第一步：三列布局让视频居中（中间列自适应宽度）
col1, col2, col3 = st.columns([0.1, 0.8, 0.1])  # 左右留10%空白，中间80%放视频
with col2:
    # 兼容旧版本：width传大整数（1200），靠CSS强制自适应
    st.video(video_arr[st.session_state['ind']]['url'], width=1200)

# 第二步：集数按钮居中+自适应
st.subheader("选择集数", divider="gray")
# 按钮容器也用三列布局，和视频对齐
btn_col1, btn_col2, btn_col3 = st.columns([0.1, 0.8, 0.1])
with btn_col2:
    st.markdown('<div class="episode-btn-container">', unsafe_allow_html=True)
    episode_cols = st.columns(len(video_arr))  # 按钮横向排列
    for idx, video in enumerate(video_arr):
        with episode_cols[idx]:
            st.button(
                label=f"第{video['episode']}集",
                use_container_width=True,
                on_click=switch_episode,
                args=(idx,)
            )
    st.markdown('</div>', unsafe_allow_html=True)
