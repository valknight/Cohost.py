class Post:
    def __init__(self, postData, project):
        # we do this here to help autosuggest figure out what project is
        from cohost.models.project import Project
        self.postData = postData
        self.project = project  # type: Project

    def __str__(self) -> str:
        return "{}".format(self.filename)

    @property
    def postId(self):
        return self.postData['postId']

    @property
    def headline(self):
        return self.postData['headline']

    @property
    def publishedAt(self):
        return self.postData['publishedAt']  # TODO: Use a datetime for this

    @property
    def filename(self):
        return self.postData['filename']

    @property
    def transparentShareOfPostId(self):
        return self.postData['transparentShareofPostId']

    @property
    def state(self):
        return self.postData['state']

    @property
    def numComments(self):
        return self.postData['numComments']

    @property
    def numSharedComments(self):
        return self.postData['numSharedComments']

    @property
    def contentWarnings(self) -> list:
        return self.postData['cws']

    @property
    def tags(self) -> list:
        return self.postData['tags']

    """Build 
    
    Returns:
        list[str]: Return a list of blocks that make up a post
    """
    @property
    def blocks(self) -> list:
        return self.postData['blocks']

    @property
    def plainTextBody(self) -> str:
        return self.postData['plainTextBody']

    @property
    def ogAuthor(self) -> str:
        if self.postData['shareTree']:
            # We use the first one, as i *think* that refers to the OG poster
            newProject = self.postData['shareTree'][0]['postingProject']
        else:
            newProject = self.postData['postingProject']
        return self.project.user.resolveSecondaryProject(newProject)

    @property
    def shareTree(self):
        return self.postData['shareTree']
    
    @property
    def relatedProjects(self) -> list:
        projects = []
        for p in self.postData['relatedProjects']:
            projects.append(self.project.user.resolveSecondaryProject(p))
        return projects

    @property
    def url(self) -> str:
        return self.postData['singlePostPageUrl']

    @property
    def adult(self) -> bool:
        return self.postData['effectiveAdultContent']

    @property
    def contributorBlock(self) -> bool:
        # i haven't blocked anyone or been blocked (i think) so idk how this works
        # anyone who gets blocekd a lot pls test this
        return self.postData['contributorBlockIncomingOrOutgoing']

    @property
    def hasAnyContributorMuted(self) -> bool:
        return self.postData['hasAnyContributorMuted']

    @property
    def renderInIframe(self) -> bool:
        return self.postData['renderInIframe']

    @property
    def postPreviewIframeUrl(self) -> str:
        return self.postData['postPreviewIFrameUrl']

    @property
    def postEditurl(self) -> str:
        return self.postData['postEditUrl']

    @property
    def liked(self) -> bool:
        return self.postData['isLiked']

    @property
    def shareable(self) -> bool:
        return self.postData['canShare']

    @property
    def publishable(self) -> bool:
        return self.postData['canPublish']
