// ------------- LISTAR FILMES ---------------
let filmes = []; // aqui vamos guardar os filmes do servidor

fetch('http://localhost:8000/listarfilmes')
  .then(res => res.json())
  .then(data => {
    filmes = data;
    const lis = document.querySelector('#listafilmes');
    data.forEach((lista) => { //forEach para iterar a cada edição
      lis.innerHTML += `
        <li>
          <img src="${lista.capa}" /><br>
          <strong>Nome do filme:</strong> ${lista.nome}<br>
          <strong>Atores:</strong> ${lista.atores}<br>
          <strong>Diretor:</strong> ${lista.diretor}<br>
          <strong>Ano:</strong> ${lista.ano}<br>
          <strong>Gênero:</strong> ${lista.genero}<br>
          <strong>Produtora:</strong> ${lista.produtora}<br>
          <strong>Sinopse:</strong> ${lista.sinopse}<br>
          <button onclick='deleteFilme(${lista.id})'>Excluir</button>
          <button onclick="window.location.href='editar.html?id=${lista.id}'">Editar</button>
        </li>
      `;
    });
  });


// ------------- EDITAR FILMES ---------------
// Enviar as alterações ao servidor
document.getElementById("formEditar").addEventListener("submit", function(e) {
    e.preventDefault();

    // Pega os valores atuais do formulário
    const id = document.getElementById('id').value;

    const filme = {
        id: id,
        nome: document.getElementById('nome').value || undefined,
        atores: document.getElementById('atores').value || undefined,
        diretor: document.getElementById('diretor').value || undefined,
        ano: document.getElementById('ano').value || undefined,
        genero: document.getElementById('genero').value || undefined,
        produtora: document.getElementById('produtora').value || undefined,
        sinopse: document.getElementById('sinopse').value || undefined,
    };

    fetch('http://localhost:8000/editarfilme', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams(filme).toString(),
    })
    .then(res => res.json())
    .then(data => {
        if (data.message) {
            alert(data.message);
            window.location.href = 'listar_filmes';
        } else {
            alert('Erro ao atualizar o filme.');
        }
    })
    .catch(err => console.error("Erro:", err));
});




// ------------- DELETE FILMES ---------------
// Função para excluir um filme
function deleteFilme(id) {
  if (confirm('Tem certeza que deseja excluir este filme?')) {
    fetch(`http://localhost:8000/deletarfilme`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams({ id }).toString() // Envia o id do filme como parâmetro
    })
    .then(res => res.json())
    .then(data => {
      alert(data.message || "Filme excluído com sucesso!");
        location.reload(); // recarrega a página inteira
    })
    .catch(err => console.error(err));
  }
}

