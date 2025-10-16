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
# Importação da biblioteca (precisa instalar: pip install mysql-connector-python)
import mysql.connector


# Interligando com a conexão do seu banco de dados
mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "senai"
)

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
        # ---------- GET LOGIN ----------
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


        # ---------- GET CADASTRO ----------
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

        # ---------- LISTA FILMES ----------
        # Serve a página HTML com a lista de filmes
        elif self.path == '/listarfilmes':
            try:
                with open(os.path.join(os.getcwd(), 'listarFilmes.html'), 'r', encoding='utf-8') as file:
                    content = file.read()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(content.encode('utf-8'))
            except FileNotFoundError:
                self.send_error(404, "File Not Found")

        # ---------- LISTA FILMES ----------
        elif self.path == '/api_listarfilmes':
            print(f"Caminho requisitado: {self.path}") 
            cursor = mydb.cursor(dictionary=True)
            sql = """
                SELECT 
                    f.id_filme,
                    f.titulo,
                    f.orcamento,
                    f.tempo_duracao,
                    f.ano,
                    f.poster,
                    GROUP_CONCAT(DISTINCT CONCAT(a.nome, ' ', a.sobrenome) SEPARATOR ', ') AS atores,
                    GROUP_CONCAT(DISTINCT CONCAT(d.nome, ' ', d.sobrenome) SEPARATOR ', ') AS diretores,
                    GROUP_CONCAT(DISTINCT p.nome SEPARATOR ', ') AS produtoras,
                    GROUP_CONCAT(DISTINCT g.nome SEPARATOR ', ') AS generos,
                    GROUP_CONCAT(DISTINCT pais.nome SEPARATOR ', ') AS paises,
                    GROUP_CONCAT(DISTINCT l.nome SEPARATOR ', ') AS linguagens
                FROM PLATAFORMA_FILMES.FIlme f
                LEFT JOIN PLATAFORMA_FILMES.Ator_Filme af ON f.id_filme = af.id_filme
                LEFT JOIN PLATAFORMA_FILMES.Ator a ON af.id_ator = a.id_ator
                LEFT JOIN PLATAFORMA_FILMES.Diretor_Filme df ON f.id_filme = df.id_filme
                LEFT JOIN PLATAFORMA_FILMES.Diretor d ON df.id_diretor = d.id_diretor
                LEFT JOIN PLATAFORMA_FILMES.Produtora_Filme pf ON f.id_filme = pf.id_filme
                LEFT JOIN PLATAFORMA_FILMES.Produtora p ON pf.id_produtora = p.id_produtora
                LEFT JOIN PLATAFORMA_FILMES.Genero_Filme gf ON f.id_filme = gf.id_filme
                LEFT JOIN PLATAFORMA_FILMES.Genero g ON gf.id_genero = g.id_genero
                LEFT JOIN PLATAFORMA_FILMES.Pais_Filme pf2 ON f.id_filme = pf2.id_filme
                LEFT JOIN PLATAFORMA_FILMES.Pais pais ON pf2.id_pais = pais.id_pais
                LEFT JOIN PLATAFORMA_FILMES.Linguagem_Filme lf ON f.id_filme = lf.id_filme
                LEFT JOIN PLATAFORMA_FILMES.Linguagem l ON lf.id_linguagem = l.id_linguagem
                GROUP BY f.id_filme
                ORDER BY f.titulo
            """
            cursor.execute(sql)
            filmes_completos = cursor.fetchall()

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(filmes_completos, default=str).encode('utf-8'))

        else:
            super().do_GET()


    def do_POST(self):
        # ---------- POST LOGIN ----------
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

        # ---------- POST CADASTRO ----------
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

            cursor = mydb.cursor()
            sql = "INSERT INTO PLATAFORMA_FILMES.Filme (titulo, atores, diretor, ano, genero, produtora, sinopse) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            values = (nome, atores, diretor, ano, genero, produtora, sinopse)
            cursor.execute(sql, values)
            mydb.commit()

            self.send_response(200)
            self.send_header("Content-type", 'text/html')
            self.end_headers()
            self.wfile.write("Filme cadastrado com sucesso!".encode('utf-8'))

        # ---------- EDITAR ----------
        elif self.path == '/editarfilme':
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length).decode('utf-8')
            form_data = parse_qs(body)

            filme_id = int(form_data.get('id', [0])[0])
            nome = form_data.get('nome', [""])[0]
            atores = form_data.get('atores', [""])[0]
            diretor = form_data.get('diretor', [""])[0]
            ano = form_data.get('ano', [""])[0]
            genero = form_data.get('genero', [""])[0]
            produtora = form_data.get('produtora', [""])[0]
            sinopse = form_data.get('sinopse', [""])[0]

            cursor = mydb.cursor()
            sql = """UPDATE PLATAFORMA_FILMES.Filme SET titulo=%s, atores=%s, diretor=%s, ano=%s, genero=%s, produtora=%s, sinopse=%s WHERE id=%s"""
            values = (nome, atores, diretor, ano, genero, produtora, sinopse, filme_id)
            cursor.execute(sql, values)
            mydb.commit()

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({'message': 'Filme editado com sucesso'}).encode('utf-8'))

        # ---------- DELETE ----------
        elif self.path == '/deletarfilme':
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length).decode('utf-8')
            form_data = parse_qs(body)

            filme_id = int(form_data.get('id', [0])[0])

            cursor = mydb.cursor()
            sql = "DELETE FROM PLATAFORMA_FILMES.Filme WHERE id=%s"
            cursor.execute(sql, (filme_id,))
            mydb.commit()

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({'message': 'Filme deletado com sucesso'}).encode('utf-8'))

        else:
            super(MyHandle, self).do_POST()
            
    
    
def main():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, MyHandle)
    print("Server Running in http://localhost:8000")
    httpd.serve_forever()

main()