from cohost.network import fetchTrpc, fetch, generate_login_cookies
from cohost.models.post import Post
from cohost.models.block import Block, AttachmentBlock
# from cohost.models.user import User


class Project:
    def __init__(self, user, data):
        from cohost.models.user import User
        self.user = user  # type: User
        # we can't specify this type globally due to all kinds of import errors
        # but that gives us our login chain back, if that makes sense!
        self.projectId = data['projectId']
        self.data = data
        if self.projectInfo is None:
            raise AttributeError("Project not found")

    def __str__(self):
        return "@{}".format(self.handle)

    @property
    def handle(self):
        return self.projectInfo['handle']

    @property
    def displayName(self):
        return self.projectInfo['displayName']

    @property
    def dek(self):
        return self.projectInfo['dek']

    @property
    def headline(self):
        return self.dek

    @property
    def description(self):
        return self.projectInfo['description']

    @property
    def avatarUrl(self):
        return self.projectInfo['avatarURL']

    @property
    def headerUrl(self):
        return self.projectInfo['headerURL']

    @property
    def privacy(self):
        return self.projectInfo['privacy']

    @property
    def bioUrl(self) -> str:
        return self.projectInfo['url']

    @property
    def pronouns(self) -> str:
        return self.projectInfo['pronouns']

    @property
    def flags(self) -> list:
        return self.projectInfo['flags']

    @property
    def avatarShape(self) -> str:
        return self.projectInfo['avatarShape']

    @property
    def projectInfo(self) -> str:
        return self.data

    def getPostsRaw(self, page=0):
        return fetch('get',
                     '/project/{}/posts?page={}'.format(self.handle, page),
                     None,
                     generate_login_cookies(self.user.cookie))

    def getPosts(self, page=0) -> list:
        postData = self.getPostsRaw(page)
        posts = []
        for post in postData['items']:
            posts.append(Post(post, self))
        return posts


"""Project but using live API data, instead of prefilled data. Intended for use in editable projects!"""


class EditableProject(Project):
    def __init__(self, user, projectId):
        from cohost.models.user import User
        self.user = user  # type: User
        # we can't specify this type globally due to all kinds of import errors
        # but that gives us our login chain back, if that makes sense!
        self.projectId = projectId
        if self.projectInfo is None:
            raise AttributeError("Project not found")

    @property
    def projectInfo(self) -> str:
        projects = self.user.editedProjectsRaw
        for project in projects:
            if project['projectId'] == self.projectId:
                return project
        return None

    def post(self, headline: str, blocks: list[Block], cws: list = [], tags: list = [], adult: bool = False, draft = False):
        # Basic flow: you send a POST to project/{handle}/posts
        # This gives us back a post ID, as well as a API link
        # For example:
        """
        {
        "postId": 53648,
        "_links": [
            {
            "href": "/api/v1/project_posts/53648",
            "rel": "post",
            "type": "GET"
            }
        ]
        }
        """
        # Then, if you have images, upload then by sending data *about* the image to project/{handle}/posts/{postId}/attach/start
        # This will respond back with something like...
        """
        {
            "attachmentId": "25ecb155-9937-4b87-b1b3-bd70a6be3bbc",
            "url": "https://sfo3.digitaloceanspaces.com/redcent-dev",
            "requiredFields": {
                "acl": "public-read",
                "Content-Type": "image/webp",
                "Content-Disposition": "inline",
                "Cache-Control": "max-age=31536000",
                "key": "attachment/25ecb155-9937-4b87-b1b3-bd70a6be3bbc/SleepFaceIcon.webp",
                "bucket": "redcent-dev",
                "X-Amz-Algorithm": "...",
                "X-Amz-Credential": "...",
                "X-Amz-Date": "20220716T110215Z",
                "Policy": "...",
                "X-Amz-Signature": "..."
        }
        """
        # We can THEN send the image to DO spaces, using the credentials
        # Once this is uploaded, we can tell cohost the upload is finished by sending another POST to project/{handle}/posts/{id}/attach/finish/{attachmentId}
        # after ALL of this we sent a PUT (what a change) request to project/{handle}/posts/{postId}
        # the body of this is the same as what we initially POST'd, but, now, we replace the initial blank attachmentId with the corresponding one back. The only catch is change postState to 1, instead of zero
        # (postState refers to if the post should be public - if it is zero, it will only exist as a draft)
        # TODO: Implement the image upload stuff within AttachmentBlock - it should handle all of this
        # For now though, we'll just send the initial post as that's good enough for text!
        blockL = []
        attachments = []
        for b in blocks:
            if type(b) is AttachmentBlock:
                attachments.append(b) # type: AttachmentBlock
            else:
                blockL.append(b.dict)
        
        for attachment in attachments:
            blockL.insert(0, attachment.dict)
        postData = {
            'postState': int(not(draft) and (len(attachments) == 0)),
            'headline': headline,
            'adultContent': adult,
            'blocks': blockL,
            'cws': cws,
            'tags': tags
        }
        req = fetch('postJSON', '/project/{}/posts'.format(self.handle), postData,
                    generate_login_cookies(self.user.cookie))
        if len(attachments) == 0 and not(draft):
            return self.getPosts()[0]  # this will be what we just posted
        if len(attachments) == 0:
            return None # TODO: Get drafts working!
        # OK so, we can now feed each attachment block our post ID
        for attachment in attachments:
            attachment.uploadIfNot(req['postId'], self)
        # Sick! Everything is uploaded - we can now rebuild the post data and send it back to cohost
        blockL = []
        for b in blocks:
            blockL.append(b.dict)
        postData = {
            'postState': int(not(draft)),
            'headline': headline,
            'adultContent': adult,
            'blocks': blockL,
            'cws': cws,
            'tags': tags
        }
        req = fetch('put', '/project/{}/posts/{}'.format(self.handle, req['postId']), postData,
                    generate_login_cookies(self.user.cookie))
        if not draft:
            return self.getPosts()[0]  # this will be what we just posted
        return None # TODO: Get drafts working!

    @staticmethod
    def create(user, projectName, private: bool = False, adult: bool = False) -> Project:
        raise NotImplemented(
            "Can be technically implemented, but I'm choosing not to to respect cohost. I don't want bots creating tons of pages and handles to be easy to build. Sorry!")
