#!/usr/bin/env python3
"""
Scan apt package dependency graph using `apt-cache depends` and rank packages
by the number of distinct packages reachable from each package (transitive closure size).

Requires:
  - networkx (pip install networkx)
  - apt-cache available (Debian/Ubuntu)
"""

import subprocess
import shlex
import sys
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, Set, List, Optional
import networkx as nx
import re

# CONFIG
MAX_WORKERS = 8
INCLUDE_RECOMMENDS = False

# Progress tracking
class ProgressTracker:
    def __init__(self, total: int, description: str = "Processing"):
        self.total = total
        self.current = 0
        self.description = description
        self.start_time = time.time()
        self.lock = threading.Lock()
    
    def update(self, increment: int = 1):
        with self.lock:
            self.current += increment
            self._print_progress()
    
    def _print_progress(self):
        if self.total == 0:
            return
            
        percent = (self.current / self.total) * 100
        elapsed = time.time() - self.start_time
        
        if self.current > 0:
            eta = (elapsed / self.current) * (self.total - self.current)
            eta_str = f"ETA: {eta:.1f}s"
        else:
            eta_str = "ETA: --"
        
        # Create progress bar
        bar_length = 30
        filled = int(bar_length * self.current / self.total)
        bar = "█" * filled + "░" * (bar_length - filled)
        
        rate = self.current / elapsed if elapsed > 0 else 0
        
        print(f"\r{self.description}: [{bar}] {self.current}/{self.total} "
              f"({percent:5.1f}%) {rate:.1f}/s {eta_str}", end="", flush=True)
        
        if self.current >= self.total:
            print()  # New line when complete

# Precompiled regex for version stripping
VERSION_PATTERN = re.compile(r'^(\S+).*')


def run_cmd_with_progress(cmd: str, description: str = "") -> str:
    """Execute command with progress indication."""
    if description:
        print(f"Running: {description}...", end=" ", flush=True)
    
    start_time = time.time()
    
    try:
        result = subprocess.run(
            shlex.split(cmd), 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            text=True,
            timeout=60
        )
        
        elapsed = time.time() - start_time
        
        if result.returncode != 0:
            if description:
                print(f"FAILED ({elapsed:.1f}s)")
            raise RuntimeError(f"Command failed: {cmd}\n{result.stderr}")
        
        if description:
            print(f"OK ({elapsed:.1f}s)")
            
        return result.stdout
        
    except subprocess.TimeoutExpired:
        if description:
            print("TIMEOUT")
        raise RuntimeError(f"Command timed out: {cmd}")


def list_installed_packages() -> List[str]:
    """Get only installed packages with progress indication."""
    try:
        out = run_cmd_with_progress("dpkg-query -W -f='${Package}\\n'", 
                                   "Querying installed packages")
        packages = [line.strip() for line in out.splitlines() if line.strip()]
        print(f"Found {len(packages)} installed packages")
        return packages
    except RuntimeError:
        print("Warning: dpkg-query failed, falling back to all packages")
        out = run_cmd_with_progress("apt-cache pkgnames", 
                                   "Querying all available packages")
        packages = [line.strip() for line in out.splitlines() if line.strip()]
        print(f"Found {len(packages)} available packages")
        return packages


def parse_apt_cache_depends_output(text: str) -> Set[str]:
    """Optimized parsing with early filtering and regex."""
    deps = set()
    dependency_types = {"Depends:", "PreDepends:"}
    if INCLUDE_RECOMMENDS:
        dependency_types.update({"Recommends:", "Suggests:"})
    
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
            
        dep_type = next((dt for dt in dependency_types if line.startswith(dt)), None)
        if not dep_type:
            continue
            
        rest = line[len(dep_type):].strip()
        if not rest:
            continue
            
        for alternative in rest.split("|"):
            match = VERSION_PATTERN.match(alternative.strip())
            if match:
                pkgname = match.group(1)
                if pkgname and not pkgname.startswith('<'):
                    deps.add(pkgname)
    
    return deps


def get_deps_batch_with_progress(packages: List[str]) -> Dict[str, Set[str]]:
    """Batch process with detailed progress tracking."""
    results = {}
    progress = ProgressTracker(len(packages), "Fetching dependencies")
    
    def fetch_single_pkg(pkg: str) -> tuple[str, Set[str]]:
        try:
            # Show individual command for debugging (optional)
            # print(f"\nFetching deps for: {pkg}", file=sys.stderr)
            
            out = subprocess.run(
                ["apt-cache", "depends", pkg],
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                text=True,
                timeout=30
            )
            
            if out.returncode != 0:
                progress.update()
                return pkg, set()
                
            deps = parse_apt_cache_depends_output(out.stdout)
            progress.update()
            return pkg, deps
            
        except Exception as e:
            progress.update()
            return pkg, set()
    
    # Show batch processing details
    print(f"Processing {len(packages)} packages with {MAX_WORKERS} workers...")
    
    failed_packages = []
    
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(fetch_single_pkg, pkg): pkg for pkg in packages}
        
        for future in as_completed(futures):
            pkg, deps = future.result()
            results[pkg] = deps
            
            if not deps and pkg in packages:  # Track failures
                failed_packages.append(pkg)
    
    print()  # New line after progress bar
    
    if failed_packages:
        print(f"Warning: Failed to fetch dependencies for {len(failed_packages)} packages")
        if len(failed_packages) <= 10:
            print("Failed packages:", ", ".join(failed_packages))
    
    return results


def build_graph_with_progress(packages: List[str]) -> nx.DiGraph:
    """Build graph with detailed progress tracking."""
    print("\n=== Building Dependency Graph ===")
    
    G = nx.DiGraph()
    print(f"Initializing graph with {len(packages)} package nodes...")
    G.add_nodes_from(packages)
    
    # Fetch dependencies with progress
    dep_cache = get_deps_batch_with_progress(packages)
    
    # Process edges with progress
    print("Processing dependency relationships...")
    edges_to_add = []
    new_nodes = set()
    edge_progress = ProgressTracker(len(dep_cache), "Building edges")
    
    for pkg, deps in dep_cache.items():
        for dep in deps:
            edges_to_add.append((pkg, dep))
            if dep not in G:
                new_nodes.add(dep)
        edge_progress.update()
    
    print()  # New line after progress
    
    if new_nodes:
        print(f"Adding {len(new_nodes)} new dependency nodes...")
        G.add_nodes_from(new_nodes)
    
    print(f"Adding {len(edges_to_add)} dependency edges...")
    G.add_edges_from(edges_to_add)
    
    print(f"Graph complete: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
    return G


def compute_reachable_counts_with_progress(G: nx.DiGraph, packages: List[str]) -> Dict[str, int]:
    """Compute reachable counts with progress tracking."""
    print("\n=== Computing Transitive Closures ===")
    
    counts = {}
    progress = ProgressTracker(len(packages), "Computing reachability")
    
    for pkg in packages:
        if pkg not in G:
            counts[pkg] = 0
        else:
            try:
                reachable = nx.descendants(G, pkg)
                counts[pkg] = len(reachable)
            except nx.NetworkXError:
                counts[pkg] = 0
        
        progress.update()
    
    print()  # New line after progress
    return counts


def main(top_n: int = 50):
    print("=== APT Package Dependency Analyzer ===")
    start_time = time.time()
    
    # Step 1: Get packages
    packages = list_installed_packages()
    
    # Step 2: Build graph
    G = build_graph_with_progress(packages)
    
    # Step 3: Compute metrics
    counts = compute_reachable_counts_with_progress(G, packages)
    
    # Step 4: Rank and analyze
    print("\n=== Ranking Packages ===")
    ranked = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    
    # Compute PageRank for top packages
    print("Computing PageRank for top packages...")
    top_packages = {name for name, _ in ranked[:min(top_n * 2, len(ranked))]}
    subgraph = G.subgraph(top_packages)
    
    try:
        pagerank = nx.pagerank(subgraph, alpha=0.85, max_iter=100)
        print("PageRank computation complete")
    except (nx.PowerIterationFailedToConverge, nx.NetworkXError) as e:
        print(f"PageRank failed: {e}")
        pagerank = {pkg: 0.0 for pkg in top_packages}
    
    # Results
    total_time = time.time() - start_time
    print(f"\n=== Results (Total time: {total_time:.1f}s) ===")
    print(f"{'Package':<40} {'Reachable':<10} {'Out':<5} {'In':<5} {'PageRank':<10}")
    print("=" * 75)
    
    for i, (name, cnt) in enumerate(ranked[:top_n], 1):
        pr_score = pagerank.get(name, 0.0)
        out_deg = G.out_degree(name) if name in G else 0
        in_deg = G.in_degree(name) if name in G else 0
        print(f"{name:<40} {cnt:<10} {out_deg:<5} {in_deg:<5} {pr_score:<10.6f}")


if __name__ == "__main__":
    top_n = 30
    if len(sys.argv) > 1:
        try:
            top_n = int(sys.argv[1])
        except ValueError:
            print(f"Warning: Invalid number '{sys.argv[1]}', using default {top_n}")
    
    try:
        main(top_n)
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}", file=sys.stderr)
        sys.exit(1)
