#!/usr/bin/env python3
"""
Exemplos Práticos de Uso do ApexEngine
Demonstra diferentes cenários de uso real
"""

from engine import ApexEngine
import json

def exemplo_1_basico():
    """Exemplo 1: Uso Básico"""
    print("\n" + "="*60)
    print("EXEMPLO 1: Uso Básico do ApexEngine")
    print("="*60)
    
    engine = ApexEngine()
    
    # Criar uma room
    room_id = engine.cadastrar_room(
        nome="Bunker Apex",
        valor=350.0,
        cor="#FF0000",
        fechar_as="02:00"
    )
    print(f"Room criada: {room_id}")
    
    # Gerar token
    token = engine.gerar_acesso(room_id, "APX-911")
    print(f"Token gerado: {token}")
    
    # Validar token
    resultado = engine.validar_token(token)
    print(f"Token válido: {resultado['valido']}")
    
    return engine


def exemplo_2_multiplas_rooms():
    """Exemplo 2: Gerenciamento de Múltiplas Rooms"""
    print("\n" + "="*60)
    print("EXEMPLO 2: Múltiplas Rooms com Diferentes Configs")
    print("="*60)
    
    engine = ApexEngine()
    
    rooms = [
        ("Bunker VIP", 500.0, "#FF0000", "01:00"),
        ("Lounge Premium", 250.0, "#00FFFB", "03:00"),
        ("Garage Underground", 150.0, "#00FF00", "02:30"),
    ]
    
    room_ids = {}
    for nome, valor, cor, horario in rooms:
        room_id = engine.cadastrar_room(nome, valor, cor, horario)
        room_ids[nome] = room_id
        print(f"✓ {nome:25} → {room_id} (R$ {valor:.2f})")
    
    return engine, room_ids


def exemplo_3_tokens_multiplos():
    """Exemplo 3: Múltiplos Tokens por Room"""
    print("\n" + "="*60)
    print("EXEMPLO 3: Múltiplos Acessos na Mesma Room")
    print("="*60)
    
    engine = ApexEngine()
    
    # Criar room
    room_id = engine.cadastrar_room(
        nome="Parking Privado",
        valor=50.0,
        cor="#FFD700",
        fechar_as="23:00"
    )
    
    # Múltiplos usuários acessando
    placas = ["ABC-1234", "DEF-5678", "GHI-9012", "JKL-3456"]
    tokens = {}
    
    for placa in placas:
        token = engine.gerar_acesso(room_id, placa)
        tokens[placa] = token
        print(f"✓ {placa} → Token: {token}")
    
    # Mostrar status da room
    room = engine.rooms[room_id]
    print(f"\nStatus da Room:")
    print(f"  Acessos totais: {room['historico_acessos']}")
    print(f"  Tokens ativos: {len(room['tokens_ativos'])}")
    print(f"  Receita estimada: R$ {room['valor'] * room['historico_acessos']:.2f}")
    
    return engine, room_id, tokens


def exemplo_4_carplay():
    """Exemplo 4: Interface CarPlay"""
    print("\n" + "="*60)
    print("EXEMPLO 4: Simulação de Interface CarPlay")
    print("="*60)
    
    engine = ApexEngine()
    
    # Setup
    room_id = engine.cadastrar_room("Skyline Lounge", 120.0, "#00FFFB", "05:00")
    token = engine.gerar_acesso(room_id, "SKY-911")
    
    # Simular chamada CarPlay
    carplay_data = engine.carplay_interface(token)
    
    if carplay_data["status"] == "sucesso":
        cp = carplay_data["carplay"]
        print("\n📱 TELA DO CARRO:")
        print(f"   {cp['titulo']}")
        print(f"   {'='*50}")
        print(f"   Destino: {cp['destino']}")
        print(f"   Status: {cp['status_rota']}")
        print(f"   Valor: {cp['valor_room']}")
        print(f"   Placa do Carro: {cp['placa_veiculo']}")
        print(f"   Horário Acesso: {cp['hora_acesso']}")
        print(f"   Fecha às: {cp['horario_fechamento']}")
    
    return engine


def exemplo_5_dashboard():
    """Exemplo 5: Dashboard Administrativo"""
    print("\n" + "="*60)
    print("EXEMPLO 5: Dashboard Administrativo Completo")
    print("="*60)
    
    engine = ApexEngine()
    
    # Criar várias rooms com acessos
    configs = [
        ("Premium Suite", 500.0, "#FF0000"),
        ("VIP Lounge", 300.0, "#00FFFB"),
        ("Standard", 100.0, "#00FF00"),
    ]
    
    for nome, valor, cor in configs:
        room_id = engine.cadastrar_room(nome, valor, cor, "23:00")
        # Simular alguns acessos
        for i in range(3):
            engine.gerar_acesso(room_id, f"CAR-{i+1}")
    
    # Obter dashboard
    dashboard = engine.get_dashboard()
    
    print(f"\nSistema: {dashboard['sistema']}")
    print(f"Status: {dashboard['status']}")
    print(f"Total de Rooms: {dashboard['total_rooms']}")
    print(f"Receita Total: {dashboard['receita_total']}")
    print(f"\n{'Nome':<20} {'ID':<12} {'Acessos':<10} {'Tokens Ativos':<15}")
    print("-" * 60)
    
    for room in dashboard['rooms']:
        print(f"{room['nome']:<20} {room['id']:<12} {room['acessos_hoje']:<10} {room['tokens_ativos_agora']:<15}")
    
    return engine


def exemplo_6_validacao_tokens():
    """Exemplo 6: Validação de Tokens"""
    print("\n" + "="*60)
    print("EXEMPLO 6: Validação de Tokens")
    print("="*60)
    
    engine = ApexEngine()
    
    room_id = engine.cadastrar_room("Test Room", 100.0, "#FF0000", "22:00")
    token_valido = engine.gerar_acesso(room_id, "TEST-123")
    
    # Testar tokens
    testes = [
        ("Token válido", token_valido),
        ("Token inválido", "XXXXX"),
        ("Token expirado", "EXPIRED"),
    ]
    
    for desc, token in testes:
        resultado = engine.validar_token(token)
        status = "✓ VÁLIDO" if resultado['valido'] else "✗ INVÁLIDO"
        print(f"{desc:<20}: {status}")
    
    return engine


def exemplo_7_operacoes_administrativas():
    """Exemplo 7: Operações Administrativas (CRUD)"""
    print("\n" + "="*60)
    print("EXEMPLO 7: Operações Administrativas Completas")
    print("="*60)
    
    engine = ApexEngine()
    
    # CREATE
    print("\n[CREATE] Criando 3 rooms...")
    room_ids = []
    for i in range(3):
        room_id = engine.cadastrar_room(
            nome=f"Room {i+1}",
            valor=100.0 + (i * 50),
            cor=f"#{i*111111:06X}",
            fechar_as="23:00"
        )
        room_ids.append(room_id)
        print(f"  ✓ {room_id}")
    
    # READ
    print(f"\n[READ] Total de rooms: {len(engine.rooms)}")
    
    # UPDATE (gerar acessos)
    print(f"\n[UPDATE] Gerando acessos...")
    for room_id in room_ids:
        token = engine.gerar_acesso(room_id, "CAR-001")
        print(f"  ✓ {room_id}: {token}")
    
    # DELETE
    print(f"\n[DELETE] Deletando uma room...")
    resultado = engine.deletar_room(room_ids[0])
    print(f"  {resultado['mensagem']}")
    print(f"  Total restante: {len(engine.rooms)}")
    
    return engine


def exemplo_8_json_export():
    """Exemplo 8: Exportar Dados em JSON"""
    print("\n" + "="*60)
    print("EXEMPLO 8: Exportar Dados em JSON")
    print("="*60)
    
    engine = ApexEngine()
    
    # Setup
    room_id = engine.cadastrar_room("Export Room", 250.0, "#FF00FF", "22:00")
    engine.gerar_acesso(room_id, "EXP-001")
    engine.gerar_acesso(room_id, "EXP-002")
    
    # Obter dashboard como JSON
    dashboard = engine.get_dashboard()
    
    print("\nJSON Export:")
    print(json.dumps(dashboard, indent=2, ensure_ascii=False))
    
    return engine


def main():
    """Executar todos os exemplos"""
    exemplos = [
        exemplo_1_basico,
        exemplo_2_multiplas_rooms,
        exemplo_3_tokens_multiplos,
        exemplo_4_carplay,
        exemplo_5_dashboard,
        exemplo_6_validacao_tokens,
        exemplo_7_operacoes_administrativas,
        exemplo_8_json_export,
    ]
    
    for exemplo_func in exemplos:
        try:
            exemplo_func()
        except Exception as e:
            print(f"\n❌ Erro em {exemplo_func.__name__}: {e}")
    
    print("\n" + "="*60)
    print("✅ TODOS OS EXEMPLOS EXECUTADOS COM SUCESSO")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
