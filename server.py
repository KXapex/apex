from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import secrets
import uvicorn
from engine import ApexEngine

app = FastAPI(title="Apex Operating System API", version="1.0.0")

# Adicionar CORS para permitir requisições do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Motor Apex (substitui o banco de dados anterior)
apex_engine = ApexEngine()
db_tokens = {}  # Manter para compatibilidade, mas o engine.py é a fonte da verdade

# Modelos de Dados
class RoomCreate(BaseModel):
    nome: str
    valor: float
    cor: str
    horario_fim: str

class TokenRequest(BaseModel):
    room_id: str
    placa: str

# --- ROTAS OPERACIONAIS ---

@app.post("/cadastrar_room")
async def cadastrar(room: RoomCreate):
    """Cadastra uma nova Safe Room no sistema"""
    room_id = apex_engine.cadastrar_room(
        nome=room.nome,
        valor=room.valor,
        cor=room.cor,
        fechar_as=room.horario_fim
    )
    return {
        "status": "sucesso",
        "room_id": room_id,
        "room": apex_engine.rooms[room_id]
    }

@app.get("/rooms")
async def listar_rooms():
    """Lista todas as Safe Rooms cadastradas"""
    return {
        "total": len(apex_engine.rooms),
        "rooms": apex_engine.rooms
    }

@app.get("/room/{room_id}")
async def obter_room(room_id: str):
    """Obtém detalhes de uma Safe Room específica"""
    if room_id not in apex_engine.rooms:
        raise HTTPException(status_code=404, detail="Safe Room não encontrada")
    return apex_engine.rooms[room_id]

@app.post("/gerar_token")
async def gerar_token(req: TokenRequest):
    """Gera um token de segurança para uma Safe Room"""
    if req.room_id not in apex_engine.rooms:
        raise HTTPException(status_code=404, detail="Safe Room não encontrada")
    
    token = apex_engine.gerar_acesso(req.room_id, req.placa)
    
    if token.startswith("Erro"):
        raise HTTPException(status_code=400, detail=token)
    
    return {
        "status": "sucesso",
        "token": token,
        "instrucoes": "Endereço liberado no CarPlay",
        "room_id": req.room_id,
        "placa": req.placa
    }

@app.get("/validar_token/{token}")
async def validar_token(token: str):
    """Valida um token e retorna informações da room"""
    resultado = apex_engine.validar_token(token)
    return resultado

@app.get("/carplay/{token}")
async def carplay_interface(token: str):
    """Interface CarPlay - retorna dados para o carro"""
    return apex_engine.carplay_interface(token)

@app.get("/dashboard")
async def dashboard():
    """Retorna informações gerais do sistema com detalhes de todas as rooms"""
    return apex_engine.get_dashboard()

@app.delete("/room/{room_id}")
async def deletar_room(room_id: str):
    """Deleta uma Safe Room e seus tokens associados"""
    result = apex_engine.deletar_room(room_id)
    if result["status"] == "erro":
        raise HTTPException(status_code=404, detail=result["mensagem"])
    return result

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
