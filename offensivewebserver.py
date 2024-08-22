#!/usr/bin/env python3
#
# Adapted from https://f95zone.to/threads/small-python-script-to-run-local-case-insensitive-web-server.189695/
# by Diego (joaninhaDark) - www.offensivethink.com - 07.2024

# UPLOAD LINUX:
# METHOD PUT : curl -T <FILE_TO_UPLOAD> http://<SERVER_IP>:<PORT>/<FILENAME_AT_DESTINATION>
# METHOD POST: curl -X POST -H "File-Name: <FILENAME_AT_DESTINATION>" --data-binary @<FILE_TO_UPLOAD> http://<SERVER_IP>:<PORT>
#
# UPLOAD WINDOWS (powershell):
# METHOD PUT : Invoke-RestMethod -Uri http://<SERVER_IP>:<PORT>/<FILENAME_AT_DESTINATION> -Method Put -InFile "<FILE_TO_UPLOAD>"
# METHOD POST: Invoke-RestMethod -Uri http://<SERVER_IP>:<PORT> -Method Post -Headers @{ "File-Name" = "<FILENAME_AT_DESTINATION>" } -InFile "<FILE_TO_UPLOAD>"
#
# DOWNLOAD LINUX:
#
# 
# DOWNLOAD WINDOWS:
# Invoke-WebRequest -Uri "http://<SERVER_IP>:<PORT>/<FILENAME>" -OutFile "<FILENAME_AT_DESTINATION>"
# Invoke-RestMethod -Uri "http://<SERVER_IP>:<PORT>/<FILENAME>" -OutFile "<FILENAME_AT_DESTINATION>"

#
#

from http.server import HTTPServer, SimpleHTTPRequestHandler, test
import os.path
import os
import argparse

class NoMatch(Exception):
    pass


def find_match(folder: str, part: str):
    if os.path.exists(os.path.join(folder, part)):
        return part

    needle = part.lower()
    print(f"Looking for {needle} in {folder}")
    candidates = [f for f in os.listdir(folder) if f.lower() == needle]   

    if len(candidates) > 1:
        print(f"{folder}/{part}: multiple candidates {candidates}")
        raise NoMatch()
    elif len(candidates) == 0:
        print(f"{folder}/{part}: no candidates {candidates}")
        raise NoMatch()
    else:
        print(f"{folder}/{part}: Found {candidates[0]}")
        return candidates[0]


class CaseInsensitiveRequestHandler(SimpleHTTPRequestHandler):

    def do_POST(self):
        length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(length)
        filename = self.headers.get('File-Name', 'uploaded_file')
        filename = filename.lower()  # Garantir que o nome do arquivo seja case-insensitive

        with open(filename, 'wb') as f:
            f.write(post_data)

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'File uploaded successfully')

    def do_PUT(self):
        length = int(self.headers['Content-Length'])
        put_data = self.rfile.read(length)
        filename = self.path[1:]  # Remove the leading slash
        filename = filename.lower()  # Garantir que o nome do arquivo seja case-insensitive

        with open(filename, 'wb') as f:
            f.write(put_data)

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'File uploaded successfully')


    def translate_path(self, path):
        safe = super().translate_path(path)
        if os.path.exists(safe):
            return safe
        
        #print(f"Cannot find {safe}")

        rel = os.path.relpath(safe, self.directory)
        parts = rel.split(os.path.sep)

        #print(f"Looking for {rel}, as parts {parts}")


        builder = self.directory
        try:
            for part in parts:
                match = find_match(builder, part)
                builder = os.path.join(builder, match)
            #print(f"Build result: {builder}")
            return builder
        except NoMatch:
            return safe


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Run a simple HTTP server.')
    parser.add_argument('--port', type=int, default=443, help='Port to listen on')
    args = parser.parse_args()

    PORT = args.port

    with HTTPServer(("", PORT), CaseInsensitiveRequestHandler) as httpd:
        print(f"Serving at http://localhost:{PORT}/")
        httpd.serve_forever()
