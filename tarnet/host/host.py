import asyncio
import websockets
import json
import base64
import io
import uuid
import time
from mss import mss
from PIL import Image
import pyautogui

class HostAgent:
    def __init__(self):
        self.host_id = str(uuid.uuid4())
        self.websocket = None
        self.running = False
        self.screen_capture = mss()
        
        # Configurações de captura
        self.capture_interval = 0.1  # 10 FPS
        self.compression_quality = 50  # Qualidade da compressão JPEG
        
        print(f"Host Agent inicializado com ID: {self.host_id}")
    
    async def connect_to_server(self, server_url="ws://localhost:8000"):
        """Conecta ao servidor WebSocket"""
        try:
            self.websocket = await websockets.connect(server_url)
            print(f"Conectado ao servidor: {server_url}")
            
            # Registrar o host no servidor
            await self.register_host()
            
            return True
        except Exception as e:
            print(f"Erro ao conectar com o servidor: {e}")
            return False
    
    async def register_host(self):
        """Registra o host no servidor com ID único"""
        registration_data = {
            "type": "register_host",
            "host_id": self.host_id,
            "timestamp": time.time()
        }
        
        await self.websocket.send(json.dumps(registration_data))
        print(f"Host registrado no servidor com ID: {self.host_id}")
    
    def capture_screen(self):
        """Captura a tela e converte para base64"""
        try:
            # Captura a tela principal
            monitor = self.screen_capture.monitors[1]  # Monitor principal
            screenshot = self.screen_capture.grab(monitor)
            
            # Converte para PIL Image
            img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
            
            # Redimensiona para otimizar (opcional)
            img = img.resize((1280, 720), Image.Resampling.LANCZOS)
            
            # Comprime e converte para base64
            buffer = io.BytesIO()
            img.save(buffer, format="JPEG", quality=self.compression_quality)
            img_str = base64.b64encode(buffer.getvalue()).decode()
            
            return img_str
        
        except Exception as e:
            print(f"Erro ao capturar tela: {e}")
            return None
    
    async def send_screen_frame(self):
        """Envia frame da tela para o servidor"""
        screen_data = self.capture_screen()
        
        if screen_data:
            frame_data = {
                "type": "screen_frame",
                "host_id": self.host_id,
                "data": screen_data,
                "timestamp": time.time()
            }
            
            try:
                await self.websocket.send(json.dumps(frame_data))
            except Exception as e:
                print(f"Erro ao enviar frame: {e}")
    
    def execute_mouse_move(self, x, y):
        """Move o mouse para a posição especificada"""
        try:
            pyautogui.moveTo(x, y)
            print(f"Mouse movido para: ({x}, {y})")
        except Exception as e:
            print(f"Erro ao mover mouse: {e}")
    
    def execute_mouse_click(self, x, y, button="left"):
        """Executa clique do mouse na posição especificada"""
        try:
            pyautogui.click(x, y, button=button)
            print(f"Clique {button} executado em: ({x}, {y})")
        except Exception as e:
            print(f"Erro ao executar clique: {e}")
    
    def execute_key_press(self, key):
        """Executa pressionamento de tecla"""
        try:
            pyautogui.press(key)
            print(f"Tecla pressionada: {key}")
        except Exception as e:
            print(f"Erro ao pressionar tecla: {e}")
    
    async def process_command(self, command_data):
        """Processa comandos recebidos do servidor"""
        try:
            command_type = command_data.get("type")
            
            if command_type == "mouse_move":
                x = command_data.get("x", 0)
                y = command_data.get("y", 0)
                self.execute_mouse_move(x, y)
            
            elif command_type == "mouse_click":
                x = command_data.get("x", 0)
                y = command_data.get("y", 0)
                button = command_data.get("button", "left")
                self.execute_mouse_click(x, y, button)
            
            elif command_type == "key_press":
                key = command_data.get("key", "")
                if key:
                    self.execute_key_press(key)
            
            else:
                print(f"Comando desconhecido: {command_type}")
        
        except Exception as e:
            print(f"Erro ao processar comando: {e}")
    
    async def listen_for_commands(self):
        """Escuta comandos do servidor"""
        try:
            async for message in self.websocket:
                try:
                    command_data = json.loads(message)
                    await self.process_command(command_data)
                except json.JSONDecodeError:
                    print("Mensagem recebida não é JSON válido")
                except Exception as e:
                    print(f"Erro ao processar mensagem: {e}")
        
        except websockets.exceptions.ConnectionClosed:
            print("Conexão com servidor foi fechada")
            self.running = False
        except Exception as e:
            print(f"Erro ao escutar comandos: {e}")
    
    async def screen_capture_loop(self):
        """Loop principal de captura e envio de tela"""
        while self.running:
            await self.send_screen_frame()
            await asyncio.sleep(self.capture_interval)
    
    async def run(self):
        """Executa o Host Agent"""
        print("Iniciando Host Agent...")
        
        # Conecta ao servidor
        if not await self.connect_to_server():
            print("Falha ao conectar com o servidor. Verifique se o servidor está rodando.")
            return
        
        self.running = True
        
        try:
            # Executa captura de tela e escuta de comandos em paralelo
            await asyncio.gather(
                self.screen_capture_loop(),
                self.listen_for_commands()
            )
        
        except KeyboardInterrupt:
            print("Host Agent interrompido pelo usuário")
        
        except Exception as e:
            print(f"Erro durante execução: {e}")
        
        finally:
            self.running = False
            if self.websocket:
                await self.websocket.close()
            print("Host Agent finalizado")

async def main():
    """Função principal"""
    # Configuração de segurança do pyautogui
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.01
    
    # Criar e executar o Host Agent
    host_agent = HostAgent()
    await host_agent.run()

if __name__ == "__main__":
    print("=== TARNet Host Agent ===")
    print("Pressione Ctrl+C para sair")
    print()
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nHost Agent finalizado pelo usuário")