#!/usr/bin/env python3

import argparse
import os.path
import socket

import process_manager


def main():
  parser = argparse.ArgumentParser(description='Server for interacting with Vivado.')
  parser.add_argument('--exec_path', default='~/Xilinx/Vivado/2020.1/bin/vivado',
                      help='Path to Vivado executable.')
  parser.add_argument('--host', default='localhost',
                      help='A hostname to which to connect.')
  parser.add_argument('--port', type=int, default=9191, help='A port number for connection.')
  args = parser.parse_args()

  vivado_args = [
      os.path.expanduser(args.exec_path),
      '-mode',
      'tcl',
      '-nolog',
      '-nojournal'
  ]

  monitor = process_manager.ProcessMonitor(vivado_args, True, True, True)
  server = process_manager.ProcessServer(monitor, args.host, args.port)
  server.serve_forever()


if __name__ == '__main__':
  main()
