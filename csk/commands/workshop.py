"""csk workshop — Serve workshop materials (kompendium, slides, handout, exercises)."""

import http.server
import json
import os
import re
import signal
import socketserver
import threading
import webbrowser
from pathlib import Path

import click
from rich.console import Console

from csk.commands.progress import load_progress, save_progress, EXERCISES

console = Console()

WORKSHOP_DIR = Path(__file__).parent.parent.parent / "workshop"
EXERCISES_DIR = Path(__file__).parent.parent.parent / "exercises"
PID_FILE = Path("/tmp/csk-workshop.pid")


def render_exercise_list(progress: dict) -> str:
    """Generate exercises list HTML."""
    exercises_html = ""
    for ex in EXERCISES:
        status = progress.get(ex["id"], "not_started")
        status_class = status.replace("_", "-")
        status_icon = {"completed": "✓", "in_progress": "◐", "not_started": "○"}.get(status, "○")

        exercises_html += f'''
        <a href="{ex["id"]}" class="exercise {status_class}">
            <span class="status-icon">{status_icon}</span>
            <span class="ex-num">{ex["id"]}</span>
            <span class="ex-title">{ex["title"]}</span>
        </a>'''

    completed = sum(1 for s in progress.values() if s == "completed")
    total = len(EXERCISES)
    pct = int((completed / total) * 100) if total > 0 else 0

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Exercises — CSK2</title>
    <style>
        :root {{ --bg: #0f172a; --surface: #1e293b; --border: #334155; --text: #e2e8f0; --muted: #94a3b8; --accent: #06b6d4; --green: #10b981; }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif; background: var(--bg); color: var(--text); padding: 2rem; }}
        .container {{ max-width: 600px; margin: 0 auto; }}
        h1 {{ color: var(--accent); margin-bottom: 0.5rem; }}
        .subtitle {{ color: var(--muted); margin-bottom: 2rem; }}
        .progress {{ background: var(--surface); border-radius: 8px; padding: 1rem; margin-bottom: 2rem; text-align: center; }}
        .progress-bar {{ background: var(--border); border-radius: 4px; height: 8px; margin-top: 0.5rem; overflow: hidden; }}
        .progress-fill {{ background: var(--green); height: 100%; width: {pct}%; transition: width 0.3s; }}
        .exercises {{ display: flex; flex-direction: column; gap: 0.5rem; }}
        .exercise {{ display: flex; align-items: center; gap: 1rem; padding: 1rem; background: var(--surface); border: 1px solid var(--border); border-radius: 8px; text-decoration: none; color: var(--text); transition: border-color 0.2s; }}
        .exercise:hover {{ border-color: var(--accent); }}
        .exercise.completed {{ border-color: var(--green); }}
        .exercise.in-progress {{ border-color: var(--accent); }}
        .status-icon {{ font-size: 1.2rem; }}
        .completed .status-icon {{ color: var(--green); }}
        .in-progress .status-icon {{ color: var(--accent); }}
        .ex-num {{ color: var(--muted); font-size: 0.9rem; }}
        .ex-title {{ flex: 1; }}
        .back {{ display: inline-block; color: var(--accent); text-decoration: none; margin-bottom: 1rem; }}
        .back:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    <div class="container">
        <a href="../" class="back">← Workshop home</a>
        <h1>Exercises</h1>
        <p class="subtitle">{completed} of {total} completed</p>
        <div class="progress">
            <strong>{pct}%</strong> complete
            <div class="progress-bar"><div class="progress-fill"></div></div>
        </div>
        <div class="exercises">{exercises_html}</div>
    </div>
</body>
</html>'''


def render_exercise(exercise_id: str, progress: dict) -> str | None:
    """Render a single exercise as HTML."""
    # Find exercise file
    matches = list(EXERCISES_DIR.glob(f"{exercise_id.zfill(2)}-*.md"))
    if not matches:
        return None

    exercise_file = matches[0]
    content = exercise_file.read_text()

    # Get exercise info
    ex_info = next((e for e in EXERCISES if e["id"] == exercise_id), None)
    status = progress.get(exercise_id, "not_started")

    # Markdown to HTML conversion
    html = content

    # Convert code blocks first (protect their content)
    code_blocks = []
    def save_code_block(match):
        code_blocks.append(match.group(2))
        return f'__CODE_BLOCK_{len(code_blocks) - 1}__'
    html = re.sub(r'```(\w+)?\n(.*?)```', save_code_block, html, flags=re.DOTALL)

    # Convert headers
    html = re.sub(r'^#### (.+)$', r'<h4>\1</h4>', html, flags=re.MULTILINE)
    html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)

    # Convert links (transform exercise .md links to relative routes)
    def convert_link(match):
        text, url = match.group(1), match.group(2)
        exercise_match = re.match(r'^(\d+)-.*\.md$', url)
        if exercise_match:
            return f'<a href="{exercise_match.group(1)}">{text}</a>'
        return f'<a href="{url}">{text}</a>'
    html = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', convert_link, html)

    # Convert inline code, bold, italic
    html = re.sub(r'`([^`]+)`', r'<code>\1</code>', html)
    html = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', html)

    # Process lines for proper list wrapping
    lines = html.split('\n')
    result = []
    in_ul = False
    in_ol = False

    for line in lines:
        stripped = line.strip()

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

        # Skip empty lines, HTML, and code block placeholders
        if not stripped:
            result.append('')
            continue
        if stripped.startswith('<') or stripped.startswith('__CODE_BLOCK_'):
            result.append(stripped)
            continue

        result.append(f'<p>{stripped}</p>')

    if in_ul: result.append('</ul>')
    if in_ol: result.append('</ol>')

    html = '\n'.join(result)

    # Restore code blocks
    for i, code in enumerate(code_blocks):
        escaped = code.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        html = html.replace(f'__CODE_BLOCK_{i}__', f'<pre><code>{escaped}</code></pre>')

    # Status buttons
    if status == "completed":
        btn = f'<button class="btn completed" onclick="updateStatus(\'{exercise_id}\', \'not_started\')">✓ Completed — Reset?</button>'
    elif status == "in_progress":
        btn = f'<button class="btn progress" onclick="updateStatus(\'{exercise_id}\', \'completed\')">Mark Complete</button>'
    else:
        btn = f'<button class="btn start" onclick="updateStatus(\'{exercise_id}\', \'in_progress\')">Start Exercise</button>'

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Exercise {exercise_id} — CSK2</title>
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
        ul.checklist {{ list-style: none; padding-left: 0.5rem; }}
        a {{ color: var(--accent); }}
        h4 {{ color: var(--muted); margin: 1rem 0 0.5rem; font-size: 0.95rem; }}
        li.todo {{ color: var(--muted); }}
        li.done {{ color: var(--green); }}
        hr {{ border: none; border-top: 1px solid var(--border); margin: 2rem 0; }}
        .back {{ display: inline-block; color: var(--accent); text-decoration: none; margin-bottom: 1rem; }}
        .back:hover {{ text-decoration: underline; }}
        strong {{ color: var(--accent); }}
        .btn {{ padding: 0.75rem 1.5rem; border: none; border-radius: 8px; cursor: pointer; font-size: 1rem; margin-top: 1rem; }}
        .btn.start {{ background: var(--accent); color: white; }}
        .btn.progress {{ background: var(--green); color: white; }}
        .btn.completed {{ background: var(--surface); color: var(--green); border: 1px solid var(--green); }}
    </style>
    <script>
        function updateStatus(id, status) {{
            fetch('update', {{
                method: 'POST',
                headers: {{ 'Content-Type': 'application/json' }},
                body: JSON.stringify({{ id: id, status: status }})
            }})
            .then(response => {{
                if (response.ok) {{
                    location.reload();
                }} else {{
                    alert('Failed to update status');
                }}
            }})
            .catch(err => {{
                console.error('Error:', err);
                alert('Error updating status');
            }});
        }}
    </script>
</head>
<body>
    <div class="container">
        <a href="./" class="back">← Back to exercises</a>
        {html}
        <hr>
        {btn}
    </div>
</body>
</html>'''


class WorkshopHandler(http.server.SimpleHTTPRequestHandler):
    """Serve workshop files and exercises."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(WORKSHOP_DIR), **kwargs)

    def do_GET(self):
        if self.path == "/exercises/" or self.path == "/exercises":
            progress = load_progress()
            html = render_exercise_list(progress)
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(html.encode())
        elif self.path.startswith("/exercises/") and self.path != "/exercises/update":
            exercise_id = self.path.split("/")[-1]
            progress = load_progress()
            html = render_exercise(exercise_id, progress)
            if html:
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(html.encode())
            else:
                self.send_error(404, "Exercise not found")
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == "/exercises/update":
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
            self.send_error(404)

    def log_message(self, format, *args):
        pass


def _get_running_pid() -> int | None:
    """Get PID of running workshop server, or None."""
    if not PID_FILE.exists():
        return None
    try:
        pid = int(PID_FILE.read_text().strip())
        os.kill(pid, 0)  # Check if process exists
        return pid
    except (ValueError, ProcessLookupError, PermissionError):
        PID_FILE.unlink(missing_ok=True)
        return None


@click.group(invoke_without_command=True)
@click.option("--port", "-p", default=9123, help="Port to run server on")
@click.option("--no-browser", is_flag=True, help="Don't open browser automatically")
@click.pass_context
def workshop(ctx, port: int, no_browser: bool):
    """Start the workshop materials server.

    Serves kompendium, slides, and handout from the workshop/ directory.

    Example:

        csk workshop           # Start on port 9123
        csk workshop -p 3000   # Start on port 3000
        csk workshop stop      # Stop running server
    """
    if ctx.invoked_subcommand is not None:
        return

    if not WORKSHOP_DIR.exists():
        console.print("[red]Error:[/red] Workshop directory not found.")
        console.print(f"Expected at: {WORKSHOP_DIR}")
        raise SystemExit(1)

    # Check if already running
    existing_pid = _get_running_pid()
    if existing_pid:
        console.print(f"[yellow]Workshop server already running (PID {existing_pid})[/yellow]")
        console.print("Run [cyan]csk workshop stop[/cyan] first, or [cyan]csk workshop restart[/cyan]")
        raise SystemExit(1)

    # Use ThreadingTCPServer for faster concurrent request handling
    class ThreadingHTTPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
        allow_reuse_address = True
        daemon_threads = True

    try:
        httpd = ThreadingHTTPServer(("", port), WorkshopHandler)
    except OSError as e:
        if "Address already in use" in str(e):
            console.print(f"[red]Error:[/red] Port {port} is already in use.")
            console.print(f"Try: [cyan]csk workshop -p {port + 1}[/cyan]")
            raise SystemExit(1)
        raise

    # Save PID
    PID_FILE.write_text(str(os.getpid()))

    console.print(f"\n[bold cyan]CSK2 Workshop Server[/bold cyan]\n")
    console.print(f"Server running at: [link]http://localhost:{port}[/link]")
    console.print()
    console.print(f"  [cyan]http://localhost:{port}/[/cyan]             — Index")
    console.print(f"  [cyan]http://localhost:{port}/kompendium.html[/cyan] — Full reference")
    console.print(f"  [cyan]http://localhost:{port}/slides.html[/cyan]     — Presentation")
    console.print(f"  [cyan]http://localhost:{port}/handout.html[/cyan]    — Print handout")
    console.print(f"  [cyan]http://localhost:{port}/exercises/[/cyan]      — Exercises")
    console.print()
    console.print("Press [bold]Ctrl+C[/bold] to stop, or run [cyan]csk workshop stop[/cyan]\n")

    with httpd:
        if not no_browser:
            threading.Timer(0.5, lambda: webbrowser.open(f"http://localhost:{port}")).start()
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
        finally:
            PID_FILE.unlink(missing_ok=True)
            console.print("\n[dim]Server stopped.[/dim]")


@workshop.command()
def stop():
    """Stop the running workshop server."""
    pid = _get_running_pid()
    if not pid:
        console.print("[yellow]No workshop server running.[/yellow]")
        return

    try:
        os.kill(pid, signal.SIGTERM)
        PID_FILE.unlink(missing_ok=True)
        console.print(f"[green]Workshop server stopped (PID {pid})[/green]")
    except ProcessLookupError:
        PID_FILE.unlink(missing_ok=True)
        console.print("[yellow]Server already stopped.[/yellow]")


@workshop.command()
@click.option("--port", "-p", default=9123, help="Port to run server on")
@click.option("--no-browser", is_flag=True, help="Don't open browser automatically")
@click.pass_context
def restart(ctx, port: int, no_browser: bool):
    """Restart the workshop server."""
    import time

    pid = _get_running_pid()
    if pid:
        console.print(f"[dim]Stopping server (PID {pid})...[/dim]")
        try:
            os.kill(pid, signal.SIGTERM)
            # Wait for process to exit
            for _ in range(20):
                try:
                    os.kill(pid, 0)
                    time.sleep(0.1)
                except ProcessLookupError:
                    break
        except ProcessLookupError:
            pass
        PID_FILE.unlink(missing_ok=True)

    # Server uses SO_REUSEADDR, so we can start immediately
    ctx.invoke(workshop, port=port, no_browser=no_browser)
