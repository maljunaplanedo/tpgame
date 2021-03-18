import socket


class Network:
    def __init__(self):
        self.subscribers = {}
        self.socket = socket.socket()
        self.receiving_message = b''
        self.target_ip = ''
        self.target_port = 0
        self.is_host = False

    def open_network_info_screen(self):
        pass

    def cause_event(self, type_, **kwargs):
        pass

    def connect(self):
        if self.is_host:
            self.socket.bind(('', self.target_port))
            self.socket.listen(1)
            self.socket.setblocking(False)
            self.socket, address = self.socket.accept()
        else:
            self.socket.setblocking(False)
            self.socket.connect((self.target_ip, self.target_port))




    def check_file_data(self):
        try:
            with open('netconfig.txt', 'r') as f:
                file = f.read()
                file.strip()

                self.target_ip, self.target_port = file.split()
                self.target_port = int(self.target_port)

                if self.target_ip == 'host':
                    self.is_host = True

            self.connect()

        except FileNotFoundError:
            self.open_network_info_screen()
        except ValueError:
            exit(0)


