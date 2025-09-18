# TARNet Host Agent

## Visão Geral

Este é o projeto TARNet (Tríade do Acesso Remoto Internet) - Host Agent, o primeiro componente de um sistema de controle remoto. O Host Agent é responsável por capturar a tela do computador, comprimir as imagens e enviá-las via WebSocket para um servidor, além de receber e executar comandos de controle remoto para mouse e teclado.

## Preferências do Usuário

Estilo de comunicação preferido: Linguagem simples e cotidiana.
Idioma: Português do Brasil (PT-BR)

## Arquitetura do Sistema

### Arquitetura do Host Agent
- **Captura de Tela**: Utiliza a biblioteca `mss` para captura rápida e eficiente da tela
- **Compressão de Imagem**: Usa `Pillow` para comprimir imagens em formato JPEG e converter para base64
- **WebSocket Client**: Conecta ao servidor em `ws://localhost:8000` usando `websockets`
- **Controle Remoto**: Executa comandos de mouse e teclado usando `pyautogui`
- **Identificação Única**: Gera UUID único para cada instância do host

### Configurações do Servidor
- **Conectividade**: Cliente WebSocket conectando em `ws://localhost:8000`
- **Taxa de Captura**: 10 FPS (configurável via `capture_interval`)
- **Qualidade de Compressão**: 50% (configurável via `compression_quality`)
- **Resolução**: Redimensiona para 1280x720 para otimizar transmissão

### Estrutura da Aplicação
- **Arquivo Principal**: `host.py` contém toda a lógica do Host Agent
- **Execução Assíncrona**: Utiliza `asyncio` para captura de tela e escuta de comandos em paralelo
- **Tratamento de Comandos**: Processa comandos JSON para mouse_move, mouse_click e key_press

### Protocolo de Comunicação
- **Registro**: Envia `register_host` com ID único ao conectar
- **Frames de Tela**: Envia `screen_frame` com dados da tela em base64
- **Comandos**: Recebe comandos JSON para controle de mouse e teclado

## Dependências Externas

### Pacotes Python
- **mss 9.0.1**: Captura de tela multiplataforma
- **pillow 10.0.1**: Processamento e compressão de imagens
- **pyautogui 0.9.54**: Controle de mouse e teclado
- **websockets 12.0**: Cliente WebSocket para comunicação

### Requisitos de Runtime
- **Python 3.11+**: Versão necessária para compatibilidade
- **Interface Gráfica**: Requer sistema com display (Windows, macOS, Linux com X11)
- **pip**: Gerenciador de pacotes para instalação de dependências

### Ferramentas de Desenvolvimento
- **Ambiente Gráfico**: Necessário para pyautogui funcionar (não compatível com servidores headless)
- **Servidor WebSocket**: Requer servidor separado rodando na porta 8000
- **Sem Banco de Dados**: Aplicação não utiliza armazenamento persistente

## Funcionalidades Implementadas

### Captura e Transmissão
- Captura automática da tela em intervalos configuráveis
- Compressão JPEG para otimizar banda
- Envio contínuo de frames via WebSocket
- Redimensionamento automático para 1280x720

### Controle Remoto
- Movimento do mouse com coordenadas x,y
- Cliques do mouse (esquerdo, direito, meio)
- Pressionamento de teclas específicas
- Execução em tempo real dos comandos recebidos

### Conectividade
- Registro automático no servidor com UUID
- Reconexão em caso de falha de rede
- Escuta contínua de comandos do servidor
- Tratamento gracioso de interrupções (Ctrl+C)

## Notas Técnicas

### Limitações Ambientais
- **Replit**: Não funciona no ambiente Replit (servidor sem interface gráfica)
- **Servidores Headless**: Requer ambiente com display gráfico
- **Permissões**: Pode precisar de permissões especiais para captura de tela e controle

### Segurança
- **Acesso Total**: Permite controle completo do sistema onde executa
- **Uso Responsável**: Deve ser usado apenas em sistemas próprios ou com autorização
- **Rede Segura**: Recomendado uso em redes confiáveis

### Próximos Componentes
Este é o primeiro de três componentes do projeto TARNet:
1. **Host Agent** (atual) - Captura tela e executa comandos
2. **Servidor WebSocket** (próximo) - Gerencia conexões e roteamento
3. **Cliente Web** (futuro) - Interface web para controle remoto