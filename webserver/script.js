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
          <button onclick='carregarParaEdicao(${lista.id})'>Editar</button>
          <button onclick="window.location.href='editarFilme.html?id=${lista.id}'">Editar</button>
        </li>
      `;
    });
  });


// ------------- EDITAR FILMES ---------------
// Enviar as alterações ao servidor
document.getElementById("formEditar").addEventListener("submit", function(e) {
  e.preventDefault(); // Evita que o formulário seja enviado como padrão

  // Cria um objeto com os dados atualizados
  const filme = {
    id: document.getElementById('id').value,
    nome: document.getElementById('nome').value,
    atores: document.getElementById('atores').value,
    diretor: document.getElementById('diretor').value,
    ano: document.getElementById('ano').value,
    genero: document.getElementById('genero').value,
    produtora: document.getElementById('produtora').value,
    sinopse: document.getElementById('sinopse').value
  };

  // Verifica se o id foi corretamente passado
  if (!filme.id) {
    alert("ID não encontrado!");
    return;
  }

  // Envia a solicitação PUT para editar o filme
  fetch(`http://localhost:8000/editarfilme?id=${filme.id}`, {
    method: 'PUT',  // Alterar de 'POST' para 'PUT'
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams(filme).toString(),  // Envia os dados do filme como parâmetros de URL
  })
  .then(res => res.json())
  .then(data => {
    alert(data.message || "Filme editado com sucesso!");
    fetchFilmes(); // Recarrega a lista de filmes após a edição
  })
  .catch(err => console.error(err));
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
      fetchFilmes(); // Recarrega a lista de filmes após a exclusão
    })
    .catch(err => console.error(err));
  }
}

