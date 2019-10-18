from socketIO_client import SocketIO, LoggingNamespace
import time
sock = SocketIO('http://localhost', 9000, LoggingNamespace)


def insert_event(message):
    print(f"Record is inserted to {message['database']}, at time {message['date']}")


sock.on('insert', insert_event)

if __name__ == '__main__':
    sock.wait()
