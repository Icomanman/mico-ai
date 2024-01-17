
import os
import time
import streamlit as st

from app import main as rag  # NOQA
from qna import qna  # NOQA
from utils.shuffle import shuffle  # NOQA
from utils.splitter import split_pdf  # NOQA
from utils.drive import Drive  # NOQA


def get_files():
    if not os.path.exists('./tmp'):
        os.mkdir('./tmp')

    drive_service = Drive()
    folder = os.environ.get('PROMPT_FOLDER')
    drive_service.download(f'{folder}/dsa_prompt.py')
    return


def main() -> None:
    st.set_page_config(
        page_title="mico.AI",
        page_icon="💭",
        layout="wide")  # NOQA
    col1, col2 = st.columns([3,  3])
    col1.markdown('# Welcome to mico.AI 💭')
    col1.subheader('| Ask me about engineering')
    # col2.bar_chart(height=150)

    toggle_label = 'Upload a PDF'
    toggle_help = 'Select between asking questions or uploading and querying your pdf'
    use_upload = st.toggle(label=toggle_label, help=toggle_help)

    if not use_upload:
        message = st.text_area(
            "How can I help you today?", key='direct_message')
        if message:
            with st.spinner(shuffle()):
                api_response = rag(message)

            st.info(f'{api_response}')
    else:
        hint = 'You can now query your pdf.'
        pdf = st.file_uploader('Upload your PDF', type='pdf')
        if pdf:
            start = time.time()
            with st.spinner(shuffle()):
                # body = split(pdf)
                success = st.success('Successfuly uploaded.', icon='✅')
                print(f'> upload only: {(time.time() - start)} s')

            message = st.text_area(label=hint, key='upload_query')

            if message:
                success.empty()
                start = time.time()
                with st.spinner(shuffle()):
                    body = split_pdf(pdf)
                    print(f'> split: {(time.time() - start)} s')
                    api_response = qna(body, message)
                    st.info(f'{api_response}')
    return


if __name__ == '__main__':
    get_files()
    # main()
