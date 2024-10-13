import streamlit as st

st.set_page_config(page_title="Other Tools", page_icon=":1234:")
st.sidebar.header("Other Tools")

st.title("Other cool things to check out")

st.markdown(""" While we won't have time to cover everything, a few things you might want to check out later:
1. You can connect databases to Streamlit [like AWS, MongoDB, etc](https://docs.streamlit.io/develop/tutorials/databases)
1. You can embed Streamlit Spaces [within other webpages](https://huggingface.co/docs/hub/en/spaces-sdks-streamlit#embed-streamlit-spaces-on-other-webpages)
1. If you have models hosted on HuggingFace, you can build [apps that use those models](https://huggingface.co/blog/streamlit-spaces) (like LLMs) and let others use them.  
 """)
