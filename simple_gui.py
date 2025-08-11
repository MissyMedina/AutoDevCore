#!/usr/bin/env python3
"""
Simple AutoDevCore GUI using Flask
"""

import json
import time
from datetime import datetime

from flask import Flask, jsonify, render_template_string, request

app = Flask(__name__)

# HTML template for the GUI
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🚀 AutoDevCore - Visual Development Hub</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 30px;
            text-align: center;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        }
        
        .header h1 {
            font-size: 3rem;
            margin-bottom: 10px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .header p {
            font-size: 1.2rem;
            color: #666;
        }
        
        .dashboard {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .card {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }
        
        .card:hover {
            transform: translateY(-5px);
        }
        
        .card h3 {
            font-size: 1.5rem;
            margin-bottom: 15px;
            color: #333;
        }
        
        .metric {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin: 10px 0;
            padding: 10px;
            background: #f8f9fa;
            border-radius: 8px;
        }
        
        .metric-value {
            font-weight: bold;
            color: #667eea;
        }
        
        .button {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 1rem;
            font-weight: 600;
            transition: all 0.3s ease;
            margin: 5px;
        }
        
        .button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        
        .status-indicator {
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 8px;
        }
        
        .status-online { background-color: #28a745; }
        .status-warning { background-color: #ffc107; }
        .status-offline { background-color: #dc3545; }
        
        .progress-bar {
            width: 100%;
            height: 8px;
            background: #e9ecef;
            border-radius: 4px;
            overflow: hidden;
            margin: 10px 0;
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #28a745, #667eea);
            transition: width 0.3s ease;
        }
        
        .role-selector {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 20px;
            text-align: center;
        }
        
        .role-selector select {
            padding: 10px 20px;
            border: 2px solid #667eea;
            border-radius: 8px;
            font-size: 1rem;
            background: white;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 AutoDevCore</h1>
            <p>Visual Development Hub - Transform ideas into fully functional applications</p>
        </div>
        
        <div class="role-selector">
            <label for="role">👤 Your Role:</label>
            <select id="role" onchange="changeRole()">
                <option value="developer">Developer</option>
                <option value="project_manager">Project Manager</option>
                <option value="devops_engineer">DevOps Engineer</option>
                <option value="new_developer">New Developer</option>
                <option value="stakeholder">Stakeholder</option>
            </select>
        </div>
        
        <div class="dashboard">
            <div class="card">
                <h3>📊 Project Overview</h3>
                <div class="metric">
                    <span>Active Projects</span>
                    <span class="metric-value">3</span>
                </div>
                <div class="metric">
                    <span>Team Members</span>
                    <span class="metric-value">8</span>
                </div>
                <div class="metric">
                    <span>Success Rate</span>
                    <span class="metric-value">94%</span>
                </div>
                <div class="metric">
                    <span>Cost Savings</span>
                    <span class="metric-value">$25,000</span>
                </div>
            </div>
            
            <div class="card">
                <h3>🤖 AI Models Status</h3>
                <div class="metric">
                    <span><span class="status-indicator status-online"></span>GPT-4</span>
                    <span class="metric-value">Online</span>
                </div>
                <div class="metric">
                    <span><span class="status-indicator status-online"></span>Claude</span>
                    <span class="metric-value">Online</span>
                </div>
                <div class="metric">
                    <span><span class="status-indicator status-warning"></span>GPT-OSS</span>
                    <span class="metric-value">Warning</span>
                </div>
                <div class="metric">
                    <span>Response Time</span>
                    <span class="metric-value">2.3s</span>
                </div>
            </div>
            
            <div class="card">
                <h3>👥 Team Activity</h3>
                <div class="metric">
                    <span><span class="status-indicator status-online"></span>John (Frontend)</span>
                    <span class="metric-value">Coding</span>
                </div>
                <div class="metric">
                    <span><span class="status-indicator status-online"></span>Sarah (Backend)</span>
                    <span class="metric-value">Testing</span>
                </div>
                <div class="metric">
                    <span><span class="status-indicator status-warning"></span>Mike (DevOps)</span>
                    <span class="metric-value">Review</span>
                </div>
                <div class="metric">
                    <span><span class="status-indicator status-offline"></span>Alice (PM)</span>
                    <span class="metric-value">Offline</span>
                </div>
            </div>
            
            <div class="card">
                <h3>🚀 Quick Actions</h3>
                <button class="button" onclick="createProject()">🆕 New Project</button>
                <button class="button" onclick="generateCode()">🤖 AI Generate</button>
                <button class="button" onclick="deployApp()">🚀 Deploy</button>
                <button class="button" onclick="runTests()">🧪 Run Tests</button>
            </div>
        </div>
        
        <div class="card">
            <h3>📈 Recent Activity</h3>
            <div id="activity-feed">
                <div class="metric">
                    <span>10:30 AM</span>
                    <span>AI generated authentication system</span>
                    <span class="metric-value">John</span>
                </div>
                <div class="metric">
                    <span>09:15 AM</span>
                    <span>Team collaboration session started</span>
                    <span class="metric-value">Sarah</span>
                </div>
                <div class="metric">
                    <span>08:45 AM</span>
                    <span>New project "E-commerce" created</span>
                    <span class="metric-value">Mike</span>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        function changeRole() {
            const role = document.getElementById('role').value;
            console.log('Role changed to:', role);
            // Here you would update the interface based on the role
        }
        
        function createProject() {
            alert('🚀 Creating new project...\n\nThis would open the project creation wizard with:\n• Project name and description\n• Framework selection\n• Complexity level\n• Team assignment');
        }
        
        function generateCode() {
            alert('🤖 AI Code Generation\n\nThis would open the AI code generation interface with:\n• Prompt input\n• Model selection\n• Code preview\n• Optimization options');
        }
        
        function deployApp() {
            alert('🚀 Deployment Pipeline\n\nThis would show the CI/CD pipeline:\n• Build status\n• Test results\n• Deployment progress\n• Environment management');
        }
        
        function runTests() {
            alert('🧪 Running Tests\n\nThis would execute:\n• Unit tests\n• Integration tests\n• Security scans\n• Performance tests');
        }
        
        // Update time every minute
        setInterval(() => {
            const now = new Date();
            console.log('GUI updated at:', now.toLocaleTimeString());
        }, 60000);
    </script>
</body>
</html>
"""


@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)


@app.route("/api/status")
def status():
    return jsonify(
        {
            "status": "online",
            "timestamp": datetime.now().isoformat(),
            "version": "1.0.0",
            "features": [
                "AI Code Generation",
                "Project Management",
                "Team Collaboration",
                "Deployment Pipeline",
            ],
        }
    )


@app.route("/api/create-project", methods=["POST"])
def create_project():
    data = request.json
    return jsonify(
        {
            "success": True,
            "project_id": "proj_" + str(int(time.time())),
            "message": f'Project "{data.get("name", "New Project")}" created successfully!',
        }
    )


if __name__ == "__main__":
    print("🚀 Starting AutoDevCore GUI...")
    print("📱 The GUI will open in your default web browser")
    print("🔗 URL: http://localhost:8501")
    print("⏹️  Press Ctrl+C to stop the server")
    print("-" * 50)

    app.run(host="0.0.0.0", port=8501, debug=True)
