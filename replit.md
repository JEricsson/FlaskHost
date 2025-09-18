# TARNet - Tríade do Acesso Remoto Internet

## Visão Geral

Este é o projeto TARNet (Tríade do Acesso Remoto Internet), um sistema completo de controle remoto composto por três componentes principais. Atualmente, temos **2 de 3 componentes completos e funcionais**.

## Preferências do Usuário

Estilo de comunicação preferido: Linguagem simples e cotidiana.
Idioma: Português do Brasil (PT-BR)

## Status do Projeto

- ✅ **Host Agent** (Projeto 1) - Completo e testado
- ✅ **WebSocket Server** (Projeto 2) - Completo e testado  
- 🔄 **Cliente Web** (Projeto 3) - Próximo a ser desenvolvido

## Arquitetura do Sistema

### 1. Host Agent (tarnet/host/)
- **Captura de Tela**: Utiliza `mss` para captura rápida e eficiente da tela
- **Compressão de Imagem**: Usa `Pillow` para comprimir imagens em formato JPEG e converter para base64
- **WebSocket Client**: Conecta ao servidor em `ws://localhost:8000` usando `websockets`
- **Controle Remoto**: Executa comandos de mouse e teclado usando `pyautogui`
- **Identificação Única**: Gera UUID único para cada instância do host

### 2. WebSocket Server (tarnet/server/)
- **Gerenciamento de Conexões**: Aceita e gerencia hosts e clientes simultaneamente
- **Sistema de Salas**: Isola hosts em salas separadas com seus respectivos clientes
- **Roteamento de Dados**: Distribui frames de tela e comandos de controle eficientemente
- **Limpeza Automática**: Remove conexões inativas e gerencia recursos automaticamente
- **Logs Detalhados**: Sistema completo de logging para monitoramento e debug

### 3. Cliente Web (tarnet/client/) - Em Desenvolvimento
- Interface web responsiva para visualização e controle
- Seleção de hosts disponíveis
- Controles de mouse e teclado em tempo real
- Configurações de qualidade e performance

## Estrutura do Projeto

```
tarnet/
├── host/                    # Host Agent (Projeto 1) ✅
│   ├── host.py             # Aplicação principal do host
│   ├── requirements.txt    # Dependências do host
│   └── README.md          # Documentação do host
├── server/                 # WebSocket Server (Projeto 2) ✅
│   ├── server.py          # Servidor de comunicação
│   ├── requirements.txt   # Dependências do servidor
│   └── README.md         # Documentação do servidor
├── client/                # Cliente Web (Projeto 3) 🔄
│   └── (próximo a ser desenvolvido)
├── shared/                # Recursos compartilhados
│   └── (utilitários comuns)
├── requirements.txt       # Dependências do projeto completo
└── README.md             # Documentação principal
```

## Dependências Externas

### Host Agent
- **mss 9.0.1**: Captura de tela multiplataforma
- **pillow 10.0.1**: Processamento e compressão de imagens
- **pyautogui 0.9.54**: Controle de mouse e teclado
- **websockets 12.0**: Cliente WebSocket para comunicação

### WebSocket Server
- **websockets 12.0**: Servidor WebSocket para gerenciar conexões

### Requisitos de Runtime
- **Python 3.7+**: Versão necessária para compatibilidade
- **Interface Gráfica**: Host Agent requer sistema com display (Windows, macOS, Linux com X11)
- **Rede**: Conectividade entre componentes (localhost ou rede local)

## Funcionalidades Implementadas

### Host Agent ✅
- Captura automática da tela em intervalos configuráveis (10 FPS)
- Compressão JPEG para otimizar transmissão
- Conexão WebSocket confiável com reconexão
- Execução de comandos de mouse e teclado em tempo real
- Registro automático no servidor com UUID
- Tratamento robusto de erros e desconexões

### WebSocket Server ✅
- Gerenciamento simultâneo de múltiplos hosts e clientes
- Sistema de salas que isola sessões por host
- Roteamento eficiente de frames de tela para clientes conectados
- Roteamento de comandos de controle dos clientes para hosts
- Limpeza automática de recursos em desconexões
- Sistema completo de logs e estatísticas
- Validação de mensagens e tratamento de erros
- API REST-like para consulta de hosts disponíveis

### Cliente Web 🔄
- Interface web moderna e responsiva (em desenvolvimento)
- Visualização de tela em tempo real (em desenvolvimento)
- Controles intuitivos de mouse e teclado (em desenvolvimento)
- Seleção de hosts disponíveis (em desenvolvimento)

## Protocolos de Comunicação

### Host → Servidor
- **Registro**: `register_host` com ID único
- **Frames**: `screen_frame` com dados da tela em base64
- **Heartbeat**: Atualizações periódicas de status

### Cliente → Servidor
- **Registro**: `register_client` especificando host alvo
- **Comandos**: `control_command` com ações de mouse/teclado
- **Consultas**: `get_hosts` para listar hosts disponíveis

### Servidor → Cliente/Host
- **Confirmações**: Confirmação de registros e operações
- **Distribuição**: Roteamento de frames e comandos
- **Notificações**: Alertas de desconexões e erros

## Limitações Ambientais

### ✅ Ambientes Suportados
- **Windows** com interface gráfica
- **macOS** com interface gráfica
- **Linux** com X11/Wayland
- **Servidores dedicados** (apenas WebSocket Server)

### ❌ Limitações Conhecidas
- **Replit/CodeSandbox**: Host Agent não funciona (sem display gráfico)
- **Containers Docker**: Requer X11 forwarding para Host Agent
- **Servidores headless**: Host Agent não pode capturar tela ou controlar

## Segurança e Uso Responsável

### ⚠️ Considerações de Segurança
- **Controle Total**: Sistema permite controle completo do computador host
- **Uso Autorizado**: Use apenas em sistemas próprios ou com autorização explícita
- **Rede Segura**: Recomendado para uso em redes locais confiáveis
- **Sem Criptografia**: Conexões atuais são em texto plano (ws://)

### 🔒 Melhorias Futuras de Segurança
- Autenticação por token/senha
- Conexões criptografadas (WSS)
- Rate limiting para prevenir abuso
- Whitelist de IPs permitidos
- Logs de auditoria de comandos

## Testes e Validação

### Testes Realizados ✅
- Conectividade Host Agent ↔ Servidor
- Registro e gerenciamento de salas
- Transmissão de frames de tela
- Roteamento de comandos de controle
- Limpeza de recursos em desconexões
- Tratamento de erros e exceções

### Resultados dos Testes
- **Host Registration**: ✅ Registra com sucesso e cria sala
- **Frame Transmission**: ✅ Envia e roteia frames corretamente  
- **Command Routing**: ✅ Comandos chegam ao host correto
- **Resource Cleanup**: ✅ Remove recursos em desconexões
- **Error Handling**: ✅ Trata erros graciosamente

## Próximos Passos

### Projeto 3: Cliente Web
1. **Interface Web**: Criar interface moderna e responsiva
2. **Visualização**: Implementar display de frames em tempo real
3. **Controles**: Adicionar controles intuitivos de mouse/teclado
4. **Configurações**: Opções de qualidade e performance
5. **Seleção de Hosts**: Interface para escolher host a controlar

### Melhorias Futuras
- Autenticação e segurança
- Suporte a múltiplas telas
- Transferência de arquivos
- Gravação de sessões
- Apps móveis (iOS/Android)

## Comandos de Execução

### Executar Projeto Completo
```bash
# Terminal 1 - Servidor WebSocket
cd tarnet/server && python server.py

# Terminal 2 - Host Agent (em sistema com GUI)
cd tarnet/host && python host.py

# Terminal 3 - Cliente Web (futuro)
cd tarnet/client && python app.py
```

### Instalar Dependências
```bash
# Projeto completo
pip install -r tarnet/requirements.txt

# Por componente
pip install -r tarnet/host/requirements.txt      # Host Agent
pip install -r tarnet/server/requirements.txt   # Servidor
```

## Troubleshooting

### Host Agent não conecta
1. Verificar se servidor está rodando em localhost:8000
2. Confirmar conectividade de rede
3. Verificar logs do servidor para erros

### Erro de captura de tela
1. Confirmar que sistema tem interface gráfica
2. Verificar permissões de acessibilidade (macOS)
3. Testar pyautogui funcionalmente

### Performance baixa
1. Ajustar `capture_interval` no host.py
2. Reduzir `compression_quality` para menor qualidade
3. Verificar latência de rede entre componentes

---

**TARNet** - Sistema completo de controle remoto via internet, simples e eficiente.