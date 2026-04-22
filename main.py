from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn
import asyncio

# 1. Criar a aplicação
app = FastAPI(title="S.U.H. - Sistema de Urgências Hospitalares")

# 2. Rota que gera o Frontend (Integrado no Backend)
@app.get("/", response_class=HTMLResponse)
async def homepage():
    return """
    <html>
        <head>
            <title>PRODIGI 2026 - Urgências</title>
            <style>
                body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; display: flex; justify-content: center; align-items: center; height: 100vh; background-color: #eef2f3; }
                .card { background: white; padding: 40px; border-radius: 15px; box-shadow: 0 10px 25px rgba(0,0,0,0.1); text-align: center; border-top: 8px solid #d32f2f; }
                h1 { color: #2c3e50; margin-bottom: 10px; }
                p { color: #7f8c8d; font-size: 1.1em; }
                .badge { background: #27ae60; color: white; padding: 5px 15px; border-radius: 20px; font-size: 0.9em; }
            </style>
        </head>
        <body>
            <div class="card">
                <h1>🏥 Hospital PRODIGI</h1>
                <p>Sistema de Gestão de Urgências</p>
                <p><span class="badge">Backend + Frontend Online</span></p>
                <hr style="border: 0; border-top: 1px solid #eee; margin: 20px 0;">
                <p style="font-size: 0.8em;">Próxima Fase: Contentorização da Base de Dados</p>
            </div>
        </body>
    </html>
    """

# 3. Função de arranque compatível com Notebooks e Docker
def start():
    config = uvicorn.Config(app, host="0.0.0.0", port=8000, log_level="info")
    server = uvicorn.Server(config)
    
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # Se já houver um loop (Notebook/Colab), criamos uma tarefa
            print("Loop existente detetado. A iniciar como tarefa...")
            loop.create_task(server.serve())
        else:
            # No Docker ou PowerShell normal
            server.run()
    except RuntimeError:
        # Caso não exista loop de todo, criamos um e corremos
        asyncio.run(server.serve())

if __name__ == "__main__":
    start()
