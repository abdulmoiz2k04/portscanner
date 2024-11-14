import socket
import sys
import ipaddress
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

#Define our target
# if len(sys.argv) == 2:
@app.route('/scan', methods=['POST'])
def scan_ip():
    data = request.get_json()

    if not data or 'ip' not in data:
        return jsonify({"error": "IP address is required in the request"}), 400
    try:
        target_ip = str(ipaddress.ip_address(data['ip']))
        print(f'Scanning Target {target_ip}')
    except ValueError:
        return jsonify({"error":"Invalid IP: Please provide a valid IP."}), 400
        # sys.exit()
    # else:
    #     print("Invalid Format! Usage: python script.py <IP_ADDRESS>")

    start_time = datetime.now()
    print(f'Scan Starting Time for {target_ip}: {str(start_time)}')

    port_result = scan_ports(target_ip)

    end_time = datetime.now()
    duration = end_time - start_time

    return jsonify({
        'target': target_ip,
        'port_result': port_result,
        'duration': duration.total_seconds()
    })
    
port_list = [21, 22, 23, 25, 53, 67, 68, 69, 80, 443, 110, 139, 445, 143, 161]
#Socket Logic
def scan_ports(target_ip):
    port_result = []
    for port in port_list:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        result = s.connect_ex((target_ip, port))
        if result == 0:
            open_status = f'Port {port} is open.'
            port_result.append(open_status)
        else:
            closed_status = f'Port {port} is closed.'
            port_result.append(closed_status)
        s.close()
    return port_result


#Socket Logic - FOR TERMINAL

# port_list = [21, 22, 23, 25, 53, 67, 68, 69, 80, 443, 110, 139, 445, 143, 161]

# try:
#     for port in port_list:
#         s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         s.settimeout(1)
#         result = s.connect_ex((target, port))
#         if result == 0:
#             print(f'Port {port} is open.')
#         else:
#             print(f'Port {port} is closed.')
#         s.close()
# except KeyboardInterrupt:
#     print('\nExiting Program!')
#     sys.exit()
# except socket.gaierror:
#     print('Hostname could not be resolved.')
#     sys.exit()
# except socket.error:
#     print('Could not connect to the server')
#     sys.exit()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)