#!/usr/bin/env python3

import argparse
import os.path
import socket


def client():
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(('localhost', 9191))
    s.sendall(b'help\r')
    print(s.recv(1024))


def main():
  parser = argparse.ArgumentParser(description='Client for interacting with Vivado.')
  parser.add_argument('--host', default='localhost',
                      help='A hostname to which to connect.')
  parser.add_argument('--port', type=int, default=9191, help='A port number for connection.')
  args = parser.parse_args()


if __name__ == '__main__':
  main()
