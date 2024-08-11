import os

# Configuration settings for the hacking assistant
NMAP_ARGUMENTS = '-sV -O -T4'
OPENVAS_CMD = 'openvas'
METASPLOIT_CMD = 'msfconsole'
DB_PATH = os.getenv('DB_PATH', 'database/hacking_assistant.db')
LOG_PATH = os.getenv('LOG_PATH', 'logs/hacking_assistant.log')
API_PORT = int(os.getenv('API_PORT', 5000))
SMTP_SERVER = os.getenv('SMTP_SERVER')
SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
SMTP_USER = os.getenv('SMTP_USER')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')

# Ensure critical configuration is set
assert SMTP_SERVER and SMTP_USER and SMTP_PASSWORD, "SMTP configuration is missing!"
