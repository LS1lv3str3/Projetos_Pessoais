import pandas as pd
from utils import calcular_quantidade_precisa, verificar_stock

quantidades_df = calcular_quantidade_precisa()
# Executar a função verificar_stock com o DataFrame resultante da função anterior
verificar_stock(quantidades_df)