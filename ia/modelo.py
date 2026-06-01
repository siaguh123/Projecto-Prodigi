"""
Treino, serialização e carregamento do modelo RandomForest
"""
import os
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np
from sqlalchemy.orm import Session

from .features import extrair_dados_treino

# Caminho para guardar o modelo serializado
MODEL_PATH = os.path.join(os.path.dirname(__file__), "modelo.pkl")

def treinar_modelo(db: Session, force_retrain: bool = False):
    """
    Treina o modelo RandomForest com dados históricos da BD.
    
    Args:
        db: Sessão da base de dados
        force_retrain: Se True, força retreino mesmo se modelo existir
    
    Returns:
        tuple: (modelo_treinado, metricas)
    """
    # Verificar se modelo já existe e não queremos forçar
    if os.path.exists(MODEL_PATH) and not force_retrain:
        print("Modelo já existe. Use force_retrain=True para retreinar.")
        return carregar_modelo(), None
    
    # Extrair dados
    print("📊 A extrair dados históricos...")
    df = extrair_dados_treino(db)
    
    if len(df) < 10:
        print("⚠️ Dados insuficientes para treino (mínimo 10 registos).")
        return None, None
    
    print(f"✅ {len(df)} registos carregados.")
    
    # Features e target
    feature_cols = ["prioridade_minutos", "hora_entrada", "dia_semana"]
    X = df[feature_cols]
    y = df["tempo_espera"]
    
    # Divisão treino/teste
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Treinar modelo
    print("🧠 A treinar RandomForestRegressor...")
    modelo = RandomForestRegressor(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        n_jobs=-1
    )
    modelo.fit(X_train, y_train)
    
    # Avaliar
    y_pred = modelo.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = modelo.score(X_test, y_test)
    
    metricas = {
        "mae_minutos": round(mae, 2),
        "rmse_minutos": round(rmse, 2),
        "r2": round(r2, 3),
        "n_amostras": len(df)
    }
    
    print(f"✅ Modelo treinado!")
    print(f"   - MAE: {mae:.1f} minutos")
    print(f"   - RMSE: {rmse:.1f} minutos")
    print(f"   - R²: {r2:.3f}")
    
    # Salvar modelo
    salvar_modelo(modelo)
    
    return modelo, metricas

def salvar_modelo(modelo):
    """Serializa o modelo para disco"""
    joblib.dump(modelo, MODEL_PATH)
    print(f"💾 Modelo guardado em {MODEL_PATH}")

def carregar_modelo():
    """Carrega o modelo serializado do disco"""
    if not os.path.exists(MODEL_PATH):
        print("⚠️ Modelo não encontrado. Execute treino primeiro.")
        return None
    return joblib.load(MODEL_PATH)

def modelo_disponivel() -> bool:
    """Verifica se o modelo já foi treinado"""
    return os.path.exists(MODEL_PATH)

