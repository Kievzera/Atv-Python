import pandas as pd
import csv
import json
import os


# Arquivos para persistência
ARQUIVO_PRODUTOS = "produtos.json"
ARQUIVO_VENDAS = "vendas.csv"

# Carregar produtos de um JSON
def carregar_produtos():
    if os.path.exists(ARQUIVO_PRODUTOS):
        with open(ARQUIVO_PRODUTOS, "r") as file:
            return json.load(file)
    else:
        # produtos iniciais
        return {
            "001": {"nome": "Camisa", "quantidade": 10, "preco": 50.00},
            "002": {"nome": "Calça", "quantidade": 15, "preco": 80.00},
            "003": {"nome": "Tênis", "quantidade": 5, "preco": 120.00},
        }

# Salvar produtos em um arquivo.JSON
def salvar_produtos():
    with open(ARQUIVO_PRODUTOS, "w") as file:
        json.dump(produtos, file)

# Carregar vendas de um arquivo.CSV
def carregar_vendas():
    if os.path.exists(ARQUIVO_VENDAS):
        return pd.read_csv(ARQUIVO_VENDAS, sep=";", encoding="utf-8").to_dict(orient="records")
    return []

# Salvar vendas em um arquivo.CSV
def salvar_vendas():
    df_vendas = pd.DataFrame(vendas)
    df_vendas.to_csv(ARQUIVO_VENDAS, index=False, sep=";", encoding="utf-8")

# Funções auxiliares de validação
def validar_inteiro(mensagem):
    while True:
        try:
            valor = int(input(mensagem))
            return valor
        except ValueError:
            print("Entrada inválida. Digite um número inteiro.")

def validar_float(mensagem):
    while True:
        try:
            valor = float(input(mensagem))
            return valor
        except ValueError:
            print("Entrada inválida. Digite um número decimal.")

# Aqui cadastra o produto
def cadastrar_produto():
    codigo = input("Digite o código do produto: ")
    nome = input("Digite o nome do produto: ")
    quantidade = validar_inteiro("Digite a quantidade em estoque: ")
    preco = validar_float("Digite o preço por unidade: ")
    
    if codigo not in produtos:
        produtos[codigo] = {"nome": nome, "quantidade": quantidade, "preco": preco}
        salvar_produtos()  # Salva o estado atualizado dos produtos
        print(f"Produto {nome} cadastrado com sucesso!")
    else:
        print("Código já cadastrado!")

# registrar a venda
def registrar_venda():
    codigo = input("Digite o código do produto: ")
    if codigo in produtos:
        quantidade_venda = validar_inteiro("Digite a quantidade a ser vendida: ")
        if quantidade_venda <= produtos[codigo]["quantidade"]:
            produtos[codigo]["quantidade"] -= quantidade_venda
            valor_total = quantidade_venda * produtos[codigo]["preco"]
            vendas.append({
                "codigo": codigo,
                "nome": produtos[codigo]["nome"],
                "quantidade": quantidade_venda,
                "valor_total": valor_total
            })
            salvar_produtos()  
            salvar_vendas()    
            print(f"Venda registrada! Valor total: R${valor_total:.2f}")
        else:
            print("Quantidade insuficiente em estoque.")
    else:
        print("Produto não encontrado.")

# Gera o relatório de vendas
def gerar_relatorio_vendas():
    if vendas:
        df_vendas = pd.DataFrame(vendas)
        df_vendas.to_csv("relatorio_vendas.csv", index=False, sep=";", encoding="utf-8")
        print("Relatório de vendas gerado: relatorio_vendas.csv")
    else:
        print("Nenhuma venda registrada.")

# Gera o de estoque
def gerar_relatorio_estoque():
    with open("relatorio_estoque.txt", "w") as file:
        file.write("Código\tNome\tQuantidade em Estoque\n")
        for codigo, info in produtos.items():
            file.write(f"{codigo}\t{info['nome']}\t{info['quantidade']}\n")
    print("Relatório de estoque gerado: relatorio_estoque.txt")

# Menu principal
def menu():
    while True:
        print("\nMenu do Sistema de Vendas:")
        print("1. Cadastrar Produto")
        print("2. Registrar Venda")
        print("3. Gerar Relatório de Vendas")
        print("4. Gerar Relatório de Estoque")
        print("5. Sair")
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            cadastrar_produto()
        elif opcao == "2":
            registrar_venda()
        elif opcao == "3":
            gerar_relatorio_vendas()
        elif opcao == "4":
            gerar_relatorio_estoque()
        elif opcao == "5":
            print("Encerrando o sistema.")
            break
        else:
            print("Opção inválida, tente novamente.")


produtos = carregar_produtos()
vendas = carregar_vendas()

# Inicia o menu
if __name__ == "__main__":
    menu()
