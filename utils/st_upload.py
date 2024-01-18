
import os
import sys


def upload_file(uploaded_file: bytes, file_name: str = 'userfile') -> str:
    if not os.path.exists('./tmp'):
        os.mkdir('./tmp')
    global message

    with open(f'./tmp/{file_name}', 'wb') as f:
        try:
            f.write(uploaded_file)
            message = f'File successfully uploaded ({file_name})'
        except ValueError as e:
            message = e

        print(message)
    return message


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python st_upload.py <file>.')
        sys.exit(1)

    upload_file(sys.argv[1], sys.argv[2])
