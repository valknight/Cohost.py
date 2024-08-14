from typing import Any

from cohost.models.block import AttachmentBlock
from cohost.models.post import Post
from cohost.network import fetch, generate_login_cookies, fetchTrpc


class Project:
    def __init__(self, user, data: dict[str, Any]):
        # this helps editors understand what we're setting
        from cohost.models.user import User  # noqa: F401
        self.user: User = user
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
    def projectInfo(self) -> dict[str, Any]:
        return self.data

    @property
    def atomFeed(self) -> str:
        # TODO: This is a bad assumption
        # Cohost gives us a rel=link we should use instead
        # However, to get this exposed in our API asap, this works
        return "https://cohost.org/{}/rss/public.atom".format(self.handle)

    @property
    def rssFeed(self) -> str:
        # Cohost's feeds aren't "RSS" but actually the atom format
        # Most RSS readers will just call this RSS though
        # As such, you *should* be fine
        # But! it's good to note the difference & technicality
        # See for more information
        # http://www.intertwingly.net/wiki/pie/Rss20AndAtom10Compared
        return self.atomFeed

    @property
    def jsonFeed(self) -> str:
        # See above note in relation to the rssFeed method
        return "https://cohost.org/{}/rss/public.json".format(self.handle)

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

    def ask(self, content, sourceProject, anon=False):
        from cohost.models.project import EditableProject
        if not isinstance(sourceProject, EditableProject):
            raise TypeError("sourceProject must be an editable project")
        sourceProject = sourceProject  # EditableProject
        fetchTrpc('asks.send', sourceProject.user.cookie, {
            "toProjectHandle": self.handle,
            "content": content,
            "anon": anon}, methodType='postjson')

    def getAsksRaw(self) -> list[dict]:
        rawResp = fetchTrpc('asks.listPending', self.user.cookie, {
            'input': {'projectHandle': self.handle}
        })
        return rawResp['result']['data']['asks']


class EditableProject(Project):
    def __init__(self, user, projectId):
        from cohost.models.user import User  # noqa: F401
        self.user = user
        # we can't specify this type globally due to all kinds of import errors
        # but that gives us our login chain back, if that makes sense!
        self.projectId = projectId
        if self.projectInfo is None:
            raise AttributeError("Project not found")

    @property
    def projectInfo(self) -> dict[str, Any]:
        projects = self.user.editedProjectsRaw
        for project in projects:
            if project['projectId'] == self.projectId:
                return project
        raise AttributeError("Project not found")

    def post(self, headline: str, blocks: list = [], cws: list = [],
             tags: list = [], adult: bool = False, draft=False, shareOfPostId: int = None):
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
        # Then, if you have images:
        # Upload them by sending data *about* the image to
        #   project/{handle}/posts/{postId}/attach/start
        # This will respond back with something like...
        """
        {
            "attachmentId": "yourattachmentid",
            "url": "https://sfo3.digitaloceanspaces.com/redcent-dev",
            "requiredFields": {
                "acl": "public-read",
                "Content-Type": "image/webp",
                "Content-Disposition": "inline",
                "Cache-Control": "max-age=31536000",
                "key": "attachment/yourattachmentid/foo.webp",
                "bucket": "redcent-dev",
                "X-Amz-Algorithm": "...",
                "X-Amz-Credential": "...",
                "X-Amz-Date": "20220716T110215Z",
                "Policy": "...",
                "X-Amz-Signature": "..."
        }
        """
        # We can THEN send the image to DO spaces, using the credentials
        # Once this is uploaded, we can tell cohost the upload is finished
        # We do this by sending another POST to the following URL:
        #   project/{handle}/posts/{id}/attach/finish/{attachmentId}
        # After ALL of this we sent a PUT (what a change) request to:
        #   project/{handle}/posts/{postId}
        # the body of this is the same as what we initially POST'd, but -
        # now, we replace the blank attachmentId
        # We do this with the corresponding one we got back
        # The only catch is change postState to 1, instead of zero
        # postState refers to if the post should be public
        # if it is zero, it will only exist as a draft
        blockL = []
        attachments = []
        for b in blocks:
            if type(b) is AttachmentBlock:
                attachments.append(b)
            else:
                blockL.append(b.dict)

        for attachment in attachments:
            blockL.insert(0, attachment.dict)
        postData = {
            'postState': int((not draft) and (len(attachments) == 0)),
            'headline': headline,
            'adultContent': adult,
            'blocks': blockL,
            'cws': cws,
            'tags': tags,
        }
        if shareOfPostId is not None:
            postData.update({
                    'shareOfPostId': shareOfPostId
                })
        req = fetch(
            'postJSON',
            '/project/{}/posts'.format(self.handle),
            postData,
            generate_login_cookies(self.user.cookie)
        )
        if len(attachments) == 0 and (not draft):
            return self.getPosts()[0]  # this will be what we just posted
        if len(attachments) == 0:
            return None  # TODO: Get drafts working!
        # OK so, we can now feed each attachment block our post ID
        for attachment in attachments:
            attachment.uploadIfNot(req['postId'], self)
        # Sick! Everything is uploaded
        # We can now rebuild the post data and send it back to cohost
        blockL = []
        for b in blocks:
            blockL.append(b.dict)
        postData = {
            'postState': int(not draft),
            'headline': headline,
            'adultContent': adult,
            'blocks': blockL,
            'cws': cws,
            'tags': tags
        }
        if shareOfPostId is not None:
            postData.update({
                    'shareOfPostId': shareOfPostId
                })
        req = fetch(
            'put',
            '/project/{}/posts/{}'.format(self.handle, req['postId']),
            postData,
            generate_login_cookies(self.user.cookie)
        )
        if not draft:
            return self.getPosts()[0]  # this will be what we just posted
        return None  # TODO: Get drafts working!

    def editPost(self, postId: int,
                 headline: str, blocks: list,
                 cws: list = [], tags: list = [],
                 adult: bool = False, draft=False):
        # same thing as post() but -
        # initial request is a PUT to project/{handle}/posts/{postId}

        blockL = []
        attachments = []
        for b in blocks:
            if type(b) is AttachmentBlock:
                attachments.append(b)
            else:
                blockL.append(b.dict)

        for attachment in attachments:
            blockL.insert(0, attachment.dict)
        postData = {
            'postState': int((not draft) and (len(attachments) == 0)),
            'headline': headline,
            'adultContent': adult,
            'blocks': blockL,
            'cws': cws,
            'tags': tags
        }

        req = fetch(
            'put',
            '/project/{}/posts/{}'.format(self.handle, postId),
            postData,
            generate_login_cookies(self.user.cookie)
        )
        if len(attachments) == 0 and (not draft):
            return self.getPosts()[0]  # this will be what we just posted
        if len(attachments) == 0:
            return None  # TODO: Get drafts working!
        # OK so, we can now feed each attachment block our post ID
        for attachment in attachments:
            attachment.uploadIfNot(postId, self)
        # Sick! Everything is uploaded
        # We can now rebuild the post data and send it back to Cohost
        blockL = []
        for b in blocks:
            blockL.append(b.dict)
        postData = {
            'postState': int(not draft),
            'headline': headline,
            'adultContent': adult,
            'blocks': blockL,
            'cws': cws,
            'tags': tags
        }
        req = fetch(
            'put',
            '/project/{}/posts/{}'.format(self.handle, req['postId']),
            postData,
            generate_login_cookies(self.user.cookie)
        )
        if not draft:
            return self.getPosts()[0]  # this will be what we just posted
        return None  # TODO: Get drafts working!

    """Set this project as the default project
    This applies for actions such as retrieving notifications
    """
    def switch(self):
        fetchTrpc('projects.switchProject', self.user.cookie, {
            "projectId": self.projectId
        }, methodType="postjson")

    @staticmethod
    def create(user, projectName, private: bool = False,
               adult: bool = False) -> Project:
        raise NotImplementedError(
            """Can be technically implemented, however -
            I'm choosing not to to respect cohost.
            I don't want bots creating tons of pages and handles.
            Sorry!""")
