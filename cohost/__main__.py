from cohost.models.user import User
from cohost.models.post import Post
from cohost.models.block import AttachmentBlock, MarkdownBlock
from cohost.models.project import Project, EditableProject
import os
import json
def main():
    cookie = os.environ.get('COHOST_COOKIE')
    if cookie is None:
        print('COHOST_COOKIE environment variable not set - please paste your cookie below')
        print('To skip this, please set the COHOST_COOKIE environment variable to the cookie you want to use')
        cookie = input('COHOST_COOKIE: ')
    user = User.loginWithCookie(cookie)
    project = user.getProject('vallerie')
    blocks = [
        MarkdownBlock('images are now working!!! so say hello to pybug. as per the previous post, little code screenie as well - the library reads from a location on disk, so you just tell it the filename and it uploads 😄'),
        MarkdownBlock('there isnt error checking though so who knows if you try uploading an 11mb file. maybe eggbug cries.'),
        MarkdownBlock('also i might add a special attachment block just for pybug. incase you just want to include pybug. let him spread his little snake wings.'),
        AttachmentBlock('pybug.png'),
        AttachmentBlock('screenshot.png'),
    ]
    p = project.post('images are now working in cohost.py!!',
                     blocks,
                     adult=False, draft=False, tags=['cohost.py', 'python', 'drafts are still WIP because i cannot figure out what the API endpoint for the life of me'])
    print('Live at: {}'.format(p.url))
    

if __name__ == '__main__':
    main()
