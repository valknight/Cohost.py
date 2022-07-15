from curses.ascii import US
import cohost
from cohost.network import fetchTrpc, fetch, generate_login_cookies
from cohost.models.post import Post
# from cohost.models.user import User

class Project:
    def __init__(self, user, data):
        from cohost.models.user import User
        self.user = user # type: User
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
    
    
    
    def getPostsRaw(self, page = 0):
        return fetch('get',
              '/project/{}/posts?page={}'.format(self.handle, page),
              None,
              generate_login_cookies(self.user.cookie))
    
    def getPosts(self, page = 0) -> list:
        postData = self.getPostsRaw(page)
        posts = []
        for post in postData['items']:
            posts.append(Post(post, self))
        return posts

"""Project but using live API data, instead of prefilled data. Intended for use in editable projects!"""
class EditableProject(Project):
    def __init__(self, user, projectId):
        from cohost.models.user import User
        self.user = user # type: User
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

    