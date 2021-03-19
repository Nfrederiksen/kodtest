from http.server import HTTPServer, BaseHTTPRequestHandler
from position_api import *
import logging
import json
import re


class RequestHandler(BaseHTTPRequestHandler):
    POST_POS_PATTERN = re.compile(r'^/position/\w+/\w+/\d+$')
    GET_POS_PATTERN = re.compile(r'^/position/\w+/\w+$')
    GET_ALL_POS_PATTERN = re.compile(r'^/position/\w+$')

    def do_GET(self):

        if re.search(self.GET_POS_PATTERN, self.path):
            path_parts = list(filter(None, self.path.split('/')))  # ['position', 'userX', 'assetX']
            userID = path_parts[1]
            assetID = path_parts[2]
            position = get_position_from_storage(userID, assetID)
            if position:
                # Return User's asset info on position
                self.send_response(200)
                self.send_header('content-type', 'text/html')
                self.end_headers()
                return self.wfile.write(position.encode())
            # Return User's asset info on position
            self.send_response(404)
            self.send_header('content-type', 'text/html')
            self.end_headers()
            msg = f'No stored position for Asset->{assetID} by User->{userID}'
            return self.wfile.write(msg.encode())

        if re.search(self.GET_ALL_POS_PATTERN, self.path):
            # Return User's asset info on position
            self.send_response(200)
            self.send_header('content-type', 'text/html')
            self.end_headers()

            path_parts = list(filter(None, self.path.split('/')))  # ['position', 'userX']
            userID = path_parts[1]
            asset_list = generate_list(userID)
            pos_list = []
            for asset in asset_list:
                # print(f'{item[0]} can be resumed at {item[1]} seconds || DATE: {item[2]})'
                pos_list.append(asset[1])
            # Convert python list to JSON list
            pos_list_json = json.dumps(pos_list)
            return self.wfile.write(pos_list_json.encode())

        self.send_response(404)
        # Add response headers.
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        # Add response content.
        self.wfile.write('Sorry! Wrong path format.'.encode('utf-8'))

    def do_POST(self):

        if re.search(self.POST_POS_PATTERN, self.path):
            path_parts = list(filter(None, self.path.split('/')))  # ['position', 'userX', 'assetX', 'XXX']
            userID = path_parts[1]
            assetID = path_parts[2]
            position = path_parts[3]

            resp = add_to_storage(userID, assetID, position)
            if not resp:
                self.send_response(404)
                self.send_header('content-type', 'text/html')
                self.end_headers()
                return self.wfile.write("POST failure".encode())

            self.send_response(200)
            self.send_header('content-type', 'text/html')
            self.end_headers()
            return self.wfile.write("POST successful".encode())

        self.send_response(404)
        self.send_header('content-type', 'text/html')
        self.end_headers()
        self.wfile.write("POST failure".encode())


# DRIVER FUNCTION
def main():
    PORT = 3000
    HOST = '127.0.0.1'
    server = HTTPServer((HOST, PORT), RequestHandler)
    print(f'My server is running at localhost, port {PORT}')
    logging.info(f'Server listening at port {PORT} \n')
    server.serve_forever()


if __name__ == '__main__':
    main()
