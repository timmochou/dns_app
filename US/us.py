from flask import Flask, request
import socket
import requests


app = Flask(__name__)


@app.route('/fibonacci')
def get_fib_request():

    hostname = request.args.get('hostname')
    fs_port = request.args.get('fs_port')
    number = request.args.get('number')
    as_ip = request.args.get('as_ip')
    as_port = request.args.get('as_port')

    if not all([hostname, fs_port, number, as_ip, as_port]):
        return "Missing parameters", 400
    

    # Use UDP to search DNS

    dns_query = f"TYPE=A\nNAME={hostname}"


    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(5)

        sock.sendto(dns_query.encode(), (as_ip, int(as_port)))
        
        # For receiving AS response
        data, _ = sock.recvfrom(1024)
        dns_response = data.decode()
        
        # TYPE=A\nNAME=...\nVALUE=1.2.3.4\nTTL=...
        lines = dns_response.splitlines()
        # IP address
        fs_ip = lines[2].split('=')[1]
        
    except Exception as e:
        return f"DNS Lookup Failed: {str(e)}", 500
    finally:
        sock.close()

    # for calculation (HTTP GET)
    try:
        fs_url = f"http://{fs_ip}:{fs_port}/fibonacci?number={number}"
        response = requests.get(fs_url)
        
        if response.status_code == 200:
            return response.text, 200
        else:
            return f"Error from FS: {response.text}", response.status_code
            
    except Exception as e:
        return f"Failed to connect to FS: {str(e)}", 500

if __name__ == "__main__":
    # run in port 8080
    app.run(host='0.0.0.0', port=8080)