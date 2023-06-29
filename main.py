import os
from prometheus_client import start_http_server, Counter
import socket

# 创建一个 counter 指标
c = Counter('my_counter', 'Description of counter')


def udp_listen():
    file = open(os.environ.get("RECEIVE_FILE", "UDP_RECEIVE.txt"), "a")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("localhost", os.environ.get("UDP_PORT", 12345)))
    while True:
        data, addr = sock.recvfrom(1024)
        message = data.decode()  # 解码为字符串
        # 将接收到的信息写入文件
        file.write(message + "\n")
        file.flush()  # 立即刷新缓冲区，确保写入文件
        c.inc()  # 增加 counter


if __name__ == '__main__':
    # 启动 Prometheus 服务器
    start_http_server(os.environ.get("HTTP_PORT", 8000))
    # 启动一个新的线程监听 UDP
    # t = Thread(target=udp_listen)
    udp_listen()
