from http.server import HTTPServer, BaseHTTPRequestHandler
from position_api import *
import logging
import json


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):

        path_parts = self.path.split('/')[1:]
        if path_parts[0] == "position" and len(path_parts) == 3:  # ['position', 'userX', 'assetX']
            # Return User's asset info on position
            self.send_response(200)
            self.send_header('content-type', 'text/html')
            self.end_headers()

            userID = path_parts[1]
            assetID = path_parts[2]
            position = get_position_from_storage(userID, assetID)
            if position:
                # print(f'{userID} may continue watching {assetID} from {position} seconds in.)'
                self.wfile.write(position.encode())
            else:
                msg = f'No stored position for Asset:{assetID} by User:{userID}'
                self.wfile.write(msg.encode())

        if path_parts[0] == "position" and len(path_parts) == 2:  # ['position', 'userX']
            # Return User's asset info on position
            self.send_response(200)
            self.send_header('content-type', 'text/html')
            self.end_headers()

            userID = path_parts[1]
            asset_list = generate_list(userID)
            pos_list = []
            for asset in asset_list:
                # print(f'{item[0]} can be resumed at {item[1]} seconds || DATE: {item[2]})'
                pos_list.append(asset[1])
            # Convert python list to JSON list
            pos_list_json = json.dumps(pos_list)
            self.wfile.write(pos_list_json.encode())


    def do_POST(self):

        path_parts = self.path.split('/')[1:]
        if path_parts[0] == "position" and len(path_parts) == 4:  # ['position', 'userX', 'assetX', 'XXX']
            userID = path_parts[1]
            assetID = path_parts[2]
            position = path_parts[3]

            resp = add_to_storage(userID, assetID, position)
            if not resp:
                self.send_response(404)
                self.send_header('content-type', 'text/html')
                self.end_headers()
                self.wfile.write("POST failure".encode())
            else:
                self.send_response(200)
                self.send_header('content-type', 'text/html')
                self.send_header('Location', f'/{path_parts[1]}/{path_parts[2]}')
                self.end_headers()
                self.wfile.write("POST successful".encode())

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
