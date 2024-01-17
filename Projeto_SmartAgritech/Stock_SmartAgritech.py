import pandas as pd

# Função para realizar a verificação e atualização de stock
def verificar_atualizar_stock():
    # Leitura dos dados das folhas do Excel
    #materiais_df = pd.read_excel('Base_Dados_SmartAgritech.xlsx', sheet_name='Materiais')

    materiais_df = pd.read_excel('C:\Stotck_SmartAgritech\Base_Dados_SmartAgritech.xlsx', sheet_name='Materiais')

    # Solicitar a quantidade a ser produzida
    quantidade_produzida = int(input("Digite a quantidade a ser produzida: "))

    # Atualizar a coluna 'Quantidade_Requerida' na tabela de materiais
    materiais_df['Quantidade_Requerida'] = quantidade_produzida * materiais_df['Quantidade_Necessaria']

    # Verificação de stock e atualização
    materiais_sem_stock = verificar_stock(materiais_df)


    # Passo 2: Exibir materiais_sem_stock antes da compra
    #print("Materiais sem stock antes da compra:")
    #print(materiais_sem_stock)

    
    # Apresentar a lista de materiais sem stock
    if not materiais_sem_stock.empty:
        print("Materiais sem stock:")
        print(materiais_sem_stock)
             
        # Solicitar compras ao usuário
        registrar_compras(materiais_sem_stock)
    else:
        print("Todos os materiais têm stock suficiente.")


    # Passo 3: Exibir materiais_sem_stock após a compra
    #materiais_sem_stock_apos_compra = verificar_stock(materiais_df)
    #print("Materiais sem stock após a compra:")
    #print(materiais_sem_stock_apos_compra)

    # Solicitar confirmação do usuário para materiais opcionais
    confirmar_opcionais(materiais_df)

    # Atualizar stock
    atualizar_stock(materiais_df)

    # Passo 4: Exibir materiais_df após a atualização do estoque
    print("Materiais após a atualização do estoque:")
    print(materiais_df)

    print(f"Stock atualizado com sucesso para a produção de {quantidade_produzida} unidades.")


# Função para Verificar o stock
def verificar_stock(materiais_df):
    materiais_sem_stock = materiais_df[materiais_df['Quantidade_Stock'] < materiais_df['Quantidade_Requerida']]

    # Adiciona a coluna 'Diferencial_Ordem' com a diferença entre a Quantidade_Requerida e a Quantidade_Stock
    materiais_sem_stock['Diferencial_Ordem'] = materiais_sem_stock['Quantidade_Requerida'] - materiais_sem_stock['Quantidade_Stock']

    # Ajuste: Apenas incluir materiais que necessitam ser comprados (Diferencial_Ordem positivo)
    materiais_sem_stock = materiais_sem_stock[materiais_sem_stock['Diferencial_Ordem'] > 0]

    return materiais_sem_stock

# Função para confirmar materiais opcionais
def confirmar_opcionais(materiais_df):
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

# Função para atualizar o stock
def atualizar_stock(materiais_df):
    # Ajuste: Adicionar a diferença (Quantidade_Stock + Quantidade_Comprada - Diferencial_Ordem) ao stock
    materiais_df['Quantidade_Stock'] = materiais_df['Quantidade_Stock'] + materiais_df['Quantidade_Comprada'] - materiais_df['Diferencial_Ordem']
    
    # Zerar a Quantidade_Comprada após a atualização
    materiais_df['Quantidade_Comprada'] = 0

    # Preencher NaN em Quantidade_Stock com zero para facilitar os cálculos
    materiais_df['Quantidade_Stock'] = materiais_df['Quantidade_Stock'].fillna(0)

    # Salvar as alterações no Excel
    materiais_df.to_excel('Base_Dados_SmartAgritech.xlsx', sheet_name='Materiais', index=False)

    
# Função para Registar as Compras
def registrar_compras(materiais_df):
    for index, row in materiais_df.iterrows():
        quantidade_comprada = int(input(f"Quantidade comprada para {row['Descricao_Material']} (Código: {row['Codigo']}): "))
        materiais_df.at[index, 'Quantidade_Comprada'] = quantidade_comprada

    # Atualizar a base de dados
    materiais_df.to_excel('Base_Dados_SmartAgritech.xlsx', sheet_name='Materiais', index=False)

# Chamada da função principal
verificar_atualizar_stock()


'''
# Listar todas as folhas disponíveis no arquivo Excel
sheets = pd.read_excel('Base_Dados_SmartAgritech.xlsx', sheet_name=None)
print("Folhas disponíveis:", list(sheets.keys()))
'''
