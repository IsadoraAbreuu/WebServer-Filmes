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
if os.path.exists('filmes.json'):
    with open('filmes.json', 'r', encoding='utf-8') as f:
        try:
            filmes_cadastrados = json.load(f)
        except json.JSONDecodeError:
            filmes_cadastrados = []

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

        elif self.path == '/listarfilmes':
            try:
                with open(os.path.join(os.getcwd(), 'listarFilmes.html'), 'r') as listarFilmes:
                    content = listarFilmes.read()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(content.encode("utf-8"))
            except FileNotFoundError:
                self.send_error(404, "File Not Found")

            html = "<html><body><h1>Filmes Cadastrados</h1><ul>"
            if filmes_cadastrados:
                for filme in filmes_cadastrados:
                    html += f"<li><strong>{filme['nome']}</strong> - {filme['diretor']} ({filme['ano']})</li>"
            else:
                html += "<p>Nenhum filme cadastrado.</p>"
            html += "</ul></body></html>"

            self.wfile.write(html.encode())

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
    
def main():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, MyHandle)
    print("Server Running in http://localhost:8000")
    httpd.serve_forever()

main()