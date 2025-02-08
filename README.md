# Database Downloader

A secure utility to download the accounts database from Render server using SCP.

## Prerequisites

- Python 3.7 or higher
- SSH key pair configured on your system
- SSH key added to Render dashboard

## SSH Key Setup

1. **Check for existing SSH key**:
   ```bash
   cat ~/.ssh/id_rsa.pub
   ```

2. **If no key exists, generate one**:
   ```bash
   ssh-keygen -t rsa -b 4096
   ```

3. **Add your key to Render**:
   - Copy your public key:
     ```bash
     pbcopy < ~/.ssh/id_rsa.pub
     ```
   - Go to Render dashboard → Account Settings → SSH Keys
   - Click "New Key" and paste your public key

## Setup

1. **Create and activate virtual environment**

   Windows:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

   Unix/MacOS:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**
   - Verify `.env` file exists with the SSH address:
     ```
     SSH_ADDRESS=srv-cs9a9raj1k6c73fktqfg@ssh.oregon.render.com
     ```

## Usage

1. Ensure your virtual environment is activated
2. Run the script:
   ```bash
   python download_db.py
   ```
3. The script will:
   - Test SSH connectivity
   - Create a timestamped backup file
   - Download the database using SCP
   - Show progress and any errors

## Troubleshooting

If you get SSH connection errors:
1. Verify your SSH key is in the default location (`~/.ssh/id_rsa` and `~/.ssh/id_rsa.pub`)
2. Check if your key is added to Render dashboard
3. Test SSH connection manually:
   ```bash
   ssh srv-cs9a9raj1k6c73fktqfg@ssh.oregon.render.com
   ```

## File Structure 