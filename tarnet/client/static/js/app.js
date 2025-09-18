// TARNet Cliente Web - JavaScript Principal

class TARNetApp {
    constructor() {
        // Usa a URL do WebSocket fornecida pelo servidor ou fallback para localhost
        const defaultServerUrl = window.TARNET_CONFIG?.websocketUrl || 'ws://localhost:8000';
        
        this.config = {
            serverUrl: localStorage.getItem('tarnet_server_url') || defaultServerUrl,
            reconnectInterval: parseInt(localStorage.getItem('tarnet_reconnect_interval')) || 5000,
            maxReconnectAttempts: 10
        };
        
        this.websocket = null;
        this.reconnectAttempts = 0;
        this.isConnecting = false;
        
        this.init();
    }
    
    init() {
        console.log('TARNet Cliente Web iniciado');
        this.loadSettings();
    }
    
    // Configurações
    loadSettings() {
        const serverUrl = localStorage.getItem('tarnet_server_url');
        const reconnectInterval = localStorage.getItem('tarnet_reconnect_interval');
        
        if (serverUrl) {
            this.config.serverUrl = serverUrl;
            const input = document.getElementById('serverUrl');
            if (input) input.value = serverUrl;
        }
        
        if (reconnectInterval) {
            this.config.reconnectInterval = parseInt(reconnectInterval);
            const input = document.getElementById('reconnectInterval');
            if (input) input.value = reconnectInterval;
        }
    }
    
    saveSettings() {
        const serverUrl = document.getElementById('serverUrl')?.value;
        const reconnectInterval = document.getElementById('reconnectInterval')?.value;
        
        if (serverUrl) {
            this.config.serverUrl = serverUrl;
            localStorage.setItem('tarnet_server_url', serverUrl);
        }
        
        if (reconnectInterval) {
            this.config.reconnectInterval = parseInt(reconnectInterval);
            localStorage.setItem('tarnet_reconnect_interval', reconnectInterval);
        }
        
        this.showNotification('Configurações salvas com sucesso', 'success');
        
        // Fecha o modal
        const modal = bootstrap.Modal.getInstance(document.getElementById('settingsModal'));
        if (modal) modal.hide();
    }
    
    // WebSocket
    connect(onMessage = null, onOpen = null, onClose = null) {
        if (this.isConnecting || (this.websocket && this.websocket.readyState === WebSocket.OPEN)) {
            return Promise.resolve();
        }
        
        this.isConnecting = true;
        
        return new Promise((resolve, reject) => {
            try {
                this.websocket = new WebSocket(this.config.serverUrl);
                
                this.websocket.onopen = (event) => {
                    console.log('Conectado ao servidor TARNet');
                    this.reconnectAttempts = 0;
                    this.isConnecting = false;
                    this.updateConnectionStatus('connected', 'Conectado ao servidor');
                    
                    if (onOpen) onOpen(event);
                    resolve();
                };
                
                this.websocket.onmessage = (event) => {
                    try {
                        const data = JSON.parse(event.data);
                        if (onMessage) onMessage(data);
                    } catch (e) {
                        console.error('Erro ao processar mensagem:', e);
                    }
                };
                
                this.websocket.onclose = (event) => {
                    console.log('Conexão fechada:', event.code, event.reason);
                    this.isConnecting = false;
                    this.updateConnectionStatus('disconnected', 'Desconectado do servidor');
                    
                    if (onClose) onClose(event);
                    
                    // Tentativa de reconexão
                    if (this.reconnectAttempts < this.config.maxReconnectAttempts) {
                        this.scheduleReconnect(onMessage, onOpen, onClose);
                    }
                };
                
                this.websocket.onerror = (error) => {
                    console.error('Erro no WebSocket:', error);
                    this.isConnecting = false;
                    this.updateConnectionStatus('disconnected', 'Erro de conexão');
                    reject(error);
                };
                
            } catch (error) {
                console.error('Erro ao criar WebSocket:', error);
                this.isConnecting = false;
                reject(error);
            }
        });
    }
    
    scheduleReconnect(onMessage, onOpen, onClose) {
        this.reconnectAttempts++;
        const delay = Math.min(this.config.reconnectInterval * this.reconnectAttempts, 30000);
        
        this.updateConnectionStatus('connecting', 
            `Tentando reconectar... (${this.reconnectAttempts}/${this.config.maxReconnectAttempts})`);
        
        setTimeout(() => {
            this.connect(onMessage, onOpen, onClose);
        }, delay);
    }
    
    disconnect() {
        if (this.websocket) {
            this.websocket.close();
            this.websocket = null;
        }
        this.reconnectAttempts = this.config.maxReconnectAttempts; // Para parar reconexão
    }
    
    send(data) {
        if (this.websocket && this.websocket.readyState === WebSocket.OPEN) {
            this.websocket.send(JSON.stringify(data));
            return true;
        }
        return false;
    }
    
    // UI Updates
    updateConnectionStatus(status, message) {
        const statusElement = document.getElementById('connection-status');
        if (!statusElement) return;
        
        // Remove classes antigas
        statusElement.className = statusElement.className.replace(/alert-\w+/g, '');
        
        // Adiciona nova classe e ícone baseado no status
        let alertClass = 'alert-warning';
        let icon = 'fas fa-spinner fa-spin';
        
        switch (status) {
            case 'connected':
                alertClass = 'alert-success';
                icon = 'fas fa-check-circle';
                break;
            case 'disconnected':
                alertClass = 'alert-danger';
                icon = 'fas fa-times-circle';
                break;
            case 'connecting':
                alertClass = 'alert-warning';
                icon = 'fas fa-spinner fa-spin';
                break;
        }
        
        statusElement.className += ` ${alertClass}`;
        statusElement.innerHTML = `<i class="${icon}"></i> ${message}`;
    }
    
    showNotification(message, type = 'info') {
        const toastElement = document.getElementById('notification-toast');
        const messageElement = document.getElementById('toast-message');
        
        if (!toastElement || !messageElement) {
            console.log('Notification:', message);
            return;
        }
        
        messageElement.textContent = message;
        
        // Atualiza ícone baseado no tipo
        const iconElement = toastElement.querySelector('i');
        if (iconElement) {
            iconElement.className = `fas fa-${type === 'success' ? 'check-circle text-success' : 
                                             type === 'error' ? 'exclamation-circle text-danger' : 
                                             'info-circle text-primary'}`;
        }
        
        const toast = new bootstrap.Toast(toastElement);
        toast.show();
    }
    
    // Utilidades
    formatHostId(hostId) {
        return hostId.length > 16 ? hostId.substring(0, 16) + '...' : hostId;
    }
    
    formatTimestamp(timestamp) {
        return new Date(timestamp).toLocaleTimeString();
    }
    
    formatLatency(ms) {
        return ms < 1000 ? `${Math.round(ms)}ms` : `${(ms/1000).toFixed(1)}s`;
    }
}

// Funções globais para compatibilidade com templates
function saveSettings() {
    if (window.tarnetApp) {
        window.tarnetApp.saveSettings();
    }
}

function refreshHosts() {
    if (window.tarnetApp && window.tarnetApp.refreshHosts) {
        window.tarnetApp.refreshHosts();
    }
}

// Inicializa a aplicação quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', function() {
    window.tarnetApp = new TARNetApp();
});