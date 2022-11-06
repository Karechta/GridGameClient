from client import Client
from pwn import context
context.log_level = 'debug'

if __name__ == '__main__':
    client = Client("localhost", 8888, "Karechta")
    client.Run()
    