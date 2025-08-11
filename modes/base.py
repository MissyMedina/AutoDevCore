"""
Base Mode Class for AutoDevCore with Advanced Thought Trail Visualization
"""

import json
import os
import base64
from datetime import datetime
from pathlib import Path
from abc import ABC, abstractmethod
from typing import Dict, List, Any


class BaseMode(ABC):
    """Base class for all AutoDevCore modes with advanced thought trail visualization."""

    def __init__(self, output_dir: str, verbose: bool = False):
        self.output_dir = Path(output_dir)
        self.verbose = verbose
        self.log_file = self.output_dir / "autodevcore.log"
        self.thought_trail = []

        # Ensure output directory exists
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def log_thought(self, agent: str, thought: str, data: dict = None):
        """Log a thought from an agent."""
        thought_entry = {
            "timestamp": datetime.now().isoformat(),
            "agent": agent,
            "thought": thought,
            "data": data or {},
            "id": len(self.thought_trail),
        }

        self.thought_trail.append(thought_entry)

        if self.verbose:
            print(f"[{agent}] {thought}")
            if data:
                print(f"  Data: {json.dumps(data, indent=2)}")

    def save_thought_trail(self):
        """Save the thought trail to JSON file and generate visualizations."""
        trail_file = self.output_dir / "thought_trail.json"
        with open(trail_file, "w") as f:
            json.dump(self.thought_trail, f, indent=2)

        print(f"💭 Thought trail saved to: {trail_file}")

        # Generate enhanced visualizations
        self.generate_mermaid_diagram()
        self.generate_interactive_html_report()

    def generate_mermaid_diagram(self):
        """Generate an enhanced Mermaid diagram from the thought trail."""
        if not self.thought_trail:
            return

        mermaid_content = "graph TD\n"

        # Color coding for different agents
        agent_colors = {
            "ComposerAgent": "#FF6B6B",
            "PRDWriterAgent": "#4ECDC4",
            "CodeGeneratorAgent": "#45B7D1",
            "READMEWriterAgent": "#96CEB4",
            "SecurityGeneratorAgent": "#FFEAA7",
            "BlueprintAgent": "#DDA0DD",
            "JournalAgent": "#98D8C8",
            "ScoreAgent": "#F7DC6F",
        }

        for i, thought in enumerate(self.thought_trail):
            node_id = f"A{i}"
            agent = thought["agent"]
            thought_text = (
                thought["thought"][:40] + "..."
                if len(thought["thought"]) > 40
                else thought["thought"]
            )

            # Get color for agent
            color = agent_colors.get(agent, "#E0E0E0")

            mermaid_content += f'    {node_id}["{agent}<br/>{thought_text}"]\n'
            mermaid_content += f"    style {node_id} fill:{color}\n"

            if i > 0:
                mermaid_content += f"    A{i-1} --> {node_id}\n"

        mermaid_file = self.output_dir / "thought_trail.md"
        with open(mermaid_file, "w") as f:
            f.write("# AutoDevCore Thought Trail Visualization\n\n")
            f.write("## Agent Reasoning Flow\n\n")
            f.write("```mermaid\n")
            f.write(mermaid_content)
            f.write("```\n\n")

            # Add timeline view
            f.write("## Timeline View\n\n")
            f.write("| Timestamp | Agent | Thought |\n")
            f.write("|-----------|-------|--------|\n")
            for thought in self.thought_trail:
                timestamp = thought["timestamp"].split("T")[1][:8]  # HH:MM:SS
                agent = thought["agent"]
                thought_text = (
                    thought["thought"][:60] + "..."
                    if len(thought["thought"]) > 60
                    else thought["thought"]
                )
                f.write(f"| {timestamp} | {agent} | {thought_text} |\n")

        print(f"📊 Enhanced Mermaid diagram saved to: {mermaid_file}")

    def generate_interactive_html_report(self):
        """Generate an interactive HTML report for the thought trail."""
        if not self.thought_trail:
            return

        html_content = self._generate_html_template()

        html_file = self.output_dir / "thought_trail.html"
        with open(html_file, "w") as f:
            f.write(html_content)

        print(f"🌐 Interactive HTML report saved to: {html_file}")

    def _generate_html_template(self) -> str:
        """Generate the HTML template for interactive visualization."""
        # Convert thought trail to JSON for JavaScript
        thought_trail_json = json.dumps(self.thought_trail, indent=2)

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AutoDevCore Thought Trail Visualization</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        .header h1 {{
            margin: 0;
            font-size: 2.5em;
            font-weight: 300;
        }}
        .header p {{
            margin: 10px 0 0 0;
            opacity: 0.9;
            font-size: 1.1em;
        }}
        .content {{
            padding: 30px;
        }}
        .section {{
            margin-bottom: 40px;
            padding: 20px;
            border-radius: 10px;
            background: #f8f9fa;
            border-left: 4px solid #667eea;
        }}
        .section h2 {{
            color: #333;
            margin-top: 0;
            font-size: 1.5em;
        }}
        .timeline {{
            position: relative;
            padding-left: 30px;
        }}
        .timeline::before {{
            content: '';
            position: absolute;
            left: 15px;
            top: 0;
            bottom: 0;
            width: 2px;
            background: #667eea;
        }}
        .timeline-item {{
            position: relative;
            margin-bottom: 20px;
            padding: 15px;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .timeline-item::before {{
            content: '';
            position: absolute;
            left: -22px;
            top: 20px;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: #667eea;
            border: 3px solid white;
        }}
        .timeline-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }}
        .agent {{
            font-weight: bold;
            color: #667eea;
            font-size: 1.1em;
        }}
        .timestamp {{
            color: #666;
            font-size: 0.9em;
        }}
        .thought {{
            color: #333;
            line-height: 1.5;
        }}
        .data-preview {{
            margin-top: 10px;
            padding: 10px;
            background: #f1f3f4;
            border-radius: 5px;
            font-family: monospace;
            font-size: 0.9em;
            color: #555;
            max-height: 100px;
            overflow-y: auto;
        }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .stat-card {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .stat-number {{
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }}
        .stat-label {{
            color: #666;
            margin-top: 5px;
        }}
        .controls {{
            margin-bottom: 20px;
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }}
        .btn {{
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 0.9em;
            transition: all 0.3s ease;
        }}
        .btn-primary {{
            background: #667eea;
            color: white;
        }}
        .btn-primary:hover {{
            background: #5a6fd8;
        }}
        .btn-secondary {{
            background: #6c757d;
            color: white;
        }}
        .btn-secondary:hover {{
            background: #5a6268;
        }}
        .filter-section {{
            margin-bottom: 20px;
        }}
        .filter-section label {{
            margin-right: 10px;
            font-weight: bold;
        }}
        .filter-section select {{
            padding: 5px 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
        }}
        .mermaid-container {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            margin-top: 20px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 AutoDevCore Thought Trail</h1>
            <p>Visualizing AI Agent Reasoning and Decision Making</p>
        </div>
        
        <div class="content">
            <div class="stats">
                <div class="stat-card">
                    <div class="stat-number" id="total-thoughts">0</div>
                    <div class="stat-label">Total Thoughts</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number" id="unique-agents">0</div>
                    <div class="stat-label">Unique Agents</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number" id="avg-thought-length">0</div>
                    <div class="stat-label">Avg Thought Length</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number" id="analysis-duration">0s</div>
                    <div class="stat-label">Analysis Duration</div>
                </div>
            </div>
            
            <div class="section">
                <h2>🎛️ Controls & Filters</h2>
                <div class="controls">
                    <button class="btn btn-primary" onclick="exportToJSON()">Export JSON</button>
                    <button class="btn btn-secondary" onclick="exportToCSV()">Export CSV</button>
                    <button class="btn btn-secondary" onclick="toggleDataPreview()">Toggle Data Preview</button>
                </div>
                <div class="filter-section">
                    <label>Filter by Agent:</label>
                    <select id="agent-filter" onchange="filterByAgent()">
                        <option value="">All Agents</option>
                    </select>
                </div>
            </div>
            
            <div class="section">
                <h2>📊 Agent Activity Chart</h2>
                <canvas id="agentChart" width="400" height="200"></canvas>
            </div>
            
            <div class="section">
                <h2>🕒 Timeline View</h2>
                <div class="timeline" id="timeline">
                    <!-- Timeline items will be populated by JavaScript -->
                </div>
            </div>
            
            <div class="section">
                <h2>🔗 Thought Flow Diagram</h2>
                <div class="mermaid-container">
                    <div class="mermaid" id="mermaid-diagram">
                        <!-- Mermaid diagram will be rendered here -->
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Initialize thought trail data
        const thoughtTrail = {thought_trail_json};
        
        // Initialize Mermaid
        mermaid.initialize({{ startOnLoad: true }});
        
        // Calculate statistics
        function calculateStats() {{
            const totalThoughts = thoughtTrail.length;
            const uniqueAgents = new Set(thoughtTrail.map(t => t.agent)).size;
            const avgLength = Math.round(thoughtTrail.reduce((sum, t) => sum + t.thought.length, 0) / totalThoughts);
            
            // Calculate duration
            const firstTime = new Date(thoughtTrail[0].timestamp);
            const lastTime = new Date(thoughtTrail[thoughtTrail.length - 1].timestamp);
            const duration = Math.round((lastTime - firstTime) / 1000);
            
            document.getElementById('total-thoughts').textContent = totalThoughts;
            document.getElementById('unique-agents').textContent = uniqueAgents;
            document.getElementById('avg-thought-length').textContent = avgLength;
            document.getElementById('analysis-duration').textContent = duration + 's';
        }}
        
        // Populate agent filter
        function populateAgentFilter() {{
            const agents = [...new Set(thoughtTrail.map(t => t.agent))];
            const select = document.getElementById('agent-filter');
            
            agents.forEach(agent => {{
                const option = document.createElement('option');
                option.value = agent;
                option.textContent = agent;
                select.appendChild(option);
            }});
        }}
        
        // Render timeline
        function renderTimeline(filteredTrail = thoughtTrail) {{
            const timeline = document.getElementById('timeline');
            timeline.innerHTML = '';
            
            filteredTrail.forEach(thought => {{
                const item = document.createElement('div');
                item.className = 'timeline-item';
                
                const timestamp = new Date(thought.timestamp).toLocaleTimeString();
                const dataPreview = thought.data && Object.keys(thought.data).length > 0 
                    ? `<div class="data-preview">Data: ${{JSON.stringify(thought.data).substring(0, 100)}}...</div>`
                    : '';
                
                item.innerHTML = `
                    <div class="timeline-header">
                        <span class="agent">${{thought.agent}}</span>
                        <span class="timestamp">${{timestamp}}</span>
                    </div>
                    <div class="thought">${{thought.thought}}</div>
                    ${{dataPreview}}
                `;
                
                timeline.appendChild(item);
            }});
        }}
        
        // Create agent activity chart
        function createAgentChart() {{
            const ctx = document.getElementById('agentChart').getContext('2d');
            const agentCounts = {{}};
            
            thoughtTrail.forEach(thought => {{
                agentCounts[thought.agent] = (agentCounts[thought.agent] || 0) + 1;
            }});
            
            new Chart(ctx, {{
                type: 'bar',
                data: {{
                    labels: Object.keys(agentCounts),
                    datasets: [{{
                        label: 'Thoughts per Agent',
                        data: Object.values(agentCounts),
                        backgroundColor: [
                            '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4',
                            '#FFEAA7', '#DDA0DD', '#98D8C8', '#F7DC6F'
                        ],
                        borderWidth: 1
                    }}]
                }},
                options: {{
                    responsive: true,
                    scales: {{
                        y: {{
                            beginAtZero: true
                        }}
                    }}
                }}
            }});
        }}
        
        // Filter by agent
        function filterByAgent() {{
            const selectedAgent = document.getElementById('agent-filter').value;
            const filteredTrail = selectedAgent 
                ? thoughtTrail.filter(t => t.agent === selectedAgent)
                : thoughtTrail;
            
            renderTimeline(filteredTrail);
        }}
        
        // Export functions
        function exportToJSON() {{
            const dataStr = JSON.stringify(thoughtTrail, null, 2);
            const dataBlob = new Blob([dataStr], {{type: 'application/json'}});
            const url = URL.createObjectURL(dataBlob);
            const link = document.createElement('a');
            link.href = url;
            link.download = 'thought_trail.json';
            link.click();
        }}
        
        function exportToCSV() {{
            const headers = ['Timestamp', 'Agent', 'Thought', 'Data'];
            const csvContent = [
                headers.join(','),
                ...thoughtTrail.map(t => [
                    t.timestamp,
                    t.agent,
                    `"${{t.thought.replace(/"/g, '""')}}"`,
                    `"${{JSON.stringify(t.data).replace(/"/g, '""')}}"`
                ].join(','))
            ].join('\\n');
            
            const dataBlob = new Blob([csvContent], {{type: 'text/csv'}});
            const url = URL.createObjectURL(dataBlob);
            const link = document.createElement('a');
            link.href = url;
            link.download = 'thought_trail.csv';
            link.click();
        }}
        
        // Toggle data preview
        function toggleDataPreview() {{
            const previews = document.querySelectorAll('.data-preview');
            previews.forEach(preview => {{
                preview.style.display = preview.style.display === 'none' ? 'block' : 'none';
            }});
        }}
        
        // Initialize everything
        document.addEventListener('DOMContentLoaded', function() {{
            calculateStats();
            populateAgentFilter();
            renderTimeline();
            createAgentChart();
        }});
    </script>
</body>
</html>"""

    def export_thought_trail(self, format: str = "json") -> str:
        """Export thought trail in various formats."""
        if format == "json":
            return json.dumps(self.thought_trail, indent=2)
        elif format == "csv":
            import csv
            import io

            output = io.StringIO()
            writer = csv.writer(output)
            writer.writerow(["Timestamp", "Agent", "Thought", "Data"])

            for thought in self.thought_trail:
                writer.writerow(
                    [
                        thought["timestamp"],
                        thought["agent"],
                        thought["thought"],
                        json.dumps(thought["data"]),
                    ]
                )

            return output.getvalue()
        else:
            raise ValueError(f"Unsupported format: {format}")

    @abstractmethod
    def execute(self):
        """Execute the mode's main functionality."""
        pass
