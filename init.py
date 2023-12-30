
import time
import streamlit as st

from utils.shuffle import shuffle  # NOQA


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
    message = st.text_area("How can I help you today?")

    if message:
        with st.spinner(shuffle()):
            api_response = send_request()

        st.success(f"API response: {api_response['data']}")
        st.info('> Result goes here...')
    return


if __name__ == '__main__':
    main()
