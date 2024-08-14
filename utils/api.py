from flask import Flask, request, jsonify
import logging
from core.engine import HackingAssistantEngine

app = Flask(__name__)
hacking_assistant = HackingAssistantEngine(None)

logger = logging.getLogger(__name__)

@app.route('/api/add_target', methods=['POST'])
def add_target():
    target = request.json.get('target')
    if not target:
        return jsonify({'status': 'error', 'message': 'Target is required.'}), 400
    hacking_assistant.add_target(target)
    logger.info(f"Target {target} added via API.")
    return jsonify({'status': 'success', 'message': f'Target {target} added successfully.'})

@app.route('/api/run_scan', methods=['POST'])
def run_scan():
    hacking_assistant.run_scan()
    logger.info("Network scan initiated via API.")
    return jsonify({'status': 'success', 'message': 'Scan completed.'})

@app.route('/api/run_info_gathering', methods=['POST'])
def run_info_gathering():
    hacking_assistant.run_info_gathering()
    logger.info("Info gathering initiated via API.")
    return jsonify({'status': 'success', 'message': 'Info gathering completed.'})

@app.route('/api/run_vulnerability_scan', methods=['POST'])
def run_vulnerability_scan():
    hacking_assistant.run_vulnerability_scan()
    logger.info("Vulnerability scan initiated via API.")
    return jsonify({'status': 'success', 'message': 'Vulnerability scan completed.'})

@app.route('/api/run_exploit', methods=['POST'])
def run_exploit():
    exploit = request.json.get('exploit')
    payload = request.json.get('payload')
    target = request.json.get('target')
    if not (exploit and payload and target):
        return jsonify({'status': 'error', 'message': 'Exploit, payload, and target are required.'}), 400
    hacking_assistant.run_exploit(target, exploit, payload)
    logger.info(f"Exploit {exploit} executed on target {target} via API.")
    return jsonify({'status': 'success', 'message': 'Exploit completed.'})

@app.route('/api/generate_report', methods=['POST'])
def generate_report():
    hacking_assistant.generate_report()
    logger.info("Report generation initiated via API.")
    return jsonify({'status': 'success', 'message': 'Report generated.'})

@app.route('/api/schedule_scan', methods=['POST'])
def schedule_scan():
    target = request.json.get('target')
    interval = request.json.get('interval')
    if not (target and interval):
        return jsonify({'status': 'error', 'message': 'Target and interval are required.'}), 400
    hacking_assistant.schedule_scan(target, interval)
    logger.info(f"Scheduled scan for target {target} every {interval} minutes via API.")
    return jsonify({'status': 'success', 'message': f'Scheduled scan for {target} every {interval} minutes successfully.'})

@app.route('/api/run_phishing_attack', methods=['POST'])
def run_phishing_attack():
    target = request.json.get('target')
    if not target:
        return jsonify({'status': 'error', 'message': 'Target is required.'}), 400
    hacking_assistant.run_phishing_attack(target)
    logger.info(f"Phishing attack initiated on target {target} via API.")
    return jsonify({'status': 'success', 'message': f'Phishing attack executed on {target}.'})

@app.route('/api/run_social_engineering_attack', methods=['POST'])
def run_social_engineering_attack():
    target = request.json.get('target')
    if not target:
        return jsonify({'status': 'error', 'message': 'Target is required.'}), 400
    hacking_assistant.run_social_engineering_attack(target)
    logger.info(f"Social engineering attack initiated on target {target} via API.")
    return jsonify({'status': 'success', 'message': f'Social engineering attack executed on {target}.'})

if __name__ == '__main__':
    app.run(port=5000)
