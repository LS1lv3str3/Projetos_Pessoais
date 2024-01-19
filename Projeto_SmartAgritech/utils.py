import pandas as pd


#Função Quantidade precisa
def calcular_quantidade_precisa():
    # Leitura dos dados das folhas do Excel
    quantidades_df = pd.read_excel('Base_Dados_SmartAgritech.xlsx', sheet_name='Quantidades')

    # Solicitar a quantidade a ser produzida
    quantidade_produzida = int(input("Digite a quantidade a ser produzida: "))

    # Calcular a Quantidade_Necessaria
    quantidades_df['Quantidade_Precisa'] = quantidade_produzida * quantidades_df['Quantidade_Necessaria']
    

    # Exibir os resultados
    print("\nQuantidade Produzida:", quantidade_produzida)
    print("Quantidade Necessária:")
    print(quantidades_df[['Codigo', 'Quantidade_Precisa']])

    return quantidades_df, quantidade_produzida


#Função verificar Stock
def verificar_stock(quantidades_df):
    # Verificar se a coluna 'Quantidade_Stock' existe no DataFrame de quantidades
    if 'Quantidade_Stock' not in quantidades_df.columns:
        print("Erro: Coluna 'Quantidade_Stock' não encontrada no DataFrame de Quantidades.")
        return None

    # Verificar se a quantidade em estoque é suficiente
    quantidades_df['Com_Stock'] = quantidades_df['Quantidade_Precisa'] <= quantidades_df['Quantidade_Stock']

    # Exibir os resultados
    print("\nTabela Quantidades com Verificação de Stock:")
    print(quantidades_df[['Codigo', 'Quantidade_Produzida', 'Quantidade_Necessaria', 'Quantidade_Precisa', 'Com_Stock']])

    return quantidades_df['Com_Stock']



# Função para atualizar o stock
def atualizar_stock(materiais_df):
    try:
        # Ajuste: Adicionar a diferença (Quantidade_Stock + Quantidade_Comprada - Diferencial_Ordem) ao stock
        materiais_df['Quantidade_Stock'] = materiais_df.apply(lambda row: 
            (row['Quantidade_Stock'] + row['Quantidade_Comprada'] - row['Diferencial_Ordem'])
            if row['Quantidade_Stock'] < row['Quantidade_Requerida']
            else (row['Quantidade_Stock'] + row['Quantidade_Comprada']), axis=1)

        # Remover a coluna temporária Quantidade_Requerida, pois não é mais necessária na base de dados
        materiais_df = materiais_df.drop(columns=['Quantidade_Requerida'])
        
        # Remover a coluna temporária Quantidade_Comprada, pois não é mais necessária na base de dados
        materiais_df = materiais_df.drop(columns=['Quantidade_Comprada'])

        # Salvar as alterações no Excel
        materiais_df.to_excel('Base_Dados_SmartAgritech.xlsx', sheet_name='Materiais', index=False)
    except Exception as e:
        print(f"Erro ao atualizar stock: {e}")

# Função para Registar as Compras
def registrar_compras(materiais_df, materiais_sem_stock):
    try:
        # Filtrar apenas os materiais que precisam ser comprados
        materiais_compra_necessaria = materiais_df[materiais_sem_stock]

        for index, row in materiais_compra_necessaria.iterrows():
            # Solicitar quantidade comprada ao usuário
            quantidade_comprada = float(input(f"Digite a quantidade a ser comprada para {row['Descricao_Material']}: "))
            
            # Atualizar a quantidade comprada no DataFrame
            materiais_df.at[index, 'Quantidade_Comprada'] = quantidade_comprada
    
        return materiais_df
    except Exception as e:
        print(f"Erro ao registrar compras: {e}")
        return materiais_df


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
                    materiais_df.at[index, 'Quantidade_Requerida'] += quantidade_necessaria

        # Salvar as alterações no Excel
        materiais_df.to_excel('Base_Dados_SmartAgritech.xlsx', sheet_name='Materiais', index=False)
        return materiais_df
    except Exception as e:
        print(f"Erro ao confirmar opcionais: {e}")
        return materiais_df
