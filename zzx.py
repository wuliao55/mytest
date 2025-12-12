import streamlit as st
# 修改标签页的文字和图标
st.set_page_config(page_title="相册", page_icon="🐱")
st.title("我的相册")
# 把当前图片的索引存储在streamlit的内存中
if 'ind' not in st.session_state:
    st.session_state['ind'] = 0
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
st.image(images[st.session_state['ind']]['url'], caption=images[st.session_state['ind']]['text'])
# 下一张图片功能
def nextImg():
    st.session_state['ind'] = (st.session_state['ind'] + 1) % len(images)
# 上一张图片功能
def prevImg():
    # 用取模实现循环切换（最后一张切到第一张）
    st.session_state['ind'] = (st.session_state['ind'] - 1) % len(images)
# 并排显示上一张和下一张按钮
col1, col2 = st.columns(2)
with col1:
    st.button("上一张", on_click=prevImg)
with col2:
    st.button("下一张", on_click=nextImg)
