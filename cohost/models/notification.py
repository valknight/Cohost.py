class BaseNotification:
    def __init__(self, createdAt, fromProject):
        self.createdAt = createdAt
        self.fromProject = fromProject

    @property
    def timestamp(self):
        return self.createdAt

class Like(BaseNotification):
    def __init__(self, createdAt, fromProject, toPost, relationshipId):
        super().__init__(createdAt, fromProject)
        self.toPost = toPost
        self.relationshipId = relationshipId
    
    def __str__(self) -> str:
        return "{} liked {} | {}".format(self.fromProject.handle, self.toPost.postId, self.timestamp)


class Share(BaseNotification):
    def __init__(self, createdAt, fromProject, toPost, sharePost, transparentShare):
        super().__init__(createdAt, fromProject)
        self.toPost = toPost
        self.sharePost = sharePost
        self.transparentShare = transparentShare
    
    def __str__(self) -> str:
        if self.transparentShare:
            return "{} shared {} with extra | {}".format(self.fromProject.handle, self.toPost.postId, self.timestamp)
        return "{} shared {} | {}".format(self.fromProject.handle, self.toPost.postId, self.timestamp)


class Comment(BaseNotification):
    def __init__(self, createdAt, fromProject, toPost, comment, inReplyTo):
        super().__init__(createdAt, fromProject)
        self.toPost = toPost
        self.comment = comment
        self.inReplyTo = inReplyTo

    def __str__(self) -> str:
        return "{} commented on {} - \"{}\" | {}".format(self.fromProject.handle, self.toPost.postId, self.comment.body, self.timestamp)

class Follow(BaseNotification):
    def __init__(self, createdAt, fromProject):
        super().__init__(createdAt, fromProject)
    
    def __str__(self) -> str:
        return "{} is now following you | {}".format(self.fromProject.handle, self.timestamp)


def buildFromNotifList(notificationsApiResp: dict, user):
    from cohost.models.user import User
    from cohost.models.post import Post
    from cohost.models.comment import Comment as CommentModel
    u = user  # type: User
    user = u  # this whole shitshow is to get intellisense working without circular imports
    # I Love Python
    # We need the user to do API operations upon - it helps us resolve things like projects!
    commentsRaw = notificationsApiResp.get('comments')
    postsRaw = notificationsApiResp.get('posts')
    projectsRaw = notificationsApiResp.get('projects')
    notificationsRaw = notificationsApiResp.get('notifications')
    # Ok, so, now we HAVE all of this, we can build the notifications
    # First step: projects
    projects = []
    for p in projectsRaw:
        projects.append(user.resolveSecondaryProject(projectsRaw[p]))
    # OK, now we have projects, we can build the posts
    posts = []
    for p in postsRaw:
        # first, let's find the project
        p = postsRaw[p]
        found = False
        for project in projects:
            if project.projectId == p['postingProject']['projectId']:
                found = True
                break
        if not found:
            project = user.resolveSecondaryProject(p['postingProject'])
        posts.append(Post(p, project))
    # OK, now we have posts, we can build the comments
    commentQueue = []
    for c in commentsRaw:
        commentQueue.append(commentsRaw[c])
    comments = []
    while len(commentQueue) > 0:
        nextNotif = commentQueue.pop(0)
        replyComment = None
        if nextNotif['comment']['inReplyTo']:
            found = False
            for n in comments:
                if n.id == nextNotif['comment']['inReplyTo']:
                    found = True
                    replyComment = n
                    break
            # we still have other notifications to be processed
            if not found and len(commentQueue) > 0:
                commentQueue.append(nextNotif)
                continue
        # Ok, sick, so, we either don't have a reply, or we do but it's already processed!
        # we need pull the Project for this comment
        posterProject = None
        for project in projects:
            if project.projectId == nextNotif['poster']['projectId']:
                posterProject = project
        c = CommentModel(nextNotif['canEdit'], nextNotif['canInteract'],
                         nextNotif, posterProject, user, replyComment)
        comments.append(c)
    # and NOW we can finally map our notifications to all of our data models
    # TODO: Build notification model
    notifications = []
    for notification in notificationsRaw:
        # first, let's resolve all the data back
        fromProject = None
        toPost = None
        sharePost = None
        comment = None
        inReplyTo = None
        if notification.get('fromProjectId'):
            for project in projects:
                if project.projectId == notification['fromProjectId']:
                    fromProject = project
                    break
        if notification.get('toPostId'):
            for post in posts:
                if post.postId == notification['toPostId']:
                    toPost = post
                    break
        if notification.get('sharePostId'):
            for post in posts:
                if post.postId == notification['sharePostId']:
                    sharePost = post
                    break
        if notification.get('commentId'):
            for c in comments:
                if c.id == notification['commentId']:
                    comment = c
                    break
        if notification.get('inReplyToId'):
            for c in comments:
                if c.id == notification['inReplyToId']:
                    inReplyTo = c
                    break
        # sick, we can now handle whichever type of notification this is
        if notification['type'] == 'like':
            notifications.append(Like(
                notification['createdAt'], fromProject, toPost, notification['relationshipId']))
        if notification['type'] == "share":
            notifications.append(Share(
                notification['createdAt'], fromProject, toPost, sharePost, notification['transparentShare']))
        if notification['type'] == "comment":
            notifications.append(
                Comment(notification['createdAt'], fromProject, toPost, comment, inReplyTo))
        if notification['type'] == 'follow':
            notifications.append(Follow(notification['createdAt'], fromProject))
    return notifications
