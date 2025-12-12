import streamlit as st

# 设置页面标题和图标
st.set_page_config(page_title="简易音乐播放器", page_icon="🎵")
st.title("简易音乐播放器")

# 初始化当前歌曲索引（存储在SessionState）
if 'current_song_idx' not in st.session_state:
    st.session_state.current_song_idx = 0

# ========== 核心修正：把函数定义提前 ==========
# 切换歌曲的函数（放在按钮调用前定义）
def prev_song():
    # 循环切换（第一首切到最后一首）
    st.session_state.current_song_idx = (st.session_state.current_song_idx - 1) % len(music_list)

def next_song():
    # 循环切换（最后一首切到第一首）
    st.session_state.current_song_idx = (st.session_state.current_song_idx + 1) % len(music_list)

# 音乐列表（包含：专辑图URL、歌手、歌名、音频URL）
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

# 获取当前选中的歌曲
current_song = music_list[st.session_state.current_song_idx]

# 【调整布局】左专辑图 + 右歌曲信息 并排显示
col_img, col_info = st.columns([1, 3], gap="small")
with col_img:
    # 匹配示例图的专辑图尺寸
    st.image(current_song["album_img"], width=130)
with col_info:
    # 突出显示歌名、歌手
    st.markdown(f"### {current_song['song_name']}")  # 用标题层级替代加粗，更醒目
    st.write(f"**歌手**：{current_song['singer']}")

# 【修正】移除height参数，保留核心音频播放功能
st.audio(current_song["audio_url"], format="audio/mp3")

# 【调整位置】上/下一首按钮（贴近播放控制）
col_prev, col_next = st.columns(2, gap="small")
with col_prev:
    st.button("上一首", on_click=prev_song, use_container_width=True)
with col_next:
    st.button("下一首", on_click=next_song, use_container_width=True)
