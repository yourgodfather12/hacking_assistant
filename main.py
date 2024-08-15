import os
import dotenv
from flask import Flask, render_template, request, jsonify, send_file
from flask_socketio import SocketIO, emit
from flask_sqlalchemy import SQLAlchemy
import paramiko
import logging
import nmap
import subprocess
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Load environment variables from .env file
dotenv.load_dotenv()

# Configurations from environment variables
LOG_PATH = os.getenv( 'LOG_PATH', 'app.log' )
API_PORT = int( os.getenv( 'API_PORT', 5000 ) )
LINODE_HOST = os.getenv( 'LINODE_HOST' )
LINODE_PORT = int( os.getenv( 'LINODE_PORT', 22 ) )
LINODE_USER = os.getenv( 'LINODE_USER' )
LINODE_PASSWORD = os.getenv( 'LINODE_PASSWORD' )

# Using an absolute path for DB_PATH
DB_PATH = os.path.abspath( os.getenv( 'DB_PATH', 'app.db' ) )

# Ensure the directory for the database exists
db_dir = os.path.dirname( DB_PATH )
if db_dir and not os.path.exists( db_dir ):
    os.makedirs( db_dir )

# Setup logging
logging.basicConfig( filename=LOG_PATH, level=logging.ERROR, format='%(asctime)s %(levelname)s: %(message)s' )

# Initialize Flask app and SocketIO
app = Flask( __name__ )
socketio = SocketIO( app )

# Setup Flask-Limiter for rate limiting
limiter = Limiter( get_remote_address, app=app, default_limits=["200 per day", "50 per hour"] )

# SQLAlchemy configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy( app )


# Define database models
class Target( db.Model ):
    id = db.Column( db.Integer, primary_key=True )
    target = db.Column( db.String( 100 ), unique=True, nullable=False )


class ScanResult( db.Model ):
    id = db.Column( db.Integer, primary_key=True )
    target = db.Column( db.String( 100 ), nullable=False )
    type = db.Column( db.String( 50 ), nullable=False )
    result = db.Column( db.Text, nullable=False )


# Setup SSH client
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy( paramiko.AutoAddPolicy() )


# Database operations
def add_target_to_db(target):
    try:
        if not Target.query.filter_by( target=target ).first():
            new_target = Target( target=target )
            db.session.add( new_target )
            db.session.commit()
    except Exception as e:
        logging.error( f"Error adding target to database: {e}" )
        db.session.rollback()


def get_targets_from_db():
    try:
        targets = Target.query.all()
        if not targets:
            logging.warning( "No targets found in the database." )
            return []
        return [target.target for target in targets]
    except Exception as e:
        logging.error( f"Error fetching targets from database: {e}" )
        return []


def store_scan_result(target, scan_type, result):
    try:
        new_result = ScanResult( target=target, type=scan_type, result=result )
        db.session.add( new_result )
        db.session.commit()
    except Exception as e:
        logging.error( f"Error storing scan result in database: {e}" )
        db.session.rollback()


def get_scan_results():
    try:
        return ScanResult.query.all()
    except Exception as e:
        logging.error( f"Error fetching scan results from database: {e}" )
        return []


@app.errorhandler( 404 )
def not_found_error(error):
    return jsonify( {'status': 'error', 'message': 'Resource not found'} ), 404


@app.errorhandler( 500 )
def internal_error(error):
    return jsonify( {'status': 'error', 'message': 'Internal server error'} ), 500


@app.route( '/' )
@limiter.limit( "5 per minute" )
def dashboard():
    return render_template( 'dashboard.html' )


@app.route( '/connect_terminal', methods=['POST'] )
@limiter.limit( "10 per hour" )
def connect_terminal():
    try:
        ssh_client.connect( LINODE_HOST, port=LINODE_PORT, username=LINODE_USER, password=LINODE_PASSWORD )
        return jsonify( {'status': 'success', 'message': 'Connected to Linode server.'} )
    except paramiko.SSHException as e:
        logging.error( f"SSH connection error: {e}" )
        return jsonify( {'status': 'error', 'message': 'SSH connection failed.'} ), 500
    except Exception as e:
        logging.error( f"Unexpected error: {e}" )
        return jsonify( {'status': 'error', 'message': str( e )} ), 500


@socketio.on( 'run_command' )
def handle_command(data):
    command = data['command']
    try:
        stdin, stdout, stderr = ssh_client.exec_command( command )
        output = stdout.read().decode()
        emit( 'command_output', {'output': output} )
    except Exception as e:
        logging.error( f"Command execution error: {e}" )
        emit( 'command_output', {'output': f'Error: {str( e )}'} )


@app.route( '/add_target', methods=['POST'] )
@limiter.limit( "20 per day" )
def add_target():
    target = request.json.get( 'target' )
    if not target:
        return jsonify( {'status': 'error', 'message': 'Target is required.'} ), 400
    add_target_to_db( target )
    return jsonify( {'status': 'success', 'message': f'Target {target} added successfully.'} )


@app.route( '/run_scan', methods=['POST'] )
@limiter.limit( "10 per day" )
def run_scan():
    targets = get_targets_from_db()
    if not targets:
        return jsonify( {'status': 'error', 'message': 'No targets available for scanning.'} ), 400

    nm = nmap.PortScanner()
    for target in targets:
        try:
            nm.scan( hosts=target, arguments=NMAP_ARGUMENTS )
            scan_results = nm[target].all_tcp() if nm.all_hosts() else {}
            store_scan_result( target, 'network_scan', str( scan_results ) )
        except nmap.PortScannerError as e:
            logging.error( f"Nmap scan error for {target}: {e}" )
            store_scan_result( target, 'network_scan', f"Error: {str( e )}" )

    return jsonify( {'status': 'success', 'message': 'Network scan completed.'} )


@app.route( '/run_info_gathering', methods=['POST'] )
@limiter.limit( "10 per day" )
def run_info_gathering():
    targets = get_targets_from_db()
    if not targets:
        return jsonify( {'status': 'error', 'message': 'No targets available for information gathering.'} ), 400

    for target in targets:
        try:
            whois_result = subprocess.run( ['whois', target], capture_output=True, text=True ).stdout
            store_scan_result( target, 'info_gathering', whois_result )
        except subprocess.SubprocessError as e:
            logging.error( f"Info gathering error for {target}: {e}" )
            store_scan_result( target, 'info_gathering', f"Error: {str( e )}" )

    return jsonify( {'status': 'success', 'message': 'Information gathering completed.'} )


@app.route( '/run_vulnerability_scan', methods=['POST'] )
@limiter.limit( "10 per day" )
def run_vulnerability_scan():
    targets = get_targets_from_db()
    if not targets:
        return jsonify( {'status': 'error', 'message': 'No targets available for vulnerability scanning.'} ), 400

    for target in targets:
        try:
            # Simulate a vulnerability scan with mocked data
            vuln_results = f"Vulnerability scan results for {target} (mocked data)"
            store_scan_result( target, 'vulnerability_scan', vuln_results )
        except Exception as e:
            logging.error( f"Vulnerability scan error for {target}: {e}" )
            store_scan_result( target, 'vulnerability_scan', f"Error: {str( e )}" )

    return jsonify( {'status': 'success', 'message': 'Vulnerability scan completed.'} )


@app.route( '/generate_report', methods=['POST'] )
@limiter.limit( "5 per day" )
def generate_report():
    results = get_scan_results()
    if not results:
        return jsonify( {'status': 'error', 'message': 'No scan results available for the report.'} ), 400

    report_path = "report.pdf"
    c = canvas.Canvas( report_path, pagesize=letter )
    width, height = letter
    y = height - 50
    try:
        for result in results:
            c.drawString( 100, y, f"Target: {result.target}, Type: {result.type}, Result: {result.result[:100]}..." )
            y -= 20
            if y < 100:
                c.showPage()
                y = height - 50
        c.save()
    except Exception as e:
        logging.error( f"Error generating report: {e}" )
        return jsonify( {'status': 'error', 'message': 'Failed to generate report.'} ), 500

    return jsonify( {'status': 'success', 'message': 'Report generated successfully.'} )


@app.route( '/targets', methods=['GET'] )
@limiter.limit( "20 per minute" )
def view_targets():
    targets = get_targets_from_db()
    if not targets:
        return jsonify( {'status': 'error', 'message': 'No targets found.'} ), 404
    return jsonify( {'targets': targets} )


@app.route( '/results', methods=['GET'] )
@limiter.limit( "20 per minute" )
def view_results():
    results = get_scan_results()
    if not results:
        return jsonify( {'status': 'error', 'message': 'No scan results found.'} ), 404
    return jsonify(
        {'results': [{'target': result.target, 'type': result.type, 'result': result.result} for result in results]} )


@app.route( '/logs', methods=['GET'] )
@limiter.limit( "5 per minute" )
def view_logs():
    if os.path.exists( LOG_PATH ):
        with open( LOG_PATH, 'r' ) as f:
            logs = f.read()
    else:
        logs = "No logs available."
    return jsonify( {'logs': logs} )


@app.route( '/download_report', methods=['GET'] )
@limiter.limit( "5 per minute" )
def download_report():
    report_path = "report.pdf"
    if not os.path.exists( report_path ):
        return jsonify( {'status': 'error', 'message': 'No report available for download.'} ), 404
    return send_file( report_path, as_attachment=True )


@app.route( '/update_config', methods=['POST'] )
@limiter.limit( "5 per day" )
def update_config():
    nmap_args = request.json.get( 'nmapArguments' )
    if not nmap_args:
        return jsonify( {'status': 'error', 'message': 'Nmap arguments are required.'} ), 400

    global NMAP_ARGUMENTS
    NMAP_ARGUMENTS = nmap_args
    return jsonify( {'status': 'success', 'message': 'Configuration updated successfully.'} )


if __name__ == '__main__':
    # Initialize database
    with app.app_context():
        db.create_all()

    socketio.run( app, port=API_PORT )
