from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Function to validate token (dummy example for offline validation)
def validate_token(token):
    # Aap is function ko apne use case ke hisab se modify kar sakte hain.
    # Example: Agar token "valid_token" hai, to return True, else False
    if token == "valid_token":
        return True
    else:
        return False

@app.route('/')
def index():
    return '''
        <html>
            <body>
                <h1>Token Validator</h1>
                <form action="/validate" method="post" enctype="multipart/form-data">
                    <label for="token">Enter your token:</label><br>
                    <input type="text" id="token" name="token" required><br><br>
                    <input type="submit" value="Validate">
                </form>
                <br><br>
                <h3>Or Upload a file with tokens (one per line):</h3>
                <form action="/upload" method="post" enctype="multipart/form-data">
                    <input type="file" name="file" accept=".txt" required>
                    <input type="submit" value="Upload Tokens">
                </form>
            </body>
        </html>
    '''

# Route for validating a single token
@app.route('/validate', methods=['POST'])
def validate():
    token = request.form.get('token')
    if token and validate_token(token):
        return jsonify({'status': 'valid', 'token': token})
    else:
        return jsonify({'status': 'invalid', 'token': token})

# Route for uploading file with tokens
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'status': 'error', 'message': 'No file part'})

    file = request.files['file']
    if file.filename == '':
        return jsonify({'status': 'error', 'message': 'No selected file'})

    if file and file.filename.endswith('.txt'):
        tokens = file.read().decode('utf-8').splitlines()
        result = []
        for token in tokens:
            result.append({'token': token, 'status': 'valid' if validate_token(token) else 'invalid'})
        
        return jsonify(result)
    else:
        return jsonify({'status': 'error', 'message': 'Invalid file type. Only .txt files are allowed.'})

# Start the server on local machine
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001)
