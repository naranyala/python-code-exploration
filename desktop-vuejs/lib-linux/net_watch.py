import psutil

def get_network_connections():
    """Collect active network connections."""
    connections = []
    try:
        for conn in psutil.net_connections(kind='inet'):
            if conn.laddr and conn.raddr:  # Only include connections with local/remote addresses
                connections.append({
                    'local': f"{conn.laddr.ip}:{conn.laddr.port}",
                    'remote': f"{conn.raddr.ip}:{conn.raddr.port}",
                    'status': conn.status,
                    'pid': conn.pid
                })
    except (psutil.AccessDenied, psutil.NoSuchProcess):
        pass
    return connections

def print_connection_map(connections):
    """Print a text-based map of network connections."""
    print("Network Connections:")
    for conn in connections:
        print(f"{conn['local']} -> {conn['remote']} [{conn['status']}] (PID: {conn['pid']})")

def main():
    connections = get_network_connections()
    print_connection_map(connections)

if __name__ == '__main__':
    main()
