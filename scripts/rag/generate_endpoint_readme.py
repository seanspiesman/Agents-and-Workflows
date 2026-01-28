
import os
import sys
import re

# Ensure we can import rag_core
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from rag_core import RAGSystem

# Heuristic patterns for endpoints
PATTERNS = {
    "MCP Tool Definitions": [
        r'@server\.list_tools\(\)',
        r'@server\.call_tool\(\)',
        r'types\.Tool\(\s*name=["\'](.*?)["\']'
    ],
    "External API Calls (URLs)": [
        r'https?://[^\s"\')]+'
    ]
}

def scan_files_heuristically(root_dir):
    results = []
    print(f"Scanning files in {root_dir} for endpoint patterns...")
    
    # Simple walk
    for root, _, files in os.walk(root_dir):
        if '.git' in root or 'node_modules' in root or '.venv' in root:
            continue
            
        for file in files:
            ext = os.path.splitext(file)[1]
            if ext not in ['.py', '.js', '.ts', '.cs', '.md', '.sh']:
                continue
                
            path = os.path.join(root, file)
            try:
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    
                for tech, patterns in PATTERNS.items():
                    for pat in patterns:
                        matches = re.finditer(pat, content)
                        for m in matches:
                            if tech == "MCP Tool Definitions" and "types.Tool" in pat:
                                endpoint = f"Tool: {m.group(1)}"
                            elif tech == "External API Calls (URLs)":
                                endpoint = m.group(0)
                            else:
                                endpoint = m.group(0)

                            # Get line context
                            start = max(0, m.start() - 50)
                            end = min(len(content), m.end() + 50)
                            snippet = content[start:end].replace('\n', ' ')
                            
                            results.append({
                                'type': 'heuristic',
                                'tech': tech,
                                'source': os.path.relpath(path, root_dir),
                                'content': f"Found: {endpoint}\nContext: ...{snippet}...",
                                'endpoint': endpoint
                            })
            except Exception as e:
                pass
    return results

def main():
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    
    # 1. Try RAG (Skipped or Minimal due to connectivity)
    # 2. Heuristic fallback
    heuristic_results = scan_files_heuristically(root_dir)
    
    # 3. Generate README
    output_path = os.path.join(root_dir, "ENDPOINTS_README.md")
    
    with open(output_path, "w") as f:
        f.write("# Analyzed Endpoints\n\n")
        f.write("This document lists API endpoints and external service calls found via heuristic scanning.\n\n")
        f.write("> [!NOTE]\n> RAG analysis was skipped/failed due to connectivity issues. Showing heuristic results.\n\n")
            
        if heuristic_results:
            f.write("## Detected Endpoints & Calls\n\n")
            # Group by category, then file
            by_tech = {}
            for item in heuristic_results:
                t = item['tech']
                if t not in by_tech: by_tech[t] = []
                by_tech[t].append(item)
            
            for tech, items in by_tech.items():
                f.write(f"### {tech}\n\n")
                
                # Deduplicate by endpoint string
                seen = set()
                unique_items = []
                for i in items:
                    if i['endpoint'] not in seen:
                        seen.add(i['endpoint'])
                        unique_items.append(i)
                
                for item in unique_items:
                    f.write(f"- `{item['endpoint']}` (Found in `{item['source']}`)\n")
        else:
            f.write("No endpoints detected via heuristics.\n")
            
    print(f"Generated README at {output_path}")

if __name__ == "__main__":
    main()
