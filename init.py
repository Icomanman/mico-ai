
import os
import time
import streamlit as st

from app import main as rag  # NOQA
from qna import qna  # NOQA
from utils.shuffle import shuffle  # NOQA
from utils.splitter import split_pdf  # NOQA
# from utils.drive import Drive  # NOQA
from utils.st_upload import upload_file  # NOQA


"""
def get_files():
    drive_service = Drive()
    # folder = os.environ.get('PROMPT_FOLDER')
    file_id = os.environ.get('FILE_ID')
    drive_service.download(file_id)
    return
"""


def init_folders() -> None:
    if not os.path.exists('./tmp'):
        os.mkdir('./tmp')

    if not os.path.exists('./pdf'):
        os.mkdir('./pdf')

    if not os.path.exists('./dump'):
        os.mkdir('./dump')
    print('> Folders initialised.')
    return


def main() -> None:
    st.set_page_config(
        page_title="mico.AI",
        page_icon="💭",
        layout="wide")  # NOQA
    col1, col2, col3 = st.columns([3, 2, 1])
    col1.markdown('# Welcome to mico.AI 💭')
    col1.subheader('| Ask me about engineering')

    wf = col3.selectbox('Profile', ['Presentation', 'Knowledge Base', 'DSA'])
    # *************************************************************************
    # *************************************************************************
    # BE upload - Streamlit only
    be_upload = col3.toggle(label='🚨')
    cont = col3.empty()
    peewee = None
    if be_upload and not peewee:
        peewee = cont.text_input(
            label='I hope you know what you are doing...SMH', type='password')

    if peewee == os.environ.get('PW') and be_upload:
        cont.empty()
        ffile = col2.file_uploader('Backend Upload')

        if ffile:
            oks = st.success('Successfuly uploaded.', icon='✅')
            with st.spinner(shuffle()):
                msg = upload_file(ffile.getbuffer(), ffile.name)
                st.info(msg)

                if msg:
                    be_upload = False
                    peewee = None
                    oks.empty()
    # *************************************************************************
    # *************************************************************************

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
    # get_files()
    init_folders()
    main()
