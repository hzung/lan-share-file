import sys
import os.path
from http.server import BaseHTTPRequestHandler, HTTPServer
import socket
from contextlib import closing
import json
from urllib.request import pathname2url
import mimetypes

if len(sys.argv) <= 1:
    print("Usage: python3 share.py <file_path>")
    sys.exit()

file_path = sys.argv[1]
file_name = file_path.split('/')[-1]
if not os.path.isfile(file_path):
    print (f"File [{file_path}] does not exist")
    sys.exit()


def get_mime_type(path):
    mine_type, _ = mimetypes.guess_type(pathname2url(file_path))
    return mine_type


def find_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', get_mime_type(file_path))
        self.send_header('Content-Disposition', f'attachment; filename="{file_name}"')
        self.end_headers()

        with open(file_path, 'rb') as file: 
            self.wfile.write(file.read())

port = find_free_port()
ip = get_ip()
myServer = HTTPServer((ip, port), MyServer)
print(f"Download link: http://{ip}:{port}")
myServer.serve_forever()