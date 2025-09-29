const lis = document.querySelector('#listafilmes');

fetch('http://localhost:8000/listarfilmes').then((res)=>{
    return res.json();
}).then((data)=> {
    data.map((lista)=> {
        console.log(lista)
        lis.innerHTML += `
        <li>
            <img src="${lista.capa}"/> </br>
            <strong>Nome do filme:</strong> ${lista.nome} </br>
            <strong>Atores:</strong> ${lista.atores} </br>
            <strong>Diretor:</strong> ${lista.diretor} </br>
            <strong>Ano:</strong> ${lista.ano} </br>
            <strong>Gênero:</strong> ${lista.genero} </br>
            <strong>Produtora:</strong> ${lista.produtora} </br>
            <strong>Sinopse:</strong> ${lista.sinopse} </br>
        </li>`
    });
});

function editFilme(filmeId) {
    const filme = {
        id: filmeId,
        nome: document.getElementById('nome').value,
        atores: document.getElementById('atores').value,
        diretor: document.getElementById('diretor').value,
        ano: document.getElementById('ano').value,
        genero: document.getElementById('genero').value,
        produtora: document.getElementById('produtora').value,
        sinopse: document.getElementById('sinopse').value,
    };

    fetch(`/edit_filme`, {
        method: 'PUT',  // Aqui estamos usando o método PUT
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams(filme).toString(),
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message);  // Exibe a mensagem de sucesso
        alert(data.message);
    })
    .catch(error => {
        console.error('Erro ao editar filme:', error);
    });
};

function deleteFilme(filmeId) {
    fetch(`/delete_filme?id=${filmeId}`, {
        method: 'DELETE',  // Aqui usamos o método DELETE
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message);  // Exibe a mensagem de sucesso
        alert(data.message);
    })
    .catch(error => {
        console.error('Erro ao excluir filme:', error);
    });
}

