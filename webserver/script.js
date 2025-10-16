// ------------- LISTAR FILMES ---------------
fetch('http://localhost:8000/api_listarfilmes')
  .then(res => res.json())
  .then(data => {
    console.log('Dados recebidos:', data);
    const listaFilmes = document.getElementById('listafilmes');
    listaFilmes.innerHTML = ''; // limpa a lista antes de adicionar

    data.forEach(filme => {
      const item = document.createElement('li');

      item.innerHTML = `
        <img src="${filme.poster || ''}" alt="Poster do filme" style="max-width:100px;"><br>
        <strong>Nome do filme:</strong> ${filme.titulo} <br>
        <strong>Atores:</strong> ${filme.atores} <br>
        <strong>Diretores:</strong> ${filme.diretores} <br>
        <strong>Ano:</strong> ${filme.ano} <br>
        <strong>Gêneros:</strong> ${filme.generos} <br>
        <strong>Produtoras:</strong> ${filme.produtoras} <br>
        <strong>Tempo de duração:</strong> ${filme.tempo_duracao} <br>
        <button onclick="deleteFilme(${filme.id_filme})">Excluir</button>
        <button onclick="window.location.href='editar.html?id=${filme.id_filme}'">Editar</button>
      `;

      listaFilmes.appendChild(item);
    });
  })
  .catch(err => {
    console.error('Erro ao carregar filmes:', err);
  });




// // ------------- EDITAR FILMES ---------------
// // Enviar as alterações ao servidor
// document.getElementById("formEditar").addEventListener("submit", function(e) {
//     e.preventDefault();

//     // Pega os valores atuais do formulário
//     const id = document.getElementById('id').value;

//     const filme = {
//         id: id,
//         nome: document.getElementById('nome').value || undefined,
//         atores: document.getElementById('atores').value || undefined,
//         diretor: document.getElementById('diretor').value || undefined,
//         ano: document.getElementById('ano').value || undefined,
//         genero: document.getElementById('genero').value || undefined,
//         produtora: document.getElementById('produtora').value || undefined,
//         sinopse: document.getElementById('sinopse').value || undefined,
//     };

//     fetch('http://localhost:8000/editarfilme', {
//         method: 'POST',
//         headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
//         body: new URLSearchParams(filme).toString(),
//     })
//     .then(res => res.json())
//     .then(data => {
//         if (data.message) {
//             alert(data.message);
//             window.location.href = 'listar_filmes';
//         } else {
//             alert('Erro ao atualizar o filme.');
//         }
//     })
//     .catch(err => console.error("Erro:", err));
// });




// // ------------- DELETE FILMES ---------------
// // Função para excluir um filme
// function deleteFilme(id) {
//   if (confirm('Tem certeza que deseja excluir este filme?')) {
//     fetch(`http://localhost:8000/deletarfilme`, {
//       method: 'POST',
//       headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
//       body: new URLSearchParams({ id }).toString() // Envia o id do filme como parâmetro
//     })
//     .then(res => res.json())
//     .then(data => {
//       alert(data.message || "Filme excluído com sucesso!");
//         location.reload(); // recarrega a página inteira
//     })
//     .catch(err => console.error(err));
//   }
// }

