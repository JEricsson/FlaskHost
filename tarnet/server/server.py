import asyncio
import websockets
import json
import logging
import time
from datetime import datetime
from typing import Dict, Set, Optional

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TARNetServer:
    def __init__(self, host='localhost', port=8000):
        self.host = host
        self.port = port
        
        # Armazenamento de conexões
        self.hosts: Dict[str, dict] = {}  # host_id -> {websocket, info, last_seen}
        self.clients: Dict[str, dict] = {}  # client_id -> {websocket, info, connected_host}
        self.rooms: Dict[str, dict] = {}  # room_id -> {host_id, clients_set, created_at}
        
        # Estatísticas
        self.stats = {
            'total_hosts': 0,
            'total_clients': 0,
            'messages_processed': 0,
            'server_start_time': datetime.now().isoformat()
        }
        
        logger.info(f"TARNet Server inicializado - {self.host}:{self.port}")
    
    async def register_host(self, websocket, data):
        """Registra um novo host agent"""
        host_id = data.get('host_id')
        if not host_id:
            await self.send_error(websocket, "ID do host não fornecido")
            return False
        
        # Registra o host
        self.hosts[host_id] = {
            'websocket': websocket,
            'info': {
                'host_id': host_id,
                'connected_at': datetime.now().isoformat(),
                'last_frame': None
            },
            'last_seen': time.time()
        }
        
        # Cria uma sala para o host
        room_id = f"room_{host_id}"
        self.rooms[room_id] = {
            'host_id': host_id,
            'clients': set(),
            'created_at': datetime.now().isoformat()
        }
        
        self.stats['total_hosts'] += 1
        
        logger.info(f"Host registrado: {host_id} na sala {room_id}")
        
        # Confirma registro
        await self.send_message(websocket, {
            'type': 'host_registered',
            'host_id': host_id,
            'room_id': room_id,
            'server_time': datetime.now().isoformat()
        })
        
        return True
    
    async def register_client(self, websocket, data):
        """Registra um novo cliente web"""
        client_id = data.get('client_id')
        target_host = data.get('target_host')
        
        if not client_id:
            await self.send_error(websocket, "ID do cliente não fornecido")
            return False
        
        if not target_host:
            await self.send_error(websocket, "Host de destino não especificado")
            return False
        
        # Verifica se o host existe
        if target_host not in self.hosts:
            await self.send_error(websocket, f"Host {target_host} não está conectado")
            return False
        
        # Registra o cliente
        self.clients[client_id] = {
            'websocket': websocket,
            'info': {
                'client_id': client_id,
                'target_host': target_host,
                'connected_at': datetime.now().isoformat()
            },
            'connected_host': target_host
        }
        
        # Adiciona o cliente à sala do host
        room_id = f"room_{target_host}"
        if room_id in self.rooms:
            self.rooms[room_id]['clients'].add(client_id)
        
        self.stats['total_clients'] += 1
        
        logger.info(f"Cliente conectado: {client_id} -> Host: {target_host}")
        
        # Confirma registro e envia lista de hosts disponíveis
        await self.send_message(websocket, {
            'type': 'client_registered',
            'client_id': client_id,
            'target_host': target_host,
            'available_hosts': list(self.hosts.keys()),
            'server_time': datetime.now().isoformat()
        })
        
        return True
    
    async def handle_screen_frame(self, websocket, data):
        """Processa frame de tela do host e distribui para clientes"""
        host_id = data.get('host_id')
        frame_data = data.get('data')
        
        if not host_id or host_id not in self.hosts:
            return
        
        # Atualiza informações do host
        self.hosts[host_id]['last_seen'] = time.time()
        self.hosts[host_id]['info']['last_frame'] = datetime.now().isoformat()
        
        # Encontra a sala do host
        room_id = f"room_{host_id}"
        if room_id not in self.rooms:
            return
        
        # Envia frame para todos os clientes conectados na sala
        room = self.rooms[room_id]
        frame_message = {
            'type': 'screen_frame',
            'host_id': host_id,
            'data': frame_data,
            'timestamp': data.get('timestamp', time.time())
        }
        
        disconnected_clients = []
        for client_id in room['clients'].copy():
            if client_id in self.clients:
                try:
                    await self.send_message(
                        self.clients[client_id]['websocket'], 
                        frame_message
                    )
                except websockets.exceptions.ConnectionClosed:
                    disconnected_clients.append(client_id)
        
        # Remove clientes desconectados
        for client_id in disconnected_clients:
            await self.remove_client(client_id)
    
    async def handle_control_command(self, websocket, data):
        """Processa comando de controle do cliente e envia para o host"""
        client_id = data.get('client_id')
        target_host = data.get('target_host')
        command = data.get('command')
        
        if not all([client_id, target_host, command]):
            await self.send_error(websocket, "Dados do comando incompletos")
            return
        
        # Verifica se o cliente está registrado
        if client_id not in self.clients:
            await self.send_error(websocket, "Cliente não registrado")
            return
        
        # Verifica se o host está conectado
        if target_host not in self.hosts:
            await self.send_error(websocket, "Host não está conectado")
            return
        
        # Envia comando para o host
        try:
            await self.send_message(self.hosts[target_host]['websocket'], command)
            logger.info(f"Comando enviado: {client_id} -> {target_host} : {command.get('type', 'unknown')}")
        except websockets.exceptions.ConnectionClosed:
            await self.remove_host(target_host)
            await self.send_error(websocket, "Host desconectado")
    
    async def handle_get_hosts(self, websocket, data):
        """Retorna lista de hosts disponíveis"""
        hosts_info = []
        for host_id, host_data in self.hosts.items():
            hosts_info.append({
                'host_id': host_id,
                'connected_at': host_data['info']['connected_at'],
                'last_frame': host_data['info']['last_frame'],
                'clients_connected': len(self.rooms.get(f"room_{host_id}", {}).get('clients', set()))
            })
        
        await self.send_message(websocket, {
            'type': 'hosts_list',
            'hosts': hosts_info,
            'server_stats': self.stats
        })
    
    async def send_message(self, websocket, message):
        """Envia mensagem via WebSocket"""
        try:
            await websocket.send(json.dumps(message))
            self.stats['messages_processed'] += 1
        except websockets.exceptions.ConnectionClosed:
            logger.warning("Tentativa de envio para conexão fechada")
        except Exception as e:
            logger.error(f"Erro ao enviar mensagem: {e}")
    
    async def send_error(self, websocket, error_message):
        """Envia mensagem de erro"""
        await self.send_message(websocket, {
            'type': 'error',
            'message': error_message,
            'timestamp': datetime.now().isoformat()
        })
    
    async def remove_host(self, host_id):
        """Remove host e limpa recursos relacionados"""
        if host_id in self.hosts:
            del self.hosts[host_id]
            
            # Remove a sala do host
            room_id = f"room_{host_id}"
            if room_id in self.rooms:
                # Notifica clientes que o host desconectou
                room = self.rooms[room_id]
                disconnect_message = {
                    'type': 'host_disconnected',
                    'host_id': host_id,
                    'message': 'Host desconectado'
                }
                
                for client_id in room['clients'].copy():
                    if client_id in self.clients:
                        try:
                            await self.send_message(
                                self.clients[client_id]['websocket'],
                                disconnect_message
                            )
                        except:
                            pass
                
                del self.rooms[room_id]
            
            logger.info(f"Host removido: {host_id}")
    
    async def remove_client(self, client_id):
        """Remove cliente e limpa recursos relacionados"""
        if client_id in self.clients:
            client_data = self.clients[client_id]
            target_host = client_data['connected_host']
            
            # Remove cliente da sala
            room_id = f"room_{target_host}"
            if room_id in self.rooms:
                self.rooms[room_id]['clients'].discard(client_id)
            
            del self.clients[client_id]
            logger.info(f"Cliente removido: {client_id}")
    
    async def handle_connection(self, websocket, path):
        """Manipula nova conexão WebSocket"""
        client_addr = websocket.remote_address
        logger.info(f"Nova conexão: {client_addr}")
        
        try:
            async for message in websocket:
                try:
                    data = json.loads(message)
                    message_type = data.get('type')
                    
                    # Roteamento de mensagens
                    if message_type == 'register_host':
                        await self.register_host(websocket, data)
                    
                    elif message_type == 'register_client':
                        await self.register_client(websocket, data)
                    
                    elif message_type == 'screen_frame':
                        await self.handle_screen_frame(websocket, data)
                    
                    elif message_type == 'control_command':
                        await self.handle_control_command(websocket, data)
                    
                    elif message_type == 'get_hosts':
                        await self.handle_get_hosts(websocket, data)
                    
                    else:
                        await self.send_error(websocket, f"Tipo de mensagem desconhecido: {message_type}")
                
                except json.JSONDecodeError:
                    await self.send_error(websocket, "Formato JSON inválido")
                except Exception as e:
                    logger.error(f"Erro ao processar mensagem: {e}")
                    await self.send_error(websocket, "Erro interno do servidor")
        
        except websockets.exceptions.ConnectionClosed:
            logger.info(f"Conexão fechada: {client_addr}")
        except Exception as e:
            logger.error(f"Erro na conexão {client_addr}: {e}")
        
        finally:
            # Limpa recursos da conexão
            await self.cleanup_connection(websocket)
    
    async def cleanup_connection(self, websocket):
        """Limpa recursos de uma conexão desconectada"""
        # Procura e remove hosts
        hosts_to_remove = []
        for host_id, host_data in self.hosts.items():
            if host_data['websocket'] == websocket:
                hosts_to_remove.append(host_id)
        
        for host_id in hosts_to_remove:
            await self.remove_host(host_id)
        
        # Procura e remove clientes
        clients_to_remove = []
        for client_id, client_data in self.clients.items():
            if client_data['websocket'] == websocket:
                clients_to_remove.append(client_id)
        
        for client_id in clients_to_remove:
            await self.remove_client(client_id)
    
    async def start_server(self):
        """Inicia o servidor WebSocket"""
        logger.info(f"Iniciando servidor TARNet em {self.host}:{self.port}")
        
        async with websockets.serve(self.handle_connection, self.host, self.port):
            logger.info(f"Servidor TARNet rodando em ws://{self.host}:{self.port}")
            logger.info("Pressione Ctrl+C para parar o servidor")
            
            # Mantém o servidor rodando
            await asyncio.Future()  # Executa indefinidamente

async def main():
    """Função principal"""
    server = TARNetServer(host='0.0.0.0', port=8000)
    
    try:
        await server.start_server()
    except KeyboardInterrupt:
        logger.info("Servidor interrompido pelo usuário")
    except Exception as e:
        logger.error(f"Erro fatal no servidor: {e}")

if __name__ == "__main__":
    print("=== TARNet WebSocket Server ===")
    print("Servidor de comunicação para o sistema TARNet")
    print("Ctrl+C para parar")
    print()
    
    asyncio.run(main())