import os
import sys
import tempfile
from flask import Flask, render_template, request, jsonify, send_file

# Ensure Flask can find the 'core' directory from the 'web' directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.data_manager import load_data, save_data
from core.pdf_exporter import export_menu_pdf

app = Flask(__name__, template_folder='../templates', static_folder='../static')

@app.route('/')
def index():
    # Load the actual data to display on the dashboard
    data = load_data()
    return render_template('index.html', data=data)

@app.route('/menu')
def menu_view():
    # A clean view of just the menu
    data = load_data()
    return render_template('menu.html', data=data)

@app.route('/api/menu', methods=['GET'])
def api_get_menu():
    return jsonify(load_data())

@app.route('/api/menu', methods=['POST'])
def api_post_menu():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    save_data(data)
    return jsonify({"ok": True})

@app.route('/api/pdf')
def api_get_pdf():
    data = load_data()
    
    # Create a temporary file to hold the PDF
    fd, temp_path = tempfile.mkstemp(suffix=".pdf")
    os.close(fd) # Close the file descriptor so reportlab can write to it
    
    try:
        export_menu_pdf(data, temp_path)
        # send_file handles the cleanup of the temp file automatically
        return send_file(temp_path, as_attachment=True, download_name="menu.pdf", mimetype='application/pdf')
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
