from distutils.command.build import build
from re import U
from cohost.models.project import EditableProject
from cohost.network import fetch, fetchTrpc, generate_login_cookies
from cohost.models.notification import buildFromNotifList
import hashlib
import base64


class User:
    def __init__(self, cookie) -> None:
        self.cookie = cookie

    def __str__(self) -> str:
        return "user_{}".format(self.userId)

    @property
    def email(self) -> str:
        return self.userInfo['email']

    @property
    def userId(self) -> str:
        return self.userInfo['userId']

    @property
    def modMode(self) -> bool:
        return self.userInfo['modMode']

    @property
    def activated(self) -> bool:
        return self.userInfo['activated']

    @property
    def readOnly(self) -> bool:
        return self.userInfo['readOnly']

    @property
    def defaultProject(self) -> EditableProject:
        from cohost.models.project import EditableProject
        return EditableProject(self, self.userInfo['projectId'])

    @property
    def userInfo(self) -> dict:
        return fetchTrpc('login.loggedIn', self.cookie)['result']['data']

    """Fetch data from the API about projets the user can edit
    
    Returns:
        dict: Project dictionaries
    """
    @property
    def editedProjectsRaw(self) -> dict:
        return fetchTrpc('projects.listEditedProjects', self.cookie)['result']['data']['projects']

    """Fetch data from the API about projects the user can edit
    
    Returns:
        list[Project]: Project objects
    """
    @property
    def editedProjects(self) -> list:
        rawP = self.editedProjectsRaw
        projects = []
        for project in rawP:
            projects.append(EditableProject(self, project['projectId']))
        return projects

    """Get a salt for an email - for use in logging in
    

    Returns:
        str: Base64 encoded salt
    """
    @staticmethod
    def getSalt(email):

        salt = fetch(
            "GET",
            "/login/salt",
            {'email': email}
        )
        return salt

    """Create a user object from a login and password"""
    @staticmethod
    def login(email, password):
        # TODO: This involves a bunch of weird base64 stuff I can't be bothered with. For now, we only support logging in with a cookie
        raise NotImplementedError("val is lazy and hasn't done this yet")

    """Create a user object from a cookie"""
    @staticmethod
    def loginWithCookie(cookie):
        # First, let's create a user
        u = User(cookie)
        # Now, we need to validate functions are working - we can do this by getting the user's info
        u.userInfo
        # If this didn't error out, we're good!
        return u

    def getProject(self, handle: str) -> EditableProject:
        # Retrieve a project that you can edit
        projects = self.editedProjects
        for project in projects:
            if project.handle == handle:
                return project
        return None

    def resolveSecondaryProject(self, projectData):
        from cohost.models.project import Project, EditableProject
        editableProjects = self.editedProjects
        for project in editableProjects:
            if project.projectId == projectData['projectId']:
                return project  # type: EditableProject
        return Project(self, projectData)  # type: Project

    @property
    def notifications(self):
        nJson = fetch('GET', 'notifications/list', {
            'offset': 0,
            'limit': 5000
        }, generate_login_cookies(self.cookie))
        return buildFromNotifList(nJson, self)


"""

def getProjects() {
    return (await fetch(
        "GET",
        "/projects/edited",
        this.sessionCookie
    )).projects.map(x => new Project(this, x));
}

def getNotifications(offset = 0, limit = 20):
    return (await fetch(
        "GET",
        "/notifications/list",
        this.sessionCookie,
        { offset, limit }
    ))
"""
