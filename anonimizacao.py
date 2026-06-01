"""
Módulo de Anonimização de Dados (RGPD)
Exporta dados clínicos sem identificar os utentes
"""
from sqlalchemy.orm import Session
import models
import pandas as pd
from datetime import date
import json
import hashlib

def anonimizar_utente(utente) -> dict:
    """
    Transforma dados do utente removendo informação pessoal.
    
    - Remove: nome, apelido, localidade, telefone
    - Pseudonimiza: numutente → código aleatório
    - Generaliza: datanasc → faixa etária
    """
    # Calcular idade
    hoje = date.today()
    idade = hoje.year - utente.datanasc.year
    if hoje.month < utente.datanasc.month or (hoje.month == utente.datanasc.month and hoje.day < utente.datanasc.day):
        idade -= 1
    
    # Faixas etárias (anonimização por generalização)
    if idade < 18:
        faixa_etaria = "0-17"
    elif idade < 30:
        faixa_etaria = "18-29"
    elif idade < 45:
        faixa_etaria = "30-44"
    elif idade < 65:
        faixa_etaria = "45-64"
    else:
        faixa_etaria = "65+"
    
    # Pseudonimização do ID (hash simples)
    id_pseudonimizado = hashlib.md5(str(utente.numutente).encode()).hexdigest()[:8]
    
    return {
        "id_pseudonimizado": id_pseudonimizado,
        "faixa_etaria": faixa_etaria,
        "sexo": utente.sexo
    }

def exportar_dados_anonimizados(db: Session, formato: str = "json"):
    """
    Exporta todos os episódios com dados anonimizados.
    
    Args:
        db: Sessão da base de dados
        formato: "json" ou "csv"
    
    Returns:
        String com os dados no formato escolhido
    """
    # Query: episódios com utente e triagem
    resultados = db.query(
        models.Episodio.numepis,
        models.Episodio.datahorainicio,
        models.Episodio.datahorasaida,
        models.Episodio.idestadoatual,
        models.Triagem.idprioridade_cor,
        models.Triagem.sintomas,
        models.Utente.numutente,
        models.Utente.datanasc,
        models.Utente.sexo
    ).outerjoin(
        models.Triagem, models.Episodio.numepis == models.Triagem.numepis
    ).join(
        models.Utente, models.Episodio.numutente == models.Utente.numutente
    ).all()
    
    dados_anonimizados = []
    
    for r in resultados:
        # Criar objeto utente temporário para anonimização
        class UtenteTemp:
            pass
        utente_temp = UtenteTemp()
        utente_temp.numutente = r.numutente
        utente_temp.datanasc = r.datanasc
        utente_temp.sexo = r.sexo
        
        # Anonimizar utente
        utente_anon = anonimizar_utente(utente_temp)
        
        # Construir registo anonimizado
        registo = {
            "id_episodio": r.numepis,
            "id_utente_pseudonimizado": utente_anon["id_pseudonimizado"],
            "faixa_etaria": utente_anon["faixa_etaria"],
            "sexo": utente_anon["sexo"],
            "data_entrada": r.datahorainicio.isoformat() if r.datahorainicio else None,
            "data_saida": r.datahorasaida.isoformat() if r.datahorasaida else None,
            "estado": r.idestadoatual,
            "prioridade_manchester": r.idprioridade_cor,
            "sintomas": r.sintomas,
            "tempo_espera_minutos": None
        }
        
        # Calcular tempo de espera (se houver saída)
        if r.datahorasaida and r.datahorainicio:
            delta = r.datahorasaida - r.datahorainicio
            registo["tempo_espera_minutos"] = int(delta.total_seconds() / 60)
        
        dados_anonimizados.append(registo)
    
    # Exportar no formato solicitado
    if formato.lower() == "csv":
        df = pd.DataFrame(dados_anonimizados)
        return df.to_csv(index=False)
    else:
        return json.dumps(dados_anonimizados, indent=2, ensure_ascii=False)