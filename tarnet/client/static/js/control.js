// TARNet Cliente Web - Controle Remoto

class RemoteControl extends TARNetApp {
    constructor(hostId, clientId) {
        super();
        this.hostId = hostId;
        this.clientId = clientId;
        
        // Canvas e contexto
        this.canvas = document.getElementById('remote-screen');
        this.ctx = this.canvas.getContext('2d');
        
        // Estado
        this.isFullscreen = false;
        this.isRegistered = false;
        this.quality = 75;
        
        // Estatísticas
        this.stats = {
            fps: 0,
            latency: 0,
            frameCount: 0,
            lastFrameTime: Date.now()
        };
        
        this.init();
    }
    
    init() {
        this.setupCanvas();
        this.setupEventListeners();
        this.setupQualityControl();
        this.connectToServer();
        
        console.log(`Controle remoto iniciado - Host: ${this.hostId}, Cliente: ${this.clientId}`);
    }
    
    async connectToServer() {
        try {
            await this.connect(
                this.handleMessage.bind(this),
                this.onConnected.bind(this),
                this.onDisconnected.bind(this)
            );
        } catch (error) {
            console.error('Erro ao conectar:', error);
            this.updateConnectionStatus('disconnected', 'Falha na conexão');
        }
    }
    
    onConnected() {
        console.log('Conectado - registrando cliente');
        this.registerClient();
    }
    
    onDisconnected() {
        this.isRegistered = false;
        this.hideLoadingOverlay();
    }
    
    registerClient() {
        const success = this.send({
            type: 'register_client',
            client_id: this.clientId,
            target_host: this.hostId
        });
        
        if (!success) {
            this.showNotification('Falha ao registrar cliente', 'error');
        }
    }
    
    handleMessage(data) {
        switch (data.type) {
            case 'client_registered':
                console.log('Cliente registrado com sucesso');
                this.isRegistered = true;
                this.updateConnectionStatus('connected', `Controlando host ${this.formatHostId(data.target_host)}`);
                this.showNotification('Conectado ao host com sucesso', 'success');
                break;
                
            case 'screen_frame':
                this.handleScreenFrame(data);
                break;
                
            case 'host_disconnected':
                this.showNotification('Host desconectado', 'error');
                this.updateConnectionStatus('disconnected', 'Host desconectado');
                setTimeout(() => {
                    window.location.href = '/';
                }, 3000);
                break;
                
            case 'error':
                console.error('Erro do servidor:', data.message);
                this.showNotification(`Erro: ${data.message}`, 'error');
                break;
                
            default:
                console.log('Mensagem não tratada:', data);
        }
    }
    
    handleScreenFrame(data) {
        if (data.host_id !== this.hostId) return;
        
        const img = new Image();
        img.onload = () => {
            // Atualiza canvas
            this.canvas.width = img.width;
            this.canvas.height = img.height;
            this.ctx.drawImage(img, 0, 0);
            
            // Atualiza estatísticas
            this.updateStats();
            this.hideLoadingOverlay();
        };
        
        img.onerror = () => {
            console.error('Erro ao carregar frame');
        };
        
        img.src = `data:image/jpeg;base64,${data.data}`;
    }
    
    setupCanvas() {
        // Configura canvas responsivo
        this.canvas.style.maxWidth = '100%';
        this.canvas.style.height = 'auto';
        
        // Previne menu de contexto
        this.canvas.addEventListener('contextmenu', (e) => {
            e.preventDefault();
        });
    }
    
    setupEventListeners() {
        // Mouse events
        this.canvas.addEventListener('mousedown', this.handleMouseDown.bind(this));
        this.canvas.addEventListener('mouseup', this.handleMouseUp.bind(this));
        this.canvas.addEventListener('mousemove', this.handleMouseMove.bind(this));
        this.canvas.addEventListener('wheel', this.handleWheel.bind(this));
        
        // Keyboard events (canvas precisa estar focado)
        this.canvas.addEventListener('keydown', this.handleKeyDown.bind(this));
        this.canvas.addEventListener('keyup', this.handleKeyUp.bind(this));
        
        // Torna canvas focável
        this.canvas.tabIndex = 0;
        this.canvas.focus();
        
        // Teclado global
        document.addEventListener('keydown', this.handleGlobalKeyDown.bind(this));
    }
    
    setupQualityControl() {
        const qualityRange = document.getElementById('qualityRange');
        if (qualityRange) {
            qualityRange.addEventListener('input', (e) => {
                this.quality = parseInt(e.target.value);
                const label = qualityRange.parentElement.querySelector('small');
                if (label) label.textContent = `${this.quality}%`;
            });
        }
    }
    
    // Event handlers
    handleMouseDown(e) {
        const coords = this.getCanvasCoordinates(e);
        const button = this.getMouseButton(e.button);
        
        this.sendControlCommand({
            type: 'mouse_click',
            x: coords.x,
            y: coords.y,
            button: button
        });
        
        e.preventDefault();
    }
    
    handleMouseUp(e) {
        // Mouse up poderia ser implementado se necessário
        e.preventDefault();
    }
    
    handleMouseMove(e) {
        const coords = this.getCanvasCoordinates(e);
        
        // Throttle mouse move para não sobrecarregar
        if (!this.lastMouseMove || Date.now() - this.lastMouseMove > 50) {
            this.sendControlCommand({
                type: 'mouse_move',
                x: coords.x,
                y: coords.y
            });
            this.lastMouseMove = Date.now();
        }
    }
    
    handleWheel(e) {
        const direction = e.deltaY > 0 ? 'down' : 'up';
        
        this.sendControlCommand({
            type: 'mouse_scroll',
            direction: direction,
            delta: Math.abs(e.deltaY)
        });
        
        e.preventDefault();
    }
    
    handleKeyDown(e) {
        const key = this.mapKey(e);
        if (key) {
            this.sendControlCommand({
                type: 'key_press',
                key: key
            });
        }
        e.preventDefault();
    }
    
    handleKeyUp(e) {
        // Key up poderia ser implementado se necessário
        e.preventDefault();
    }
    
    handleGlobalKeyDown(e) {
        // Atalhos especiais (Esc para sair do fullscreen, etc.)
        if (e.key === 'Escape' && this.isFullscreen) {
            this.toggleFullscreen();
            e.preventDefault();
        }
    }
    
    // Utilidades
    getCanvasCoordinates(e) {
        const rect = this.canvas.getBoundingClientRect();
        const scaleX = this.canvas.width / rect.width;
        const scaleY = this.canvas.height / rect.height;
        
        return {
            x: Math.round((e.clientX - rect.left) * scaleX),
            y: Math.round((e.clientY - rect.top) * scaleY)
        };
    }
    
    getMouseButton(button) {
        switch (button) {
            case 0: return 'left';
            case 1: return 'middle';
            case 2: return 'right';
            default: return 'left';
        }
    }
    
    mapKey(e) {
        // Mapeia teclas para formato compatível com pyautogui
        const key = e.key.toLowerCase();
        
        // Teclas especiais
        const specialKeys = {
            ' ': 'space',
            'enter': 'enter',
            'tab': 'tab',
            'escape': 'esc',
            'backspace': 'backspace',
            'delete': 'delete',
            'arrowup': 'up',
            'arrowdown': 'down',
            'arrowleft': 'left',
            'arrowright': 'right',
            'home': 'home',
            'end': 'end',
            'pageup': 'pageup',
            'pagedown': 'pagedown'
        };
        
        return specialKeys[key] || key;
    }
    
    sendControlCommand(command) {
        if (!this.isRegistered) return false;
        
        return this.send({
            type: 'control_command',
            client_id: this.clientId,
            target_host: this.hostId,
            command: command
        });
    }
    
    updateStats() {
        const now = Date.now();
        const timeDiff = now - this.stats.lastFrameTime;
        
        this.stats.frameCount++;
        this.stats.fps = Math.round(1000 / timeDiff);
        this.stats.latency = timeDiff;
        this.stats.lastFrameTime = now;
        
        // Atualiza UI
        const fpsElement = document.getElementById('fps-counter');
        const latencyElement = document.getElementById('latency-counter');
        
        if (fpsElement) fpsElement.textContent = this.stats.fps;
        if (latencyElement) latencyElement.textContent = this.formatLatency(this.stats.latency);
    }
    
    hideLoadingOverlay() {
        const overlay = document.getElementById('loading-overlay');
        if (overlay) {
            overlay.style.display = 'none';
        }
    }
    
    // Funções públicas
    toggleFullscreen() {
        const container = document.getElementById('screen-container');
        
        if (!this.isFullscreen) {
            // Entra em fullscreen
            if (container.requestFullscreen) {
                container.requestFullscreen();
            }
            this.isFullscreen = true;
        } else {
            // Sai do fullscreen
            if (document.exitFullscreen) {
                document.exitFullscreen();
            }
            this.isFullscreen = false;
        }
    }
    
    fitToScreen() {
        this.canvas.style.width = '100%';
        this.canvas.style.height = 'auto';
    }
    
    disconnect() {
        this.disconnect();
        window.location.href = '/';
    }
}

// Funções globais
function toggleFullscreen() {
    if (window.remoteControl) {
        window.remoteControl.toggleFullscreen();
    }
}

function fitToScreen() {
    if (window.remoteControl) {
        window.remoteControl.fitToScreen();
    }
}

function disconnect() {
    if (window.remoteControl) {
        window.remoteControl.disconnect();
    }
}

function sendKey(key) {
    if (window.remoteControl) {
        window.remoteControl.sendControlCommand({
            type: 'key_press',
            key: key
        });
    }
}

// Inicializa controle remoto
document.addEventListener('DOMContentLoaded', function() {
    // Só inicializa se estivermos na página de controle
    if (window.TARNet && window.TARNet.hostId) {
        window.remoteControl = new RemoteControl(window.TARNet.hostId, window.TARNet.clientId);
        window.tarnetApp = window.remoteControl;
    }
});