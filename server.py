import http.server
import socketserver
import json
import urllib.parse

PORT = 8000

# Simple in-memory task storage
TASKS = {
    "buy": ["Пример задачи"],
    "port": [],
    "middle": [],
    "to-rf": [],
    "customs": [],
    "client": []
}

class KanbanHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/tasks':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(json.dumps(TASKS, ensure_ascii=False).encode('utf-8'))
        else:
            if self.path == '/' or self.path == '/index.html':
                self.path = '/kanban.html'
            return super().do_GET()

    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        data = self.rfile.read(length)
        params = urllib.parse.parse_qs(data.decode())
        if self.path == '/move':
            task = params.get('task', [''])[0]
            from_col = params.get('from', [''])[0]
            to_col = params.get('to', [''])[0]
            if task and from_col in TASKS and to_col in TASKS:
                if task in TASKS[from_col]:
                    TASKS[from_col].remove(task)
                TASKS[to_col].append(task)
            self.send_response(204)
        elif self.path == '/add':
            task = params.get('task', [''])[0]
            column = params.get('column', ['buy'])[0]
            if task and column in TASKS:
                TASKS[column].append(task)
                self.send_response(204)
            else:
                self.send_response(400)
        else:
            self.send_response(404)
        self.end_headers()

if __name__ == '__main__':
    with socketserver.TCPServer(('', PORT), KanbanHandler) as httpd:
        print(f'Serving on http://localhost:{PORT}')
        httpd.serve_forever()
