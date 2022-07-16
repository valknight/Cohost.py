class Comment:
    def __init__(self, canEdit, canInteract, comment, user, poster, inReplyTo = None) -> None:
        self.id = comment['comment']['commentId']
        self.canEdit = canEdit
        self.canInteract = canInteract
        self.comment = comment['comment']
        self.poster = poster
        self.inReplyTo = inReplyTo
    
    @property
    def body(self):
        return self.comment['body']
