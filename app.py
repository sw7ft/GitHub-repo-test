from flask import Flask, render_template_string, request, jsonify
from datetime import datetime
import json
import os

app = Flask(__name__)

# Simple in-memory storage for messages
messages = []

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ProApp - Professional Web Application</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Poppins', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        nav {
            background: rgba(255, 255, 255, 0.95);
            padding: 1rem 2rem;
            border-radius: 10px;
            margin-bottom: 2rem;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        nav h2 {
            color: #667eea;
            font-weight: 700;
        }
        
        .nav-links {
            display: flex;
            gap: 2rem;
            list-style: none;
        }
        
        .nav-links a {
            color: #333;
            text-decoration: none;
            font-weight: 500;
            transition: color 0.3s;
            cursor: pointer;
        }
        
        .nav-links a:hover {
            color: #667eea;
        }
        
        .main-content {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .hero {
            background: white;
            border-radius: 15px;
            padding: 60px 40px;
            text-align: center;
            margin-bottom: 2rem;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
            animation: slideDown 0.6s ease-out;
        }
        
        @keyframes slideDown {
            from {
                opacity: 0;
                transform: translateY(-20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .hero h1 {
            color: #667eea;
            font-size: 3rem;
            margin-bottom: 1rem;
            font-weight: 700;
        }
        
        .hero p {
            color: #666;
            font-size: 1.1rem;
            margin-bottom: 2rem;
        }
        
        .features {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
            margin-bottom: 2rem;
        }
        
        .feature-card {
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s, box-shadow 0.3s;
            animation: slideUp 0.6s ease-out;
        }
        
        @keyframes slideUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .feature-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        }
        
        .feature-card h3 {
            color: #667eea;
            margin-bottom: 1rem;
            font-size: 1.3rem;
        }
        
        .feature-card p {
            color: #666;
            line-height: 1.6;
        }
        
        .container {
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
            padding: 40px;
            max-width: 600px;
            margin: 0 auto 2rem;
            animation: slideUp 0.6s ease-out;
        }
        
        h2 {
            color: #333;
            margin-bottom: 1.5rem;
            font-size: 2rem;
        }
        
        .form-group {
            margin-bottom: 1.5rem;
        }
        
        label {
            display: block;
            margin-bottom: 0.5rem;
            color: #333;
            font-weight: 600;
        }
        
        input[type="text"],
        input[type="email"],
        textarea {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-family: 'Poppins', sans-serif;
            font-size: 1rem;
            transition: border-color 0.3s;
        }
        
        input[type="text"]:focus,
        input[type="email"]:focus,
        textarea:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        
        textarea {
            resize: vertical;
            min-height: 120px;
        }
        
        button {
            width: 100%;
            padding: 14px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
        }
        
        button:active {
            transform: translateY(0);
        }
        
        .message {
            margin-top: 20px;
            padding: 15px;
            background: #d4edda;
            color: #155724;
            border-radius: 8px;
            text-align: center;
            display: none;
            animation: slideDown 0.3s ease-out;
        }
        
        .message.show {
            display: block;
        }
        
        .message.error {
            background: #f8d7da;
            color: #721c24;
        }
        
        .messages-section {
            background: white;
            border-radius: 15px;
            padding: 40px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
            margin-bottom: 2rem;
        }
        
        .message-item {
            padding: 20px;
            background: #f9f9f9;
            border-left: 4px solid #667eea;
            margin-bottom: 1rem;
            border-radius: 5px;
            animation: slideUp 0.3s ease-out;
        }
        
        .message-item h4 {
            color: #333;
            margin-bottom: 0.5rem;
        }
        
        .message-item p {
            color: #666;
            margin-bottom: 0.5rem;
        }
        
        .message-time {
            font-size: 0.85rem;
            color: #999;
        }
        
        .loading {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid rgba(255, 255, 255, 0.3);
            border-radius: 50%;
            border-top-color: white;
            animation: spin 1s ease-in-out infinite;
        }
        
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 1rem;
            margin-bottom: 2rem;
        }
        
        .stat-card {
            background: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
        }
        
        .stat-number {
            font-size: 2rem;
            color: #667eea;
            font-weight: 700;
        }
        
        .stat-label {
            color: #666;
            margin-top: 0.5rem;
        }
        
        .hidden {
            display: none;
        }
    </style>
</head>
<body>
    <nav>
        <h2>ProApp</h2>
        <ul class="nav-links">
            <li><a onclick="showHome()">Home</a></li>
            <li><a onclick="showMessages()">Messages</a></li>
            <li><a onclick="showAbout()">About</a></li>
        </ul>
    </nav>
    
    <div class="main-content">
        <div id="homePage">
            <div class="hero">
                <h1>Welcome to ProApp</h1>
                <p>A modern, professional web application built with Flask</p>
            </div>
            
            <div class="stats">
                <div class="stat-card">
                    <div class="stat-number" id="messageCount">0</div>
                    <div class="stat-label">Messages Sent</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">100%</div>
                    <div class="stat-label">Uptime</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">⚡</div>
                    <div class="stat-label">Lightning Fast</div>
                </div>
            </div>
            
            <div class="features">
                <div class="feature-card">
                    <h3>💬 Message System</h3>
                    <p>Send and receive messages with real-time updates and persistent storage.</p>
                </div>
                <div class="feature-card">
                    <h3>📱 Responsive Design</h3>
                    <p>Beautiful interface that works seamlessly on all devices and screen sizes.</p>
                </div>
                <div class="feature-card">
                    <h3>⚙️ REST API</h3>
                    <p>Powerful API endpoints for integration with other applications.</p>
                </div>
                <div class="feature-card">
                    <h3>🚀 Fast Performance</h3>
                    <p>Optimized for speed with smooth animations and instant responses.</p>
                </div>
                <div class="feature-card">
                    <h3>🎨 Modern UI</h3>
                    <p>Clean, professional design with gradient colors and smooth transitions.</p>
                </div>
                <div class="feature-card">
                    <h3>📊 Analytics Ready</h3>
                    <p>Built with data collection and analytics capabilities in mind.</p>
                </div>
            </div>
        </div>
        
        <div id="messagesPage" class="hidden">
            <div class="container">
                <h2>Send a Message</h2>
                <form id="contactForm">
                    <div class="form-group">
                        <label for="name">Name:</label>
                        <input type="text" id="name" name="name" placeholder="John Doe" required>
                    </div>
                    <div class="form-group">
                        <label for="email">Email:</label>
                        <input type="email" id="email" name="email" placeholder="john@example.com" required>
                    </div>
                    <div class="form-group">
                        <label for="message">Message:</label>
                        <textarea id="message" name="message" placeholder="Write your message here..." required></textarea>
                    </div>
                    <button type="submit">
                        <span id="buttonText">Send Message</span>
                        <span id="buttonLoader" class="hidden loading"></span>
                    </button>
                </form>
                <div class="message" id="successMessage">
                    ✓ Thanks! Your message has been received.
                </div>
                <div class="message error hidden" id="errorMessage">
                    ✗ An error occurred. Please try again.
                </div>
            </div>
            
            <div class="messages-section">
                <h2>Recent Messages</h2>
                <div id="messagesList">
                    <p style="text-align: center; color: #999;">No messages yet. Be the first to send one!</p>
                </div>
            </div>
        </div>
        
        <div id="aboutPage" class="hidden">
            <div class="container">
                <h2>About ProApp</h2>
                <p style="color: #666; line-height: 1.8; margin-bottom: 1rem;">
                    ProApp is a demonstration of a modern, professional web application built with Flask. 
                    It showcases best practices in web development including:
                </p>
                <ul style="color: #666; margin-left: 2rem; line-height: 1.8;">
                    <li>Clean, responsive UI design</li>
                    <li>RESTful API architecture</li>
                    <li>Form validation and error handling</li>
                    <li>Smooth animations and transitions</li>
                    <li>Real-time message updates</li>
                    <li>Professional code organization</li>
                </ul>
                <p style="color: #666; margin-top: 1rem;">
                    Built with ❤️ using Python and Flask
                </p>
            </div>
        </div>
    </div>

    <script>
        const API_ENDPOINT = '/api/messages';
        
        // Page navigation
        function showPage(pageId) {
            document.querySelectorAll('[id$="Page"]').forEach(page => page.classList.add('hidden'));
            document.getElementById(pageId).classList.remove('hidden');
            if (pageId === 'messagesPage') loadMessages();
        }
        
        function showHome() { showPage('homePage'); }
        function showMessages() { showPage('messagesPage'); }
        function showAbout() { showPage('aboutPage'); }
        
        // Form submission
        document.getElementById('contactForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const name = document.getElementById('name').value.trim();
            const email = document.getElementById('email').value.trim();
            const message = document.getElementById('message').value.trim();
            
            if (!name || !email || !message) {
                showError('Please fill in all fields');
                return;
            }
            
            setLoading(true);
            
            try {
                const response = await fetch(API_ENDPOINT, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ name, email, message })
                });
                
                if (response.ok) {
                    showSuccess();
                    this.reset();
                    updateStats();
                    setTimeout(loadMessages, 500);
                } else {
                    showError('Failed to send message');
                }
            } catch (error) {
                showError('Network error');
            } finally {
                setLoading(false);
            }
        });
        
        function showSuccess() {
            const msg = document.getElementById('successMessage');
            msg.classList.add('show');
            setTimeout(() => msg.classList.remove('show'), 3000);
        }
        
        function showError(errorMsg) {
            const msg = document.getElementById('errorMessage');
            msg.textContent = '✗ ' + errorMsg;
            msg.classList.remove('hidden');
            msg.classList.add('show');
            setTimeout(() => msg.classList.remove('show'), 3000);
        }
        
        function setLoading(isLoading) {
            document.getElementById('buttonText').classList.toggle('hidden', isLoading);
            document.getElementById('buttonLoader').classList.toggle('hidden', !isLoading);
            document.getElementById('contactForm').style.opacity = isLoading ? '0.7' : '1';
        }
        
        async function loadMessages() {
            try {
                const response = await fetch(API_ENDPOINT);
                const data = await response.json();
                const messagesList = document.getElementById('messagesList');
                
                if (data.messages.length === 0) {
                    messagesList.innerHTML = '<p style="text-align: center; color: #999;">No messages yet.</p>';
                    return;
                }
                
                messagesList.innerHTML = data.messages
                    .reverse()
                    .map(msg => `
                        <div class="message-item">
                            <h4>${msg.name}</h4>
                            <p>${msg.message}</p>
                            <div class="message-time">${msg.email} • ${msg.timestamp}</div>
                        </div>
                    `)
                    .join('');
            } catch (error) {
                console.error('Error loading messages:', error);
            }
        }
        
        async function updateStats() {
            try {
                const response = await fetch(API_ENDPOINT);
                const data = await response.json();
                document.getElementById('messageCount').textContent = data.messages.length;
            } catch (error) {
                console.error('Error updating stats:', error);
            }
        }
        
        // Initialize
        updateStats();
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/messages', methods=['GET', 'POST'])
def handle_messages():
    if request.method == 'POST':
        data = request.get_json()
        
        if not data.get('name') or not data.get('email') or not data.get('message'):
            return jsonify({'error': 'Missing fields'}), 400
        
        message_entry = {
            'name': data['name'],
            'email': data['email'],
            'message': data['message'],
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        messages.append(message_entry)
        return jsonify({'success': True, 'message': 'Message saved'}), 201
    
    return jsonify({'messages': messages}), 200

@app.route('/api/data')
def get_data():
    return jsonify({
        'message': 'Hello from the API!',
        'status': 'success',
        'version': '2.0',
        'features': ['messaging', 'api', 'responsive design']
    }), 200

@app.route('/api/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'messages_count': len(messages),
        'timestamp': datetime.now().isoformat()
    }), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
