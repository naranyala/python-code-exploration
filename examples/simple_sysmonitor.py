import psutil
import time
import csv
from datetime import datetime

def get_system_stats():
    """Collect system resource metrics."""
    return {
        'cpu_percent': psutil.cpu_percent(interval=1),
        'memory_percent': psutil.virtual_memory().percent,
        'disk_percent': psutil.disk_usage('/').percent
    }

def log_stats(filename):
    """Log stats to a CSV file."""
    stats = get_system_stats()
    with open(filename, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([datetime.now(), stats['cpu_percent'], stats['memory_percent'], stats['disk_percent']])

def display_stats():
    """Display real-time stats."""
    while True:
        stats = get_system_stats()
        print(f"\rCPU: {stats['cpu_percent']}%, Memory: {stats['memory_percent']}%, Disk: {stats['disk_percent']}%", end='')
        time.sleep(1)

def main():
    # Initialize CSV with headers
    with open('system_stats.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Timestamp', 'CPU (%)', 'Memory (%)', 'Disk (%)'])
    
    # Log stats every 5 seconds for 30 seconds
    for _ in range(6):
        log_stats('system_stats.csv')
        time.sleep(5)

if __name__ == '__main__':
    main()
