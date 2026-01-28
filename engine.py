"""
ApexEngine - Motor de Gerenciamento de Safe Rooms
Sistema completo de autenticação, tokens e dashboard administrativo
"""

import secrets
from datetime import datetime
from typing import Dict, List, Optional

class ApexEngine:
    """Motor central do sistema Apex de Safe Rooms"""
    
    def __init__(self):
        self.rooms: Dict = {}
        self.total_revenue: float = 0.0
        self.created_at = datetime.now().isoformat()

    def cadastrar_room(self, nome: str, valor: float, cor: str, fechar_as: str) -> str:
        """
        Cadastra uma nova Safe Room no sistema
        
        Args:
            nome: Nome da room (ex: "Bunker Apex")
            valor: Valor por acesso em R$
            cor: Cor da room em formato hex (ex: "#FF0000")
            fechar_as: Horário de fechamento (ex: "02:00")
        
        Returns:
            room_id: ID único da room (APX-XXXX)
        """
        room_id = f"APX-{secrets.token_hex(2).upper()}"
        self.rooms[room_id] = {
            "nome": nome,
            "valor": valor,
            "cor": cor,
            "fim": fechar_as,
            "tokens_ativos": {},
            "historico_acessos": 0,
            "criada_em": datetime.now().isoformat()
        }
        return room_id

    def gerar_acesso(self, room_id: str, placa: str) -> str:
        """
        Gera um token de acesso para um veículo em uma room específica
        
        Args:
            room_id: ID da Safe Room
            placa: Placa do veículo (ex: "APX-911")
        
        Returns:
            token: Token de acesso único
        """
        if room_id not in self.rooms:
            return f"Erro: Room {room_id} não encontrada."
        
        token = secrets.token_hex(3).upper()
        self.rooms[room_id]["tokens_ativos"][token] = {
            "placa": placa,
            "entrada": datetime.now().strftime("%H:%M:%S"),
            "data": datetime.now().strftime("%Y-%m-%d")
        }
        self.rooms[room_id]["historico_acessos"] += 1
        self.total_revenue += self.rooms[room_id]["valor"]
        return token

    def validar_token(self, token: str) -> Optional[Dict]:
        """
        Valida um token e retorna informações da room associada
        
        Args:
            token: Token de acesso
        
        Returns:
            Dados da room ou None se inválido
        """
        for r_id, data in self.rooms.items():
            if token in data["tokens_ativos"]:
                return {
                    "room_id": r_id,
                    "room_data": data,
                    "token_data": data["tokens_ativos"][token],
                    "valido": True
                }
        return {"valido": False, "mensagem": "Token inválido ou expirado"}

    def carplay_interface(self, token: str) -> Dict:
        """
        Retorna dados formatados para exibição no CarPlay
        Simula a tela que apareceria no carro do usuário
        
        Args:
            token: Token de acesso
        
        Returns:
            Dicionário com informações para exibição no carro
        """
        validacao = self.validar_token(token)
        
        if validacao.get("valido"):
            room_data = validacao["room_data"]
            token_data = validacao["token_data"]
            return {
                "status": "sucesso",
                "carplay": {
                    "titulo": "APEX DRIVE - MODO CARPLAY",
                    "destino": room_data["nome"],
                    "cor_equipe": room_data["cor"],
                    "status_rota": "Rota Privada Desbloqueada ✓",
                    "valor_room": f"R$ {room_data['valor']:.2f}",
                    "horario_fechamento": room_data["fim"],
                    "placa_veiculo": token_data["placa"],
                    "hora_acesso": token_data["entrada"]
                }
            }
        else:
            return {
                "status": "erro",
                "carplay": {
                    "titulo": "APEX DRIVE - ERRO",
                    "mensagem": "Token inválido ou expirado",
                    "status_rota": "Acesso Negado ✗"
                }
            }

    def get_dashboard(self) -> Dict:
        """
        Retorna dados completos do dashboard administrativo
        
        Returns:
            Dicionário com informações gerenciais
        """
        rooms_info = []
        for r_id, info in self.rooms.items():
            rooms_info.append({
                "id": r_id,
                "nome": info["nome"],
                "valor": info["valor"],
                "cor": info["cor"],
                "horario_fechamento": info["fim"],
                "acessos_hoje": info["historico_acessos"],
                "tokens_ativos_agora": len(info["tokens_ativos"]),
                "tokens": list(info["tokens_ativos"].keys()),
                "criada_em": info["criada_em"]
            })
        
        return {
            "sistema": "Apex Operating System",
            "status": "operacional",
            "timestamp": datetime.now().isoformat(),
            "total_rooms": len(self.rooms),
            "rooms": rooms_info,
            "receita_total": f"R$ {self.total_revenue:.2f}",
            "receita_valor": self.total_revenue,
            "uptime": self.created_at
        }

    def deletar_room(self, room_id: str) -> Dict:
        """
        Deleta uma room e seus tokens associados
        
        Args:
            room_id: ID da room a deletar
        
        Returns:
            Status da operação
        """
        if room_id not in self.rooms:
            return {"status": "erro", "mensagem": f"Room {room_id} não encontrada"}
        
        room = self.rooms[room_id]
        tokens_removidos = len(room["tokens_ativos"])
        del self.rooms[room_id]
        
        return {
            "status": "sucesso",
            "mensagem": f"Room {room_id} deletada",
            "tokens_removidos": tokens_removidos,
            "room_nome": room["nome"]
        }

    def listar_rooms(self) -> List[Dict]:
        """Retorna lista simples de todas as rooms"""
        return [
            {
                "id": r_id,
                "nome": data["nome"],
                "valor": data["valor"],
                "cor": data["cor"],
                "acessos": data["historico_acessos"]
            }
            for r_id, data in self.rooms.items()
        ]

    def show_dashboard_text(self) -> str:
        """Retorna dashboard formatado como texto para terminal"""
        output = "\n" + "="*50
        output += "\n    APEX ADMIN DASHBOARD"
        output += "\n" + "="*50 + "\n"
        
        if not self.rooms:
            output += "Nenhuma room cadastrada ainda.\n"
        else:
            for r_id, info in self.rooms.items():
                output += f"📍 Room: {info['nome']} [{r_id}]\n"
                output += f"   💰 Valor: R$ {info['valor']:.2f}/acesso\n"
                output += f"   🎨 Cor: {info['cor']}\n"
                output += f"   🕐 Fecha às: {info['fim']}\n"
                output += f"   👥 Acessos Hoje: {info['historico_acessos']}\n"
                output += f"   🔑 Tokens Ativos: {len(info['tokens_ativos'])}\n"
                output += "-" * 50 + "\n"
        
        output += f"\n💵 RECEITA TOTAL: R$ {self.total_revenue:.2f}\n"
        output += "="*50 + "\n"
        return output


# Instância global do engine (usada pelo FastAPI)
engine = ApexEngine()
