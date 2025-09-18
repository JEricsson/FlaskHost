#!/usr/bin/env python3
"""
Script de teste para verificar comunicação entre componentes do TARNet
"""
import asyncio
import websockets
import json
import uuid
import time

async def test_host_connection():
    """Simula um Host Agent conectando ao servidor"""
    try:
        uri = "ws://localhost:8000"
        print(f"🔌 Conectando como HOST ao servidor {uri}")
        
        async with websockets.connect(uri) as websocket:
            host_id = str(uuid.uuid4())
            
            # Registra o host
            register_msg = {
                "type": "register_host",
                "host_id": host_id,
                "timestamp": time.time()
            }
            
            await websocket.send(json.dumps(register_msg))
            print(f"📤 Enviado registro do host: {host_id}")
            
            # Aguarda confirmação
            response = await websocket.recv()
            data = json.loads(response)
            print(f"📥 Resposta do servidor: {data}")
            
            if data.get('type') == 'host_registered':
                print("✅ Host registrado com sucesso!")
                
                # Simula envio de frame
                frame_msg = {
                    "type": "screen_frame",
                    "host_id": host_id,
                    "data": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg==",  # 1x1 pixel PNG em base64
                    "timestamp": time.time()
                }
                
                await websocket.send(json.dumps(frame_msg))
                print("📤 Frame de teste enviado")
                
                return True
            else:
                print("❌ Erro no registro do host")
                return False
                
    except Exception as e:
        print(f"❌ Erro na conexão do host: {e}")
        return False

async def test_client_connection():
    """Simula um Cliente Web conectando ao servidor"""
    try:
        uri = "ws://localhost:8000"
        print(f"\n🔌 Conectando como CLIENTE ao servidor {uri}")
        
        async with websockets.connect(uri) as websocket:
            client_id = str(uuid.uuid4())
            
            # Primeiro, solicita lista de hosts
            get_hosts_msg = {
                "type": "get_hosts"
            }
            
            await websocket.send(json.dumps(get_hosts_msg))
            print("📤 Solicitando lista de hosts")
            
            response = await websocket.recv()
            data = json.loads(response)
            print(f"📥 Lista de hosts: {data}")
            
            hosts = data.get('hosts', [])
            if not hosts:
                print("⚠️ Nenhum host disponível para teste")
                return False
            
            # Usa o primeiro host disponível
            target_host = hosts[0]['host_id']
            print(f"🎯 Conectando ao host: {target_host}")
            
            # Registra o cliente
            register_msg = {
                "type": "register_client",
                "client_id": client_id,
                "target_host": target_host
            }
            
            await websocket.send(json.dumps(register_msg))
            print(f"📤 Enviado registro do cliente: {client_id}")
            
            # Aguarda confirmação
            response = await websocket.recv()
            data = json.loads(response)
            print(f"📥 Resposta do servidor: {data}")
            
            if data.get('type') == 'client_registered':
                print("✅ Cliente registrado com sucesso!")
                
                # Simula comando de controle
                control_msg = {
                    "type": "control_command",
                    "client_id": client_id,
                    "target_host": target_host,
                    "command": {
                        "type": "mouse_move",
                        "x": 100,
                        "y": 200
                    }
                }
                
                await websocket.send(json.dumps(control_msg))
                print("📤 Comando de controle enviado")
                
                return True
            else:
                print("❌ Erro no registro do cliente")
                return False
                
    except Exception as e:
        print(f"❌ Erro na conexão do cliente: {e}")
        return False

async def main():
    """Executa testes de comunicação"""
    print("🧪 === Teste de Comunicação TARNet ===")
    print("Testando conectividade entre componentes\n")
    
    # Teste do Host Agent
    host_success = await test_host_connection()
    
    # Aguarda um pouco para o host se registrar
    await asyncio.sleep(1)
    
    # Teste do Cliente Web
    client_success = await test_client_connection()
    
    print("\n📊 === Resultados dos Testes ===")
    print(f"Host Agent: {'✅ PASSOU' if host_success else '❌ FALHOU'}")
    print(f"Cliente Web: {'✅ PASSOU' if client_success else '❌ FALHOU'}")
    
    if host_success and client_success:
        print("\n🎉 Todos os testes passaram! Sistema funcionando corretamente.")
    else:
        print("\n⚠️ Alguns testes falharam. Verifique o servidor e tente novamente.")

if __name__ == "__main__":
    print("Pressione Ctrl+C para parar os testes\n")
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Testes interrompidos pelo usuário")