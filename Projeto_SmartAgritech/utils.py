import pandas as pd


#Função Quantidade precisa
def calcular_quantidade_precisa():
    # Leitura dos dados das folhas do Excel
    quantidades_df = pd.read_excel('Base_Dados_SmartAgritech.xlsx', sheet_name='Quantidades')
    materiais_df = pd.read_excel('Base_Dados_SmartAgritech.xlsx', sheet_name='Materiais')

    # Solicitar a quantidade a ser produzida
    quantidade_produzida = int(input("Digite a quantidade a ser produzida: "))

    # Calcular a Quantidade_Necessaria
    quantidades_df['Quantidade_Precisa'] = quantidade_produzida * quantidades_df['Quantidade_Necessaria']
    
    # Adiciona a descrição de cada código da sheet 'Materiais'
    quantidades_df = pd.merge(quantidades_df, materiais_df[['Codigo', 'Descricao_Material']], on='Codigo')

    # Exibir os resultados
    print("\nQuantidade Produzida:", quantidade_produzida)
    print("Quantidade Necessária:")
    print(quantidades_df[['Codigo', 'Descricao_Material', 'Quantidade_Precisa']])

    return quantidades_df, quantidade_produzida


#Função verificar Stock
def verificar_stock(quantidades_df):
    
    # Verificar se a quantidade em estoque é suficiente
    quantidades_df['Materiais_Com_Stock'] = quantidades_df['Quantidade_Stock'] >= quantidades_df['Quantidade_Necessaria']
        
      
    if quantidades_df['Materiais_Com_Stock'].any():
        quantidades_df['Quantidade_Stock_Updated'] = quantidades_df['Quantidade_Stock'] - quantidades_df['Quantidade_Precisa']
        resultados_df = quantidades_df[['Codigo', 'Descricao_Material', 'Quantidade_Necessaria', 'Quantidade_Precisa', 'Materiais_Com_Stock', 'Quantidade_Stock_Updated' ]]
        resultados_df['Codigo'] = resultados_df['Codigo'].astype(int)
        print("\nTabela Quantidades com Verificação de Stock:")
        print(resultados_df)
    
    else:
        quantidades_df['Quantidade_Stock_Updated'] = quantidades_df['Quantidade_Stock'] - quantidades_df['Quantidade_Precisa'] #Resultado negativo!!!!!
        resultados_df = quantidades_df[['Codigo', 'Descricao_Material', 'Quantidade_Necessaria', 'Quantidade_Precisa', 'Materiais_Com_Stock', 'Quantidade_Stock_Updated' ]]
        resultados_df['Codigo'] = resultados_df['Codigo'].astype(int)
        print("\nTabela Quantidades com Verificação de Stock:")
        print(resultados_df)

    return resultados_df


# Função para Registar as Compras
def registrar_compras(quantidades_df):
    materiais_sem_stock = quantidades_df[quantidades_df['Quantidade_Stock_Updated'] < 0]
    
    # Verificar se há materiais com estoque negativo
    if not materiais_sem_stock.empty:
        
        # Exibir os materiais com estoque negativo
        print("\nMateriais a necessitar de compra:\n")
        materiais_sem_stock['Codigo'] = materiais_sem_stock['Codigo'].astype(int)
        print(materiais_sem_stock[['Codigo', 'Descricao_Material', 'Quantidade_Stock_Updated']])
        
        for index, row in materiais_sem_stock.iterrows():
            
            if row['Quantidade_Stock'] < row['Quantidade_Necessaria']:        
                quantidade_comprada = int(input(f"Digite a quantidade comprada para {row['Descricao_Material']} (Código {row['Codigo']}): "))

                print(quantidade_comprada)


    
    



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
