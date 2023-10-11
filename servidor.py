import http.server
import socketserver
import os
import threading
import socket
import psutil 
import time 

# Variáveis globais para estatísticas
request_count = 0

# Função para iniciar o servidor
def start_server():
    porta = 8080
    handler = http.server.SimpleHTTPRequestHandler
    # Diretório da subpasta que contém os arquivos HTML
    pasta_servidor = os.path.join(os.getcwd(), "site_festa_junina")

    print(f"Servidor está rodando em: http://seuIPaqui:{porta}")

    with socketserver.TCPServer(('0.0.0.0', porta), handler) as httpd:
        os.chdir(pasta_servidor)  # Muda o diretório para a subpasta
        httpd.serve_forever()

# Custom handler para adicionar funcionalidades extras
class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        # Captura o endereço IP do cliente
        client_ip = self.client_address[0]
        # Adiciona o endereço IP ao registro de log
        super().log_message("%s - - [%s] %s\n" % (client_ip, self.log_date_time_string(), format % args))

    def do_GET(self):
        global request_count

        # Conta o número de requisições
        request_count += 1

        # Responde à solicitação GET normalmente
        super().do_GET()

# Função para monitorar o uso de CPU, memória e rede
def monitor_usage():
    while True:
        # Obtém o uso de CPU e memória
        cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
        memory_percent = psutil.virtual_memory().percent

        # Obtém estatísticas de rede
        net_io = psutil.net_io_counters()

        # Exibe o uso de CPU, memória e estatísticas de rede
        print(f"Uso de CPU (por núcleo): {cpu_percent}% | Uso de Memória: {memory_percent}%")
        print(f"Bytes Recebidos: {net_io.bytes_recv} | Bytes Enviados: {net_io.bytes_sent}")

        time.sleep(1)

# Inicia o servidor em uma thread separada
server_thread = threading.Thread(target=start_server)
server_thread.start()

# Inicia o monitoramento em outra thread
monitor_thread = threading.Thread(target=monitor_usage)
monitor_thread.start()
