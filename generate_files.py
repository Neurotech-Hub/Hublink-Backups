import os
import time
import random
import csv
from datetime import datetime
import shutil
import psutil
import string

# Hard-coded drive path - update this for your system
DRIVE_PATH = "/Volumes/HUBLINK"  # Update this path for your system

def get_drive_usage(path):
    """Get drive usage percentage"""
    usage = psutil.disk_usage(path)
    return (usage.used / usage.total) * 100

def generate_random_csv(size_bytes):
    """Generate CSV data of approximately specified size"""
    # Create header row
    headers = ['timestamp', 'sensor_id', 'temperature', 'humidity', 'pressure']
    
    # Calculate approximate number of rows needed to reach target size
    # Each row is roughly 50 bytes (varies with random values)
    num_rows = size_bytes // 50
    
    # Generate random data
    data = []
    for _ in range(num_rows):
        row = [
            datetime.now().isoformat(),
            f"SENSOR_{random.randint(1, 100):03d}",
            round(random.uniform(20, 30), 2),
            round(random.uniform(30, 90), 2),
            round(random.uniform(980, 1020), 2)
        ]
        data.append(row)
    
    return headers, data

def create_files(drive_path, target_usage=50):
    """Create files until drive is 50% full"""
    base_path = os.path.join(drive_path, 'data')
    os.makedirs(base_path, exist_ok=True)
    
    file_count = 0
    
    while get_drive_usage(drive_path) < target_usage:
        # Create timestamp-based directory
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S%f')[:17]  # Including milliseconds
        dir_path = os.path.join(base_path, timestamp)
        os.makedirs(dir_path, exist_ok=True)
        
        # Random file size between 10KB and 10MB
        file_size = random.randint(10 * 1024, 10 * 1024 * 1024)
        
        # Generate random filename
        filename = f"data_{timestamp}_{file_size//1024}KB.csv"
        file_path = os.path.join(dir_path, filename)
        
        # Generate and save file
        headers, data = generate_random_csv(file_size)
        
        with open(file_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(data)
        
        file_count += 1
        current_usage = get_drive_usage(drive_path)
        print(f"Created file {file_count}: {filename}")
        print(f"Current drive usage: {current_usage:.1f}%")

if __name__ == "__main__":
    if not os.path.exists(DRIVE_PATH):
        print(f"Error: Drive path {DRIVE_PATH} not found!")
        exit(1)
        
    print(f"Starting file generation on {DRIVE_PATH}")
    print(f"Initial drive usage: {get_drive_usage(DRIVE_PATH):.1f}%")
    
    try:
        create_files(DRIVE_PATH)
        print("File generation complete!")
    except KeyboardInterrupt:
        print("\nProcess interrupted by user")
    except Exception as e:
        print(f"Error occurred: {str(e)}") 