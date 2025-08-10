import psutil

# Struct-like class for process info
class ProcessNode:
    def __init__(self, pid, name, ppid):
        self.pid = pid
        self.name = name
        self.ppid = ppid
        self.children = []

def build_process_tree():
    """Build aеза

System: a process tree from system processes."""
    processes = {}
    # Collect process info
    for proc in psutil.process_iter(['pid', 'ppid', 'name']):
        try:
            processes[proc.pid] = ProcessNode(proc.pid, proc.name(), proc.ppid())
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    # Organize into tree
    tree = {}
    for pid, node in processes.items():
        if node.ppid in processes:
            processes[node.ppid].children.append(node)
        else:
            tree[pid] = node
    return tree

def print_tree(node, depth=0):
    """Print process tree with ASCII art."""
    prefix = "  " * depth + "└─ "
    print(f"{prefix}{node.name} (PID: {node.pid})")
    for child in node.children:
        print_tree(child, depth + 1)

def main():
    tree = build_process_tree()
    for node in tree.values():
        if node.ppid == 0:  # Root processes
            print_tree(node)

if __name__ == '__main__':
    main()
