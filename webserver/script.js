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
          <button onclick='deleteFilme(${lista.id})'>Excluir</button>
        </li>
      `;
    });
  });

// ------------- EDITAR FILMES ---------------
// função de carregar os dados do filme no formulário
function carregarParaEdicao(id) {
    const filme = filmes.find(f => f.id === id);
    if (!filme) return alert("Filme não encontrado!");
    
    document.getElementById("id").value = filme.id;
    document.getElementById("nome").value = filme.nome;
    document.getElementById("atores").value = filme.atores;
    document.getElementById("diretor").value = filme.diretor;
    document.getElementById("ano").value = filme.ano;
    document.getElementById("genero").value = filme.genero;
    document.getElementById("produtora").value = filme.produtora;
    document.getElementById("sinopse").value = filme.sinopse;
}

// enviar edição para o servidor
document.getElementById("formEditar").addEventListener("submit", function(e){
    e.preventDefault();
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

    fetch('http://localhost:8000/editarfilme', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams(filme).toString(),
    })
    .then(res => res.json())
    .then(data => alert(data.message || "Filme editado!"))
    .catch(err => console.error(err));
});


// ------------- DELETAR FILMES ---------------
function deleteFilme(id){
    fetch(`http://localhost:8000/deletarfilme?id=${id}`, { method: 'DELETE' })
        .then(res => res.json())
        .then(data => {
            alert(data.message);
            // opcional: remover da tela sem recarregar
            filmes = filmes.filter(f => f.id !== id);
            document.querySelector('#listafilmes').innerHTML = '';
            filmes.forEach(filme => {
                document.querySelector('#listafilmes').innerHTML += `
                  <li>
                    <strong>${filme.nome}</strong> (${filme.ano})<br>
                    <button onclick="carregarParaEdicao(${filme.id})">Editar</button>
                    <button onclick="deleteFilme(${filme.id})">Excluir</button>
                  </li>
                `;
            });
        })
        .catch(err => console.error(err));
}

