"""
Módulo de Inteligência Artificial do SIAGUH
Previsão de tempos de espera em urgências hospitalares
"""

from .modelo import treinar_modelo, carregar_modelo, salvar_modelo, modelo_disponivel
from .previsao import prever_tempo_espera

__all__ = [
    "treinar_modelo",
    "carregar_modelo", 
    "salvar_modelo",
    "modelo_disponivel",
    "prever_tempo_espera"
]

