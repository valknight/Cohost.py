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
        MarkdownBlock('<div style="position: relative; top: 3px; display: inline-block; animation: 1s ease-in-out 0s infinite normal none running bounce;">cohost.py 0.2.1 is out!!</div>'),
        MarkdownBlock('''smaller release this time round, but, big news is we've now extended compatibility back to python 3.8 (and maybe older !!)'''),
        MarkdownBlock('''notifications also now suck less, with pagified notification support (and everything doesn't catch fire if you delete a post you got a comment on)'''),
        MarkdownBlock('''as always, install the library with `pip install cohost` - see below for code samples :)'''),
        MarkdownBlock(generateWarningNote("Cohost.py is still experimental, and uses the private Cohost API! Please submit bugs, but, no promises of stability.")),
        MarkdownBlock(generateDangerNote("If you're making a bot, please honor [@jkap's little notes on bots](https://cohost.org/jkap/post/201002-small-request-that-i)! And, as always, don't make this site awful :)")),
        MarkdownBlock('<hr>'),
        MarkdownBlock('<hr>as always, check out the <a href="https://github.com/valknight/Cohost.py/blob/main/demos/releaseNotes/0.2.1.py">script used to post this release note :)</a>')
    ]
    # woah !!! logging in !!! that's so cool !!!
    user = User.login(username, password)
    project = user.getProject(handle)
    newPost = project.post('new release of cohost.py for all your automated Chostin\'!',
      blocks, tags=['cohost.py', 'python', 'development', 'cohost api'], draft=False)
    print('Check out your post at {}'.format(newPost.url))

if __name__ == '__main__':
    main()