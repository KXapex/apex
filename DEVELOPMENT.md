# Apex Operating System - Configurações de Desenvolvimento

## Iniciar o Servidor

### Terminal 1 - Backend FastAPI
```bash
python server.py
```
ou
```bash
uvicorn server:app --reload --port 8000
```

O servidor rodará em: http://localhost:8000

### Terminal 2 - Frontend Web
Abra `index.html` em um navegador web

## Testar API

### Com curl:
```bash
# Listar rooms
curl http://localhost:8000/rooms

# Cadastrar room
curl -X POST http://localhost:8000/cadastrar_room \
  -H "Content-Type: application/json" \
  -d '{"nome":"Test","valor":100,"cor":"#FF0000","horario_fim":"22:00"}'

# Dashboard
curl http://localhost:8000/dashboard
```

### Com Python:
```python
from engine import ApexEngine

engine = ApexEngine()
room_id = engine.cadastrar_room("Test", 100, "#FF0000", "22:00")
token = engine.gerar_acesso(room_id, "TEST-123")
print(engine.get_dashboard())
```

## Scripts Disponíveis

```bash
# Executar demonstração
python demo.py

# Iniciar servidor web
python server.py

# Testar importação do engine
python -c "from engine import ApexEngine; print('OK')"
```

## Estrutura de Dados

### Room Object
```json
{
  "nome": "Bunker Apex",
  "valor": 350.0,
  "cor": "#FF0000",
  "fim": "02:00",
  "tokens_ativos": {
    "05E6F9": {
      "placa": "APX-911",
      "entrada": "14:02:58",
      "data": "2026-01-28"
    }
  },
  "historico_acessos": 1,
  "criada_em": "2026-01-28T14:02:00"
}
```

### Token Object
```json
{
  "placa": "APX-911",
  "entrada": "14:02:58",
  "data": "2026-01-28"
}
```

## Fluxo de Desenvolvimento

1. **Local Testing**: `python demo.py`
2. **Backend**: `python server.py`
3. **Frontend**: Abrir `index.html`
4. **Ativar API**: Mudar `UseAPI = true` em `app.js`
5. **Testar**: Criar rooms e gerar tokens na UI

## Debug Mode

Para ver logs detalhados:

```bash
# FastAPI com reload
uvicorn server:app --reload --log-level debug

# Python script com verbosidade
python -u demo.py
```

## Endpoints Disponíveis

```
POST   /cadastrar_room          Criar nova room
GET    /rooms                   Listar todas
GET    /room/{room_id}          Detalhes
POST   /gerar_token             Gerar token
GET    /validar_token/{token}   Validar
GET    /carplay/{token}         Interface CarPlay
GET    /dashboard               Admin dashboard
DELETE /room/{room_id}          Deletar room
```

## Troubleshooting

**ModuleNotFoundError: No module named 'fastapi'**
```bash
pip install -r requirements.txt
```

**Address already in use**
```bash
# Matar processo na porta 8000
lsof -ti:8000 | xargs kill -9
```

**CORS Error**
- Verifique se `UseAPI = true` em app.js
- Verifique se servidor está rodando em http://localhost:8000
