import pandas as pd
import os

# Função para Verificar o stock
def verificar_stock(materiais_df):
    # Crie uma cópia do DataFrame para evitar SettingWithCopyWarning
    materiais_sem_stock = materiais_df.copy()

    # Adicionar a coluna 'Diferencial_Ordem' com a diferença entre a Quantidade_Requerida e a Quantidade_Stock
    materiais_sem_stock['Diferencial_Ordem'] = materiais_sem_stock['Quantidade_Stock'] - materiais_sem_stock['Quantidade_Requerida']

    # Adicionar a coluna 'Compra_Necessaria' que indica se é necessário comprar (True/False)
    materiais_sem_stock['Compra_Necessaria'] = materiais_sem_stock['Diferencial_Ordem'] < 0

    return materiais_sem_stock
    

# Função para atualizar o stock
def atualizar_stock(materiais_df):
    try:
        # Ajuste: Adicionar a diferença (Quantidade_Stock + Quantidade_Comprada - Diferencial_Ordem) ao stock
        materiais_df['Quantidade_Stock'] = materiais_df.apply(lambda row: 
            (row['Quantidade_Stock'] + row['Quantidade_Comprada'] - row['Diferencial_Ordem'])
            if row['Quantidade_Stock'] < row['Quantidade_Requerida']
            else (row['Quantidade_Stock'] + row['Quantidade_Comprada']), axis=1)

        # Zerar a Quantidade_Comprada após a atualização
        materiais_df['Quantidade_Comprada'] = 0

        # Preencher NaN em Quantidade_Stock com zero para facilitar os cálculos
        materiais_df['Quantidade_Stock'] = materiais_df['Quantidade_Stock'].fillna(0)

        # Salvar as alterações no Excel
        materiais_df.to_excel('Base_Dados_SmartAgritech.xlsx', sheet_name='Materiais', index=False)
    except Exception as e:
        print(f"Erro ao atualizar stock: {e}")

  
# Função para Registar as Compras
def registrar_compras(materiais_df):
    try:
        for index, row in materiais_df.iterrows():
            quantidade_comprada = int(input(f"Quantidade comprada para {row['Descricao_Material']} (Código: {row['Codigo']}): "))

            # Atualizar a Quantidade_Stock
            if row['Quantidade_Stock'] < row['Quantidade_Requerida']:
                # Se a quantidade em estoque for menor que a requerida, adicione a quantidade comprada ao estoque
                materiais_df.at[index, 'Quantidade_Stock'] += quantidade_comprada
            else:
                # Se a quantidade em estoque for suficiente, subtrai a quantidade requerida do estoque
                if row['Quantidade_Stock'] >= row['Quantidade_Requerida']:
                    materiais_df.at[index, 'Quantidade_Stock'] -= row['Quantidade_Requerida']
                else:
                    # Se a quantidade em estoque for menor que a requerida, adiciona a quantidade comprada ao estoque
                    materiais_df.at[index, 'Quantidade_Stock'] += quantidade_comprada
                    materiais_df.at[index, 'Quantidade_Comprada'] = quantidade_comprada

        # Salvar as alterações no Excel
        materiais_df.to_excel('Base_Dados_SmartAgritech.xlsx', sheet_name='Materiais', index=False)
    except Exception as e:
        print(f"Erro ao registrar compras: {e}")

    
# Função para confirmar materiais opcionais
def confirmar_opcionais(materiais_df):
    try:
        for index, row in materiais_df.iterrows():
            codigo_material = row['Codigo']
            quantidade_necessaria = row['Quantidade_Necessaria']
            opcional = row['Opcional']

            # Verificar se o material é opcional
            if opcional == 'Sim':
                confirmacao = input(f"Deseja incluir o material '{row['Descricao_Material']}' (Codigo: {codigo_material})? (S para Sim, qualquer outra tecla para não): ")

                # Se o usuário confirmar, atualizar a quantidade necessária
                if confirmacao.upper() == 'S':
                    materiais_df.loc[materiais_df['Codigo'] == codigo_material, 'Quantidade_Requerida'] += quantidade_necessaria

        # Salvar as alterações no Excel
        materiais_df.to_excel('Base_Dados_SmartAgritech.xlsx', sheet_name='Materiais', index=False)
    except Exception as e:
        print(f"Erro ao confirmar opcionais: {e}")
