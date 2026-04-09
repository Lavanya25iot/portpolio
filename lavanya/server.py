from flask import Flask, request, jsonify, send_from_directory, render_template_string
from flask_cors import CORS
import os
import sys

sys.path.append(os.path.dirname(__file__))

from database import init_database, add_contact, increment_visitor_count, get_all_contacts

app = Flask(__name__, static_folder='.')
CORS(app)

init_database()


# ---------------- HOME ----------------
@app.route('/')
def home():
    return send_from_directory('.', 'index.html')


# ---------------- ADMIN ----------------
@app.route('/admin')
def admin():
    contacts = get_all_contacts()

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Admin Panel</title>
        <style>
            body {
                font-family: Arial;
                padding: 20px;
                background: #f4f6fb;
            }
            h1 {
                text-align: center;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                background: white;
            }
            th, td {
                padding: 12px;
                border-bottom: 1px solid #eef1f8;
                text-align: left;
            }
            th {
                background: #1b2440;
                color: #fff;
            }
            .count {
                text-align: center;
                margin: 16px 0;
                font-weight: bold;
            }
        </style>
    </head>
    <body>
        <h1>📬 Lavanya Portfolio Contact Messages</h1>

        <div class="count">
            Total Messages: {{ contacts|length }}
        </div>

        <table>
            <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Email</th>
                <th>Message</th>
                <th>Date</th>
            </tr>

            {% for contact in contacts %}
            <tr>
                <td>{{ contact.id }}</td>
                <td>{{ contact.name }}</td>
                <td>{{ contact.email }}</td>
                <td>{{ contact.message }}</td>
                <td>{{ contact.created_at }}</td>
            </tr>
            {% endfor %}
        </table>

    </body>
    </html>
    """

    return render_template_string(html, contacts=contacts)


# ---------------- STATIC FILES ----------------
@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)


# ---------------- CONTACT API ----------------
@app.route('/api/contact', methods=['POST'])
def contact():
    try:
        data = request.get_json() or {}

        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        message = data.get('message', '').strip()

        if not name or not email or not message:
            return jsonify({
                'error': 'All fields are required',
                'success': False
            }), 400

        if '@' not in email or '.' not in email:
            return jsonify({
                'error': 'Invalid email address',
                'success': False
            }), 400

        success = add_contact(name, email, message)

        if success:
            return jsonify({
                'message': 'Message sent successfully. Sindhu will get back to you soon!',
                'success': True
            }), 200

        return jsonify({
            'error': 'Failed to save message. Please try again.',
            'success': False
        }), 500

    except Exception as e:
        print(f"Error in contact endpoint: {e}")
        return jsonify({
            'error': 'Internal server error',
            'success': False
        }), 500


# ---------------- STATS ----------------
@app.route('/api/stats', methods=['GET'])
def stats():
    try:
        visitor_count = increment_visitor_count()
        return jsonify({
            'visitors': visitor_count,
            'success': True
        }), 200
    except Exception as e:
        print(f"Error in stats endpoint: {e}")
        return jsonify({
            'error': 'Internal server error',
            'success': False
        }), 500


# ---------------- PROFILE ----------------
@app.route('/api/profile', methods=['GET'])
def profile():
    return jsonify({
        'name': 'Lavanya HM',
        'role': 'BCA Student',
        'about': 'I am a BCA student passionate about web development, problem solving, and building clean user experiences.',
        'skills': ['HTML', 'CSS', 'JavaScript', 'Python', 'Flask', 'SQLite'],
        'email': 'lavanya@example.com'
    }), 200


# ---------------- HEALTH ----------------
@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'healthy',
        'message': 'Server is running'
    }), 200


# ---------------- RUN ----------------
if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("🚀 Starting Lavanya's Portfolio Server")
    print("=" * 60)
    print("📍 Website: http://localhost:5000")
    print("📍 Admin:   http://localhost:5000/admin")
    print("=" * 60 + "\n")

    app.run(debug=True, host='0.0.0.0', port=5000)