from flask import Flask, request, jsonify
from core.engine import HackingAssistantEngine

app = Flask(__name__)
hacking_assistant = HackingAssistantEngine(None)

@app.route('/api/add_target', methods=['POST'])
def add_target():
    target = request.json.get('target')
    hacking_assistant.add_target(target)
    return jsonify({'status': 'success', 'message': f'Target {target} added successfully.'})

@app.route('/api/run_scan', methods=['POST'])
def run_scan():
    hacking_assistant.run_scan()
    return jsonify({'status': 'success', 'message': 'Scan completed.'})

@app.route('/api/run_info_gathering', methods=['POST'])
def run_info_gathering():
    hacking_assistant.run_info_gathering()
    return jsonify({'status': 'success', 'message': 'Info gathering completed.'})

@app.route('/api/run_vulnerability_scan', methods=['POST'])
def run_vulnerability_scan():
    hacking_assistant.run_vulnerability_scan()
    return jsonify({'status': 'success', 'message': 'Vulnerability scan completed.'})

@app.route('/api/run_exploit', methods=['POST'])
def run_exploit():
    exploit = request.json.get('exploit')
    payload = request.json.get('payload')
    target = request.json.get('target')
    hacking_assistant.run_exploit(target, exploit, payload)
    return jsonify({'status': 'success', 'message': 'Exploit completed.'})

@app.route('/api/generate_report', methods=['POST'])
def generate_report():
    hacking_assistant.generate_report()
    return jsonify({'status': 'success', 'message': 'Report generated.'})

@app.route('/api/schedule_scan', methods=['POST'])
def schedule_scan():
    target = request.json.get('target')
    interval = request.json.get('interval')
    hacking_assistant.schedule_scan(target, interval)
    return jsonify({'status': 'success', 'message': f'Scheduled scan for {target} every {interval} minutes successfully.'})

@app.route('/api/run_phishing_attack', methods=['POST'])
def run_phishing_attack():
    target = request.json.get('target')
    hacking_assistant.run_phishing_attack(target)
    return jsonify({'status': 'success', 'message': f'Phishing attack executed on {target}.'})

@app.route('/api/run_social_engineering_attack', methods=['POST'])
def run_social_engineering_attack():
    target = request.json.get('target')
    hacking_assistant.run_social_engineering_attack(target)
    return jsonify({'status': 'success', 'message': f'Social engineering attack executed on {target}.'})

if __name__ == '__main__':
    app.run(port=5000)
