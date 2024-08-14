class Post:
    def __init__(self, postData, project):
        # we do this here to help autosuggest figure out what project is
        from cohost.models.project import Project  # noqa: F401
        self.postData = postData
        self.project = project

    def __str__(self) -> str:
        return "{}".format(self.filename)

    def edit(self, headline: str, blocks: list = [], cws: list = [],
             tags: list = [], adult: bool = False, draft=False):
        from cohost.models.project import EditableProject
        if not isinstance(self.project, EditableProject):
            raise AttributeError("Post isn't attached to an EditableProject -\
                                 do you have Edit permissions for this post?")
        return self.project.editPost(
            self.postId,
            headline=headline,
            blocks=blocks,
            cws=cws,
            tags=tags,
            adult=adult,
            draft=draft
        )
    
    def share(self, headline: str, blocks: list = [], cws: list = [], 
              tags: list = [], adult: bool = False, draft=False):
        from cohost.models.project import EditableProject
        if not isinstance(self.project, EditableProject):
            raise AttributeError("Post isn't attached to an EditableProject -\
                                 do you have Post permissions for this project?")
        return self.project.post(
            headline=headline,
            blocks=blocks,
            cws=cws,
            tags=tags,
            adult=adult,
            draft=draft,
            shareOfPostId=self.postId
            )

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
        return self.postData['transparentShareOfPostId']

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
        # NOTE: This is still untested as I'm still not sure how blocks work
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
