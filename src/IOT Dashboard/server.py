from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class SimpleAuthHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        # هذه الإعدادات ضرورية للسماح للمتصفح بالاتصال (CORS)
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        # التأكد أن الطلب رايح للمسار /verify
        if self.path == '/verify':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)
            
            password_attempt = data.get("password")
            print(f"[*] Testing password: {password_attempt}")

            # الرد بالنجاح لو الباسوورد صح
            if password_attempt == "HosIoT25":
                self.send_response(200)
                response = {"success": True}
            else:
                self.send_response(401)
                response = {"success": False}

            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
        else:
            # لو المسار غلط هيدي 404
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")

print("Server starting on http://0.0.0.0:3000...")
HTTPServer(('0.0.0.0', 3000), SimpleAuthHandler).serve_forever()