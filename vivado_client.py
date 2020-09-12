#!/usr/bin/env python3

import argparse
import os.path
import socket
import time


class VivadoClient:
  def __init__(self, host, port):
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.socket.settimeout(0.2)
    self.socket.connect((host, port))

  def close(self):
    self.socket.close()

  def find_prompt(self, timeout=1):
    self.socket.sendall(b'\r')

    b = bytearray()
    alarm = time.time() + timeout
    while time.time() < alarm:
      try:
        b += self.socket.recv(1024)
      except socket.timeout:
        pass
      if b.endswith(b'Vivado% '):
        return True

    return False


def main():
  parser = argparse.ArgumentParser(description='Client for interacting with Vivado.')
  parser.add_argument('--host', default='localhost',
                      help='A hostname to which to connect.')
  parser.add_argument('--port', type=int, default=9191, help='A port number for connection.')
  args = parser.parse_args()

  client = VivadoClient(args.host, args.port)
  while not client.find_prompt():
    pass
  client.close()


if __name__ == '__main__':
  main()
