"""from http.server import SimpleHTTPRequestHandler, HTTPServer

#definindo a porta
port = 8000

#definindo o gerenciador/manipulador de requisições
handler = SimpleHTTPRequestHandler

#criando a instância do servidor
server = HTTPServer(('localhost', port), handler)

#imprimindo mensagem de OK
print(f"Server Running in http://localhost:{port}")

server.serve_forever()"""

import os
from http.server import SimpleHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
import json

# Lista para armazenar os livros cadastrados 
filmes_cadastrados = []

# Carregar filmes do arquivo JSON (se existir)
def load_filmes():
    global filmes_cadastrados
    if os.path.exists('filmes.json'):
        with open('filmes.json', 'r', encoding='utf-8') as f:
            try:
                filmes_cadastrados = json.load(f)
            except json.JSONDecodeError:
                filmes_cadastrados = []

# Salvar filmes no arquivo JSON
def save_filmes():
    with open('filmes.json', 'w', encoding='utf-8') as f:
        json.dump(filmes_cadastrados, f, ensure_ascii=False, indent=4)

# Carregar filmes ao iniciar o servidor
load_filmes()

class MyHandle (SimpleHTTPRequestHandler):
    def list_directory(self, path):
        try:
            f = open(os.path.join(path, 'index.html'), 'r')

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(f.read().encode('utf-8'))
            f.close()
            return None
        except FileNotFoundError:
            pass
        return super().list_directory(path)
    
    def account_user(self, usuario, senha):
        login = "isaabreucorrea@gmail.com"
        password = "12345"

        if usuario == login and senha == password:
            return "Usuário logado com sucess :)"
        else:
            return "Usuário não existente :("


    def do_GET(self):
        if self.path == '/login':
            try:
                with open(os.path.join(os.getcwd(), 'login.html'), 'r') as login:
                    content = login.read()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(content.encode("utf-8"))
            except FileNotFoundError:
                self.send_error(404, "File Not Found")

        elif self.path == '/cadastro':
            try:
                with open(os.path.join(os.getcwd(), 'cadastro.html'), 'r') as cadastro:
                    content = cadastro.read()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(content.encode("utf-8"))
            except FileNotFoundError:
                self.send_error(404, "File Not Found")

        # lista de filmes em html
        elif self.path == '/listar_filmes':
            try:
                with open(os.path.join(os.getcwd(), 'listarFilmes.html'), 'r') as listarFilmes:
                    content = listarFilmes.read()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(content.encode("utf-8"))
            except FileNotFoundError:
                self.send_error(404, "File Not Found")

        # lista filmes em json
        elif self.path == '/listarfilmes':
            arquivo = 'filmes.json'

            if os.path.exists(arquivo):
                with open(arquivo, encoding='utf-8') as listagem:
                    try:
                        filmes = json.load(listagem)
                    except json.JSONDecodeError:
                        filmes = []
            else:
                filmes = []

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(filmes).encode('utf-8'))

        else:
            super().do_GET()


    def do_POST(self):
        if self.path == '/sendlogin':
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length).decode('utf-8')
            form_data = parse_qs(body)

            usuario = form_data.get('usuario',[""])[0]
            senha = form_data.get('senha', [""])[0]

            logou = self.account_user(usuario, senha)

            print("Data Form: ")
            print("Email: ", form_data.get('usuario', [''])[0])
            print("Password: ", form_data.get('senha', [''])[0])

            self.send_response(200)
            self.send_header("Content-type", 'text/html')
            self.end_headers()
            self.wfile.write(logou.encode('utf-8'))

        elif self.path == '/sendcadastro':
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length).decode('utf-8')
            form_data = parse_qs(body)

            nome = form_data.get('nome',[""])[0]
            atores = form_data.get('atores', [""])[0]
            diretor = form_data.get('diretor', [""])[0]
            ano = form_data.get('ano', [""])[0]
            genero = form_data.get('genero', [""])[0]
            produtora = form_data.get('produtora', [""])[0]
            sinopse = form_data.get('sinopse', [""])[0]

            # Criando dicionário com os dados do livro
            filme = {
                "nome": nome,
                "atores": atores,
                "diretor": diretor,
                "ano": ano,
                "genero": genero,
                "produtora": produtora,
                "sinopse": sinopse
            }

            filmes_cadastrados.append(filme)

            # Salvar no arquivo JSON
            with open('filmes.json', 'w', encoding='utf-8') as f:
                json.dump(filmes_cadastrados, f, ensure_ascii=False, indent=4)

            print("Data Form: ")
            print("Nome do Filme: ", form_data.get('nome', [''])[0])
            print("Atores: ", form_data.get('atores', [''])[0])
            print("Diretor: ", form_data.get('diretor', [''])[0])
            print("Ano: ", form_data.get('ano', [''])[0])
            print("Genero: ", form_data.get('genero', [''])[0])
            print("Produtora: ", form_data.get('produtora', [''])[0])
            print("Sinopse: ", form_data.get('sinopse', [''])[0])

            self.send_response(200)
            self.send_header("Content-type", 'text/html')
            self.end_headers()
            self.wfile.write("Filme cadastrado com sucess !".encode('utf-8'))

        else:
            super(MyHandle, self).do_POST()
            
    def do_PUT(self):
        if self.path == '/editarfilme':
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length).decode('utf-8')
            form_data = parse_qs(body)
            print(self.path)

            filme_id = form_data.get('id', [None])[0]
            if filme_id:
                try:
                    filme_id = int(filme_id)
                    if 0 <= filme_id < len(filmes_cadastrados):
                        # Atualiza filme
                        filme = filmes_cadastrados[filme_id]
                        filme['nome'] = form_data.get('nome', [''])[0]
                        filme['atores'] = form_data.get('atores', [''])[0]
                        filme['diretor'] = form_data.get('diretor', [''])[0]
                        filme['ano'] = form_data.get('ano', [''])[0]
                        filme['genero'] = form_data.get('genero', [''])[0]
                        filme['produtora'] = form_data.get('produtora', [''])[0]
                        filme['sinopse'] = form_data.get('sinopse', [''])[0]

                        # Atualizar o arquivo JSON com a lista de filmes atualizada
                        save_filmes()

                        self.send_response(200)
                        self.send_header("Content-type", "application/json")
                        self.end_headers()
                        self.wfile.write(json.dumps({'message': 'Filme editado com sucesso'}).encode('utf-8'))
                    else:
                        self.send_response(404)
                        self.end_headers()
                        self.wfile.write(json.dumps({'error': 'Filme não encontrado'}).encode('utf-8'))
                except ValueError:
                    self.send_response(400)
                    self.end_headers()
                    self.wfile.write(json.dumps({'error': 'ID inválido'}).encode('utf-8'))
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'ID do filme não fornecido'}).encode('utf-8'))

    def do_DELETE(self):
        """Método para excluir um filme"""
        if self.path.startswith('/deletarfilme'):
            query = urlparse(self.path).query
            params = parse_qs(query)
            filme_id = params.get('id', [None])[0]
            if filme_id:
                try:
                    filme_id = int(filme_id)
                    if 0 <= filme_id < len(filmes_cadastrados):
                        # Exclui o filme da lista
                        del filmes_cadastrados[filme_id]

                        # Atualizar o arquivo JSON após exclusão
                        save_filmes()

                        self.send_response(200)
                        self.send_header("Content-type", "application/json")
                        self.end_headers()
                        self.wfile.write(json.dumps({'message': 'Filme deletado com sucesso'}).encode('utf-8'))
                    else:
                        self.send_response(404)
                        self.end_headers()
                        self.wfile.write(json.dumps({'error': 'Filme não encontrado'}).encode('utf-8'))
                except ValueError:
                    self.send_response(400)
                    self.end_headers()
                    self.wfile.write(json.dumps({'error': 'ID inválido'}).encode('utf-8'))
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'ID do filme não fornecido'}).encode('utf-8'))
    
def main():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, MyHandle)
    print("Server Running in http://localhost:8000")
    httpd.serve_forever()

main()