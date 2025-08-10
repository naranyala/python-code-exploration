import psutil
import time

def collect_cpu_usage(duration, interval):
    """Collect CPU usage data for a given duration (seconds) at given intervals."""
    usage = []
    end_time = time.time() + duration
    while time.time() < end_time:
        usage.append(psutil.cpu_percent(interval=interval))
        time.sleep(interval)
    return usage

def sparkline(data, width=50):
    """Generate a sparkline from CPU usage data."""
    if not data:
        return ""
    max_val = max(data)
    if max_val == 0:
        return "▁" * width
    chars = "▁▂▃▅▆▇"
    scaled = [int((x / max_val) * (len(chars) - 1)) for x in data]
    return "".join(chars[i] for i in scaled[:width])

def main():
    # Collect CPU usage for 30 seconds, every 1 second
    usage = collect_cpu_usage(30, 1)
    print("CPU Usage History:")
    print(sparkline(usage))
    print(f"Average: {sum(usage) / len(usage):.1f}%")

if __name__ == '__main__':
    main()
