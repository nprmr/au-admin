import http.server
import socketserver
import json
import urllib.parse
from datetime import datetime

PORT = 8000

# Simple in-memory task storage
# Each task is a dictionary with keys: title, user, time, place
TASKS = {
    "buy": [
        {
            "title": "Пример задачи",
            "user": "Иван Иванов",
            "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "place": ""
        }
    ],
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
            task_data = params.get('task', [''])[0]
            from_col = params.get('from', [''])[0]
            to_col = params.get('to', [''])[0]
            if task_data and from_col in TASKS and to_col in TASKS:
                try:
                    task = json.loads(task_data)
                except json.JSONDecodeError:
                    self.send_response(400)
                    self.end_headers()
                    return
                if task in TASKS[from_col]:
                    TASKS[from_col].remove(task)
                TASKS[to_col].append(task)
            self.send_response(204)
        elif self.path == '/add':
            title = params.get('title', [''])[0]
            user = params.get('user', [''])[0]
            place = params.get('place', [''])[0]
            column = params.get('column', ['buy'])[0]
            if title and user and column in TASKS:
                TASKS[column].append({
                    'title': title,
                    'user': user,
                    'place': place,
                    'time': datetime.now().strftime('%Y-%m-%d %H:%M')
                })
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
