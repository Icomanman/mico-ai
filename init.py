
import streamlit as st

from app import main as rag  # NOQA
from qna import qna  # NOQA
from utils.shuffle import shuffle  # NOQA
from utils.splitter import split  # NOQA


def main() -> None:
    st.set_page_config(
        page_title="mico.AI", page_icon="💭")
    col1, col2, col3 = st.columns([1, 2, 1])
    col1.markdown('# Welcome')
    col2.markdown('# to mico.AI 💭')
    col3.markdown('### | Ask me about engineering')

    pdf = st.file_uploader('Upload your PDF', type='pdf')
    message = st.text_area("How can I help you today?")
    body = None

    if pdf:
        with st.spinner(shuffle()):
            body = split(pdf, 'aci-handbook-2015')
            if body:
                st.success('Successfuly uploaded.')

    if message and body:
        with st.spinner(shuffle()):
            api_response = qna(message, body)
            st.info(f'{api_response}')
    elif message:
        with st.spinner(shuffle()):
            api_response = rag(message)

        st.info(f'{api_response}')

    return


if __name__ == '__main__':
    main()
