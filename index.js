// Lista para armazenar os participantes
const participantes = [];

// Evento para cadastrar participantes
document.getElementById('formCadastro').addEventListener('submit', function(event) {
    event.preventDefault();

    const nome = document.getElementById('nome').value;
    const comprarCarne = document.getElementById('comprar_carne').checked;
    const comprarBebidas = document.getElementById('comprar_bebidas').checked;

    // Adiciona participante à lista
    participantes.push({ nome, comprar_carne: comprarCarne, comprar_bebidas: comprarBebidas });

    // Atualiza a lista de participantes na tela
    atualizarParticipantes();

    // Limpa o formulário
    document.getElementById('formCadastro').reset();
    closeModal(); // Fecha o modal após cadastrar
});

// Função para atualizar a lista de participantes
function atualizarParticipantes() {
    const lista = document.getElementById('lista-participantes');
    lista.innerHTML = ''; // Limpa a lista antes de atualizar

    participantes.forEach((part, index) => {
        const li = document.createElement('li');
        li.textContent = `${part.nome} - Carne: ${part.comprar_carne ? 'Sim' : 'Não'} - Bebidas: ${part.comprar_bebidas ? 'Sim' : 'Não'}`;
        lista.appendChild(li);
    });
}

// Evento para calcular a quantidade de carne e bebidas
document.getElementById('calcularBtn').addEventListener('click', function() {
    const adultos = parseInt(document.getElementById('adultos').value) || 0;
    const criancas = parseInt(document.getElementById('criancas').value) || 0;
    const tipo = document.getElementById('tipo').value;

    // Dados para enviar ao backend
    const data = {
        adultos,
        criancas,
        tipo,
        carne: participantes.filter(p => p.comprar_carne).length,
        bebidas: participantes.filter(p => p.comprar_bebidas).length
    };

    // Envia os dados ao backend via POST
    fetch('/calcular', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert("Erro: " + data.error);
            return;
        }

        // Atualiza os campos da tela com os resultados
        document.getElementById('total_carne').textContent = data.total_carne_kg;
        document.getElementById('cerveja_latas').textContent = data.cerveja_latas;
        document.getElementById('refrigerante_litros').textContent = data.refrigerante_litros;
        document.getElementById('agua_litros').textContent = data.agua_litros;
        document.getElementById('preco_total').textContent = data.preco_total.toFixed(2);
    })
    .catch(error => {
        console.error('Erro na requisição:', error);
        alert("Erro ao calcular: " + error.message);
    });
});

// Modal open and close
const modal = document.getElementById('modalCadastro');
const openModalBtn = document.getElementById('openModalBtn');
const closeModalBtn = document.getElementById('closeModalBtn');

// Função para abrir o modal
openModalBtn.onclick = function() {
    modal.style.display = 'block';
}

// Função para fechar o modal
closeModalBtn.onclick = function() {
    modal.style.display = 'none';
}

// Fechar o modal quando clicar fora da área do modal
window.onclick = function(event) {
    if (event.target === modal) {
        modal.style.display = 'none';
    }
}
