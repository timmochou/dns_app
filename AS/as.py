import socket

def run_as():
    # 建立 UDP Socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # 綁定 53533 Port (根據題目要求)
    sock.bind(('0.0.0.0', 53533))
    
    # 記憶體內的通訊錄 (Dictionary)
    # 格式: { "fibonacci.com": "172.18.0.3" }
    dns_table = {}
    
    print("AS Server is listening on UDP port 53533...")
    
    while True:
        # 接收資料
        data, addr = sock.recvfrom(1024)
        message = data.decode()
        print(f"Received message: \n{message} from {addr}")
        
        lines = message.splitlines()
        
        # 判斷是「註冊」還是「查詢」
        # 註冊格式通常包含 VALUE=...
        if "VALUE=" in message:
            # 解析註冊訊息
            record = {}
            for line in lines:
                if '=' in line:
                    key, val = line.split('=')
                    record[key] = val
            
            # 存入通訊錄
            name = record.get('NAME')
            value = record.get('VALUE')
            if name and value:
                dns_table[name] = value
                print(f"Registered: {name} -> {value}")
        
        # 查詢格式 (只有 TYPE=A 和 NAME=...)
        else:
            name_to_query = ""
            for line in lines:
                if "NAME=" in line:
                    name_to_query = line.split('=')[1]
            
            if name_to_query in dns_table:
                # 構造回傳訊息
                response = f"TYPE=A\nNAME={name_to_query}\nVALUE={dns_table[name_to_query]}\nTTL=10"
                sock.sendto(response.encode(), addr)
                print(f"Sent response to {addr}")

if __name__ == "__main__":
    run_as()