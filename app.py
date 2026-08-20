from flask import Flask, render_template_string, jsonify, request, abort
import os
import subprocess
from datetime import datetime

app = Flask(__name__)

# Portfolio-safe demo:
# - No GPS collection
# - No IP geolocation
# - No root requirement
# - Authentication token required
# - Commands are allow-listed
# - shell=False to avoid arbitrary shell interpretation

ACCESS_TOKEN = os.environ.get("REMOTE_LAB_TOKEN", "")
ALLOWED_COMMANDS = {
    "whoami": ["whoami"],
    "hostname": ["hostname"],
    "pwd": ["pwd"],
    "date": ["date"],
    "ip addr": ["ip", "addr"],
    "uname -a": ["uname", "-a"],
}

HTML_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>Remote Lab</title>
  <style>
    body { background:#1e1e1e; color:#0f0; font-family:monospace; padding:20px; }
    #terminal { background:#000; border:1px solid #333; padding:15px; height:400px;
                overflow-y:auto; white-space:pre-wrap; }
    .input-line { display:flex; margin-top:10px; gap:8px; }
    input { background:#000; border:1px solid #333; color:#fff; flex:1; padding:8px; }
    button { background:#333; color:#fff; border:0; padding:8px 16px; cursor:pointer; }
  </style>
</head>
<body>
  <h2>Remote Lab - Controlled Command Interface</h2>
  <div id="terminal">Ready.<br>Allowed: whoami, hostname, pwd, date, ip addr, uname -a<br></div>
  <div class="input-line">
    <input id="cmd" placeholder="Enter an allowed command">
    <input id="token" type="password" placeholder="Access token">
    <button onclick="runCommand()">Send</button>
  </div>
<script>
async function runCommand() {
  const cmd = document.getElementById('cmd').value.trim();
  const token = document.getElementById('token').value;
  const term = document.getElementById('terminal');
  if (!cmd) return;

  const r = await fetch('/execute', {
    method: 'POST',
    headers: {'Content-Type':'application/json','X-Access-Token':token},
    body: JSON.stringify({command: cmd})
  });

  const data = await r.json();
  term.textContent += `\\nlab$ ${cmd}\\n${data.output || data.error || ''}`;
  term.scrollTop = term.scrollHeight;
}
</script>
</body>
</html>
"""

def authorized(req):
    return ACCESS_TOKEN and req.headers.get("X-Access-Token") == ACCESS_TOKEN

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route("/metadata", methods=["GET"])
def metadata():
    # Intentionally minimal: avoids collecting personal identifiers.
    return jsonify({
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "client": "connected"
    })

@app.route("/execute", methods=["POST"])
def execute_command():
    if not authorized(request):
        abort(401)

    data = request.get_json(silent=True) or {}
    command = data.get("command", "").strip()

    argv = ALLOWED_COMMANDS.get(command)
    if argv is None:
        return jsonify({"error": "Command is not allowed."}), 400

    try:
        result = subprocess.run(
            argv,
            shell=False,
            capture_output=True,
            text=True,
            timeout=10
        )
        output = (result.stdout + result.stderr).strip()
        return jsonify({"output": output})
    except subprocess.TimeoutExpired:
        return jsonify({"error": "Command timed out."}), 408

if __name__ == "__main__":
    if not ACCESS_TOKEN:
        raise RuntimeError("Set REMOTE_LAB_TOKEN before starting the app.")
    app.run(host="127.0.0.1", port=8080, debug=False)
