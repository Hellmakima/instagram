print("localhost:8080/login.html")
print("to run with cmd: python -m http.server 8080")
# python -m http.server 8080
import http.server
import socketserver

PORT = 8080

Handler = http.server.SimpleHTTPRequestHandler

try:
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving at port {PORT}")
        httpd.serve_forever()
except KeyboardInterrupt:
    print("\nServer stopped gracefully.")
    httpd.server_close()  # Close the server properly
