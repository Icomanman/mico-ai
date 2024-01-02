
import time
import streamlit as st

from utils.shuffle import shuffle  # NOQA
from utils.splitter import split  # NOQA
import app  # NOQA


def send_request(msg=''):
    time.sleep(2)
    return {"data": "API response data"}


def main():
    st.set_page_config(
        page_title="mico.AI", page_icon="💭")
    col1, col2, col3 = st.columns([1, 2, 1])
    col1.markdown('# Welcome')
    col2.markdown('# to mico.AI 💭')
    col3.markdown('### | Ask me about engineering')

    pdf = st.file_uploader('Upload your PDF', type='pdf')
    message = st.text_area("How can I help you today?")

    if message:
        with st.spinner(shuffle()):
            # api_response = send_request()
            api_response = app.main(message)

        # st.success(f"API response: {api_response['data']}")
        st.info(f'{api_response}')

    if pdf:
        with st.spinner(shuffle()):
            body = split(pdf, 'aci-handbook-2015')
            st.info(body)
    return


if __name__ == '__main__':
    main()
