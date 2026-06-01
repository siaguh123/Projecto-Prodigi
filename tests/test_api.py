"""
Testes básicos à API do SIAGUH
Cobre: autenticação, endpoints principais e validação de inputs
"""
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# =====================================================================
# FIXTURES — credenciais de teste
# =====================================================================

def obter_token(username, password):
    resp = client.post("/auth/login", json={"username": username, "password": password})
    return resp.json().get("access_token")

@pytest.fixture
def token_medico():
    return obter_token("dr.silva", "medico123")

@pytest.fixture
def token_enfermeiro():
    return obter_token("enf.ana", "enfermeiro123")

@pytest.fixture
def token_admin():
    return obter_token("admin", "admin123")

@pytest.fixture
def headers_medico(token_medico):
    return {"Authorization": f"Bearer {token_medico}"}

@pytest.fixture
def headers_enfermeiro(token_enfermeiro):
    return {"Authorization": f"Bearer {token_enfermeiro}"}

@pytest.fixture
def headers_admin(token_admin):
    return {"Authorization": f"Bearer {token_admin}"}

# =====================================================================
# 1. TESTES DE AUTENTICAÇÃO
# =====================================================================

def test_homepage():
    resp = client.get("/")
    assert resp.status_code == 200

def test_login_valido_medico():
    resp = client.post("/auth/login", json={"username": "dr.silva", "password": "medico123"})
    assert resp.status_code == 200
    dados = resp.json()
    assert "access_token" in dados
    assert dados["idperfil"] == 1
    assert dados["username"] == "dr.silva"

def test_login_valido_enfermeiro():
    resp = client.post("/auth/login", json={"username": "enf.ana", "password": "enfermeiro123"})
    assert resp.status_code == 200
    assert resp.json()["idperfil"] == 2

def test_login_password_errada():
    resp = client.post("/auth/login", json={"username": "dr.silva", "password": "errada"})
    assert resp.status_code == 401

def test_login_utilizador_inexistente():
    resp = client.post("/auth/login", json={"username": "naoexiste", "password": "qualquer"})
    assert resp.status_code == 401

def test_endpoint_protegido_sem_token():
    resp = client.get("/utentes/")
    assert resp.status_code == 401

def test_utilizador_autenticado(headers_medico):
    resp = client.get("/auth/me", headers=headers_medico)
    assert resp.status_code == 200
    assert resp.json()["username"] == "dr.silva"

# =====================================================================
# 2. TESTES DE UTENTES
# =====================================================================

def test_listar_utentes_autenticado(headers_medico):
    resp = client.get("/utentes/", headers=headers_medico)
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)

def test_criar_utente_sem_permissao(headers_enfermeiro):
    utente = {"numutente": 999991, "nome": "Teste", "apelido": "Silva",
              "localidade": "Lisboa", "sexo": "M", "datanasc": "1990-01-01"}
    resp = client.post("/utentes/", json=utente, headers=headers_enfermeiro)
    assert resp.status_code == 403

def test_utente_nao_encontrado(headers_medico):
    resp = client.get("/utentes/999999", headers=headers_medico)
    assert resp.status_code == 404

# =====================================================================
# 3. TESTES DE EPISÓDIOS
# =====================================================================

def test_listar_episodios_autenticado(headers_medico):
    resp = client.get("/episodios/", headers=headers_medico)
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)

def test_episodio_nao_encontrado(headers_medico):
    resp = client.get("/episodios/999999", headers=headers_medico)
    assert resp.status_code == 404

# =====================================================================
# 4. TESTES DE TRIAGEM
# =====================================================================

def test_listar_triagens_autenticado(headers_enfermeiro):
    resp = client.get("/triagens/", headers=headers_enfermeiro)
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)

def test_criar_triagem_sem_permissao_medico(headers_medico):
    triagem = {"numepis": 1, "enfnumfunc": 1, "idprioridade_cor": 3,
               "sintomas": "Dor de cabeça"}
    resp = client.post("/triagens/", json=triagem, headers=headers_medico)
    assert resp.status_code == 403

# =====================================================================
# 5. TESTES DE ATOS MÉDICOS
# =====================================================================

def test_listar_atos_autenticado(headers_medico):
    resp = client.get("/atos/", headers=headers_medico)
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)

def test_criar_ato_sem_permissao_enfermeiro(headers_enfermeiro):
    from datetime import datetime
    ato = {"numepis": 1, "mednumfunc": 1, "idtipoato": 1,
           "datahorainic": datetime.now().isoformat()}
    resp = client.post("/atos/", json=ato, headers=headers_enfermeiro)
    assert resp.status_code == 403

# =====================================================================
# 6. TESTES DE PRESCRIÇÕES
# =====================================================================

def test_listar_prescricoes_autenticado(headers_medico):
    resp = client.get("/prescricoes/", headers=headers_medico)
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)

def test_criar_prescricao_sem_permissao_enfermeiro(headers_enfermeiro):
    prescricao = {"numepis": 1, "mednumfunc": 1, "medicamento": "Paracetamol",
                  "dosagem": "500mg", "frequencia": "3x/dia"}
    resp = client.post("/prescricoes/", json=prescricao, headers=headers_enfermeiro)
    assert resp.status_code == 403

# =====================================================================
# 7. TESTES DE IA
# =====================================================================

def test_ia_status():
    resp = client.get("/ia/status")
    assert resp.status_code == 200
    assert "modelo_disponivel" in resp.json()

def test_ia_previsao_valida(headers_medico):
    resp = client.get("/ia/tempo-espera?prioridade=3&hora=10&dia_semana=1",
                      headers=headers_medico)
    assert resp.status_code == 200
    assert "tempo_estimado_minutos" in resp.json()

def test_ia_previsao_prioridade_invalida(headers_medico):
    resp = client.get("/ia/tempo-espera?prioridade=99&hora=10&dia_semana=1",
                      headers=headers_medico)
    assert resp.status_code == 400

def test_ia_previsao_hora_invalida(headers_medico):
    resp = client.get("/ia/tempo-espera?prioridade=3&hora=25&dia_semana=1",
                      headers=headers_medico)
    assert resp.status_code == 400

# =====================================================================
# 8. TESTES DE EXPORTAÇÃO
# =====================================================================

def test_exportar_json_autenticado(headers_admin):
    resp = client.get("/exportar/anonimizado?formato=json", headers=headers_admin)
    assert resp.status_code == 200

def test_exportar_csv_autenticado(headers_admin):
    resp = client.get("/exportar/anonimizado?formato=csv", headers=headers_admin)
    assert resp.status_code == 200
    assert "text/csv" in resp.headers.get("content-type", "")

def test_exportar_sem_autenticacao():
    resp = client.get("/exportar/anonimizado")
    assert resp.status_code == 401
