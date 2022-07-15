from cohost.models.user import User
from cohost.models.post import Post
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
    print("Established connection as: {}".format(user))
    #print(user.editedProjects)
    print('Default project: {}'.format(user.defaultProject))
    posts = user.defaultProject.getPosts()
    for p in posts:
        p = p # type: Post
        print(p, end = ' | ')
        if type(p.ogAuthor) == EditableProject:
            print(' OG author: you! |', end = ' ')
        else:
            print('OG author: {} |'.format(p.ogAuthor), end=' ')
        if len(p.relatedProjects) > 0:
            print("Related projects:", end= " ")
            names = []
            for r in p.relatedProjects:
                if type(r) == EditableProject:
                    names.append('@{}(you!)'.format(r.handle))
                else:
                    names.append('@{}'.format(r.handle))
            print(', '.join(names), end = ' | ')
        print("")
    print('[DONE - {} POSTS]'.format(len(posts)))
    print('Getting posts from someone who isn\'t you... (using last project on list)')
    project = posts[-1].ogAuthor
    print('Project: @{}'.format(project.handle))
    print('{} posts retrieved!'.format(len(project.getPosts())))

if __name__ == '__main__':
    main()