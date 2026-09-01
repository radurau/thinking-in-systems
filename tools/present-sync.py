#!/usr/bin/env python3
"""Presenter sync server — deck on the laptop, live notes on a tablet.

Serves the repo over HTTP *and* relays slide changes, stdlib only:

    python3 tools/present-sync.py           # port 8765
    python3 tools/present-sync.py 9000      # custom port

Then:
  laptop:  http://localhost:8765/presentation.html
  tablet:  http://<laptop-ip>:8765/thinking-in-systems-notes.html
           (the script prints the laptop's LAN IP at startup)

The deck POSTs /sync/set on every slide change (it probes /sync/state at load,
so the same file works untouched on GitHub Pages or file://). The notes page
subscribes to /sync/events (SSE) and follows — same behaviour as the
BroadcastChannel sync, but across devices.

Venue Wi-Fi often isolates clients; safest is a phone hotspot or the laptop's
own hotspot, with the tablet joined to it.
"""
import http.server, json, queue, socket, socketserver, sys, threading, pathlib, functools

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
ROOT = pathlib.Path(__file__).resolve().parent.parent

state = {'slide': 1, 'seq': 0}
clients = []          # list[queue.Queue]
lock = threading.Lock()

class Handler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass

    def _cors(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-store')

    def do_GET(self):
        if self.path.split('?')[0] == '/sync/state':
            body = json.dumps(state).encode()
            self.send_response(200)
            self._cors()
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        if self.path.split('?')[0] == '/sync/events':
            self.send_response(200)
            self._cors()
            self.send_header('Content-Type', 'text/event-stream')
            self.send_header('Connection', 'keep-alive')
            self.end_headers()
            q = queue.Queue()
            with lock:
                clients.append(q)
            try:
                self.wfile.write(f'data: {json.dumps(state)}\n\n'.encode())
                self.wfile.flush()
                while True:
                    try:
                        msg = q.get(timeout=20)
                        self.wfile.write(f'data: {msg}\n\n'.encode())
                    except queue.Empty:
                        self.wfile.write(b': keepalive\n\n')
                    self.wfile.flush()
            except (BrokenPipeError, ConnectionResetError, OSError):
                pass
            finally:
                with lock:
                    if q in clients:
                        clients.remove(q)
            return
        super().do_GET()

    def do_POST(self):
        if self.path.split('?')[0] == '/sync/set':
            n = int(self.headers.get('Content-Length') or 0)
            try:
                data = json.loads(self.rfile.read(n) or b'{}')
                slide = int(data.get('slide'))
            except Exception:
                self.send_response(400); self._cors(); self.end_headers(); return
            with lock:
                state['slide'] = slide
                state['seq'] += 1
                msg = json.dumps(state)
                for q in clients:
                    q.put(msg)
            self.send_response(204); self._cors(); self.end_headers()
            return
        self.send_response(404); self.end_headers()

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

def lan_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return '<laptop-ip>'

class Server(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True

if __name__ == '__main__':
    handler = functools.partial(Handler, directory=str(ROOT))
    ip = lan_ip()
    print(f'presenter sync running:')
    print(f'  laptop deck : http://localhost:{PORT}/presentation.html')
    print(f'  tablet notes: http://{ip}:{PORT}/thinking-in-systems-notes.html')
    print(f'  (tablet must be on the same network — a phone/laptop hotspot is safest)')
    Server(('0.0.0.0', PORT), handler).serve_forever()
