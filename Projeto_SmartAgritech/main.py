import pandas as pd
import os
from utils import calcular_quantidade_precisa, verificar_stock, compras_temporario, guardar_alteracoes_BD
# Obtém o diretório do script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define o diretório de trabalho para o diretório do script
os.chdir(script_dir)

# Chame a função calcular_quantidasde_precisa para obter quantidades_df
quantidades_df, quantidade_produzida = calcular_quantidade_precisa()

# Chame a função verificar_stock passando quantidades_df como argumento
verificar_stock(quantidades_df)

#quantidades_df = compras_temporario(quantidades_df)

quantidades_df_atualizado = compras_temporario(quantidades_df)

guardar_alteracoes_BD(quantidades_df_atualizado)


