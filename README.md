# Cohost.py

![Edit of Eggbug into the python logo](pybug_small.png)


A python library for Cohost!

## Hyperstart

> `pip install cohost`

## Quickstart

> `pip install cohost`

```python3
from cohost.models.user import User
from cohost.models.block import AttachmentBlock, MarkdownBlock

cookie = 'yourCookie'
user = User.loginWithCookie(cookie)
for project in user.editedProjects:
    print(project) # Print all pages you have edit permissions for
project = user.getProject('vallerie') # will retrieve the page I have edit writes for with handle @vallerie
blocks = [
    AttachmentBlock('pybug.png'), # References image file pybug.png
    MarkdownBlock('**Hello from Python!**') # Example of markdown / text block
]
newPost = project.post('Title of python post!', blocks, tags=['cohost.py', 'python'])
print('Check out your post at {}'.format(newPost.url))
```
## Getting started

1. Have an activated Cohost.org account. This entire library will probably explode if you use it with an unactivated account, and it defo isn't some bypass.
2. Install library with `pip install cohost`
3. Retrieve your token (see below!)
4. Import data models you require, and go from there!

## Terminology

Some things are different on the API, and on the UI, and for the most part this library will match the API's terminology. Some key concepts:

- A user is minimal - it will contain authentication, email, and some other key details but not much else
- All the pages you can edit are referred to as "projects"
- Each post is made up content "Blocks"


## Tokens

To function, you need a token for Cohost. This can be retrieved by:
1. Open Developer Tools in your browser
2. Go to "Storage"
3. Find the "Cookies" entry
4. Copy the data for "`connect.sid`".
5. Use this in the library

## What's working? (allegedly)

- Logging in as a user (using a cookie)
- Retrieving projects of a user (and of other people when you got a post to go with it)
- Retrieving posts of a page
- Posting to a page (with image support!)
- Retrieving notifications
## What's not done but needs to be done?

- Logging in with a username and password - this is possible (Cohost.js does it!) so feel free to create a pull request for this :)
- Retrieving single posts - currently have to read entire projects
- Retrieving a project's drafts
- Retrieving a projects of others without a post inbetween
- Sharing posts (with comment)
- Editing profiles
- Deleting posts
- Editing posts
- Likely a whole bunch of other things I haven't thought about
- Better docs

## What's not implemented intentionally?

Some features I intend not to add. These features aren't impossible to build, but, they could be detrimental to the Cohost experience for other users, send mass notifications without an account being activated, or pose security issues. This is designed to deter low effort malicious bots, to reduce the workload on Cohost's staff

These include:
- Editing a user's password
- Accepting follow requests
- Sharing a post without a comment
- Creating new projects

If you implement these features, please keep them **private** for your projects.
If you think one of these should be implemented, please file a GitHub issue with your case as to why.

## Support Cohost

[Buy Cohost PLUS](https://cohost.org/rc/user/settings)

## Follow me on Cohost!

[hello is me](https://cohost.org/vallerie)

## Thanks

- [cohost.js](https://github.com/mogery/cohost.js/) - provided a good point to start looking at how to go about this, and how cohost works in fundamental aspects. also has a working login thing which i need to properly understand at some point
- [cohost.org](https://cohost.org) - home of eggbug
- [requests](https://requests.readthedocs.io/en/latest/) - i would be lost in python if it weren't for requests, my beloved
- the random tumblr anon who sent me an activation link - thanks