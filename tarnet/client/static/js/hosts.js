// TARNet Cliente Web - Gerenciamento de Hosts

class HostsManager extends TARNetApp {
    constructor() {
        super();
        this.hosts = [];
        this.refreshInterval = null;
        this.connectToServer();
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
        console.log('Conectado - iniciando busca por hosts');
        this.requestHosts();
        
        // Atualiza lista de hosts a cada 5 segundos
        this.refreshInterval = setInterval(() => {
            this.requestHosts();
        }, 5000);
    }
    
    onDisconnected() {
        if (this.refreshInterval) {
            clearInterval(this.refreshInterval);
            this.refreshInterval = null;
        }
        this.hosts = [];
        this.renderHosts();
    }
    
    handleMessage(data) {
        switch (data.type) {
            case 'hosts_list':
                this.hosts = data.hosts || [];
                this.renderHosts();
                this.updateStats(data.server_stats);
                break;
                
            case 'error':
                console.error('Erro do servidor:', data.message);
                this.showNotification(`Erro: ${data.message}`, 'error');
                break;
                
            default:
                console.log('Mensagem não tratada:', data);
        }
    }
    
    requestHosts() {
        const success = this.send({
            type: 'get_hosts'
        });
        
        if (!success) {
            console.error('Falha ao solicitar hosts - WebSocket não conectado');
        }
    }
    
    renderHosts() {
        const container = document.getElementById('hosts-container');
        if (!container) return;
        
        if (this.hosts.length === 0) {
            container.innerHTML = `
                <div class="text-center py-5">
                    <i class="fas fa-desktop fa-3x text-muted"></i>
                    <p class="mt-3 text-muted">Nenhum host encontrado</p>
                    <p class="text-muted">Certifique-se de que o Host Agent esteja rodando</p>
                </div>
            `;
            return;
        }
        
        const hostsHtml = this.hosts.map(host => this.renderHostCard(host)).join('');
        container.innerHTML = `
            <div class="row">
                ${hostsHtml}
            </div>
        `;
    }
    
    renderHostCard(host) {
        const isOnline = host.last_frame && this.isRecentFrame(host.last_frame);
        const statusClass = isOnline ? 'online' : 'offline';
        const statusText = isOnline ? 'Online' : 'Offline';
        
        const connectedAt = new Date(host.connected_at).toLocaleString();
        const lastFrame = host.last_frame ? 
            new Date(host.last_frame).toLocaleString() : 'Nunca';
        
        return `
            <div class="col-md-6 col-lg-4 mb-3">
                <div class="card host-card fade-in" onclick="connectToHost('${host.host_id}')">
                    <div class="card-body">
                        <div class="d-flex justify-content-between align-items-start mb-2">
                            <h6 class="card-title mb-0">
                                <span class="host-status ${statusClass}"></span>
                                Host ${this.formatHostId(host.host_id)}
                            </h6>
                            <span class="badge bg-${isOnline ? 'success' : 'secondary'}">${statusText}</span>
                        </div>
                        
                        <div class="small text-muted mb-2">
                            <div><strong>Conectado:</strong> ${connectedAt}</div>
                            <div><strong>Último frame:</strong> ${lastFrame}</div>
                            <div><strong>Clientes:</strong> ${host.clients_connected || 0}</div>
                        </div>
                        
                        <div class="d-flex justify-content-between align-items-center">
                            <small class="text-muted font-monospace">${host.host_id}</small>
                            <button class="btn btn-primary btn-sm" onclick="event.stopPropagation(); connectToHost('${host.host_id}')">
                                <i class="fas fa-play"></i> Conectar
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }
    
    isRecentFrame(frameTimestamp) {
        const now = new Date();
        const frameTime = new Date(frameTimestamp);
        const diffSeconds = (now - frameTime) / 1000;
        return diffSeconds < 30; // Considera online se último frame foi há menos de 30s
    }
    
    updateStats(stats) {
        if (!stats) return;
        
        // Atualiza título da página com estatísticas
        document.title = `TARNet - ${stats.total_hosts} hosts, ${stats.total_clients} clientes`;
    }
    
    refreshHosts() {
        this.showNotification('Atualizando lista de hosts...', 'info');
        this.requestHosts();
    }
}

// Função global para conectar a um host
function connectToHost(hostId) {
    if (!hostId) {
        console.error('Host ID não fornecido');
        return;
    }
    
    console.log('Conectando ao host:', hostId);
    window.location.href = `/control/${hostId}`;
}

// Inicializa o gerenciador de hosts
document.addEventListener('DOMContentLoaded', function() {
    // Só inicializa se estivermos na página de hosts
    if (document.getElementById('hosts-container')) {
        window.hostsManager = new HostsManager();
        
        // Sobrescreve a instância global para usar o HostsManager
        window.tarnetApp = window.hostsManager;
    }
});