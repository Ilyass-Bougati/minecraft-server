import http.server, json, urllib.request

class H(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        addr = "tunnel starting…"
        try:
            with urllib.request.urlopen("http://127.0.0.1:4040/api/tunnels", timeout=2) as r:
                tcp = [t for t in json.load(r).get("tunnels", []) if t.get("proto") == "tcp"]
                if tcp:
                    addr = tcp[0]["public_url"].replace("tcp://", "")
        except Exception as e:
            addr = f"not up yet ({e})"
        body = f"<pre>Minecraft Fabric on HF Spaces\nConnect: {addr}\n(offline mode)</pre>".encode()
        self.send_response(200); self.send_header("Content-Type","text/html"); self.end_headers()
        self.wfile.write(body)
    def log_message(self, *a): pass

http.server.HTTPServer(("0.0.0.0", 7860), H).serve_forever()
