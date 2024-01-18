import os
import pandas as pd
from utils import verificar_stock, atualizar_stock, registrar_compras, confirmar_opcionais

# Função para realizar a verificação e atualização de stock
def verificar_atualizar_stock():
        
    # Obter o diretório do script (onde este script está localizado)
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Construir o caminho completo para o arquivo Excel
    excel_path = os.path.join(script_dir, 'Base_Dados_SmartAgritech.xlsx')
    
    # Leitura dos dados das folhas do Excel
    materiais_df = pd.read_excel(excel_path, sheet_name='Materiais')

    # Solicitar a quantidade a ser produzida
    quantidade_produzida = int(input("Digite a quantidade a ser produzida: "))

    # Atualizar a coluna 'Quantidade_Requerida' na tabela de materiais
    materiais_df['Quantidade_Requerida'] = quantidade_produzida * materiais_df['Quantidade_Necessaria']

    # Verificação de stock e atualização
    materiais_sem_stock = verificar_stock(materiais_df)

    
    # Apresentar a lista de materiais sem stock
    if not materiais_sem_stock.empty:
        print("Materiais sem stock:")
        print(materiais_sem_stock)
             
        # Solicitar compras ao usuário
        registrar_compras(materiais_sem_stock)
    else:
        print("Todos os materiais têm stock suficiente.")
    
    # Solicitar confirmação do usuário para materiais opcionais
    confirmar_opcionais(materiais_df)

    # Atualizar stock
    atualizar_stock(materiais_df)

    print(f"Stock atualizado com sucesso para a produção de {quantidade_produzida} unidades.")


# Chamada da função principal
verificar_atualizar_stock()

