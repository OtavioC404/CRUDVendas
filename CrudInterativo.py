import requests
from tkinter import *
from tkinter.simpledialog import askstring, askfloat
import mysql.connector
from tkinter import ttk
import threading
import datetime

conexao = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = '1320',
    database = 'test',
    
)

cursor = conexao.cursor()

def limpar_mensagem():
    texto_addprod["text"] = ""
    texto_attprod["text"] = ""
    texto_delprod["text"] = ""

def atualizar_tabela():
    listar_produto()    

def adicionar_produto():
    nome_produto = askstring("Adicionar Produto", "Digite o nome do produto:")
    if nome_produto is not None:
        valor_str = askstring("Adicionar Produto", f"Digite o valor para {nome_produto}:")
        if valor_str is not None:
            
            valor_str = valor_str.replace(',', '.')

            try:
                # Tenta converter o valor para um número de ponto flutuante
                valor = float(valor_str)
                
                data_atual = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                print(data_atual)
                comando = comando = f'INSERT INTO vendas (nome_produto, valor, data_vendas) VALUES ("{nome_produto}", {valor}, "{data_atual}")'
                cursor.execute(comando)
                conexao.commit()

                texto_addprod["text"] = "Produto adicionado"
                threading.Thread(target=lambda: janela.after(5000, limpar_mensagem)).start()
            except ValueError:
                # Em caso de erro na conversão, exibe uma mensagem de erro
                texto_addprod["text"] = "Erro: Valor inválido"
                threading.Thread(target=lambda: janela.after(5000, limpar_mensagem)).start()
            
            
            texto_addprod["text"] = "Produto adicionado" #Mostra a mensagem apos o produto ter sido adicionado com sucesso
            threading.Thread(target=lambda: janela.after(5000, limpar_mensagem)).start() #Limpa a mensagem apos 5 segundos
            atualizar_tabela()
            
def listar_produto():
    comando = f'SELECT * FROM vendas'
    cursor.execute(comando)
    resultado = cursor.fetchall() #Ler o banco de dados
    # Limpa o Treeview antes de atualizar
    for item in tree.get_children():
        tree.delete(item)
    
    # Adiciona os dados ao Treeview
    for row in resultado:
        valor_formatado = "{:.2f}".format(row[2])  # Formata o valor com duas casas decimais
        data_formatada = datetime.datetime.strftime(row[3], '%d/%m/%Y %H:%M')
        tree.insert("", "end", values=(row[0], row[1], valor_formatado, data_formatada))

#Atualiza os produtos da lista
def atualizar_produto():
    nome_produto = askstring("Atualizar Produto", "Digite o novo nome do produto:")
    if nome_produto is not None:
        novo_valor_str = askstring("Atualizar Produto", f"Digite o novo valor para {nome_produto}:")

        if novo_valor_str is not None:
            novo_valor_str = novo_valor_str.replace(',', '.')

            try:
                novo_valor = float(novo_valor_str)

                id = askfloat("Atualizar Produto", f"Digite o ID do produto para {nome_produto}:")

                if id is not None:
                    comando = f'UPDATE vendas SET nome_produto = "{nome_produto}", valor = {novo_valor} WHERE idVendas = {id}'
                    cursor.execute(comando)
                    conexao.commit()

                    texto_attprod["text"] = "Produto atualizado"
                    threading.Thread(target=lambda: janela.after(5000, limpar_mensagem)).start()
                    atualizar_tabela()
            except ValueError:
                texto_attprod["text"] = "Erro: Valor inválido"
                threading.Thread(target=lambda: janela.after(5000, limpar_mensagem)).start()

      
#Deleta os produtos da lista
def deletar_produto():
    nome_produto = askstring("Deletar Produto", "Digite o nome do produto:")
    if nome_produto is not None:
        id = askfloat("Deletar Produto", f"Digite o id do produto para {nome_produto}:")
        if id is not None:
            comando = f'DELETE FROM vendas WHERE idVendas = {id}'
            cursor.execute(comando)
            conexao.commit()
            
            comando = 'SET @count = 0'
            cursor.execute(comando)
            comando = 'UPDATE vendas SET idVendas = @count := @count + 1'
            cursor.execute(comando)
            comando = 'ALTER TABLE vendas AUTO_INCREMENT = 1'
            cursor.execute(comando)
            conexao.commit()
            
            
            texto_attprod["text"] = "Produto excluido" 
            threading.Thread(target=lambda: janela.after(5000, limpar_mensagem)).start() 
            atualizar_tabela()
    
#Abre uma janela interativa    
janela = Tk()
janela.title("Tabela de Vendas")
janela.geometry("900x600")


#Adiciona texto de orientaçao na janela
texto_orientacao = Label(janela, text = "Escolha uma opção")
texto_orientacao.grid (column=0, row=0, padx=10, pady=10)

#Cria botao na janela
botao = Button(janela, text="Adicionar Produto", command=adicionar_produto)
botao.grid(column=0, row=1, padx=10, pady=10)
texto_addprod = Label(janela, text = "")
texto_addprod.grid (column=1, row=3)

botao = Button(janela, text="Consultar Produtos", command=listar_produto)
botao.grid(column=1, row=1, padx=10, pady=10)
texto_listprod = Label(janela, text = "")
texto_listprod.grid (column=1, row=4)

botao = Button(janela, text="Atualizar Produto", command=atualizar_produto)
botao.grid(column=0, row=2, padx=10, pady=10)
texto_attprod = Label(janela, text = "")
texto_attprod.grid (column=1, row=4)

botao = Button(janela, text="Deletar Produto", command=deletar_produto)
botao.grid(column=1, row=2, padx=10, pady=10)
texto_delprod = Label(janela, text = "")
texto_delprod.grid (column=1, row=5)

#Adiciona uma tabela de maneira mais organizada na janela
tree = ttk.Treeview(janela, columns=("ID", "Nome do Produto", "Valor", "Data"))
tree.grid(column=0, row=5, padx=10, pady=10, columnspan=3)
tree.heading("#1", text="ID")
tree.heading("#2", text="Nome do Produto")
tree.heading("#3", text="Valor")
tree.heading("#4", text="Data")



janela.mainloop()

cursor.close()
conexao.close()