# TARNet Host Agent

## Descrição

O TARNet (Tríade do Acesso Remoto Internet) Host Agent é o primeiro componente do sistema de controle remoto. Este agente é responsável por capturar a tela do computador e enviar os frames para um servidor WebSocket, além de receber e executar comandos de controle remoto (mouse e teclado).

## Funcionalidades

### Captura de Tela
- Captura automática da tela em intervalos configuráveis (padrão: 10 FPS)
- Compressão de imagem usando Pillow para otimizar a transmissão
- Redimensionamento automático para 1280x720 pixels
- Conversão para formato base64 para transmissão via WebSocket

### Conectividade
- Conexão WebSocket com servidor em `ws://localhost:8000`
- Registro automático com identificador único (UUID)
- Envio contínuo de frames da tela para o servidor
- Escuta de comandos em tempo real

### Controle Remoto
- **Movimento do Mouse**: Recebe comandos `mouse_move` com coordenadas x,y
- **Clique do Mouse**: Executa cliques com `mouse_click` (esquerdo, direito, meio)
- **Pressionamento de Teclas**: Executa comandos `key_press` com teclas específicas

## Instalação

### Pré-requisitos
- Python 3.7 ou superior
- Sistema operacional: Windows, macOS ou Linux

### Instalando Dependências

```bash
pip install -r requirements.txt
```

### Dependências Incluídas
- **mss**: Captura rápida de tela multiplataforma
- **pillow**: Processamento e compressão de imagens
- **pyautogui**: Controle de mouse e teclado
- **websockets**: Cliente WebSocket para comunicação

## Como Usar

### Executando o Host Agent

```bash
python host.py
```

### Requisitos para Funcionamento
1. **Servidor WebSocket**: O servidor deve estar rodando em `ws://localhost:8000`
2. **Permissões**: O sistema pode solicitar permissões para:
   - Captura de tela (macOS/Linux)
   - Controle de acessibilidade (macOS)
   - Acesso ao mouse e teclado

### Saída do Programa
- Pressione `Ctrl+C` para interromper o Host Agent
- O programa exibe logs de todas as operações realizadas

## Funcionamento Técnico

### Fluxo de Operação
1. **Inicialização**: Gera ID único e configura parâmetros
2. **Conexão**: Conecta ao servidor WebSocket
3. **Registro**: Registra o host no servidor com seu ID
4. **Loop Principal**: 
   - Captura tela continuamente
   - Envia frames comprimidos para o servidor
   - Escuta comandos do servidor
   - Executa comandos recebidos

### Formato dos Comandos JSON

#### Movimento do Mouse
```json
{
  "type": "mouse_move",
  "x": 100,
  "y": 200
}
```

#### Clique do Mouse
```json
{
  "type": "mouse_click", 
  "x": 100,
  "y": 200,
  "button": "left"
}
```

#### Pressionamento de Tecla
```json
{
  "type": "key_press",
  "key": "enter"
}
```

### Configurações Ajustáveis
- **Intervalo de Captura**: Modificar `capture_interval` (padrão: 0.1s = 10 FPS)
- **Qualidade de Compressão**: Ajustar `compression_quality` (padrão: 50)
- **Resolução**: Alterar redimensionamento na função `capture_screen()`

## Segurança

### Medidas Implementadas
- **Failsafe do PyAutoGUI**: Mover mouse para canto superior esquerdo interrompe operações
- **Pause entre Comandos**: Pequeno delay entre execuções de comandos
- **Tratamento de Erros**: Captura e log de exceções sem travar o programa

### Importante
- Este é um software de controle remoto. Use apenas em sistemas próprios ou com autorização
- O Host Agent permite controle total do sistema onde está executando
- Mantenha o servidor seguro e use apenas em redes confiáveis

## Troubleshooting

### Problemas Comuns
1. **Erro de Conexão**: Verifique se o servidor WebSocket está rodando em `localhost:8000`
2. **Permissões Negadas**: Conceda permissões de acessibilidade nas configurações do sistema
3. **Captura de Tela Falha**: Alguns sistemas requerem permissões especiais para captura de tela

### Logs de Debug
O programa exibe logs detalhados de todas as operações. Monitore a saída do console para identificar problemas.

---

**Projeto**: TARNet (Tríade do Acesso Remoto Internet)  
**Componente**: Host Agent (1/3)  
**Próximos Componentes**: Servidor WebSocket e Cliente Web