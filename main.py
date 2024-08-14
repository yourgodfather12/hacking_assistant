from flask import Flask, render_template, request, jsonify, send_file
from flask_socketio import SocketIO, emit
import paramiko
import logging
import os
from config import LOG_PATH, API_PORT, LINODE_HOST, LINODE_PORT, LINODE_USER, LINODE_PASSWORD, DB_PATH, NMAP_ARGUMENTS
import sqlite3
import nmap
import subprocess
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Setup logging
logging.basicConfig(filename=LOG_PATH, level=logging.ERROR, format='%(asctime)s %(levelname)s: %(message)s')

# Initialize Flask app and SocketIO
app = Flask(__name__)
socketio = SocketIO(app)

# Setup SSH client
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Database setup
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def add_target_to_db(target):
    conn = get_db_connection()
    conn.execute("INSERT OR IGNORE INTO targets (target) VALUES (?)", (target,))
    conn.commit()
    conn.close()

def get_targets_from_db():
    conn = get_db_connection()
    targets = conn.execute("SELECT target FROM targets").fetchall()
    conn.close()
    return [target['target'] for target in targets]

def store_scan_result(target, scan_type, result):
    conn = get_db_connection()
    conn.execute("INSERT INTO results (target, type, result) VALUES (?, ?, ?)", (target, scan_type, result))
    conn.commit()
    conn.close()

def get_scan_results():
    conn = get_db_connection()
    results = conn.execute("SELECT * FROM results").fetchall()
    conn.close()
    return results

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/connect_terminal', methods=['POST'])
def connect_terminal():
    try:
        ssh_client.connect(LINODE_HOST, port=LINODE_PORT, username=LINODE_USER, password=LINODE_PASSWORD)
        return jsonify({'status': 'success', 'message': 'Connected to Linode server.'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@socketio.on('run_command')
def handle_command(data):
    command = data['command']
    try:
        stdin, stdout, stderr = ssh_client.exec_command(command)
        output = stdout.read().decode()
        emit('command_output', {'output': output})
    except Exception as e:
        emit('command_output', {'output': f'Error: {str(e)}'})

@app.route('/add_target', methods=['POST'])
def add_target():
    target = request.json.get('target')
    add_target_to_db(target)
    return jsonify({'status': 'success', 'message': f'Target {target} added successfully.'})

@app.route('/run_scan', methods=['POST'])
def run_scan():
    targets = get_targets_from_db()
    nm = nmap.PortScanner()
    for target in targets:
        nm.scan(hosts=target, arguments=NMAP_ARGUMENTS)
        scan_results = nm[target].all_tcp() if nm.all_hosts() else {}
        store_scan_result(target, 'network_scan', str(scan_results))
    return jsonify({'status': 'success', 'message': 'Network scan completed.'})

@app.route('/run_info_gathering', methods=['POST'])
def run_info_gathering():
    targets = get_targets_from_db()
    for target in targets:
        whois_result = subprocess.run(['whois', target], capture_output=True, text=True).stdout
        store_scan_result(target, 'info_gathering', whois_result)
    return jsonify({'status': 'success', 'message': 'Info gathering completed.'})

@app.route('/run_vulnerability_scan', methods=['POST'])
def run_vulnerability_scan():
    targets = get_targets_from_db()
    for target in targets:
        vuln_results = f"Vulnerability scan results for {target} (mocked data)"
        store_scan_result(target, 'vulnerability_scan', vuln_results)
    return jsonify({'status': 'success', 'message': 'Vulnerability scan completed.'})

@app.route('/generate_report', methods=['POST'])
def generate_report():
    results = get_scan_results()
    report_path = "report.pdf"
    c = canvas.Canvas(report_path, pagesize=letter)
    width, height = letter
    y = height - 50
    for result in results:
        c.drawString(100, y, f"Target: {result['target']}, Type: {result['type']}, Result: {result['result'][:100]}...")
        y -= 20
        if y < 100:
            c.showPage()
            y = height - 50
    c.save()
    return jsonify({'status': 'success', 'message': 'Report generated successfully.'})

@app.route('/targets', methods=['GET'])
def view_targets():
    targets = get_targets_from_db()
    return jsonify({'targets': targets})

@app.route('/results', methods=['GET'])
def view_results():
    results = get_scan_results()
    return jsonify({'results': [{'target': result['target'], 'type': result['type'], 'result': result['result']} for result in results]})

@app.route('/logs', methods=['GET'])
def view_logs():
    if os.path.exists(LOG_PATH):
        with open(LOG_PATH, 'r') as f:
            logs = f.read()
    else:
        logs = "No logs available."
    return jsonify({'logs': logs})

@app.route('/download_report', methods=['GET'])
def download_report():
    report_path = "report.pdf"
    return send_file(report_path, as_attachment=True)

@app.route('/update_config', methods=['POST'])
def update_config():
    nmap_args = request.json.get('nmapArguments')
    global NMAP_ARGUMENTS
    NMAP_ARGUMENTS = nmap_args
    return jsonify({'status': 'success', 'message': 'Configuration updated successfully.'})

if __name__ == '__main__':
    socketio.run(app, port=API_PORT)
