import pandas as pd
import os
from utils import calcular_quantidade_precisa, verificar_stock, registrar_compras

# Obtém o diretório do script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define o diretório de trabalho para o diretório do script
os.chdir(script_dir)

# Chame a função calcular_quantidade_precisa para obter quantidades_df
quantidades_df, quantidade_produzida = calcular_quantidade_precisa()

# Chame a função verificar_stock passando quantidades_df como argumento
verificar_stock(quantidades_df)

# Exemplo de chamada da função
registrar_compras(quantidades_df)

'''
é preciso verificar o erro de copy e pensar como adicionar as quantidades comprasdas à quantidade existente
'''