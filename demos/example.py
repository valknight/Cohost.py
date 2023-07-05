import os

from cohost.models.block import AttachmentBlock, MarkdownBlock
from cohost.models.user import User


def main():
    cookie = os.environ.get('COHOST_COOKIE')
    if cookie is None:
        print('COHOST_COOKIE environment variable not set - please paste your cookie below')
        print('To skip this, please set the COHOST_COOKIE environment variable to the cookie you want to use')
        cookie = input('COHOST_COOKIE: ')
    user = User.loginWithCookie(cookie)
    project = user.getProject('yourhandle')
    print('Logged in as: {}'.format(project))
    blocks = [
        MarkdownBlock('hello from cohost!'),
        AttachmentBlock('pybug.png'),
    ]
    p = project.post('Cohost.py is working!',
                     blocks,
                     adult=False, draft=False, tags=['cohost.py', 'python'])
    print('Live at: {}'.format(p.url))
    

if __name__ == '__main__':
    main()
