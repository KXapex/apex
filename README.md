# 🔐 Apex Operating System

Sistema avançado de gerenciamento de **Safe Rooms** com arquitetura completa front-end/back-end. Motor Python puro com validação de tokens, interface CarPlay e dashboard administrativo em tempo real.

## 📦 Estrutura do Projeto

```
apex/
├── index.html          # Interface web (Tailwind CSS)
├── app.js             # Lógica front-end com suporte a API
├── server.py          # API FastAPI com rotas REST
├── engine.py          # ⭐ Motor central (ApexEngine)
├── demo.py            # Script de demonstração
├── requirements.txt   # Dependências Python
└── README.md         # Este arquivo
```

## 🚀 Quickstart

### Opção 1: Demonstração Local (Sem Servidor)

```bash
# Executar demo do engine
python demo.py
```

**Saída esperada:**
```
============================================================
  🔐 APEX OPERATING SYSTEM - DEMO
============================================================

[FASE 1] Cadastrando Safe Rooms...
✓ Bunker Apex cadastrado: APX-EC29
✓ Skyline Lounge cadastrado: APX-7811
...
```

### Opção 2: App Web com Backend FastAPI

#### Instalação:
```bash
pip install -r requirements.txt
```

#### Iniciar servidor:
```bash
python server.py
# ou
uvicorn server:app --reload --port 8000
```

#### Usar app web:
1. Abra `index.html` no navegador
2. Em `app.js`, mude `const UseAPI = false` para `true`
3. Pronto! Agora se conecta ao backend em `http://localhost:8000`

### Opção 3: Interface Offline (LocalStorage)

Abra `index.html` sem servidor - funciona completamente offline com dados locais.

## 🎯 Componentes Principais

### `engine.py` - ApexEngine
Motor central que implementa toda a lógica de negócio:

```python
from engine import ApexEngine

engine = ApexEngine()

# Criar room
room_id = engine.cadastrar_room(
    nome="Bunker Apex",
    valor=350.0,
    cor="#FF0000",
    fechar_as="02:00"
)

# Gerar token
token = engine.gerar_acesso(room_id, "APX-911")

# Validar token
validacao = engine.validar_token(token)

# Interface CarPlay
carplay = engine.carplay_interface(token)

# Dashboard administrativo
dashboard = engine.get_dashboard()
```

### API REST (server.py)

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| **POST** | `/cadastrar_room` | Registra nova Safe Room |
| **GET** | `/rooms` | Lista todas as rooms |
| **GET** | `/room/{room_id}` | Detalhes de uma room |
| **POST** | `/gerar_token` | Gera token de acesso |
| **GET** | `/validar_token/{token}` | Valida um token |
| **GET** | `/carplay/{token}` | Interface CarPlay |
| **GET** | `/dashboard` | Dashboard administrativo |
| **DELETE** | `/room/{room_id}` | Deleta uma room |

## 📝 Exemplos de Uso

### 1. Criar Uma Safe Room

**Backend Python:**
```python
engine = ApexEngine()
room_id = engine.cadastrar_room(
    nome="Bunker Apex",
    valor=350.0,
    cor="#FF0000",
    fechar_as="02:00"
)
print(room_id)  # APX-EC29
```

**API REST:**
```bash
curl -X POST http://localhost:8000/cadastrar_room \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Bunker Apex",
    "valor": 350.0,
    "cor": "#FF0000",
    "horario_fim": "02:00"
  }'
```

### 2. Gerar Token de Acesso

```python
token = engine.gerar_acesso("APX-EC29", "APX-911")
# token = "05E6F9"
```

```bash
curl -X POST http://localhost:8000/gerar_token \
  -H "Content-Type: application/json" \
  -d '{
    "room_id": "APX-EC29",
    "placa": "APX-911"
  }'
```

### 3. Interface CarPlay (Para o Carro)

```python
resultado = engine.carplay_interface("05E6F9")
# Retorna:
# {
#   "status": "sucesso",
#   "carplay": {
#     "titulo": "APEX DRIVE - MODO CARPLAY",
#     "destino": "Bunker Apex",
#     "cor_equipe": "#FF0000",
#     "status_rota": "Rota Privada Desbloqueada ✓",
#     "valor_room": "R$ 350.00",
#     "horario_fechamento": "02:00",
#     "placa_veiculo": "APX-911",
#     "hora_acesso": "14:02:58"
#   }
# }
```

### 4. Dashboard Administrativo

```python
dashboard = engine.get_dashboard()
# {
#   "sistema": "Apex Operating System",
#   "status": "operacional",
#   "total_rooms": 3,
#   "receita_total": "R$ 1020.00",
#   "rooms": [...]
# }
```

## 🔧 Métodos do ApexEngine

### `cadastrar_room(nome, valor, cor, fechar_as)`
Cria uma nova Safe Room.
- **Retorna**: `room_id` (str) - ID único formato APX-XXXX
- **Exemplos**:
  ```python
  id1 = engine.cadastrar_room("Bunker A", 350, "#FF0000", "02:00")
  id2 = engine.cadastrar_room("Lounge B", 120, "#00FFFB", "05:00")
  ```

### `gerar_acesso(room_id, placa)`
Gera token de acesso para um veículo.
- **Retorna**: `token` (str) - Token único
- **Exemplo**:
  ```python
  token = engine.gerar_acesso("APX-EC29", "APX-911")
  ```

### `validar_token(token)`
Valida um token e retorna dados da room.
- **Retorna**: Dict com dados ou `{"valido": False}`
- **Exemplo**:
  ```python
  resultado = engine.validar_token("05E6F9")
  if resultado["valido"]:
      print(resultado["room_data"]["nome"])
  ```

### `carplay_interface(token)`
Retorna dados formatados para CarPlay.
- **Exemplo**:
  ```python
  carplay = engine.carplay_interface(token)
  print(carplay["carplay"]["destino"])
  ```

### `get_dashboard()`
Retorna dados estruturados do dashboard.
- **Retorna**: Dict com estatísticas completas

### `deletar_room(room_id)`
Remove uma room e seus tokens.
- **Retorna**: Dict com status de operação

### `show_dashboard_text()`
Retorna dashboard formatado como texto para terminal.

## 📊 Fluxo Operacional

```
1. CADASTRO (admin)
   └─> cadastrar_room() → room_id

2. GERAÇÃO DE TOKEN (admin ou sistema)
   └─> gerar_acesso(room_id, placa) → token

3. VALIDAÇÃO (no carro)
   └─> validar_token(token) → dados_da_room

4. INTERFACE CARPLAY
   └─> carplay_interface(token) → dados_para_exibição

5. DASHBOARD ADMINISTRATIVO
   └─> get_dashboard() → estatísticas_completas
```

## 🎨 Características

✅ **Motor robusto**: Classe `ApexEngine` com lógica completa
✅ **IDs únicos**: Gerados automaticamente (APX-XXXX)
✅ **Tokens de segurança**: Validação e rastreamento
✅ **Interface CarPlay**: Dados formatados para veículos
✅ **Dashboard**: Visão completa em tempo real
✅ **API REST**: Integração com frontend
✅ **Offline**: Funciona sem servidor com LocalStorage
✅ **Receita**: Rastreamento automático de ganhos
✅ **Histórico**: Logs de acessos por room

## 📈 Dados Rastreados

### Por Room:
- Nome e ID único
- Valor por acesso
- Cor (para identificação)
- Horário de fechamento
- Quantidade de acessos
- Tokens ativos
- Data de criação

### Sistema:
- Total de rooms
- Receita total acumulada
- Tokens gerados
- Uptime do sistema

## 🔒 Segurança

- Tokens aleatórios de 6 caracteres (hexadecimal)
- Validação obrigatória antes de acesso
- IDs únicos por room
- Rastreamento de todas as operações
- CORS habilitado apenas em desenvolvimento

## 📚 Dependências

```
fastapi==0.104.1
uvicorn==0.24.0
pydantic==2.5.0
python-multipart==0.0.6
```

## 🚀 Próximas Melhorias

- [ ] Integração com PostgreSQL/Supabase
- [ ] Autenticação JWT
- [ ] WebSockets para real-time
- [ ] Persistência de dados
- [ ] Sistema de pagamento
- [ ] Relatórios avançados
- [ ] Autenticação por QR code
- [ ] Integração com sistema de câmeras

## 📝 Notas

- Backend usa memória volátil (perdido ao reiniciar)
- Para produção: usar banco de dados persistente
- Frontend oferece fallback para LocalStorage
- CORS habilitado para desenvolvimento local
- Port padrão: 8000

---

**Desenvolvido com ❤️ para sistemas de acesso seguro**