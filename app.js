// Motor Apex com integração FastAPI
// Tenta conectar à API, caso falhe usa LocalStorage como fallback
const API_URL = "http://localhost:8000";
const UseAPI = false; // Mude para true quando o servidor estiver rodando

const ApexEngine = {
    saveRoom: async (dados) => {
        if (UseAPI) {
            try {
                const response = await fetch(`${API_URL}/cadastrar_room`, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        nome: dados.nome,
                        valor: parseFloat(dados.valor),
                        cor: dados.cor,
                        horario_fim: dados.fim
                    })
                });
                const result = await response.json();
                return result.room || result;
            } catch (error) {
                console.warn("API indisponível, usando LocalStorage", error);
            }
        }
        
        // Fallback para LocalStorage
        const id = "APX-" + Math.random().toString(36).substr(2, 4).toUpperCase();
        const room = { id, ...dados, tokens: [], createdAt: new Date().toISOString() };
        localStorage.setItem(id, JSON.stringify(room));
        return room;
    },
    
    getRooms: async () => {
        if (UseAPI) {
            try {
                const response = await fetch(`${API_URL}/rooms`);
                const result = await response.json();
                return Object.values(result.rooms || {});
            } catch (error) {
                console.warn("API indisponível, usando LocalStorage", error);
            }
        }
        
        // Fallback para LocalStorage
        return Object.keys(localStorage)
            .filter(key => key.startsWith('APX-'))
            .map(key => JSON.parse(localStorage.getItem(key)));
    },
    
    deleteRoom: async (id) => {
        if (UseAPI) {
            try {
                await fetch(`${API_URL}/room/${id}`, { method: "DELETE" });
                return;
            } catch (error) {
                console.warn("API indisponível, usando LocalStorage", error);
            }
        }
        
        // Fallback para LocalStorage
        localStorage.removeItem(id);
    },
    
    gerarToken: async (room_id, placa) => {
        if (UseAPI) {
            try {
                const response = await fetch(`${API_URL}/gerar_token`, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ room_id, placa })
                });
                return await response.json();
            } catch (error) {
                console.warn("Erro ao gerar token", error);
            }
        }
        return { token: "LOCAL-" + Math.random().toString(36).substr(2, 8).toUpperCase() };
    }
};

// Função para capturar os dados do formulário
function cadastrarSafeRoom() {
    const inputs = document.querySelectorAll('input');
    const nome = inputs[0].value; // Bunker name
    const valor = inputs[1].value; // Token value
    const cor = inputs[2].value; // Color
    const fim = inputs[4].value; // End time

    if(!nome || !valor) {
        alert("Por favor, preencha o nome e o valor da Room.");
        return;
    }

    const novaRoom = ApexEngine.saveRoom({ nome, valor: parseInt(valor), cor, fim });
    
    // Atualiza a visualização na tela (Preview)
    document.querySelector('.text-2xl.font-bold.italic').innerText = `SAFE ROOM ${novaRoom.id}`;
    document.querySelector('.border-l-8').style.borderColor = cor;
    document.querySelector('.text-blue-400.font-bold').innerText = Math.random().toString(36).substr(2, 5).toUpperCase();
    
    // Limpa o formulário
    document.querySelectorAll('input[type="text"], input[type="number"], input[type="time"]').forEach(input => input.value = '');
    document.querySelector('input[type="color"]').value = '#3b82f6';
    
    // Atualiza a lista de rooms
    atualizarListaRooms();
    
    alert(`Apex: Room ${novaRoom.nome} cadastrada com sucesso!`);
}

// Função para atualizar a lista de rooms
function atualizarListaRooms() {
    const roomsList = document.getElementById('roomsList');
    const rooms = ApexEngine.getRooms();
    
    if (rooms.length === 0) {
        roomsList.innerHTML = '<div class="bg-slate-700 p-4 rounded border border-slate-600 text-center text-gray-400 col-span-full">Nenhuma room registrada</div>';
        return;
    }
    
    roomsList.innerHTML = rooms.map(room => `
        <div class="bg-slate-700 p-4 rounded border-l-4" style="border-color: ${room.cor};">
            <div class="font-bold text-blue-300 mb-2">${room.id}</div>
            <div class="text-sm">
                <div class="text-gray-400">Nome: <span class="text-white">${room.nome}</span></div>
                <div class="text-gray-400">Tokens: <span class="text-yellow-400">${room.valor}</span></div>
                <div class="text-gray-400">Fim: <span class="text-white">${room.fim || 'N/A'}</span></div>
            </div>
            <button type="button" onclick="ApexEngine.deleteRoom('${room.id}'); atualizarListaRooms();" class="mt-3 px-2 py-1 bg-red-600 hover:bg-red-500 rounded text-xs font-bold transition w-full">
                DELETAR
            </button>
        </div>
    `).join('');
}

// Vincula a função ao botão
document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('button.bg-blue-600').onclick = cadastrarSafeRoom;
    atualizarListaRooms();
});
