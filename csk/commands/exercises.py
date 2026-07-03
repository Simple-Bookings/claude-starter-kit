"""csk exercises — Start exercise server and track progress."""

import http.server
import socketserver
import threading
import webbrowser
from pathlib import Path

import click
from rich.console import Console

from csk.commands.progress import load_progress, save_progress, EXERCISES

console = Console()

from csk.resources import exercises_dir

EXERCISES_DIR = exercises_dir() or Path(__file__).parent.parent.parent / "exercises"


def generate_html(progress: dict) -> str:
    """Generate the exercises HTML page."""
    exercises_html = ""
    for ex in EXERCISES:
        status = progress.get(ex["id"], "not_started")
        status_icon = {
            "not_started": "○",
            "in_progress": "◐",
            "completed": "✓",
        }.get(status, "○")
        status_class = status.replace("_", "-")

        # Determine button text based on status
        if status == "completed":
            btn_text = "✓ Completed"
            btn_class = "btn-completed"
            next_status = "not_started"
        elif status == "in_progress":
            btn_text = "Mark Complete"
            btn_class = "btn-progress"
            next_status = "completed"
        else:
            btn_text = "Start Exercise"
            btn_class = "btn-start"
            next_status = "in_progress"

        exercises_html += f'''
        <div class="exercise {status_class}">
            <div class="exercise-header">
                <span class="exercise-number">{ex["id"]}</span>
                <span class="exercise-status">{status_icon}</span>
            </div>
            <h3>{ex["title"]}</h3>
            <p class="learning-goal">{ex["goal"]}</p>
            <div class="skills">
                {"".join(f'<span class="skill">{s}</span>' for s in ex["skills"])}
            </div>
            <button class="btn {btn_class}" onclick="updateStatus('{ex["id"]}', '{next_status}')">{btn_text}</button>
        </div>
        '''

    completed = sum(1 for s in progress.values() if s == "completed")
    total = len(EXERCISES)
    pct = int((completed / total) * 100) if total > 0 else 0

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CSK — Exercises</title>
    <style>
        :root {{
            --bg: #0f172a;
            --surface: #1e293b;
            --border: #334155;
            --text: #e2e8f0;
            --muted: #94a3b8;
            --accent: #06b6d4;
            --green: #10b981;
            --yellow: #f59e0b;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif;
            background: var(--bg);
            color: var(--text);
            min-height: 100vh;
            padding: 2rem;
        }}
        .container {{ max-width: 1000px; margin: 0 auto; }}
        h1 {{ color: var(--accent); margin-bottom: 0.5rem; }}
        .subtitle {{ color: var(--muted); margin-bottom: 2rem; }}
        .progress-bar {{
            background: var(--surface);
            border-radius: 8px;
            height: 24px;
            margin-bottom: 2rem;
            overflow: hidden;
        }}
        .progress-fill {{
            background: linear-gradient(90deg, var(--accent), var(--green));
            height: 100%;
            width: {pct}%;
            transition: width 0.3s;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.75rem;
            font-weight: 600;
        }}
        .exercises {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 1rem;
        }}
        .exercise {{
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 1.25rem;
            transition: transform 0.2s, border-color 0.2s;
        }}
        .exercise:hover {{
            transform: translateY(-2px);
            border-color: var(--accent);
        }}
        .exercise.completed {{ border-left: 3px solid var(--green); }}
        .exercise.in-progress {{ border-left: 3px solid var(--yellow); }}
        .exercise-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 0.5rem;
        }}
        .exercise-number {{
            background: var(--bg);
            padding: 0.25rem 0.5rem;
            border-radius: 4px;
            font-size: 0.75rem;
            font-weight: 600;
            color: var(--accent);
        }}
        .exercise-status {{ font-size: 1.25rem; }}
        .exercise h3 {{
            font-size: 1rem;
            margin-bottom: 0.5rem;
        }}
        .learning-goal {{
            color: var(--muted);
            font-size: 0.875rem;
            margin-bottom: 0.75rem;
        }}
        .skills {{ display: flex; flex-wrap: wrap; gap: 0.5rem; }}
        .skill {{
            background: var(--bg);
            padding: 0.25rem 0.5rem;
            border-radius: 4px;
            font-size: 0.7rem;
            color: var(--muted);
        }}
        .stats {{
            display: flex;
            gap: 2rem;
            margin-bottom: 1.5rem;
        }}
        .stat {{
            text-align: center;
        }}
        .stat-value {{
            font-size: 2rem;
            font-weight: 700;
            color: var(--accent);
        }}
        .stat-label {{
            font-size: 0.75rem;
            color: var(--muted);
            text-transform: uppercase;
        }}
        .btn {{
            width: 100%;
            margin-top: 0.75rem;
            padding: 0.5rem 1rem;
            border: none;
            border-radius: 6px;
            font-size: 0.85rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
        }}
        .btn-start {{
            background: var(--accent);
            color: white;
        }}
        .btn-start:hover {{ background: #0891b2; }}
        .btn-progress {{
            background: var(--yellow);
            color: #0f172a;
        }}
        .btn-progress:hover {{ background: #d97706; }}
        .btn-completed {{
            background: var(--green);
            color: white;
        }}
        .btn-completed:hover {{ background: #059669; }}
    </style>
    <script>
        function updateStatus(exerciseId, newStatus) {{
            fetch('/update', {{
                method: 'POST',
                headers: {{ 'Content-Type': 'application/json' }},
                body: JSON.stringify({{ id: exerciseId, status: newStatus }})
            }}).then(() => location.reload());
        }}
    </script>
</head>
<body>
    <div class="container">
        <h1>CSK Exercises</h1>
        <p class="subtitle">Claude Starter Kit 2.0 — Interactive Learning</p>

        <div class="stats">
            <div class="stat">
                <div class="stat-value">{completed}</div>
                <div class="stat-label">Completed</div>
            </div>
            <div class="stat">
                <div class="stat-value">{total - completed}</div>
                <div class="stat-label">Remaining</div>
            </div>
            <div class="stat">
                <div class="stat-value">{pct}%</div>
                <div class="stat-label">Progress</div>
            </div>
        </div>

        <div class="progress-bar">
            <div class="progress-fill">{pct}%</div>
        </div>

        <div class="exercises">
            {exercises_html}
        </div>
    </div>
</body>
</html>'''


def render_exercise(exercise_id: str) -> str | None:
    """Render an exercise markdown file as HTML."""
    # Find the exercise file
    for ex in EXERCISES:
        if ex["id"] == exercise_id:
            filename = f"{exercise_id}-{ex['title'].lower().replace(' ', '-').replace(':', '')}.md"
            break
    else:
        return None

    # Try common filename patterns
    patterns = [
        EXERCISES_DIR / f"{exercise_id}-*.md",
        EXERCISES_DIR / f"{exercise_id.zfill(2)}-*.md",
    ]

    exercise_file = None
    for pattern in patterns:
        matches = list(EXERCISES_DIR.glob(f"{exercise_id.zfill(2)}-*.md"))
        if matches:
            exercise_file = matches[0]
            break

    if not exercise_file or not exercise_file.exists():
        return None

    content = exercise_file.read_text()

    # Markdown to HTML conversion
    import re
    html_content = content

    # Convert code blocks first (protect their content)
    code_blocks = []
    def save_code_block(match):
        code_blocks.append(match.group(2))
        return f'__CODE_BLOCK_{len(code_blocks) - 1}__'
    html_content = re.sub(r'```(\w+)?\n(.*?)```', save_code_block, html_content, flags=re.DOTALL)

    # Convert headers
    html_content = re.sub(r'^#### (.+)$', r'<h4>\1</h4>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html_content, flags=re.MULTILINE)

    # Convert links (transform exercise .md links to relative routes)
    def convert_link(match):
        text, url = match.group(1), match.group(2)
        exercise_match = re.match(r'^(\d+)-.*\.md$', url)
        if exercise_match:
            return f'<a href="{exercise_match.group(1)}">{text}</a>'
        return f'<a href="{url}">{text}</a>'
    html_content = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', convert_link, html_content)

    # Convert inline code
    html_content = re.sub(r'`([^`]+)`', r'<code>\1</code>', html_content)

    # Convert bold and italic
    html_content = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', html_content)
    html_content = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', html_content)

    # Process lines for lists and paragraphs
    lines = html_content.split('\n')
    result = []
    in_ul = False
    in_ol = False

    for line in lines:
        stripped = line.strip()

        # Horizontal rule
        if stripped == '---':
            if in_ul: result.append('</ul>'); in_ul = False
            if in_ol: result.append('</ol>'); in_ol = False
            result.append('<hr>')
            continue

        # Checkbox list items
        if re.match(r'^- \[ \] ', stripped):
            if in_ol: result.append('</ol>'); in_ol = False
            if not in_ul: result.append('<ul class="checklist">'); in_ul = True
            result.append(f'<li class="todo">☐ {stripped[6:]}</li>')
            continue
        if re.match(r'^- \[x\] ', stripped):
            if in_ol: result.append('</ol>'); in_ol = False
            if not in_ul: result.append('<ul class="checklist">'); in_ul = True
            result.append(f'<li class="done">☑ {stripped[6:]}</li>')
            continue

        # Unordered list items
        if re.match(r'^- ', stripped):
            if in_ol: result.append('</ol>'); in_ol = False
            if not in_ul: result.append('<ul>'); in_ul = True
            result.append(f'<li>{stripped[2:]}</li>')
            continue

        # Numbered list items
        num_match = re.match(r'^(\d+)\. (.+)$', stripped)
        if num_match:
            if in_ul: result.append('</ul>'); in_ul = False
            if not in_ol: result.append('<ol>'); in_ol = True
            result.append(f'<li>{num_match.group(2)}</li>')
            continue

        # Close lists if needed
        if in_ul and stripped and not stripped.startswith('<li'):
            result.append('</ul>'); in_ul = False
        if in_ol and stripped and not stripped.startswith('<li'):
            result.append('</ol>'); in_ol = False

        # Skip empty lines, already-converted HTML, and code block placeholders
        if not stripped:
            result.append('')
            continue
        if stripped.startswith('<') or stripped.startswith('__CODE_BLOCK_'):
            result.append(stripped)
            continue

        # Regular paragraph
        result.append(f'<p>{stripped}</p>')

    # Close any open lists
    if in_ul: result.append('</ul>')
    if in_ol: result.append('</ol>')

    html_content = '\n'.join(result)

    # Restore code blocks
    for i, code in enumerate(code_blocks):
        escaped_code = code.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        html_content = html_content.replace(f'__CODE_BLOCK_{i}__', f'<pre><code>{escaped_code}</code></pre>')

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Exercise {exercise_id} — CSK</title>
    <style>
        :root {{ --bg: #0f172a; --surface: #1e293b; --border: #334155; --text: #e2e8f0; --muted: #94a3b8; --accent: #06b6d4; --green: #10b981; }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif; background: var(--bg); color: var(--text); line-height: 1.6; padding: 2rem; }}
        .container {{ max-width: 800px; margin: 0 auto; }}
        h1 {{ color: var(--accent); margin-bottom: 1rem; }}
        h2 {{ color: var(--text); margin: 2rem 0 1rem; border-bottom: 1px solid var(--border); padding-bottom: 0.5rem; }}
        h3 {{ color: var(--muted); margin: 1.5rem 0 0.5rem; }}
        p {{ margin: 0.5rem 0; }}
        pre {{ background: var(--surface); border: 1px solid var(--border); border-radius: 8px; padding: 1rem; overflow-x: auto; margin: 1rem 0; }}
        code {{ font-family: "JetBrains Mono", monospace; font-size: 0.9em; }}
        p code {{ background: var(--surface); padding: 2px 6px; border-radius: 4px; }}
        ul, ol {{ margin: 1rem 0; padding-left: 1.5rem; }}
        li {{ margin: 0.5rem 0; }}
        li.todo {{ color: var(--muted); list-style: none; margin-left: -1rem; }}
        li.done {{ color: var(--green); list-style: none; margin-left: -1rem; }}
        ul.checklist {{ list-style: none; padding-left: 0.5rem; }}
        a {{ color: var(--accent); }}
        h4 {{ color: var(--muted); margin: 1rem 0 0.5rem; font-size: 0.95rem; }}
        hr {{ border: none; border-top: 1px solid var(--border); margin: 2rem 0; }}
        .back {{ display: inline-block; color: var(--accent); text-decoration: none; margin-bottom: 1rem; }}
        .back:hover {{ text-decoration: underline; }}
        strong {{ color: var(--accent); }}
    </style>
</head>
<body>
    <div class="container">
        <a href="/" class="back">← Back to exercises</a>
        {html_content}
    </div>
</body>
</html>'''


class ExerciseHandler(http.server.SimpleHTTPRequestHandler):
    """Custom handler for exercise server."""

    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            progress = load_progress()
            html = generate_html(progress)
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(html.encode())
        elif self.path.startswith("/exercise/"):
            exercise_id = self.path.split("/")[-1]
            html = render_exercise(exercise_id)
            if html:
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(html.encode())
            else:
                self.send_response(404)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(b"<h1>Exercise not found</h1>")
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == "/update":
            import json
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode())

            progress = load_progress()
            progress[data["id"]] = data["status"]
            save_progress(progress)

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"ok": true}')
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        pass


@click.command()
@click.option("--port", "-p", default=9123, help="Port to run server on")
@click.option("--no-browser", is_flag=True, help="Don't open browser automatically")
def exercises(port: int, no_browser: bool):
    """Start the exercise server and track your progress.

    Opens a web interface showing all 6 exercises with your progress.
    Progress is saved locally in .csk-progress.md.

    Note: If using 'csk workshop', exercises are available at /exercises/

    Example:

        csk exercises           # Start on port 9123
        csk exercises -p 3000   # Start on port 3000
    """
    import socket
    import signal
    import os

    def is_port_in_use(p: int) -> bool:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(('localhost', p)) == 0

    def kill_process_on_port(p: int) -> bool:
        """Try to kill process using the port. Returns True if killed."""
        try:
            import subprocess
            result = subprocess.run(
                ['fuser', '-k', f'{p}/tcp'],
                capture_output=True,
                timeout=5
            )
            return result.returncode == 0
        except Exception:
            return False

    # Check if port is in use and try to free it
    if is_port_in_use(port):
        console.print(f"[yellow]Port {port} is in use. Attempting to free it...[/yellow]")
        if kill_process_on_port(port):
            import time
            time.sleep(1)
            console.print(f"[green]Port {port} freed.[/green]")
        else:
            # Try next available port
            for p in range(port + 1, port + 100):
                if not is_port_in_use(p):
                    console.print(f"[yellow]Using port {p} instead.[/yellow]")
                    port = p
                    break
            else:
                console.print(f"[red]Could not find an available port.[/red]")
                return

    console.print(f"\n[bold cyan]Starting CSK Exercise Server[/bold cyan]\n")
    console.print(f"Server running at: [link]http://localhost:{port}[/link]")
    console.print("Press [bold]Ctrl+C[/bold] to stop.\n")

    # Threading server for faster concurrent request handling
    class ThreadingHTTPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
        allow_reuse_address = True
        daemon_threads = True

    with ThreadingHTTPServer(("", port), ExerciseHandler) as httpd:
        if not no_browser:
            threading.Timer(0.5, lambda: webbrowser.open(f"http://localhost:{port}")).start()
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            console.print("\n[dim]Server stopped.[/dim]")
