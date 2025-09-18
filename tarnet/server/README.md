# TARNet WebSocket Server

## Descrição

O TARNet WebSocket Server é o componente central do sistema TARNet (Tríade do Acesso Remoto Internet). Este servidor gerencia a comunicação entre os Host Agents (que capturam tela) e os Clientes Web (que visualizam e controlam remotamente).

## Funcionalidades

### Gerenciamento de Conexões
- **Registro de Hosts**: Aceita conexões de Host Agents e os registra com ID único
- **Registro de Clientes**: Conecta clientes web aos hosts disponíveis
- **Sistema de Salas**: Organiza hosts e clientes em salas isoladas
- **Limpeza Automática**: Remove conexões inativas e limpa recursos

### Roteamento de Dados
- **Frames de Tela**: Recebe frames dos hosts e distribui para clientes conectados
- **Comandos de Controle**: Roteia comandos de mouse/teclado dos clientes para os hosts
- **Lista de Hosts**: Fornece informações sobre hosts disponíveis
- **Estatísticas**: Monitora conexões e performance do servidor

### Tratamento de Erros
- **Validação de Mensagens**: Verifica formato JSON e campos obrigatórios
- **Reconexão Automática**: Gerencia desconexões e limpeza de recursos
- **Logs Detalhados**: Sistema de logging para monitoramento e debug

## Instalação

### Dependências
```bash
pip install -r requirements.txt
```

### Executando o Servidor
```bash
python server.py
```

O servidor iniciará em `ws://0.0.0.0:8000` e ficará aguardando conexões.

## Protocolo de Comunicação

### Mensagens do Host Agent

#### Registro do Host
```json
{
  "type": "register_host",
  "host_id": "uuid-do-host",
  "timestamp": 1234567890
}
```

#### Frame de Tela
```json
{
  "type": "screen_frame",
  "host_id": "uuid-do-host",
  "data": "base64-encoded-image",
  "timestamp": 1234567890
}
```

### Mensagens do Cliente Web

#### Registro do Cliente
```json
{
  "type": "register_client",
  "client_id": "uuid-do-cliente",
  "target_host": "uuid-do-host-alvo"
}
```

#### Comando de Controle
```json
{
  "type": "control_command",
  "client_id": "uuid-do-cliente",
  "target_host": "uuid-do-host",
  "command": {
    "type": "mouse_click",
    "x": 100,
    "y": 200,
    "button": "left"
  }
}
```

#### Solicitar Lista de Hosts
```json
{
  "type": "get_hosts"
}
```

### Respostas do Servidor

#### Confirmação de Registro
```json
{
  "type": "host_registered",
  "host_id": "uuid-do-host",
  "room_id": "room_uuid-do-host",
  "server_time": "2023-09-18T12:00:00"
}
```

#### Lista de Hosts
```json
{
  "type": "hosts_list",
  "hosts": [
    {
      "host_id": "uuid-do-host",
      "connected_at": "2023-09-18T12:00:00",
      "last_frame": "2023-09-18T12:00:30",
      "clients_connected": 2
    }
  ],
  "server_stats": {
    "total_hosts": 1,
    "total_clients": 2,
    "messages_processed": 1500
  }
}
```

#### Erro
```json
{
  "type": "error",
  "message": "Descrição do erro",
  "timestamp": "2023-09-18T12:00:00"
}
```

## Arquitetura Técnica

### Estrutura de Dados
- **hosts**: Dicionário com informações dos Host Agents conectados
- **clients**: Dicionário com informações dos clientes web conectados  
- **rooms**: Sistema de salas que agrupa hosts e seus clientes
- **stats**: Estatísticas de uso e performance do servidor

### Fluxo de Dados
1. **Host se conecta** → Servidor cria sala para o host
2. **Cliente se conecta** → Servidor adiciona cliente à sala do host escolhido
3. **Host envia frame** → Servidor distribui para todos os clientes da sala
4. **Cliente envia comando** → Servidor roteia para o host correspondente

### Tratamento de Desconexões
- Detecta conexões fechadas automaticamente
- Remove hosts/clientes das estruturas internas
- Notifica clientes quando host desconecta
- Limpa salas vazias

## Configuração

### Parâmetros do Servidor
- **Host**: `0.0.0.0` (aceita conexões de qualquer IP)
- **Porta**: `8000` (padrão WebSocket)
- **Logging**: Nível INFO com timestamps

### Personalização
Para alterar host/porta, modifique a linha no `main()`:
```python
server = TARNetServer(host='localhost', port=8000)
```

## Logs e Monitoramento

O servidor produz logs detalhados:
- Conexões e desconexões
- Registro de hosts e clientes
- Roteamento de mensagens
- Erros e exceções

### Exemplo de Log
```
2023-09-18 12:00:00 - TARNetServer - INFO - TARNet Server inicializado - 0.0.0.0:8000
2023-09-18 12:00:01 - TARNetServer - INFO - Nova conexão: ('192.168.1.100', 45678)
2023-09-18 12:00:02 - TARNetServer - INFO - Host registrado: abc-123 na sala room_abc-123
```

## Segurança

### Considerações Atuais
- Servidor aceita conexões de qualquer IP (`0.0.0.0`)
- Sem autenticação ou criptografia
- Adequado para redes locais confiáveis

### Recomendações para Produção
- Implementar autenticação por token
- Usar WSS (WebSocket Secure) com TLS
- Limitar IPs permitidos
- Rate limiting para prevenir abuse

## Próximos Componentes

Este é o segundo de três componentes do TARNet:
1. **Host Agent** ✅ - Captura tela e executa comandos
2. **WebSocket Server** ✅ - Gerencia comunicação (atual)
3. **Cliente Web** 🔄 - Interface web para controle remoto