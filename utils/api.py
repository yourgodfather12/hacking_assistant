from flask import Flask, request, jsonify
import logging
from core.engine import HackingAssistantEngine

app = Flask(__name__)
hacking_assistant = HackingAssistantEngine()  # Proper initialization of the engine

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def authenticate(request):
    # Simple authentication example; replace with a real authentication mechanism
    api_key = request.headers.get("Authorization")
    if api_key != "your-secure-api-key":
        return False
    return True


@app.before_request
def before_request():
    if not authenticate(request):
        return jsonify({'status': 'error', 'message': 'Unauthorized'}), 401


@app.route('/api/add_target', methods=['POST'])
def add_target():
    try:
        target = request.json.get('target')
        if not target:
            logger.error('Target is missing in the request data.')
            return jsonify({'status': 'error', 'message': 'Target is required.'}), 400

        # Add detailed logging before calling the method
        logger.info(f"Attempting to add target: {target}")

        hacking_assistant.add_target(target)
        logger.info(f"Target {target} added successfully via API.")
        return jsonify({'status': 'success', 'message': f'Target {target} added successfully.'})

    except Exception as e:
        logger.error(f"Error adding target: {str(e)}")
        return jsonify({'status': 'error', 'message': f"Error adding target: {str(e)}"}), 500


@app.route('/api/run_scan', methods=['POST'])
def run_scan():
    try:
        hacking_assistant.run_scan()
        logger.info("Network scan initiated via API.")
        return jsonify({'status': 'success', 'message': 'Scan completed.'})
    except Exception as e:
        logger.error(f"Error running scan: {str(e)}")
        return jsonify({'status': 'error', 'message': f"Error running scan: {str(e)}"}), 500


@app.route('/api/run_info_gathering', methods=['POST'])
def run_info_gathering():
    try:
        hacking_assistant.run_info_gathering()
        logger.info("Info gathering initiated via API.")
        return jsonify({'status': 'success', 'message': 'Info gathering completed.'})
    except Exception as e:
        logger.error(f"Error during info gathering: {str(e)}")
        return jsonify({'status': 'error', 'message': f"Error during info gathering: {str(e)}"}), 500


@app.route('/api/run_vulnerability_scan', methods=['POST'])
def run_vulnerability_scan():
    try:
        hacking_assistant.run_vulnerability_scan()
        logger.info("Vulnerability scan initiated via API.")
        return jsonify({'status': 'success', 'message': 'Vulnerability scan completed.'})
    except Exception as e:
        logger.error(f"Error running vulnerability scan: {str(e)}")
        return jsonify({'status': 'error', 'message': f"Error running vulnerability scan: {str(e)}"}), 500


@app.route('/api/run_exploit', methods=['POST'])
def run_exploit():
    try:
        exploit = request.json.get('exploit')
        payload = request.json.get('payload')
        target = request.json.get('target')
        if not (exploit, payload, target):
            logger.error('Exploit, payload, and target are required.')
            return jsonify({'status': 'error', 'message': 'Exploit, payload, and target are required.'}), 400

        hacking_assistant.run_exploit(target, exploit, payload)
        logger.info(f"Exploit {exploit} executed on target {target} via API.")
        return jsonify({'status': 'success', 'message': 'Exploit completed.'})

    except Exception as e:
        logger.error(f"Error running exploit: {str(e)}")
        return jsonify({'status': 'error', 'message': f"Error running exploit: {str(e)}"}), 500


@app.route('/api/generate_report', methods=['POST'])
def generate_report():
    try:
        hacking_assistant.generate_report()
        logger.info("Report generation initiated via API.")
        return jsonify({'status': 'success', 'message': 'Report generated.'})
    except Exception as e:
        logger.error(f"Error generating report: {str(e)}")
        return jsonify({'status': 'error', 'message': f"Error generating report: {str(e)}"}), 500


@app.route('/api/schedule_scan', methods=['POST'])
def schedule_scan():
    try:
        target = request.json.get('target')
        interval = request.json.get('interval')
        if not (target and interval):
            logger.error('Target and interval are required.')
            return jsonify({'status': 'error', 'message': 'Target and interval are required.'}), 400

        hacking_assistant.schedule_scan(target, interval)
        logger.info(f"Scheduled scan for target {target} every {interval} minutes via API.")
        return jsonify(
            {'status': 'success', 'message': f'Scheduled scan for {target} every {interval} minutes successfully.'})

    except Exception as e:
        logger.error(f"Error scheduling scan: {str(e)}")
        return jsonify({'status': 'error', 'message': f"Error scheduling scan: {str(e)}"}), 500


@app.route('/api/run_phishing_attack', methods=['POST'])
def run_phishing_attack():
    try:
        target = request.json.get('target')
        if not target:
            logger.error('Target is required for phishing attack.')
            return jsonify({'status': 'error', 'message': 'Target is required.'}), 400

        hacking_assistant.run_phishing_attack(target)
        logger.info(f"Phishing attack initiated on target {target} via API.")
        return jsonify({'status': 'success', 'message': f'Phishing attack executed on {target}.'})

    except Exception as e:
        logger.error(f"Error running phishing attack: {str(e)}")
        return jsonify({'status': 'error', 'message': f"Error running phishing attack: {str(e)}"}), 500


@app.route('/api/run_social_engineering_attack', methods=['POST'])
def run_social_engineering_attack():
    try:
        target = request.json.get('target')
        if not target:
            logger.error('Target is required for social engineering attack.')
            return jsonify({'status': 'error', 'message': 'Target is required.'}), 400

        hacking_assistant.run_social_engineering_attack(target)
        logger.info(f"Social engineering attack initiated on target {target} via API.")
        return jsonify({'status': 'success', 'message': f'Social engineering attack executed on {target}.'})

    except Exception as e:
        logger.error(f"Error running social engineering attack: {str(e)}")
        return jsonify({'status': 'error', 'message': f"Error running social engineering attack: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(port=5000)
