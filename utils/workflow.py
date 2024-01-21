
import sys
from tmp import dsa, knowledge, presentation


def get_worfklow(workflow: str) -> dict:
    prompt = ''
    src_file = ''

    if workflow == 'Presentation':
        prompt = presentation()
        src_file = './dump/notes.md'
    elif workflow == 'DSA':
        prompt = dsa()
        src_file = ''
    elif 'Knowledge Base':
        prompt = knowledge()
        src_file = './dump/dat.csv'
    else:
        raise ValueError('> Invalid workflow')
        sys.exit(1)

    return {src_file, prompt}
