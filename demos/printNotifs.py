import os
from cohost.models.user import User

def main():
    print('logging in... ')
    username = os.environ.get('cohostUser')
    password = os.environ.get('cohostPass')
    handle = os.environ.get('cohostHandle')
    if username is None:
        username = input('username: ')
    if password is None:
        password = input('password: ')
    if handle is None:
        handle = input('handle: ')
    user = User.login(username, password)
    
    print('done!', end='\n\n')
    # get last 10 notifications
    print('last 10 notifs: {}'.format(len(user.notifications)), end='\n\n')

    # example of custom pagination
    user.notificationsPagified(page = 2, notificationsPerPage=5)

    # Example of all notifications!
    print('retrieving all notifs... ')
    notifs = user.allNotifications
    print('you have recieved {} total lifetime notifs.'.format(len(notifs)))

if __name__ == '__main__':
    main()