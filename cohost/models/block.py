from typing import Any, Optional

import requests

from cohost.network import fetch, generate_login_cookies


class Block:
    """Posts are made up of blocks

    Think of each section of text, or an image - it's all blocks baybe!

    To implement blocks, make subclasses of this!
    """

    def __init__(self) -> None:
        raise NotImplementedError('Base block is an abstract class')

    @property
    def dict(self) -> dict:
        raise NotImplementedError('Base block is an abstract class')


class MarkdownBlock(Block):
    """A block that contains markdown text"""

    def __init__(self, markdown: str) -> None:
        self.data = markdown

    @property
    def dict(self) -> dict:
        return {
            'type': 'markdown',
            'markdown': {
                'content': self.data
            }
        }


class AttachmentBlock(Block):
    """A block that contains an attachment"""

    def __init__(self, filepath: str,
                 attachment_id: Optional[str] = None, alt_text=None) -> None:
        try:
            with open(filepath, 'rb') as f:
                f.read()
        except FileNotFoundError:
            raise FileNotFoundError(
                'Attachment could not be found at: {}'.format(filepath))
        self.filepath = filepath
        self.filename = self.filepath.split('/')[-1]
        content_type = None
        if self.filename.lower().endswith('.webp'):
            content_type = 'image/webp'
        elif (self.filename.lower().endswith('.jpg')
              or self.filename.lower().endswith('.jpeg')):
            content_type = 'image/jpeg'
        elif self.filename.lower().endswith('.png'):
            content_type = 'image/png'
        elif self.filename.lower().endswith('.svg'):
            content_type = 'image/svg+xml'
        elif self.filename.lower().endswith('.gif'):
            content_type = 'image/gif'
        self.content_type: Optional[str] = content_type
        with open(self.filepath, 'rb') as f:
            content_length = len(f.read())
        self.content_length: int = content_length
        self.attachment_id: Optional[str] = attachment_id
        self.alt_text: str = alt_text

    @property
    def dict(self) -> dict[str, Any]:
        aid = self.attachment_id
        if self.attachment_id is None:
            aid = "00000000-0000-0000-0000-000000000000"
        toReturn: dict[str, Any] = {
            'type': 'attachment',
            'attachment': {
                'attachmentId': aid
            }
        }
        if self.alt_text:
            toReturn['attachment']['altText'] = self.alt_text
        return toReturn

    def uploadIfNot(self, postId, project):
        if self.attachment_id is not None:
            return
        # we don't have an attachment ID!
        # that means this file isn't tied to a cohost file
        # Step 1: tell cohost we're uploading a file
        # we do this using project/{handle}/posts/53633/attach/start
        endpoint = 'project/{}/posts/{}/attach/start'.format(
            project.handle, postId)

        # example data: filename=foo.jpg&
        #   content_type=image%2Fjpeg&content_length=20829
        dospacecreds = fetch('postjson', endpoint, {
            'filename': self.filename,
            'content_type': self.content_type,
            'content_length': int(self.content_length)
        }, generate_login_cookies(project.user.cookie))
        # Step 2: digitalocean time
        # we now have digitalocean creds to upload the image to Spaces
        # we need to use raw requests here
        # this is because we're not talking to Cohost
        spacesUrl = dospacecreds.get('url')
        b = None
        with open(self.filepath, 'rb') as f:
            b = f.read()
        spaceresp = requests.post(
            spacesUrl, data=dospacecreds.get('requiredFields'), files={
                'file': (self.filename, b, self.content_type)
            })
        if spaceresp.status_code != 204:
            raise Exception('Error uploading to Spaces')
        # and now, tell cohost we're done!
        endpoint = 'project/{}/posts/{}/attach/finish/{}'.format(
            project.handle, postId, dospacecreds.get('attachmentId'))
        fetch('post', endpoint, {}, generate_login_cookies(
            project.user.cookie))  # Will indicate we're done!
        self.attachment_id = dospacecreds.get('attachmentId')
