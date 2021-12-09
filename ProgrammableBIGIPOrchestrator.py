from http.server import HTTPServer, BaseHTTPRequestHandler

from io import BytesIO

from as3utils import *

class ProgrammableBIGIPOrchestrator(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)

        self.end_headers()

        self.wfile.write(b'Hello, world!')

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.send_response(200)
        self.end_headers()
        response = BytesIO()
        response.write(body)
        try:
            # self.wfile.write(response.getvalue())
            print("Received request")
            request = json.loads(body)
            # Parsing the request
            parsed_data = parse_request(request)
            for bigip in parsed_data['list_of_bigips']:
                process_request(bigip, parsed_data)
        except:
            print(f"Error occured in processing this request: {request}")

httpd = HTTPServer(('localhost', 8000), ProgrammableBIGIPOrchestrator)

httpd.serve_forever()