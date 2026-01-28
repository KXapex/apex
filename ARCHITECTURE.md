```
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║           🔐  APEX OPERATING SYSTEM - PROJETO INTEGRADO  🔐                ║
║                                                                            ║
║                Sistema de Gerenciamento de Safe Rooms v1.0                ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝


┌─── ARQUITETURA DO PROJETO ───────────────────────────────────────────────┐
│                                                                           │
│                          ┌──────────────────┐                            │
│                          │   NAVEGADOR WEB  │                            │
│                          │  (index.html +   │                            │
│                          │    app.js)       │                            │
│                          └────────┬─────────┘                            │
│                                   │                                      │
│                    ┌──────────────┴──────────────┐                       │
│                    │                             │                       │
│            ┌───────▼─────────┐        ┌──────────▼────────┐             │
│            │  LocalStorage   │        │  FastAPI/Uvicorn │             │
│            │  (Modo Offline) │        │   (:8000)        │             │
│            └────────────────┘        └──────────┬────────┘             │
│                                                  │                       │
│                                    ┌─────────────▼──────────────┐        │
│                                    │   ApexEngine (engine.py)   │        │
│                                    │  - cadastrar_room()        │        │
│                                    │  - gerar_acesso()          │        │
│                                    │  - validar_token()         │        │
│                                    │  - carplay_interface()     │        │
│                                    │  - get_dashboard()         │        │
│                                    │  - deletar_room()          │        │
│                                    └────────────────────────────┘        │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘


┌─── ESTRUTURA DE ARQUIVOS ─────────────────────────────────────────────────┐
│                                                                           │
│  apex/                                                                   │
│  ├── 📦 CORE                                                             │
│  │   └── engine.py                 Motor Python puro (~250 linhas)      │
│  │                                                                       │
│  ├── 🌐 BACKEND                                                          │
│  │   └── server.py                 API FastAPI (~100 linhas)            │
│  │                                                                       │
│  ├── 💻 FRONTEND                                                         │
│  │   ├── index.html                Interface web (~120 linhas)          │
│  │   └── app.js                    Lógica JS (~150 linhas)              │
│  │                                                                       │
│  ├── 🎬 SCRIPTS                                                          │
│  │   ├── demo.py                   Demonstração (~200 linhas)           │
│  │   ├── exemplos.py               8 exemplos práticos (~350 linhas)    │
│  │   ├── project_info.py           Info do projeto (~200 linhas)        │
│  │   └── setup.sh                  Setup automático                     │
│  │                                                                       │
│  ├── 📚 DOCS                                                             │
│  │   ├── README.md                 Documentação completa                │
│  │   └── DEVELOPMENT.md            Guia de desenvolvimento              │
│  │                                                                       │
│  └── ⚙️  CONFIG                                                          │
│      └── requirements.txt           Dependências Python                 │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘


┌─── FLUXO DE DADOS ──────────────────────────────────────────────────────────┐
│                                                                            │
│   1. CADASTRO (ADMIN)                                                     │
│      └─→ cadastrar_room(nome, valor, cor, horario)                       │
│          └─→ Retorna: room_id (APX-XXXX)                                 │
│                                                                            │
│   2. GERAÇÃO DE TOKEN (SISTEMA)                                           │
│      └─→ gerar_acesso(room_id, placa)                                    │
│          └─→ Retorna: token (HEX de 6 chars)                             │
│          └─→ Incrementa: contador de acessos e receita                   │
│                                                                            │
│   3. VALIDAÇÃO (VERIFICAÇÃO)                                              │
│      └─→ validar_token(token)                                            │
│          └─→ Retorna: dados da room ou erro                              │
│                                                                            │
│   4. INTERFACE CARPLAY (VEÍCULO)                                          │
│      └─→ carplay_interface(token)                                        │
│          └─→ Retorna: dados formatados para display do carro             │
│                                                                            │
│   5. DASHBOARD (ADMIN)                                                    │
│      └─→ get_dashboard()                                                 │
│          └─→ Retorna: estatísticas completas em JSON                     │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘


┌─── API REST ENDPOINTS ──────────────────────────────────────────────────────┐
│                                                                            │
│  POST   /cadastrar_room           Criar nova Safe Room                   │
│  ├── Input:  { nome, valor, cor, horario_fim }                          │
│  └── Output: { status, room_id, room }                                   │
│                                                                            │
│  GET    /rooms                    Listar todas as rooms                  │
│  ├── Input:  -                                                           │
│  └── Output: { total, rooms }                                            │
│                                                                            │
│  GET    /room/{room_id}           Detalhes de uma room                   │
│  ├── Input:  room_id                                                     │
│  └── Output: room data                                                   │
│                                                                            │
│  POST   /gerar_token              Gerar token de acesso                  │
│  ├── Input:  { room_id, placa }                                         │
│  └── Output: { status, token, instrucoes, room_id, placa }             │
│                                                                            │
│  GET    /validar_token/{token}    Validar um token                       │
│  ├── Input:  token                                                       │
│  └── Output: { valido, room_data, token_data }                          │
│                                                                            │
│  GET    /carplay/{token}          Interface para carro                   │
│  ├── Input:  token                                                       │
│  └── Output: { status, carplay { destino, cor, status, valor... } }    │
│                                                                            │
│  GET    /dashboard                Dashboard administrativo               │
│  ├── Input:  -                                                           │
│  └── Output: { sistema, status, total_rooms, receita, rooms[] }        │
│                                                                            │
│  DELETE /room/{room_id}           Deletar uma room                       │
│  ├── Input:  room_id                                                     │
│  └── Output: { status, mensagem, tokens_removidos }                     │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘


┌─── DADOS RASTREADOS ────────────────────────────────────────────────────────┐
│                                                                            │
│  POR ROOM:                         SISTEMA:                              │
│  ├─ Nome                           ├─ Total de rooms                     │
│  ├─ ID único (APX-XXXX)            ├─ Receita total acumulada            │
│  ├─ Valor por acesso (R$)          ├─ Tokens gerados                     │
│  ├─ Cor (hex)                      ├─ Uptime                             │
│  ├─ Horário de fechamento          └─ Status operacional                │
│  ├─ Histórico de acessos                                                │
│  ├─ Tokens ativos                                                        │
│  ├─ Data de criação                                                      │
│  └─ Placas dos veículos                                                  │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘


┌─── EXECUTAR O PROJETO ──────────────────────────────────────────────────────┐
│                                                                            │
│  OPÇÃO 1: Demo Automática                                                │
│  ─────────────────────────                                               │
│  $ python demo.py                                                        │
│  Demonstra: 3 rooms, 4 tokens, CarPlay, Dashboard                        │
│                                                                            │
│  OPÇÃO 2: Exemplos Práticos                                              │
│  ────────────────────────                                                │
│  $ python exemplos.py                                                    │
│  Demonstra: 8 cenários diferentes de uso                                 │
│                                                                            │
│  OPÇÃO 3: Servidor FastAPI                                               │
│  ───────────────────────────                                             │
│  $ python server.py                                                      │
│  Servidor rodará em: http://localhost:8000                               │
│  API disponível em: http://localhost:8000/docs                          │
│                                                                            │
│  OPÇÃO 4: Web UI                                                         │
│  ─────────────                                                           │
│  1. Abra: index.html no navegador                                        │
│  2. Use: App.js (LocalStorage) ou mude UseAPI=true para API             │
│                                                                            │
│  OPÇÃO 5: Setup Automático                                               │
│  ──────────────────────────                                              │
│  $ chmod +x setup.sh                                                     │
│  $ ./setup.sh                                                            │
│  Menu interativo para escolher opção                                     │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘


┌─── CARACTERÍSTICAS ─────────────────────────────────────────────────────────┐
│                                                                            │
│  ✓ Motor robusto em Python puro                                          │
│  ✓ API REST com 7 endpoints                                              │
│  ✓ Interface web moderna (Tailwind CSS)                                  │
│  ✓ Suporte offline (LocalStorage)                                        │
│  ✓ Validação de tokens com segurança                                     │
│  ✓ Rastreamento automático de receita                                    │
│  ✓ Interface CarPlay simulada                                            │
│  ✓ Dashboard administrativo em tempo real                                │
│  ✓ CRUD completo de rooms                                                │
│  ✓ Histórico de acessos detalhado                                        │
│  ✓ IDs únicos automáticos (APX-XXXX)                                     │
│  ✓ Tokens de segurança aleatórios                                        │
│  ✓ Documentação completa                                                 │
│  ✓ Scripts de demonstração                                               │
│  ✓ Pronto para produção (com banco de dados)                            │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘


┌─── DEPENDÊNCIAS ────────────────────────────────────────────────────────────┐
│                                                                            │
│  fastapi==0.104.1            Framework web assíncrono                    │
│  uvicorn==0.24.0             Servidor ASGI                               │
│  pydantic==2.5.0             Validação de dados                          │
│  python-multipart==0.0.6     Parsing de forms multipart                 │
│                                                                            │
│  Instalar: pip install -r requirements.txt                               │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘


╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║                    ✅ PROJETO PRONTO PARA PRODUÇÃO                        ║
║                                                                            ║
║              Desenvolvido com ❤️ para sistemas de acesso seguro            ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
```
