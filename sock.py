import threading
import socket
import time
import nonblockconsole
import logging

#Just a little multithreaded wrapper class to make socket nonblocking

class Sock(socket.socket):

    def __init__(self, host = None, port = None, encoding = 'UTF-8'):
        socket.socket.__init__(self, socket.AF_INET, socket.SOCK_STREAM)

        self.threads = []
        self.con = None
        self.data_send = ''
        self.data_receive = ''
        self.encoding = encoding
        self.running = True

        if host == None and socket != None:
            host = socket.gethostname()
            self.bind((host, port))
            self.listen(5)

            t1 = threading.Thread(target = self.send_data)
            self.threads.append(t1)
            t2 = threading.Thread(target = self.receive_data)
            self.threads.append(t2)
            t3 = threading.Thread(target = self.accept_con)
            self.threads.append(t3)

            for t in self.threads:
                t.start()

        elif host != None and port != None:
            self.connect((host, port))
            self.con = self

            t1 = threading.Thread(target = self.send_data)
            self.threads.append(t1)
            t2 = threading.Thread(target = self.receive_data)
            self.threads.append(t2)

            for t in self.threads:
                t.start()

        else:
            logging.error("Socket not created with proper arguments")
            raise error

    def deliver(self, msg):
        self.data_send += msg

    def receive(self):
        if self.data_receive:
            a = self.data_receive
            self.data_receive = ''
            return a

    def end_con(self):
        if self.con != self and self.con != None:
            self.con.shutdown(1)
            self.con.close()
        self.shutdown(1)
        self.close()
        self.running = False
        for t in self.threads:
            t.join()
        logging.info("socket closed")

#

    def send_data(self):
        while self.running:
            if self.data_send != '':
                logging.info("<--| " + self.data_send)
                self.con.sendall(bytes(self.data_send, self.encoding))
                self.data_send = ''
            time.sleep(.1)

    def receive_data(self):
        while self.running:
            if self.con:
                d = self.con.recv(1024).decode(self.encoding)
                self.data_receive += d
                if d == '':
                    logging.info("connection aborted")
                    self.con = None
                else:
                    logging.info("-->| " + d)

    def accept_con(self):
        while self.running:
            if self.con == None:
                self.con, addr = self.accept()
                logging.info("accepted connection")
