# TARNet - Tríade do Acesso Remoto Internet

## Visão Geral

O TARNet é um sistema completo de controle remoto composto por três componentes principais que trabalham em conjunto para permitir acesso remoto seguro e eficiente a computadores através da web.

### Componentes do Sistema

1. **Host Agent** 🖥️ - Agente instalado no computador a ser controlado
2. **WebSocket Server** 🌐 - Servidor central de comunicação
3. **Cliente Web** 💻 - Interface web para controle remoto

## Status do Projeto

- ✅ **Host Agent** - Completo e funcional
- ✅ **WebSocket Server** - Completo e funcional  
- 🔄 **Cliente Web** - Em desenvolvimento

## Estrutura do Projeto

```
tarnet/
├── host/                    # Host Agent
│   ├── host.py             # Aplicação principal do host
│   ├── requirements.txt    # Dependências do host
│   └── README.md          # Documentação do host
├── server/                 # WebSocket Server
│   ├── server.py          # Servidor de comunicação
│   ├── requirements.txt   # Dependências do servidor
│   └── README.md         # Documentação do servidor
├── client/                # Cliente Web (futuro)
│   └── (em desenvolvimento)
├── shared/                # Recursos compartilhados
│   └── (utilitários comuns)
├── requirements.txt       # Dependências do projeto completo
└── README.md             # Este arquivo
```

## Instalação Rápida

### 1. Instalar Dependências
```bash
# No diretório raiz do projeto
pip install -r requirements.txt
```

### 2. Executar Servidor WebSocket
```bash
cd server
python server.py
```
O servidor iniciará em `ws://localhost:8000`

### 3. Executar Host Agent
```bash
cd host
python host.py
```
O host se conectará automaticamente ao servidor

## Fluxo de Funcionamento

### 1. Inicialização
1. **Servidor** inicia e aguarda conexões na porta 8000
2. **Host Agent** conecta ao servidor e se registra com ID único
3. **Cliente Web** conecta ao servidor e escolhe host para controlar

### 2. Transmissão de Tela
1. Host captura tela continuamente (10 FPS)
2. Imagem é comprimida (JPEG) e convertida para base64
3. Frame é enviado via WebSocket para o servidor
4. Servidor distribui frame para clientes conectados ao host

### 3. Controle Remoto
1. Cliente envia comando de mouse/teclado via WebSocket
2. Servidor roteia comando para o host correspondente
3. Host executa comando usando pyautogui
4. Resultado é refletido na próxima captura de tela

## Protocolos de Comunicação

### Host → Servidor

#### Registro
```json
{
  "type": "register_host",
  "host_id": "uuid-gerado",
  "timestamp": 1234567890
}
```

#### Frame de Tela
```json
{
  "type": "screen_frame",
  "host_id": "uuid-do-host",
  "data": "base64-image-data",
  "timestamp": 1234567890
}
```

### Cliente → Servidor

#### Comando de Mouse
```json
{
  "type": "control_command",
  "client_id": "uuid-cliente",
  "target_host": "uuid-host",
  "command": {
    "type": "mouse_click",
    "x": 100,
    "y": 200,
    "button": "left"
  }
}
```

#### Comando de Teclado
```json
{
  "type": "control_command",
  "client_id": "uuid-cliente", 
  "target_host": "uuid-host",
  "command": {
    "type": "key_press",
    "key": "enter"
  }
}
```

## Requisitos do Sistema

### Host Agent
- **Python 3.7+**
- **Sistema com Interface Gráfica** (Windows, macOS, Linux com X11)
- **Dependências**: mss, pillow, pyautogui, websockets

### WebSocket Server
- **Python 3.7+**
- **Qualquer Sistema Operacional**
- **Dependências**: websockets

### Cliente Web (futuro)
- **Navegador Moderno** com suporte a WebSocket
- **JavaScript habilitado**

## Compatibilidade de Ambiente

### ✅ Funciona
- **Windows** com interface gráfica
- **macOS** com interface gráfica
- **Linux** com X11/Wayland
- **Servidores dedicados** (apenas servidor WebSocket)

### ❌ Não Funciona
- **Replit/CodeSandbox** (host agent apenas - sem display)
- **Containers Docker** sem X11 forwarding
- **Servidores headless** (host agent apenas)

## Funcionalidades Implementadas

### Host Agent
- ✅ Captura de tela em tempo real (configurável)
- ✅ Compressão de imagem otimizada
- ✅ Conexão WebSocket confiável
- ✅ Execução de comandos de mouse e teclado
- ✅ Registro automático no servidor
- ✅ Tratamento de erros e reconexão

### WebSocket Server
- ✅ Gerenciamento de múltiplos hosts
- ✅ Sistema de salas para isolar sessões
- ✅ Roteamento eficiente de dados
- ✅ Limpeza automática de conexões
- ✅ Logs detalhados e estatísticas
- ✅ Tratamento robusto de erros

### Cliente Web (em desenvolvimento)
- 🔄 Interface web responsiva
- 🔄 Visualização de tela em tempo real
- 🔄 Controles de mouse e teclado
- 🔄 Lista de hosts disponíveis
- 🔄 Configurações de qualidade

## Comandos Úteis

### Executar Projeto Completo
```bash
# Terminal 1 - Servidor
cd tarnet/server && python server.py

# Terminal 2 - Host Agent
cd tarnet/host && python host.py

# Terminal 3 - Cliente Web (futuro)
cd tarnet/client && python app.py
```

### Instalar por Componente
```bash
# Apenas Host Agent
cd tarnet/host && pip install -r requirements.txt

# Apenas Servidor
cd tarnet/server && pip install -r requirements.txt
```

## Segurança e Uso Responsável

### ⚠️ Avisos Importantes
- **Controle Total**: O sistema permite controle completo do computador host
- **Uso Autorizado**: Use apenas em sistemas próprios ou com autorização explícita
- **Rede Segura**: Recomendado para uso em redes locais confiáveis
- **Sem Criptografia**: Conexões são em texto plano (ws://)

### 🔒 Melhorias de Segurança Futuras
- Autenticação por token/senha
- Conexões criptografadas (WSS)
- Rate limiting
- Whitelist de IPs
- Logs de auditoria

## Troubleshooting

### Host Agent não conecta
1. Verifique se o servidor está rodando
2. Confirme se a porta 8000 está liberada
3. Teste conectividade: `telnet localhost 8000`

### Erro de captura de tela
1. Verifique permissões de acessibilidade (macOS)
2. Confirme que há interface gráfica disponível
3. Teste se pyautogui funciona: `python -c "import pyautogui; print('OK')"`

### Performance baixa
1. Ajuste `capture_interval` no host.py (aumentar = menos FPS)
2. Reduza `compression_quality` para menor qualidade
3. Verifique latência de rede

## Roadmap

### Fase 1 (Completa) ✅
- Host Agent funcional
- Servidor WebSocket robusto
- Protocolo de comunicação definido

### Fase 2 (Em Desenvolvimento) 🔄
- Cliente Web com interface moderna
- Controles avançados de qualidade
- Suporte a múltiplas telas

### Fase 3 (Futuro) 📋
- Autenticação e segurança
- Transferência de arquivos
- Gravação de sessões
- Apps mobile (iOS/Android)

## Contribuição

### Como Contribuir
1. Faça fork do projeto
2. Crie branch para sua feature
3. Implemente e teste thoroughly
4. Submeta pull request com descrição detalhada

### Áreas que Precisam de Ajuda
- Testes automatizados
- Segurança e criptografia
- Performance e otimização
- Interface do cliente web
- Documentação

## Licença

Este projeto está licenciado sob a MIT License - veja o arquivo LICENSE para detalhes.

## Suporte

Para dúvidas, bugs ou sugestões:
1. Abra uma issue no GitHub
2. Forneça logs detalhados
3. Inclua informações do sistema
4. Descreva passos para reproduzir

---

**TARNet** - Conectando computadores através da internet de forma simples e eficiente.