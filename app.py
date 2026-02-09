from flask import Flask, request, jsonify
import jwt
import time
import datetime

app = Flask(__name__)

SECRET_KEY = "demo-secret-key-not-for-production"

# Fake user database
USERS = {
    "admin": "password123",
    "user": "pass456",
}


@app.route("/")
def index():
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>JWT Demo - Why Tokens Differ</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

  * { box-sizing: border-box; margin: 0; padding: 0; }

  body {
    font-family: 'Inter', system-ui, sans-serif;
    background: #050a18;
    color: #e2e8f0;
    min-height: 100vh;
    overflow-x: hidden;
  }

  /* Animated background */
  body::before {
    content: '';
    position: fixed;
    top: -50%; left: -50%;
    width: 200%; height: 200%;
    background: radial-gradient(ellipse at 20% 50%, rgba(56,189,248,0.08) 0%, transparent 50%),
                radial-gradient(ellipse at 80% 20%, rgba(139,92,246,0.08) 0%, transparent 50%),
                radial-gradient(ellipse at 50% 80%, rgba(244,114,182,0.06) 0%, transparent 50%);
    animation: bgDrift 20s ease-in-out infinite alternate;
    z-index: 0;
    pointer-events: none;
  }
  @keyframes bgDrift {
    0% { transform: translate(0, 0) rotate(0deg); }
    100% { transform: translate(-3%, 3%) rotate(3deg); }
  }

  /* Grid overlay */
  body::after {
    content: '';
    position: fixed; inset: 0;
    background-image:
      linear-gradient(rgba(148,163,184,0.03) 1px, transparent 1px),
      linear-gradient(90deg, rgba(148,163,184,0.03) 1px, transparent 1px);
    background-size: 60px 60px;
    z-index: 0;
    pointer-events: none;
  }

  .container { max-width: 960px; margin: 0 auto; padding: 2.5rem 1.5rem 4rem; position: relative; z-index: 1; }

  /* Header */
  .header { text-align: center; margin-bottom: 2.5rem; }
  .logo {
    display: inline-flex; align-items: center; gap: 0.6rem;
    background: linear-gradient(135deg, rgba(56,189,248,0.12), rgba(139,92,246,0.12));
    border: 1px solid rgba(139,92,246,0.2);
    padding: 0.45rem 1.2rem; border-radius: 100px;
    font-size: 0.8rem; font-weight: 600; color: #a78bfa;
    letter-spacing: 0.05em; text-transform: uppercase;
    margin-bottom: 1.25rem;
  }
  .logo .dot { width: 6px; height: 6px; border-radius: 50%; background: #a78bfa; animation: pulse 2s ease-in-out infinite; }
  @keyframes pulse { 0%,100% { opacity: 0.4; transform: scale(1); } 50% { opacity: 1; transform: scale(1.3); } }

  h1 {
    font-size: 2.2rem; font-weight: 800; line-height: 1.2; margin-bottom: 0.6rem;
    background: linear-gradient(135deg, #f8fafc 0%, #94a3b8 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text;
  }
  .subtitle { color: #64748b; font-size: 1.05rem; font-weight: 400; }

  /* Glass card base */
  .glass {
    background: rgba(15,23,42,0.6);
    backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(148,163,184,0.08);
    border-radius: 16px;
  }

  /* Login box */
  .login-box {
    padding: 1.75rem; margin-bottom: 2rem;
    position: relative; overflow: hidden;
  }
  .login-box::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(56,189,248,0.4), rgba(139,92,246,0.4), transparent);
  }
  .login-box h2 {
    font-size: 0.85rem; font-weight: 600; color: #64748b;
    text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 1.1rem;
  }
  .form-row { display: flex; gap: 0.75rem; align-items: center; flex-wrap: wrap; }

  .input-wrap {
    position: relative; flex: 1; min-width: 160px;
  }
  .input-wrap label {
    position: absolute; top: -0.5rem; left: 0.75rem;
    background: #0c1425; padding: 0 0.35rem;
    font-size: 0.7rem; font-weight: 500; color: #475569;
    text-transform: uppercase; letter-spacing: 0.05em;
  }
  input {
    width: 100%;
    background: rgba(15,23,42,0.8);
    border: 1px solid rgba(71,85,105,0.5);
    color: #e2e8f0;
    padding: 0.75rem 1rem;
    border-radius: 10px;
    font-size: 0.95rem;
    font-family: 'Inter', sans-serif;
    transition: all 0.2s ease;
  }
  input:focus {
    outline: none;
    border-color: rgba(56,189,248,0.5);
    box-shadow: 0 0 0 3px rgba(56,189,248,0.1), inset 0 0 0 1px rgba(56,189,248,0.1);
  }

  button {
    padding: 0.75rem 1.75rem; border-radius: 10px; border: none;
    font-size: 0.9rem; font-weight: 600; cursor: pointer;
    font-family: 'Inter', sans-serif;
    transition: all 0.2s ease;
    position: relative; overflow: hidden;
  }
  .btn-login {
    background: linear-gradient(135deg, #3b82f6, #8b5cf6);
    color: white;
    box-shadow: 0 4px 15px rgba(59,130,246,0.3), 0 1px 3px rgba(0,0,0,0.2);
  }
  .btn-login:hover {
    transform: translateY(-1px);
    box-shadow: 0 6px 25px rgba(59,130,246,0.4), 0 2px 6px rgba(0,0,0,0.3);
  }
  .btn-login:active { transform: translateY(0); }
  .btn-clear {
    background: rgba(51,65,85,0.4); color: #64748b;
    border: 1px solid rgba(71,85,105,0.3);
    margin-left: auto;
  }
  .btn-clear:hover { background: rgba(71,85,105,0.4); color: #94a3b8; }

  .error-msg { color: #fb7185; font-size: 0.85rem; margin-top: 0.75rem; font-weight: 500; }

  /* Counter badge */
  .counter {
    display: flex; align-items: center; gap: 0.75rem;
    margin-bottom: 1.25rem;
  }
  .counter-badge {
    display: inline-flex; align-items: center; gap: 0.4rem;
    background: rgba(56,189,248,0.1); border: 1px solid rgba(56,189,248,0.15);
    padding: 0.3rem 0.85rem; border-radius: 100px;
    font-size: 0.8rem; font-weight: 600; color: #38bdf8;
  }
  .counter-line { flex: 1; height: 1px; background: rgba(148,163,184,0.08); }

  /* Token cards */
  .tokens-area { display: flex; flex-direction: column; gap: 1.25rem; }

  .token-card {
    padding: 1.5rem; position: relative; overflow: hidden;
    animation: slideUp 0.4s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    opacity: 0;
  }
  @keyframes slideUp {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
  }
  .token-card.latest { border-color: rgba(56,189,248,0.15); }
  .token-card.latest::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(56,189,248,0.5), transparent);
  }

  .token-header {
    display: flex; justify-content: space-between; align-items: center;
    margin-bottom: 1rem;
  }
  .token-number {
    display: inline-flex; align-items: center; gap: 0.5rem;
    font-weight: 700; font-size: 0.95rem;
  }
  .token-number .num {
    display: inline-flex; align-items: center; justify-content: center;
    width: 26px; height: 26px; border-radius: 8px; font-size: 0.8rem;
    background: linear-gradient(135deg, #3b82f6, #8b5cf6);
    color: white;
  }
  .token-time {
    color: #475569; font-size: 0.8rem;
    font-family: 'JetBrains Mono', monospace;
  }

  /* Color-coded JWT parts */
  .raw-token {
    background: rgba(0,0,0,0.3);
    border: 1px solid rgba(148,163,184,0.06);
    padding: 1rem; border-radius: 10px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem; word-break: break-all;
    line-height: 1.7; margin-bottom: 1rem;
  }
  .jwt-header { color: #f472b6; }
  .jwt-payload { color: #a78bfa; }
  .jwt-sig { color: #38bdf8; }
  .jwt-dot { color: #334155; }

  .jwt-legend {
    display: flex; gap: 1rem; margin-bottom: 1rem; flex-wrap: wrap;
  }
  .jwt-legend span {
    display: inline-flex; align-items: center; gap: 0.35rem;
    font-size: 0.72rem; color: #64748b; font-weight: 500;
  }
  .jwt-legend .swatch {
    width: 10px; height: 10px; border-radius: 3px;
  }

  /* Payload table */
  .payload-table { width: 100%; border-collapse: collapse; }
  .payload-table th {
    text-align: left; padding: 0.55rem 0.85rem; font-size: 0.72rem;
    color: #475569; font-weight: 600; text-transform: uppercase; letter-spacing: 0.06em;
    border-bottom: 1px solid rgba(148,163,184,0.08);
  }
  .payload-table td {
    text-align: left; padding: 0.65rem 0.85rem; font-size: 0.88rem;
    color: #cbd5e1; font-family: 'JetBrains Mono', monospace;
    border-bottom: 1px solid rgba(148,163,184,0.04);
  }
  .payload-table tr:last-child td { border-bottom: none; }

  .badge {
    display: inline-block; padding: 0.2rem 0.65rem; border-radius: 100px;
    font-size: 0.72rem; font-weight: 600; font-family: 'Inter', sans-serif;
    letter-spacing: 0.02em;
  }
  .badge-same { background: rgba(74,222,128,0.1); color: #4ade80; border: 1px solid rgba(74,222,128,0.15); }
  .badge-diff { background: rgba(250,204,21,0.1); color: #facc15; border: 1px solid rgba(250,204,21,0.2); animation: glowYellow 2s ease-in-out infinite; }
  .badge-na { background: rgba(100,116,139,0.1); color: #64748b; border: 1px solid rgba(100,116,139,0.15); }
  @keyframes glowYellow { 0%,100% { box-shadow: 0 0 0 rgba(250,204,21,0); } 50% { box-shadow: 0 0 12px rgba(250,204,21,0.15); } }

  .highlight { color: #fbbf24 !important; }

  /* Diff banner */
  .diff-banner {
    margin-top: 1.5rem; padding: 1.75rem;
    position: relative; overflow: hidden;
    border-color: rgba(251,191,36,0.12);
    animation: slideUp 0.5s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    opacity: 0;
  }
  .diff-banner::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(251,191,36,0.5), transparent);
  }
  .diff-banner-icon {
    display: inline-flex; align-items: center; justify-content: center;
    width: 36px; height: 36px; border-radius: 10px;
    background: rgba(251,191,36,0.1); border: 1px solid rgba(251,191,36,0.15);
    margin-bottom: 0.85rem; font-size: 1.1rem;
  }
  .diff-banner h3 {
    font-size: 1.05rem; font-weight: 700; color: #fbbf24; margin-bottom: 0.85rem;
  }
  .diff-banner p {
    color: #94a3b8; font-size: 0.9rem; line-height: 1.8;
  }
  .diff-banner code {
    background: rgba(251,191,36,0.08); border: 1px solid rgba(251,191,36,0.12);
    padding: 0.15rem 0.5rem; border-radius: 5px;
    font-size: 0.82rem; color: #fbbf24;
    font-family: 'JetBrains Mono', monospace;
  }
  .diff-banner strong { color: #e2e8f0; }

  .formula-box {
    background: rgba(0,0,0,0.3); border: 1px solid rgba(148,163,184,0.06);
    border-radius: 10px; padding: 1rem 1.25rem; margin-top: 1rem;
    font-family: 'JetBrains Mono', monospace; font-size: 0.82rem;
    color: #94a3b8; line-height: 1.7;
  }
  .formula-box .op { color: #64748b; }
  .formula-box .fn { color: #38bdf8; }
  .formula-box .arrow { color: #f472b6; }

  /* Responsive */
  @media (max-width: 600px) {
    .container { padding: 1.5rem 1rem; }
    h1 { font-size: 1.5rem; }
    .form-row { flex-direction: column; }
    .input-wrap { width: 100%; }
    button { width: 100%; }
    .btn-clear { margin-left: 0; }
  }
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <div class="logo"><span class="dot"></span> JWT Explorer</div>
    <h1>Why Does Each Login Generate a Different JWT?</h1>
    <p class="subtitle">Log in multiple times with the same credentials and compare the tokens</p>
  </div>

  <div class="login-box glass">
    <h2>Authenticate</h2>
    <div class="form-row">
      <div class="input-wrap">
        <label>Username</label>
        <input type="text" id="username" value="admin">
      </div>
      <div class="input-wrap">
        <label>Password</label>
        <input type="password" id="password" value="password123">
      </div>
      <button class="btn-login" onclick="doLogin()">Login &rarr;</button>
      <button class="btn-clear" onclick="clearTokens()">Clear</button>
    </div>
    <div id="error" class="error-msg"></div>
  </div>

  <div id="counter-area"></div>
  <div class="tokens-area" id="tokens-area"></div>
  <div id="diff-area"></div>
</div>

<script>
let tokens = [];

async function doLogin() {
  const username = document.getElementById('username').value;
  const password = document.getElementById('password').value;
  document.getElementById('error').textContent = '';

  const res = await fetch('/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password })
  });
  const data = await res.json();

  if (!res.ok) {
    document.getElementById('error').textContent = data.error;
    return;
  }

  tokens.push(data);
  renderTokens();
}

function clearTokens() {
  tokens = [];
  document.getElementById('tokens-area').innerHTML = '';
  document.getElementById('diff-area').innerHTML = '';
  document.getElementById('counter-area').innerHTML = '';
}

function fmtTime(ts) {
  return new Date(ts * 1000).toLocaleTimeString('en-US', { hour12: true, hour: '2-digit', minute: '2-digit', second: '2-digit', fractionalSecondDigits: 3 });
}

function colorToken(raw) {
  const parts = raw.split('.');
  if (parts.length !== 3) return raw;
  return `<span class="jwt-header">${parts[0]}</span><span class="jwt-dot">.</span><span class="jwt-payload">${parts[1]}</span><span class="jwt-dot">.</span><span class="jwt-sig">${parts[2]}</span>`;
}

function renderTokens() {
  const area = document.getElementById('tokens-area');
  area.innerHTML = '';

  // Counter
  const cArea = document.getElementById('counter-area');
  cArea.innerHTML = `<div class="counter">
    <span class="counter-badge">${tokens.length} token${tokens.length !== 1 ? 's' : ''} generated</span>
    <span class="counter-line"></span>
  </div>`;

  tokens.forEach((t, i) => {
    const p = t.decoded;
    const isLatest = i === tokens.length - 1;
    const prevToken = i > 0 ? tokens[i - 1] : null;

    const iatChanged = prevToken && p.iat !== prevToken.decoded.iat;
    const expChanged = prevToken && p.exp !== prevToken.decoded.exp;

    const card = document.createElement('div');
    card.className = 'token-card glass' + (isLatest ? ' latest' : '');
    card.style.animationDelay = (i * 0.05) + 's';
    card.innerHTML = `
      <div class="token-header">
        <span class="token-number"><span class="num">${i + 1}</span> Token #${i + 1}</span>
        <span class="token-time">${fmtTime(p.iat)}</span>
      </div>
      <div class="jwt-legend">
        <span><span class="swatch" style="background:#f472b6"></span> Header</span>
        <span><span class="swatch" style="background:#a78bfa"></span> Payload</span>
        <span><span class="swatch" style="background:#38bdf8"></span> Signature</span>
      </div>
      <div class="raw-token">${colorToken(t.token)}</div>
      <table class="payload-table">
        <tr><th>Field</th><th>Value</th><th>Status</th></tr>
        <tr>
          <td>sub</td>
          <td>${p.sub}</td>
          <td><span class="badge badge-same">SAME</span></td>
        </tr>
        <tr>
          <td>iat</td>
          <td class="${iatChanged ? 'highlight' : ''}">${p.iat} &mdash; ${fmtTime(p.iat)}</td>
          <td>${iatChanged ? '<span class="badge badge-diff">CHANGED</span>' : (i === 0 ? '<span class="badge badge-na">&mdash;</span>' : '<span class="badge badge-same">SAME</span>')}</td>
        </tr>
        <tr>
          <td>exp</td>
          <td class="${expChanged ? 'highlight' : ''}">${p.exp} &mdash; ${fmtTime(p.exp)}</td>
          <td>${expChanged ? '<span class="badge badge-diff">CHANGED</span>' : (i === 0 ? '<span class="badge badge-na">&mdash;</span>' : '<span class="badge badge-same">SAME</span>')}</td>
        </tr>
      </table>
    `;
    area.appendChild(card);
  });

  // Show explanation after 2+ tokens
  const diffArea = document.getElementById('diff-area');
  if (tokens.length >= 2) {
    diffArea.innerHTML = `
      <div class="diff-banner glass">
        <div class="diff-banner-icon">?</div>
        <h3>Why are the tokens different?</h3>
        <p>
          The <code>sub</code> (subject/username) stays the same, but
          <code>iat</code> and <code>exp</code> change every time you log in
          because they capture the <strong>exact moment</strong> the token was created.
        </p>
        <br>
        <p>
          Since the <strong>payload is different</strong>, the <strong>signature</strong> (computed
          from the payload + secret key) is also different. That's why the entire JWT string changes
          even though you used the same credentials.
        </p>
        <div class="formula-box">
          JWT <span class="op">=</span> <span class="fn">base64</span>(header) <span class="op">+</span> "." <span class="op">+</span> <span class="fn">base64</span>(payload) <span class="op">+</span> "." <span class="op">+</span> <span class="fn">HMAC</span>(header + payload, secret)<br>
          <br>
          Different payload <span class="arrow">&rarr;</span> different signature <span class="arrow">&rarr;</span> <strong style="color:#fbbf24">different token</strong>
        </div>
      </div>
    `;
  } else {
    diffArea.innerHTML = '';
  }
}
</script>
</body>
</html>"""


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username", "")
    password = data.get("password", "")

    if username not in USERS or USERS[username] != password:
        return jsonify({"error": "Invalid username or password"}), 401

    now = time.time()
    payload = {
        "sub": username,
        "iat": now,
        "exp": now + 3600,  # 1 hour
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    return jsonify({
        "token": token,
        "decoded": payload,
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)
