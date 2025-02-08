import os
from dotenv import load_dotenv
import subprocess
from datetime import datetime

def test_ssh_connection(ssh_address):
    """Test SSH connection before attempting file transfer"""
    test_cmd = f'ssh {ssh_address} "echo Connection successful"'
    process = subprocess.Popen(test_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    
    if process.returncode != 0:
        print("\nSSH Connection Test Failed:")
        print("1. Verify your SSH key is added to Render:")
        print("   - Check ~/.ssh/id_rsa.pub exists")
        print("   - Ensure key is added to Render dashboard")
        print("\nDetailed error:")
        print(stderr.decode())
        return False
    return True

def download_database():
    load_dotenv()
    ssh_address = os.getenv('SSH_ADDRESS')
    
    if not ssh_address:
        raise EnvironmentError("SSH_ADDRESS not found in .env file")
    
    # Test SSH connection first
    print("Testing SSH connection...")
    if not test_ssh_connection(ssh_address):
        raise Exception("SSH connection failed - please check your SSH key setup")
    
    # Create timestamp for the filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    local_filename = f'accounts_{timestamp}.db'
    
    # Construct the scp command
    remote_path = '/var/data/accounts.db'
    scp_cmd = f'scp -s {ssh_address}:{remote_path} {local_filename}'
    
    print(f"Initiating secure copy...")
    process = subprocess.Popen(scp_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    
    if process.returncode != 0:
        print("Error during file transfer:")
        print(stderr.decode())
        raise Exception("SCP transfer failed")
    
    print(f"File downloaded successfully as: {local_filename}")

if __name__ == "__main__":
    download_database() 