"""
Extração e preparação de features para o modelo de IA
"""
from sqlalchemy.orm import Session
from datetime import datetime
import pandas as pd
import models

# Mapeamento de prioridades Manchester para minutos base
PRIORIDADE_MINUTOS = {
    1: 0,    # Vermelho - Imediata
    2: 15,   # Laranja - Muito Urgente
    3: 30,   # Amarelo - Urgente
    4: 60,   # Verde - Pouco Urgente
    5: 120   # Azul - Não Urgente
}

def extrair_dados_treino(db: Session) -> pd.DataFrame:
    """
    Extrai dados históricos da BD para treino do modelo.
    
    Returns:
        DataFrame com colunas: prioridade, hora_entrada, dia_semana, tempo_espera
    """
    # Query: episódios encerrados com triagem associada
    resultados = db.query(
        models.Episodio.numepis,
        models.Episodio.datahorainicio,
        models.Episodio.datahorasaida,
        models.Triagem.idprioridade_cor
    ).join(
        models.Triagem, models.Episodio.numepis == models.Triagem.numepis
    ).filter(
        models.Episodio.datahorasaida.isnot(None)  # Apenas encerrados
    ).all()
    
    dados = []
    for r in resultados:
        if r.datahorasaida and r.datahorainicio:
            # Calcular tempo de espera em minutos
            tempo_espera = int((r.datahorasaida - r.datahorainicio).total_seconds() / 60)
            
            # Extrair features
            hora_entrada = r.datahorainicio.hour
            dia_semana = r.datahorainicio.weekday()  # 0=Segunda, 6=Domingo
            
            dados.append({
                "prioridade": r.idprioridade_cor,
                "prioridade_minutos": PRIORIDADE_MINUTOS.get(r.idprioridade_cor, 60),
                "hora_entrada": hora_entrada,
                "dia_semana": dia_semana,
                "tempo_espera": tempo_espera
            })
    
    return pd.DataFrame(dados)

def preparar_features_para_previsao(prioridade: int, hora: int, dia_semana: int) -> pd.DataFrame:
    """
    Prepara features para uma previsão em tempo real.
    
    Args:
        prioridade: 1-5 (Manchester)
        hora: 0-23
        dia_semana: 0-6
    
    Returns:
        DataFrame com uma linha para inferência
    """
    return pd.DataFrame([{
        "prioridade": prioridade,
        "prioridade_minutos": PRIORIDADE_MINUTOS.get(prioridade, 60),
        "hora_entrada": hora,
        "dia_semana": dia_semana
    }])
