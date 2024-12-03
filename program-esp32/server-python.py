from flask import Flask, request
import os

app = Flask(__name__)

# Caminho para a pasta onde o arquivo CSV será salvo
pasta_destino = "C:\\esp32-teste"
# pasta_destino = "/home/usuario/pasta"     # Altere para Linux/Mac

# Caminho completo do arquivo CSV
arquivo_csv = os.path.join(pasta_destino, "dados_sensor.csv")

# Função para verificar se o cabeçalho já foi escrito no arquivo
def verificar_cabecalho():
    # Verifica se o arquivo existe
    if not os.path.exists(arquivo_csv):
        return True  # Se não existir, o cabeçalho precisa ser adicionado
    else:
        # Verifica se o arquivo não está vazio e se o cabeçalho já foi escrito
        with open(arquivo_csv, 'r') as file:
            first_line = file.readline().strip()  # Lê a primeira linha
            if first_line == "data_hora,volume_db,timestamp":  # Verifica o cabeçalho
                return False  # Cabeçalho já existe
            else:
                return True  # O cabeçalho ainda não existe

@app.route('/upload', methods=['POST'])
def upload_dados():
    conteudo = request.data.decode('utf-8')  # Recebe os dados

    print(conteudo)

    # Criar a pasta se não existir
    if not os.path.exists(pasta_destino):
        os.makedirs(pasta_destino)

    # Verifica se precisa adicionar o cabeçalho
    if verificar_cabecalho():
        # Adiciona o cabeçalho e os dados no arquivo CSV
        with open(arquivo_csv, 'a') as arquivo:
            arquivo.write("data_hora,volume_db,timestamp\n")  # Adiciona cabeçalho
            arquivo.write(conteudo + '\n')  # Adiciona os dados recebidos
    else:
        # Adiciona apenas os dados no arquivo CSV, sem o cabeçalho
        with open(arquivo_csv, 'a') as arquivo:
            arquivo.write(conteudo + '\n')  # Adiciona apenas os valores

    return "Dados recebidos e armazenados!", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
