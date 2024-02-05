import pandas as pd

def calcular_quantidade_precisa():
    # Leitura dos dados da folha 'Quantidades' do Excel
    quantidades_df = pd.read_excel('Base_Dados_SmartAgritech.xlsx', sheet_name='Quantidades')

    # Solicitar a quantidade a ser produzida
    quantidade_produzida = int(input("Digite a quantidade a ser produzida: "))

    # Calcular a Quantidade_Necessaria
    quantidades_df['Quantidade_Precisa'] = quantidade_produzida * quantidades_df['Quantidade_Necessaria']
    

    # Exibir os resultados
    print("\nQuantidade Produzida:", quantidade_produzida)
    print("Quantidade Necessária:")
    print(quantidades_df[['Codigo', 'Descricao_Material', 'Quantidade_Precisa']])

    return quantidades_df, quantidade_produzida


# Função verificar Stock
def verificar_stock(quantidades_df):
    # Verificar se a quantidade em estoque é suficiente
    stock_check = quantidades_df['Quantidade_Stock'] >= quantidades_df['Quantidade_Necessaria']
    
    if stock_check.any():
        quantidades_df.loc[:, 'Quantidade_Stock_Updated'] = quantidades_df['Quantidade_Stock'] - quantidades_df['Quantidade_Precisa']
        resultados_df = quantidades_df[['Codigo', 'Descricao_Material', 'Quantidade_Necessaria', 'Quantidade_Precisa', 'Quantidade_Stock_Updated']]
        resultados_df.loc[:, 'Codigo'] = resultados_df['Codigo'].astype(int)
        print("\nTabela Quantidades com Verificação de Stock:")
        print(resultados_df)
    else:
        quantidades_df.loc[:, 'Quantidade_Stock_Updated'] = quantidades_df['Quantidade_Stock'] - quantidades_df['Quantidade_Precisa']  # Resultado negativo!!!!!
        resultados_df = quantidades_df[['Codigo', 'Descricao_Material', 'Quantidade_Necessaria', 'Quantidade_Precisa', 'Quantidade_Stock_Updated']]
        resultados_df.loc[:, 'Codigo'] = resultados_df['Codigo'].astype(int)
        print("\nTabela Quantidades com Verificação de Stock:")
        print(resultados_df)

    return resultados_df


def compras_temporario(quantidades_df):
    # Criar uma coluna temporária para lidar com a lógica de compras
    quantidades_df['Quantidade_Comprar_Temporario'] = 0

    # Criar máscara para identificar materiais com necessidade de compra (positivos e negativos)
    mask_positivos = quantidades_df['Quantidade_Stock_Updated'] >= 0
    mask_negativos = quantidades_df['Quantidade_Stock_Updated'] < 0

    # Lógica para materiais com Quantidade_Stock_Updated positiva
    quantidades_df.loc[mask_positivos, 'Quantidade_Comprar_Temporario'] = (quantidades_df['Quantidade_Stock'] - quantidades_df['Quantidade_Precisa']).astype(int)

    # Lógica para materiais com Quantidade_Stock_Updated negativa (necessidade de compra)
    quantidades_df.loc[mask_negativos, 'Quantidade_Comprar_Temporario'] = (quantidades_df['Quantidade_Stock_Updated']).astype(int)

    # Filtra apenas os materiais que precisam ser comprados
    materiais_comprar = quantidades_df.loc[quantidades_df['Quantidade_Comprar_Temporario'] < 0, ['Codigo', 'Descricao_Material', 'Quantidade_Comprar_Temporario']]

    # Exibe a lista de materiais que precisam ser comprados
    print("Materiais que precisam ser comprados:")
    print(materiais_comprar)

    # Registro das compras
    for index, row in materiais_comprar.iterrows():
        while True:
            try:
                quantidade_comprada = int(input(f"Digite a quantidade comprada para {row['Descricao_Material']} (Código {row['Codigo']}): "))
                
                # Validação da quantidade comprada
                if quantidade_comprada >= abs(row['Quantidade_Comprar_Temporario']):
                    break
                else:
                    print(f"A quantidade comprada deve ser maior ou igual a {abs(row['Quantidade_Comprar_Temporario'])}.")
            except ValueError:
                print("Quantidade inválida. Digite um número inteiro não negativo.")

        # Atualização do estoque após as compras
        quantidades_df.loc[index, 'Quantidade_Comprar_Temporario'] += quantidade_comprada

    # Print da atualização do estoque após todas as compras
    print("\nEstoque atualizado após as compras:")
    print(quantidades_df[['Codigo', 'Descricao_Material', 'Quantidade_Comprar_Temporario']])

    return quantidades_df

#Função responsavél pelo o tratamento de dados
def guardar_alteracoes_BD(quantidades_df):
    
    # Atualiza a coluna Quantidade_Stock com os valores de Quantidade_Comprar_Temporario
    quantidades_df['Quantidade_Stock'] = quantidades_df['Quantidade_Comprar_Temporario']
    
    # Apaga a coluna Quantidade_Precisa
    quantidades_df = quantidades_df.drop(columns=['Quantidade_Precisa', 'Quantidade_Stock_Updated', 'Quantidade_Comprar_Temporario' ])
    
        # Salva as alterações no Excel
    try:
        quantidades_df.to_excel('Base_Dados_SmartAgritech.xlsx', sheet_name='Quantidades', index=False)
        print("Alterações salvas com sucesso.")
    except Exception as e:
        print(f"Erro ao salvar as alterações: {e}")

    
    # Exibir DataFrame para visualização
    print("DataFrame após todas as alterações:")
    print(quantidades_df)



  