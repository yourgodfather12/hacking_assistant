import os

# Linode SSH Configuration
LINODE_HOST = os.getenv('LINODE_HOST', 'your-linode-ip')
LINODE_PORT = int(os.getenv('LINODE_PORT', 22))
LINODE_USER = os.getenv('LINODE_USER', 'your-username')
LINODE_PASSWORD = os.getenv('LINODE_PASSWORD', 'your-password')

# SMTP Configuration
SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.example.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
SMTP_USER = os.getenv('SMTP_USER', 'your-email@example.com')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', 'your-email-password')

# Other configurations
NMAP_ARGUMENTS = '-sV -O -T4'
DB_PATH = os.getenv('DB_PATH', 'database/hacking_assistant.db')
LOG_PATH = os.getenv('LOG_PATH', 'logs/hacking_assistant.log')
API_PORT = int(os.getenv('API_PORT', 5000))

# Metasploit Configuration
METASPLOIT_CMD = os.getenv('METASPLOIT_CMD', 'msfconsole')

# Ensure database and log directories exist
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
