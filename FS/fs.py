from flask import Flask, request
import socket
import json

app = Flask(__name__)

# fibonacci
def calculate_fibonacci(n):
    if n <= 0: return 0
    if n == 1: return 1
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

# Provide HTTP GET interface for US 
@app.route('/fibonacci')
def fibonacci():
    number = request.args.get('number')
    
    # parameter validation
    if not number or not number.isdigit():
        return "Bad Request: 'number' must be an integer", 400
    
    result = calculate_fibonacci(int(number))
    return str(result), 200

# Register FS details with the Authoritative Server (AS) using UDP
@app.route('/register', methods=['PUT'])
def register():
    content = request.json
    hostname = content.get('hostname')
    ip = content.get('ip')
    as_ip = content.get('as_ip')
    as_port = content.get('as_port')

    
    # TYPE=A, NAME=..., VALUE=..., TTL=10
    registration_msg = f"TYPE=A\nNAME={hostname}\nVALUE={ip}\nTTL=10"
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(registration_msg.encode(), (as_ip, int(as_port)))
        return "Registration successful", 201
    except Exception as e:
        return f"Registration failed: {str(e)}", 500

if __name__ == "__main__":
    # FS running 9090
    app.run(host='0.0.0.0', port=9090)