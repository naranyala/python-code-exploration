# dep_ranker.py
import re
import subprocess
from collections import defaultdict
import networkx as nx
import matplotlib.pyplot as plt

def fetch_dependencies():
    """Parse local apt cache to get package dependencies"""
    cmd = ["apt-cache", "dumpavail"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    packages = defaultdict(list)
    current_pkg = None

    for line in result.stdout.splitlines():
        pkg_match = re.match(r"^Package: (.+)", line)
        dep_match = re.match(r"^Depends: (.+)", line)
        
        if pkg_match:
            current_pkg = pkg_match.group(1)
        if dep_match and current_pkg:
            # Simple split; real parsing should handle version constraints, ORs, etc.
            deps = dep_match.group(1).split(",")
            for dep in deps:
                dep_name = dep.strip().split()[0]  # ignore version
                packages[current_pkg].append(dep_name)
    
    return packages

def build_graph(packages):
    """Create a directed graph from package dependencies"""
    G = nx.DiGraph()
    for pkg, deps in packages.items():
        G.add_node(pkg)
        for dep in deps:
            G.add_edge(pkg, dep)  # pkg -> depends on -> dep
    return G

def rank_packages(G):
    """Rank packages using various centrality measures"""
    # In-degree: how many depend on this package (popularity)
    in_degree = nx.in_degree_centrality(G)
    
    # Betweenness: how critical it is in the graph
    try:
        betweenness = nx.betweenness_centrality(G, k=50)  # approx for speed
    except nx.NetworkXError:
        betweenness = {}

    # PageRank: Google-style importance
    pagerank = nx.pagerank(G)

    # Combine or show top packages
    print("Top 10 by In-Degree (most depended-on):")
    for pkg, score in sorted(in_degree.items(), key=lambda x: -x[1])[:10]:
        print(f"  {pkg}: {score:.4f}")

    print("\nTop 10 by PageRank (most influential):")
    for pkg, score in sorted(pagerank.items(), key=lambda x: -x[1])[:10]:
        print(f"  {pkg}: {score:.6f}")

def main():
    print("Fetching package dependencies...")
    packages = fetch_dependencies()
    print(f"Found {len(packages)} packages.")

    print("Building dependency graph...")
    G = build_graph(packages)

    print("Ranking packages...")
    rank_packages(G)

    # Optional: Draw a small subgraph
    # nx.draw(G.subgraph(list(G.nodes())[:30]), with_labels=True, node_size=50, font_size=8)
    # plt.show()

if __name__ == "__main__":
    main()
