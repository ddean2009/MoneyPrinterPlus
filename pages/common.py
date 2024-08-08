import streamlit as st

from tools.tr_utils import tr


def common_ui():
    st.set_page_config(page_title="MoneyPrinterPlus",
                       page_icon=":pretzel:",
                       layout="wide",
                       initial_sidebar_state="auto",
                       menu_items={
                           'Report a Bug': "https://github.com/ddean2009/MoneyPrinterPlus",
                           'About': "这是一个轻松搞钱的项目,关注我,带你搞钱",
                           'Get help': "https://www.flydean.com"
                       })

    st.sidebar.page_link("gui.py", label=tr("Base Config"))
    st.sidebar.page_link("pages/01_auto_video.py", label=tr("Generate Video"))
    st.sidebar.page_link("pages/02_mix_video.py", label=tr("Mix Video"))
    st.sidebar.page_link("pages/02_merge_video.py", label=tr("Merge Video"))
    st.sidebar.page_link("pages/03_auto_publish.py", label=tr("Video Auto Publish"))
    st.sidebar.markdown(
        '<a style="text-align: center;padding-top: 0rem;" href="http://www.flydean.com">Developed by 程序那些事</a>',
        unsafe_allow_html=True)

    with st.sidebar:
        st.markdown('---')