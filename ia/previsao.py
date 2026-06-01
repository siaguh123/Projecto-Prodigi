"""
Funções de inferência em tempo real
"""
import pandas as pd
from .modelo import carregar_modelo, modelo_disponivel
from .features import preparar_features_para_previsao, PRIORIDADE_MINUTOS

def prever_tempo_espera(prioridade: int, hora: int, dia_semana: int) -> dict:
    """
    Prevê o tempo de espera estimado com base nos parâmetros.
    
    Args:
        prioridade: 1-5 (1=Imediata, 5=Não Urgente)
        hora: 0-23 (hora de entrada)
        dia_semana: 0-6 (0=Segunda, 6=Domingo)
    
    Returns:
        dict: {
            "tempo_estimado_minutos": int,
            "prioridade_base_minutos": int,
            "mensagem": str
        }
    """
    # Verificar se modelo existe
    if not modelo_disponivel():
        # Fallback: usar regra simples baseada na prioridade
        tempo_base = PRIORIDADE_MINUTOS.get(prioridade, 60)
        
        # Ajuste por hora (hora de ponta: 9-11h e 14-16h)
        ajuste_hora = 15 if 9 <= hora <= 11 or 14 <= hora <= 16 else 0
        
        tempo_estimado = tempo_base + ajuste_hora
        
        return {
            "tempo_estimado_minutos": tempo_estimado,
            "prioridade_base_minutos": tempo_base,
            "mensagem": "Estimativa baseada em regra simples (modelo em treino)"
        }
    
    # Carregar modelo
    modelo = carregar_modelo()
    if modelo is None:
        tempo_base = PRIORIDADE_MINUTOS.get(prioridade, 60)
        return {
            "tempo_estimado_minutos": tempo_base,
            "prioridade_base_minutos": tempo_base,
            "mensagem": "Modelo não disponível. Estimativa baseada apenas na prioridade.",
            "modelo_usado": "fallback"
        }
    
    # Preparar features
    df = preparar_features_para_previsao(prioridade, hora, dia_semana)
    feature_cols = ["prioridade_minutos", "hora_entrada", "dia_semana"]
    
    # Fazer previsão
    tempo_estimado = int(round(modelo.predict(df[feature_cols])[0]))
    tempo_estimado = max(0, tempo_estimado)
    
    tempo_base = PRIORIDADE_MINUTOS.get(prioridade, 60)
    
    return {
        "tempo_estimado_minutos": tempo_estimado,
        "prioridade_base_minutos": tempo_base,
        "mensagem": f"Tempo estimado: {tempo_estimado} minutos",
        "modelo_usado": "RandomForest"
    }
