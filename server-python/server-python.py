from flask import Flask, request
import os
from datetime import datetime

app = Flask(__name__)

# Caminho para a pasta onde os arquivos CSV serão salvos
pasta_destino = "C:\\esp32-teste"
# pasta_destino = "/home/usuario/pasta"  # Altere para Linux/Mac

def caminho_arquivo_csv():
    # Gera o nome do arquivo com base na data atual
    data_atual = datetime.now().strftime("%Y-%m-%d")
    return os.path.join(pasta_destino, f"dados_sensor_{data_atual}.csv")

# Função para verificar se o cabeçalho já foi escrito no arquivo
def verificar_cabecalho(arquivo_csv):
    if not os.path.exists(arquivo_csv):
        return True
    with open(arquivo_csv, 'r') as file:
        first_line = file.readline().strip()
        return first_line != "data_hora,volume_db,timestamp"

@app.route('/upload', methods=['POST'])
def upload_dados():
    conteudo = request.data.decode('utf-8')

    print(conteudo)

    if not os.path.exists(pasta_destino):
        os.makedirs(pasta_destino)

    arquivo_csv = caminho_arquivo_csv()

    # Verifica se precisa adicionar o cabeçalho
    if verificar_cabecalho(arquivo_csv):
        with open(arquivo_csv, 'a') as arquivo:
            arquivo.write("data_hora,volume_db,timestamp\n")
            arquivo.write(conteudo + '\n')
    else:
        with open(arquivo_csv, 'a') as arquivo:
            arquivo.write(conteudo + '\n')

    return "Dados recebidos e armazenados!", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
