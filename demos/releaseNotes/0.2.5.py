import os
from cohost.models.user import User
from cohost.models.block import AttachmentBlock, MarkdownBlock

def generateWarningNote(message: str, title = "Heads up! :host-shock:"):
    # stolen from https://cohost.org/aristurtle/post/176671-admonitions-on-cohos
    return """<div style="background-color: rgb(255, 255, 255); border: 0.05rem solid #DBAF24; border-radius: 0.2rem; box-shadow: rgba(0, 0, 0, 0.05) 0px 4.4px 11px 0px, rgba(0, 0, 0, 0.1) 0px 0px 1.1px 0px; color: rgba(0, 0, 0, 0.87); margin: 1.5em 0; padding: 0 0.6rem; line-height: 1.6;">
  <p style="background-color: rgba(219, 175, 36, 0.1); padding-left: 2rem; padding-right: 0.6rem; border: none; font-weight: 700; margin: 0 -0.6rem; padding-bottom: 0.4rem; padding-top: 0.4rem; position: relative; box-sizing: border-box; line-height: 1.6;">
    <span style="position: absolute; left: 0.6rem">⚠️</span>&nbsp;{}
  </p>
  <p style="margin-bottom: 0.6rem; box-sizing: border-box; color: rgba(0, 0, 0, 0.87); line-height: 1.6">
    {}
  </p>
</div>""".format(title, message)

def generateDangerNote(message: str, title = "Danger!"):
    # stolen from https://cohost.org/aristurtle/post/176671-admonitions-on-cohos
    return """<div style="background-color: rgb(255, 255, 255); border: 0.05rem solid #A00D24; border-radius: 0.2rem; box-shadow: rgba(0, 0, 0, 0.05) 0px 4.4px 11px 0px, rgba(0, 0, 0, 0.1) 0px 0px 1.1px 0px; color: rgba(0, 0, 0, 0.87); margin: 1.5em 0; padding: 0 0.6rem; line-height: 1.6;">
  <p style="background-color: rgba(210, 28, 57, 0.1); padding-left: 2rem; padding-right: 0.6rem; border: none; font-weight: 700; margin: 0 -0.6rem; padding-bottom: 0.4rem; padding-top: 0.4rem; position: relative; box-sizing: border-box; line-height: 1.6;">
    <span style="position: absolute; left: 0.6rem">🔺</span>&nbsp;{}
  </p>
  <p style="margin-bottom: 0.6rem; box-sizing: border-box; color: rgba(0, 0, 0, 0.87); line-height: 1.6">
    {}
  </p>
</div>""".format(title, message)

def main():
    username = os.environ.get('cohostUser')
    password = os.environ.get('cohostPass')
    handle = os.environ.get('cohostHandle')
    if username is None:
        username = input('username: ')
    if password is None:
        password = input('password: ')
    if handle is None:
        handle = input('handle: ')
    blocks = [
      MarkdownBlock('<div style="position: relative; top: 3px; display: inline-block; animation: 1s ease-in-out 0s infinite normal none running bounce;">cohost.py 0.2.5 is out!!</div>'),
        MarkdownBlock('we have: one (1) bug fix, and one (1) new feature - both related to Notifications!'),
        MarkdownBlock('Bug fix: notifications now silently unwrap! Cohost\'s notification grouping broke most of our notification code, so we now transparently unwrap them!'),
        MarkdownBlock('Feature: you can now switch your active project, by calling `.switch` on a project. This will mean things like notifications will be based on that project'),
        MarkdownBlock('More work needs to be done for notifications, but, these two issues were fairly big.'),
        MarkdownBlock('Many thanks to <a href="https://cohost.org/aurysystem">@AurySystem</a> for the bug report here!'),
        MarkdownBlock('as always you can install cohost.py with `pip install cohost` - enjoy chosting!'),
        MarkdownBlock(generateWarningNote("Cohost.py is still experimental, etc etc etc... you get the picture. Please submit bugs, feature requests and PRs to the <a href=\"https://github.com/valknight/cohost.py\">GitHub repo</a>!")),
        MarkdownBlock(generateDangerNote('If you\'re making a bot, please honor <a href="https://cohost.org/jkap/post/201002-small-request-that-i">@jkap\'s little notes on bots</a>! And, as always, don\'t make this site awful :)')),
        MarkdownBlock('<hr>'),
        MarkdownBlock('check out <a href="https://github.com/valknight/Cohost.py/blob/main/demos/releaseNotes/0.2.5.py">the source for this post</a>'),
        MarkdownBlock("<hr>"),
        MarkdownBlock('<small><i>ps: feature requests, bug reports and PRs? super welcome. <a href="https://github.com/valknight/Cohost.py">check out our github.</a> pybug is waiting.</small>')
    ]
    # woah !!! logging in !!! that's so cool !!!
    user = User.login(username, password)
    project = user.getProject(handle)
    newPost = project.post('little updates to cohost.py :D', blocks, tags=['cohost.py', 'python', 'development', 'cohost api'], draft=False)
    print('Check out your post at {}'.format(newPost.url))

if __name__ == '__main__':
    main()