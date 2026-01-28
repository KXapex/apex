#!/usr/bin/env python3
"""
Script de Demonstração do ApexEngine
Simula o fluxo completo: cadastro de rooms, geração de tokens e interfaces
"""

import time
from engine import ApexEngine

def main():
    print("\n" + "="*60)
    print("  🔐 APEX OPERATING SYSTEM - DEMO")
    print("="*60)
    
    # Inicializar engine
    apex = ApexEngine()
    
    # ===== FASE 1: CADASTRO DE ROOMS =====
    print("\n[FASE 1] Cadastrando Safe Rooms...")
    print("-" * 60)
    
    bunker_id = apex.cadastrar_room(
        nome="Bunker Apex",
        valor=350.0,
        cor="#FF0000",
        fechar_as="02:00"
    )
    print(f"✓ Bunker Apex cadastrado: {bunker_id}")
    
    lounge_id = apex.cadastrar_room(
        nome="Skyline Lounge",
        valor=120.0,
        cor="#00FFFB",
        fechar_as="05:00"
    )
    print(f"✓ Skyline Lounge cadastrado: {lounge_id}")
    
    garage_id = apex.cadastrar_room(
        nome="Underground Garage",
        valor=200.0,
        cor="#00FF00",
        fechar_as="03:30"
    )
    print(f"✓ Underground Garage cadastrado: {garage_id}")
    
    # ===== FASE 2: GERANDO TOKENS DE ACESSO =====
    print("\n[FASE 2] Gerando Tokens de Acesso...")
    print("-" * 60)
    
    token_porsche = apex.gerar_acesso(bunker_id, "APX-911")
    print(f"✓ Token para Porsche (APX-911): {token_porsche}")
    
    token_nissan = apex.gerar_acesso(lounge_id, "SKY-34")
    print(f"✓ Token para Nissan (SKY-34): {token_nissan}")
    
    token_bmw = apex.gerar_acesso(garage_id, "UGG-67")
    print(f"✓ Token para BMW (UGG-67): {token_bmw}")
    
    # Múltiplos acessos à mesma room
    token_audi = apex.gerar_acesso(bunker_id, "APX-A8")
    print(f"✓ Token para Audi (APX-A8): {token_audi}")
    
    # ===== FASE 3: VALIDAÇÃO DE TOKENS =====
    print("\n[FASE 3] Validando Tokens...")
    print("-" * 60)
    
    validacao = apex.validar_token(token_porsche)
    print(f"✓ Token {token_porsche} validado: {validacao['valido']}")
    
    validacao_invalida = apex.validar_token("XXXXX")
    print(f"✗ Token XXXXX validado: {validacao_invalida['valido']}")
    
    # ===== FASE 4: INTERFACE CARPLAY =====
    print("\n[FASE 4] Simulando CarPlay Interface...")
    print("-" * 60)
    
    carplay_porsche = apex.carplay_interface(token_porsche)
    if carplay_porsche["status"] == "sucesso":
        cp = carplay_porsche["carplay"]
        print(f"\n📱 {cp['titulo']}")
        print(f"   🎯 Destino: {cp['destino']}")
        print(f"   🎨 Cor Equipe: {cp['cor_equipe']}")
        print(f"   ✓ {cp['status_rota']}")
        print(f"   💰 {cp['valor_room']}")
        print(f"   🚗 Placa: {cp['placa_veiculo']}")
        print(f"   🕐 Acesso às: {cp['hora_acesso']}")
        print(f"   ⏰ Fecha às: {cp['horario_fechamento']}")
    
    # ===== FASE 5: DASHBOARD ADMINISTRATIVO =====
    print("\n[FASE 5] Dashboard Administrativo")
    print("-" * 60)
    print(apex.show_dashboard_text())
    
    # ===== FASE 6: DADOS JSON DO DASHBOARD =====
    print("\n[FASE 6] Dados Estruturados do Dashboard")
    print("-" * 60)
    
    import json
    dashboard_data = apex.get_dashboard()
    
    print(f"Sistema: {dashboard_data['sistema']}")
    print(f"Status: {dashboard_data['status']}")
    print(f"Total de Rooms: {dashboard_data['total_rooms']}")
    print(f"Receita Total: {dashboard_data['receita_total']}")
    print(f"\nRooms Cadastradas:")
    
    for room in dashboard_data['rooms']:
        print(f"  - {room['nome']} ({room['id']})")
        print(f"    Acessos: {room['acessos_hoje']} | Tokens Ativos: {room['tokens_ativos_agora']}")
    
    # ===== FASE 7: DELETAR ROOM =====
    print("\n[FASE 7] Deletando uma Room...")
    print("-" * 60)
    
    resultado_delecao = apex.deletar_room(lounge_id)
    print(f"✓ {resultado_delecao['mensagem']}")
    print(f"  Tokens removidos: {resultado_delecao['tokens_removidos']}")
    
    # ===== DASHBOARD FINAL =====
    print("\n[FINAL] Dashboard Atualizado")
    print("-" * 60)
    
    final_dashboard = apex.get_dashboard()
    print(f"Total de Rooms Restantes: {final_dashboard['total_rooms']}")
    print(f"Receita Total: {final_dashboard['receita_total']}")
    
    print("\n" + "="*60)
    print("  ✅ DEMO CONCLUÍDA COM SUCESSO")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
