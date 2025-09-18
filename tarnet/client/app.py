from flask import Flask, render_template, request, jsonify
import uuid
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SESSION_SECRET', 'tarnet-dev-secret-key')

# Configuração para permitir conexões externas no Replit
app.config['HOST'] = '0.0.0.0'
app.config['PORT'] = 5000

@app.route('/')
def index():
    """Página principal do cliente web"""
    return render_template('index.html')

@app.route('/control/<host_id>')
def control_host(host_id):
    """Página de controle para um host específico"""
    client_id = str(uuid.uuid4())
    return render_template('control.html', host_id=host_id, client_id=client_id)

@app.route('/api/hosts')
def get_hosts():
    """API para obter lista de hosts (placeholder - será implementado via WebSocket)"""
    return jsonify({
        'hosts': [],
        'message': 'Use WebSocket para obter hosts em tempo real'
    })

@app.route('/health')
def health():
    """Endpoint de saúde da aplicação"""
    return jsonify({
        'status': 'healthy',
        'service': 'tarnet-client',
        'version': '1.0.0'
    })

if __name__ == '__main__':
    print("=== TARNet Cliente Web ===")
    print("Interface web para controle remoto")
    print(f"Acesse: http://localhost:{app.config['PORT']}")
    print()
    
    # Executa o servidor Flask
    app.run(
        host=app.config['HOST'],
        port=app.config['PORT'], 
        debug=True
    )