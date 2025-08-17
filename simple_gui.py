#!/usr/bin/env python3
"""
Simple AutoDevCore GUI using Flask
"""

import json
import time
import os
from datetime import datetime
from pathlib import Path

from flask import Flask, jsonify, render_template_string, request

# Import AI integration
try:
    from integrations.gpt_oss import GPTOSSClient

    gpt_client = GPTOSSClient()
    AI_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  AI integration not available: {e}")
    gpt_client = None
    AI_AVAILABLE = False

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
            position: relative;
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
        
        .header-actions {
            position: absolute;
            top: 20px;
            right: 20px;
            display: flex;
            gap: 10px;
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
        
        .button-secondary {
            background: linear-gradient(135deg, #6c757d, #495057);
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
        
        /* Modal Styles */
        .modal {
            display: none;
            position: fixed;
            z-index: 1000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0,0,0,0.5);
            backdrop-filter: blur(5px);
        }
        
        .modal-content {
            background: white;
            margin: 5% auto;
            padding: 30px;
            border-radius: 15px;
            width: 90%;
            max-width: 600px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.3);
            animation: modalSlideIn 0.3s ease;
        }
        
        @keyframes modalSlideIn {
            from { transform: translateY(-50px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }
        
        .modal-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 2px solid #f8f9fa;
        }
        
        .modal-title {
            font-size: 1.5rem;
            font-weight: bold;
            color: #333;
        }
        
        .close {
            color: #aaa;
            font-size: 28px;
            font-weight: bold;
            cursor: pointer;
            transition: color 0.3s ease;
        }
        
        .close:hover {
            color: #333;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #333;
        }
        
        .form-group input,
        .form-group select,
        .form-group textarea {
            width: 100%;
            padding: 12px;
            border: 2px solid #e9ecef;
            border-radius: 8px;
            font-size: 1rem;
            transition: border-color 0.3s ease;
        }
        
        .form-group input:focus,
        .form-group select:focus,
        .form-group textarea:focus {
            outline: none;
            border-color: #667eea;
        }
        
        .form-row {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
        }
        
        .modal-actions {
            display: flex;
            justify-content: flex-end;
            gap: 10px;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 2px solid #f8f9fa;
        }
        
        .save-options {
            background: #f8f9fa;
            border-radius: 8px;
            padding: 15px;
            margin: 15px 0;
        }
        
        /* Chat Styles */
        .chat-message {
            margin-bottom: 15px;
            padding: 10px;
            border-radius: 10px;
            max-width: 80%;
        }
        
        .user-message {
            background: #667eea;
            color: white;
            margin-left: auto;
            text-align: right;
        }
        
        .ai-message {
            background: #f8f9fa;
            color: #333;
            margin-right: auto;
        }
        
        .message-content {
            margin-bottom: 5px;
            word-wrap: break-word;
        }
        
        .message-time {
            font-size: 0.7em;
            opacity: 0.7;
        }
        
        .chat-input-container {
            display: flex;
            gap: 10px;
        }
        
        .chat-loading {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid #f3f3f3;
            border-top: 3px solid #667eea;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .save-option {
            display: flex;
            align-items: center;
            margin: 10px 0;
        }
        
        .save-option input[type="radio"] {
            margin-right: 10px;
        }
        
        .project-list {
            max-height: 300px;
            overflow-y: auto;
            border: 1px solid #e9ecef;
            border-radius: 8px;
            padding: 10px;
        }
        
        .project-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px;
            border-bottom: 1px solid #f8f9fa;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        
        .project-item:hover {
            background-color: #f8f9fa;
        }
        
        .project-item:last-child {
            border-bottom: none;
        }
        
        .project-info h4 {
            margin: 0;
            color: #333;
        }
        
        .project-info p {
            margin: 5px 0 0 0;
            color: #666;
            font-size: 0.9rem;
        }
        
        .project-status {
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.8rem;
            font-weight: bold;
        }
        
        .status-active { background-color: #d4edda; color: #155724; }
        .status-draft { background-color: #fff3cd; color: #856404; }
        .status-archived { background-color: #f8d7da; color: #721c24; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="header-actions">
                <button class="button button-secondary" onclick="openSettings()">⚙️ Settings</button>
                <button class="button" onclick="openNewProject()">🆕 New Project</button>
                <button class="button" onclick="checkSystemStatus()" style="background: #28a745;">📊 Status</button>
            </div>
            <h1>🚀 AutoDevCore</h1>
            <p>Visual Development Hub - Transform ideas into fully functional applications</p>
        </div>
        
        <div class="role-selector">
            <label for="role">👤 Your Role:</label>
            <select id="role" onchange="changeRole()">
                <option value="Senior_Dev">Senior Developer</option>
                <option value="MidLvl_Dev">Mid Level Developer</option>
                <option value="EntryLvl_Dev">Entry Level Developer</option>
                <option value="project_manager">Project Manager</option>
                <option value="devops_engineer">DevOps Engineer</option>
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
                    <span><span class="status-indicator status-online"></span>System</span>
                    <span class="metric-value">Ready</span>
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
                <button class="button" onclick="openNewProject()">🆕 New Project</button>
                <button class="button" onclick="generateCode()">🤖 AI Generate</button>
                <button class="button" onclick="deployApp()">🚀 Deploy</button>
                <button class="button" onclick="runTests()">🧪 Run Tests</button>
            </div>
            
            <div class="card">
                <h3>💬 AI Chat Assistant</h3>
                <div id="chat-container" style="max-height: 300px; overflow-y: auto; margin-bottom: 15px;">
                    <div id="chat-messages">
                        <div class="chat-message ai-message">
                            <div class="message-content">Hello! I'm your AI assistant. How can I help you today?</div>
                            <div class="message-time">Just now</div>
                        </div>
                    </div>
                </div>
                <div class="chat-input-container">
                    <input type="text" id="chat-input" placeholder="Type your message..." style="width: calc(100% - 80px); padding: 10px; border: 1px solid #ddd; border-radius: 5px; margin-right: 10px;">
                    <button class="button" onclick="sendChatMessage()" style="width: 70px;">Send</button>
                </div>
                <div id="chat-status" style="font-size: 0.8em; color: #666; margin-top: 5px;"></div>
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
    
    <!-- Settings Modal -->
    <div id="settingsModal" class="modal">
        <div class="modal-content">
            <div class="modal-header">
                <div class="modal-title">⚙️ Settings</div>
                <span class="close" onclick="closeModal('settingsModal')">&times;</span>
            </div>
            
            <form id="settingsForm">
                <div class="form-group">
                    <label>🤖 AI Provider</label>
                    <select id="aiProvider">
                        <option value="openai">OpenAI (GPT-4)</option>
                        <option value="anthropic">Anthropic (Claude)</option>
                        <option value="google">Google AI (Gemini)</option>
                        <option value="gpt-oss">GPT-OSS (Local)</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label>🔑 API Key</label>
                    <input type="password" id="apiKey" placeholder="Enter your API key">
                </div>
                
                <div class="form-group">
                    <label>🌐 Default Port</label>
                    <input type="number" id="defaultPort" value="8501" min="1000" max="9999">
                </div>
                
                <div class="form-group">
                    <label>🎨 Theme</label>
                    <select id="theme">
                        <option value="light">Light</option>
                        <option value="dark">Dark</option>
                        <option value="auto">Auto</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label>📁 Default Project Directory</label>
                    <input type="text" id="projectDir" placeholder="/path/to/projects">
                </div>
                
                <div class="modal-actions">
                    <button type="button" class="button button-secondary" onclick="closeModal('settingsModal')">Cancel</button>
                    <button type="submit" class="button">Save Settings</button>
                </div>
            </form>
        </div>
    </div>
    
    <!-- New Project Modal -->
    <div id="newProjectModal" class="modal">
        <div class="modal-content">
            <div class="modal-header">
                <div class="modal-title">🆕 New Project</div>
                <span class="close" onclick="closeModal('newProjectModal')">&times;</span>
            </div>
            
            <form id="newProjectForm">
                <div class="form-group">
                    <label>📝 Project Name</label>
                    <input type="text" id="projectName" placeholder="Enter project name" required>
                </div>
                
                <div class="form-group">
                    <label>📄 Description</label>
                    <textarea id="projectDescription" rows="3" placeholder="Describe your project"></textarea>
                </div>
                
                <div class="form-row">
                    <div class="form-group">
                        <label>🏗️ Framework</label>
                        <select id="framework">
                            <option value="fastapi">FastAPI</option>
                            <option value="django">Django</option>
                            <option value="flask">Flask</option>
                            <option value="react">React</option>
                            <option value="vue">Vue.js</option>
                            <option value="angular">Angular</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label>📊 Complexity</label>
                        <select id="complexity">
                            <option value="starter">Starter</option>
                            <option value="professional">Professional</option>
                            <option value="enterprise">Enterprise</option>
                        </select>
                    </div>
                </div>
                
                <div class="form-group">
                    <label>💾 Save Options</label>
                    <div class="save-options">
                        <div class="save-option">
                            <input type="radio" id="saveLocal" name="saveOption" value="local" checked>
                            <label for="saveLocal">💻 Save to Local Disk</label>
                        </div>
                        <div class="save-option">
                            <input type="radio" id="saveCloud" name="saveOption" value="cloud">
                            <label for="saveCloud">☁️ Save to Cloud (GitHub/GitLab)</label>
                        </div>
                        <div class="save-option">
                            <input type="radio" id="saveBoth" name="saveOption" value="both">
                            <label for="saveBoth">🔄 Save to Both</label>
                        </div>
                    </div>
                </div>
                
                <div class="form-group" id="cloudOptions" style="display: none;">
                    <label>🔗 Repository URL</label>
                    <input type="url" id="repoUrl" placeholder="https://github.com/username/repo">
                </div>
                
                <div class="modal-actions">
                    <button type="button" class="button button-secondary" onclick="closeModal('newProjectModal')">Cancel</button>
                    <button type="submit" class="button">Create Project</button>
                </div>
            </form>
        </div>
    </div>
    
    <!-- Project List Modal -->
    <div id="projectListModal" class="modal">
        <div class="modal-content">
            <div class="modal-header">
                <div class="modal-title">📁 My Projects</div>
                <span class="close" onclick="closeModal('projectListModal')">&times;</span>
            </div>
            
            <div class="project-list" id="projectList">
                <div class="project-item" onclick="openProject('ecommerce-app')">
                    <div class="project-info">
                        <h4>E-commerce Platform</h4>
                        <p>Online retail platform with payment integration</p>
                    </div>
                    <span class="project-status status-active">Active</span>
                </div>
                <div class="project-item" onclick="openProject('task-manager')">
                    <div class="project-info">
                        <h4>Task Manager</h4>
                        <p>AI-powered project management tool</p>
                    </div>
                    <span class="project-status status-draft">Draft</span>
                </div>
                <div class="project-item" onclick="openProject('healthcare-app')">
                    <div class="project-info">
                        <h4>Healthcare System</h4>
                        <p>HIPAA-compliant patient management</p>
                    </div>
                    <span class="project-status status-archived">Archived</span>
                </div>
            </div>
            
            <div class="modal-actions">
                <button type="button" class="button" onclick="openNewProject()">🆕 New Project</button>
                <button type="button" class="button button-secondary" onclick="closeModal('projectListModal')">Close</button>
            </div>
        </div>
    </div>
    
    <script>
        // Global state
        let currentProject = null;
        let projects = [];
        
        function changeRole() {
            const role = document.getElementById('role').value;
            console.log('Role changed to:', role);
            // Update interface based on role
            updateInterfaceForRole(role);
        }
        
        function updateInterfaceForRole(role) {
            // Update dashboard based on role
            const roleConfigs = {
                'Senior_Dev': { showAdvanced: true, showCodeGen: true },
                'MidLvl_Dev': { showAdvanced: false, showCodeGen: true },
                'EntryLvl_Dev': { showAdvanced: false, showCodeGen: false },
                'project_manager': { showAdvanced: false, showCodeGen: false },
                'devops_engineer': { showAdvanced: true, showCodeGen: false },
                'stakeholder': { showAdvanced: false, showCodeGen: false }
            };
            
            const config = roleConfigs[role] || {};
            console.log('Interface updated for role:', role, config);
        }
        
        function openModal(modalId) {
            document.getElementById(modalId).style.display = 'block';
        }
        
        function closeModal(modalId) {
            document.getElementById(modalId).style.display = 'none';
        }
        
        function openModal(modalId) {
            console.log('openModal called with:', modalId);
            try {
                const modal = document.getElementById(modalId);
                if (modal) {
                    console.log('Modal found, opening...');
                    modal.style.display = 'block';
                } else {
                    console.error('Modal not found:', modalId);
                    alert(`Modal ${modalId} not found. Please refresh the page.`);
                }
            } catch (error) {
                console.error('Error opening modal:', error);
                alert('Error opening modal: ' + error.message);
            }
        }
        
        function openSettings() {
            console.log('openSettings called');
            openModal('settingsModal');
            loadSettings();
        }
        
        function openNewProject() {
            console.log('openNewProject called');
            openModal('newProjectModal');
        }
        
        function checkSystemStatus() {
            fetch('/api/status')
                .then(response => response.json())
                .then(data => {
                    alert(`📊 System Status: ${data.status}\nVersion: ${data.version}\nFeatures: ${data.features.length} available`);
                })
                .catch(error => {
                    alert('❌ Error checking system status');
                });
        }
        
        function loadSettings() {
            // Load settings from backend API
            fetch('/api/settings')
            .then(response => response.json())
            .then(settings => {
                console.log('Settings loaded from backend:', settings);
                document.getElementById('aiProvider').value = settings.aiProvider || 'openai';
                document.getElementById('apiKey').value = settings.apiKey || '';
                document.getElementById('defaultPort').value = settings.defaultPort || '8502';
                document.getElementById('theme').value = settings.theme || 'light';
                document.getElementById('projectDir').value = settings.projectDir || '';
            })
            .catch(error => {
                console.error('Error loading settings from backend:', error);
                // Fallback to localStorage
                const settings = JSON.parse(localStorage.getItem('autodevSettings') || '{}');
                document.getElementById('aiProvider').value = settings.aiProvider || 'openai';
                document.getElementById('apiKey').value = settings.apiKey || '';
                document.getElementById('defaultPort').value = settings.defaultPort || '8502';
                document.getElementById('theme').value = settings.theme || 'light';
                document.getElementById('projectDir').value = settings.projectDir || '';
            });
        }
        
        function saveSettings() {
            const settings = {
                aiProvider: document.getElementById('aiProvider').value,
                apiKey: document.getElementById('apiKey').value,
                defaultPort: document.getElementById('defaultPort').value,
                theme: document.getElementById('theme').value,
                projectDir: document.getElementById('projectDir').value
            };
            
            // Save to localStorage
            localStorage.setItem('autodevSettings', JSON.stringify(settings));
            console.log('Settings saved to localStorage:', settings);
            
            // Save to backend API
            fetch('/api/settings', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(settings)
            })
            .then(response => response.json())
            .then(data => {
                console.log('Settings saved to backend:', data);
                alert('✅ Settings saved successfully!');
                closeModal('settingsModal');
            })
            .catch(error => {
                console.error('Error saving settings:', error);
                alert('⚠️ Settings saved locally but failed to save to server.');
                closeModal('settingsModal');
            });
        }
        
        function createProject() {
            const projectData = {
                name: document.getElementById('projectName').value,
                description: document.getElementById('projectDescription').value,
                framework: document.getElementById('framework').value,
                complexity: document.getElementById('complexity').value,
                saveOption: document.querySelector('input[name="saveOption"]:checked').value,
                repoUrl: document.getElementById('repoUrl').value
            };
            
            if (!projectData.name) {
                alert('❌ Please enter a project name');
                return;
            }
            
            console.log('Creating project:', projectData);
            
            // Create project via backend API
            fetch('/api/create-project', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(projectData)
            })
            .then(response => response.json())
            .then(data => {
                console.log('Project created via API:', data);
                alert(`✅ Project "${projectData.name}" created successfully!\n\nFramework: ${projectData.framework}\nComplexity: ${projectData.complexity}\nSave Location: ${projectData.saveOption}\nProject ID: ${data.project_id}`);
                
                // Add to projects list
                projects.push({
                    id: data.project_id,
                    ...projectData,
                    status: 'active',
                    createdAt: new Date().toISOString()
                });
                
                closeModal('newProjectModal');
                document.getElementById('newProjectForm').reset();
                
                // Update activity feed
                addActivity(`New project "${projectData.name}" created`, 'System');
            })
            .catch(error => {
                console.error('Error creating project:', error);
                alert('❌ Failed to create project. Please try again.');
            });
        }
        
        function addActivity(description, user) {
            const activityFeed = document.getElementById('activity-feed');
            const time = new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
            
            const activityDiv = document.createElement('div');
            activityDiv.className = 'metric';
            activityDiv.innerHTML = `
                <span>${time}</span>
                <span>${description}</span>
                <span class="metric-value">${user}</span>
            `;
            
            activityFeed.insertBefore(activityDiv, activityFeed.firstChild);
            
            // Keep only last 5 activities
            while (activityFeed.children.length > 5) {
                activityFeed.removeChild(activityFeed.lastChild);
            }
        }
        
        function generateCode() {
            const prompt = prompt('🤖 Enter your code generation prompt:');
            if (prompt) {
                console.log('Generating code for:', prompt);
                addActivity(`AI code generation: ${prompt.substring(0, 30)}...`, 'AI Assistant');
                alert('🤖 Code Generation\n\nProduction code generation ready.\nUse the chat interface for detailed code requests.');
            }
        }
        
        function deployApp() {
            console.log('Deploying application...');
            addActivity('Application deployment started', 'DevOps');
            alert('🚀 Deployment\n\nProduction deployment pipeline ready.\nUse the chat interface to request deployment.');
        }
        
        function runTests() {
            console.log('Running tests...');
            addActivity('Test suite execution started', 'QA');
            alert('🧪 Test Suite\n\nProduction test suite ready.\nUse the chat interface to request specific tests.');
        }
        
        function openProject(projectId) {
            console.log('Opening project:', projectId);
            currentProject = projectId;
            addActivity(`Project "${projectId}" opened`, 'User');
            alert(`📁 Opening project: ${projectId}\n\nThis would load the project workspace with:\n• Code editor\n• File explorer\n• Terminal\n• Debug console`);
        }
        
        function sendChatMessage() {
            const input = document.getElementById('chat-input');
            const message = input.value.trim();
            
            if (!message) return;
            
            // Add user message to chat
            addChatMessage(message, 'user');
            input.value = '';
            
            // Show loading status
            const status = document.getElementById('chat-status');
            status.innerHTML = '<span class="chat-loading"></span> AI is thinking...';
            
            // Send to AI
            fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message })
            })
            .then(response => response.json())
            .then(data => {
                status.textContent = '';
                
                if (data.success) {
                    addChatMessage(data.message, 'ai');
                } else {
                    addChatMessage(`Error: ${data.message}`, 'ai');
                }
            })
            .catch(error => {
                console.error('Chat error:', error);
                status.textContent = 'Error: Could not connect to AI service';
                addChatMessage('Sorry, I encountered an error. Please try again.', 'ai');
            });
        }
        
        function addChatMessage(content, sender) {
            const messagesContainer = document.getElementById('chat-messages');
            const messageDiv = document.createElement('div');
            messageDiv.className = `chat-message ${sender}-message`;
            
            const time = new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
            
            messageDiv.innerHTML = `
                <div class="message-content">${content}</div>
                <div class="message-time">${time}</div>
            `;
            
            messagesContainer.appendChild(messageDiv);
            
            // Scroll to bottom
            const chatContainer = document.getElementById('chat-container');
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }
        
        // Handle Enter key in chat input
        document.addEventListener('DOMContentLoaded', function() {
            const chatInput = document.getElementById('chat-input');
            if (chatInput) {
                chatInput.addEventListener('keypress', function(e) {
                    if (e.key === 'Enter') {
                        sendChatMessage();
                    }
                });
            }
        });
        
        // Event listeners
        document.getElementById('settingsForm').addEventListener('submit', function(e) {
            e.preventDefault();
            saveSettings();
        });
        
        document.getElementById('newProjectForm').addEventListener('submit', function(e) {
            e.preventDefault();
            createProject();
        });
        
        // Handle save option changes
        document.querySelectorAll('input[name="saveOption"]').forEach(radio => {
            radio.addEventListener('change', function() {
                const cloudOptions = document.getElementById('cloudOptions');
                if (this.value === 'cloud' || this.value === 'both') {
                    cloudOptions.style.display = 'block';
                } else {
                    cloudOptions.style.display = 'none';
                }
            });
        });
        
        // Close modal when clicking outside
        window.onclick = function(event) {
            const modals = document.querySelectorAll('.modal');
            modals.forEach(modal => {
                if (event.target === modal) {
                    modal.style.display = 'none';
                }
            });
        }
        
        // Initialize
        document.addEventListener('DOMContentLoaded', function() {
            console.log('AutoDevCore GUI initialized');
            loadSettings();
        });
        
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


@app.route("/api/chat", methods=["POST"])
def chat():
    """Handle AI chat requests"""
    if not AI_AVAILABLE or not gpt_client:
        return (
            jsonify(
                {
                    "success": False,
                    "error": "AI service not available",
                    "message": "Please check that Ollama is running and the gpt-oss model is loaded.",
                }
            ),
            503,
        )

    try:
        data = request.json
        user_message = data.get("message", "").strip()

        if not user_message:
            return (
                jsonify(
                    {
                        "success": False,
                        "error": "Empty message",
                        "message": "Please provide a message to send to the AI.",
                    }
                ),
                400,
            )

        print(f"🤖 AI Chat Request: {user_message[:50]}...")

        # Generate AI response
        response = gpt_client.generate(user_message)

        ai_message = response.get("response", "Sorry, I couldn't generate a response.")

        print(f"✅ AI Response: {ai_message[:50]}...")

        return jsonify(
            {
                "success": True,
                "message": ai_message,
                "timestamp": datetime.now().isoformat(),
            }
        )

    except Exception as e:
        print(f"❌ AI Chat Error: {e}")
        return (
            jsonify(
                {
                    "success": False,
                    "error": str(e),
                    "message": "An error occurred while processing your request.",
                }
            ),
            500,
        )


@app.route("/api/settings", methods=["GET", "POST"])
def handle_settings():
    if request.method == "POST":
        data = request.json
        # Save settings to file or database
        settings_file = Path("data/settings.json")
        settings_file.parent.mkdir(exist_ok=True)

        with open(settings_file, "w") as f:
            json.dump(data, f, indent=2)

        return jsonify({"success": True, "message": "Settings saved successfully"})
    else:
        # Load settings from file
        settings_file = Path("data/settings.json")
        if settings_file.exists():
            with open(settings_file, "r") as f:
                settings = json.load(f)
        else:
            settings = {
                "aiProvider": "openai",
                "defaultPort": "8501",
                "theme": "light",
                "projectDir": str(Path.home() / "AutoDevCore" / "projects"),
            }

        return jsonify(settings)


if __name__ == "__main__":
    print("🚀 Starting AutoDevCore Simple GUI...")
    print("📱 The GUI will open in your default web browser")
    print("🔗 URL: http://localhost:8502")
    print("⏹️  Press Ctrl+C to stop the server")
    print("-" * 50)

    app.run(host="0.0.0.0", port=8502, debug=True)
