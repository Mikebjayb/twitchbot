from sock import Sock
from nonblockconsole import NonBlockConsole
import logging

#example:
# ~$ python ircclient.py
# $send password
# $send username
# $enable membership
# $join:mibaz
# $msg: kappa kappa kappa
# $quit
# ~$

class IrcClient:

    sock = None
    console = NonBlockConsole()
    host = ''
    port = -1
    username = ''
    password = ''
    channel = ''

#

    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.sock = Sock(host = host, port = port)

    def get_response(self):
        return self.sock.receive()

    def join_chann(self, chan):
        if self.channel != '':
            self.leave_chann();
        self.sock.deliver("JOIN #{1}\r\n".format(self.username, chan))
        self.channel = chan

    def privmsg(self, msg):
        self.sock.deliver('PRIVMSG #{} :{}\r\n'.format(self.channel, msg))

    def take_input(self):
        values = self.console.get_commands()
        for key in values:
            if key == "quit":
                return 1
            if key == "send password":
                self.send_password()
            if key == "send username":
                self.send_username()
            if key == "send":
                self.sock.deliver(values[key][0])
            if key == "msg":
                self.privmsg(values[key][0])
            if key == "join":
                self.join_chann(values[key][0])
            if key == "pong":
                self.send_pong(values[key][0])
            if key == "enable membership":
                self.enable_membership()

    def shutdown(self):
        self.leave_chann()
        self.sock.end_con()

#

    def send_pong(self, msg):
        self.sock.deliver('PONG :{}\r\n'.format(msg))

    def send_username(self):
        self.sock.deliver('NICK {}\r\n'.format(self.username))

    def send_password(self):
        self.sock.deliver('PASS {}\r\n'.format(self.password))

    def enable_membership(self):
        self.sock.deliver('CAP REQ :twitch.tv/membership\r\n')

    def leave_chann(self):
        self.sock.deliver('PART #{}\r\n'.format(self.channel))


#

logging.basicConfig(level = logging.DEBUG, format='[%(levelname)s] (%(threadName)-10s) %(message)s')
logging.info("\n" * 5)

bot = IrcClient(  'irc.twitch.tv'
                ,  6667
                , 'mibaz'
                , 'oauth:yj3************************7k7t'
                )

run = True
while run:

    bot.get_response() #printing done in sock.py
    if bot.take_input() == 1:
        run = False

bot.shutdown()
