from erro import SistemaError
from banco import BancoDeDados
import sqlite3
from rich import print
    
class InterfaceLoja:
    
    def __init__(self):
        self.banco = BancoDeDados()
        self.por_pagina = 35
        
    def __enter__(self):
        self.banco.__enter__()
        return self
        
    def __exit__(self, *args):
        self.banco.__exit__(*args)
    
    def _paginar(self, total: int, pagina: int) -> tuple[int,int]:
        if pagina <= 0:
            raise SistemaError(f'[red]ERRO! Valor abaixo das paginas![/]')
        total_paginas = (total + self.por_pagina - 1)// self.por_pagina
        if pagina > total_paginas:
            raise SistemaError('[red]ERRO! Valor acima das paginas![/]')
        offset = (pagina - 1) * self.por_pagina
        return total_paginas, offset
    
    def _ler_inteiro(self, text: str) -> int:
        while True:
            try:
                valor = int(input(text))
                return valor
            except ValueError:
                print('[red]ERRO! Formato de valor invalido![/]')
    
    
    def listar(self, termo: str, pagina: int = 1) -> None:
        match termo:
            case 'clientes':
                print('Clientes cadastrados')
                total = self.banco.contar_clientes()
                total_paginas, offset = self._paginar(total, pagina)
                clientes = self.banco.listar_clientes(self.por_pagina, offset)
                for cliente in clientes:
                    id_, nome = cliente
                    print(f'{id_} - {nome}')
                print(f'Clientes pagina: {pagina}/{total_paginas}')
            case 'jogos':
                print('Jogos cadastrados')
                total = self.banco.contar_jogos()
                total_paginas, offset = self._paginar(total, pagina)
                jogos = self.banco.listar_jogos(self.por_pagina, offset)
                for jogo in jogos:
                    id_, titulo, preco, qtd_estq = jogo
                    print(f'{id_} - {titulo} - {preco/100:.2f} [{qtd_estq} exemplares]')
                print(f'Jogos pagina: {pagina}/{total_paginas}')
    
    
    def menu_principal(self):
        lista = ['Cadastrar cliente', 'Cadastrar jogo', 'Realizar venda', 'Listar vendas', 'Consultar historico', 'Buscar cliente', 'Listar jogos', 'Sair']
        while True:
            print('\n === LOJA DE JOGOS ===')
            for c, i in enumerate(lista, 1):
                print(f'{c} - {i}')
            try:
                opcao = self._ler_inteiro('Opcao escolhida: ')
                match opcao:
                    case 1:
                        self.cadastrar_clientes()
                    case 2:
                        self.cadastrar_jogos()
                    case 3:
                        self.realizar_venda()
                    case 4:
                        self.listar_vendas()
                    case 5:
                        self.consultar_historico()
                    case 6:
                        self.busca_por_nome()
                    case 7:
                        self.listar_jogos_preco()
                    case 8:
                        print('Encerrando sistema...')
                        break
                    case _:
                        print('[red]ERRO! Essa opcao nao existe![/]')
            
            except NameError as erro:
                print(f'[red]ERRO! {erro}[/]')
        
    
    def cadastrar_clientes(self):
        print('\n === CADASTRAR CLIENTE ===')
        while True:
            try:
                nome = input('Nome do cliente: ').strip()
                if nome == '':
                    raise SistemaError('[red]ERRO! Nome invalido![/]')
                email = input('Gmail: ').strip()
                if email == '':
                    raise SistemaError('[red]ERRO! Gmail invalido![/]')
                self.banco.adicionar_cliente(nome, email)
                print('Cliente cadastrado com sucesso!')
                break
            except sqlite3.IntegrityError:
                print('[red]ERRO! email ja cadastrado![/]')
            except SistemaError as erro:
                print(f'{erro}')
        
    def cadastrar_jogos(self):
        print('\n === CADASTRAR JOGO ===')
        while True:
            try:
                titulo = input('Titulo do jogo: ').strip()
                if titulo == '':
                    raise SistemaError('[red]ERRO! Titulo de jogo invalido![/]')
                preco = int(float(input('Preco: R$')) * 100)
                break
            except ValueError:
                print('[red]ERRO! Formato de valor invalido![/]')
        while True:
            try:
                quantidade_estoque = int(input('Quantidade no estoque: '))
                self.banco.adicionar_jogo(titulo, preco, quantidade_estoque)
                print('Jogo cadastrado com sucesso!')
                return
            except ValueError:
                print('[red]ERRO! Formato de valor invalido![/]')
 
    
    def realizar_venda(self):
        print('\n === REALIZAR VENDA ===')
        while True:
            try:
                pag = self._ler_inteiro('Qual pagina do cliente? ')
                self.listar('clientes', pag)
                id_cliente = self._ler_inteiro('ID do cliente: ')
                cliente = self.banco.encontrar_cliente(id_cliente)
                if not cliente:
                    raise SistemaError('[red]ERRO! ID de cliente nao existe![/]')
                break
            except SistemaError as erro:
                print(f'{erro}')
        while True:
            try:
                pag = self._ler_inteiro('Qual pagina do jogo? ')
                self.listar('jogos', pag)
                id_jogo = self._ler_inteiro('ID do jogo que vai levar: ')
                jogo = self.banco.encontrar_jogo(id_jogo)
                if not jogo:
                    raise SistemaError('\n[red]ERRO! ID de jogo nao existe![/]')
                resultado = self.banco.transacao(id_cliente, id_jogo)
                data, qntd_atual = resultado
                print('Venda realizada com sucesso!')
                print(f'Cliente: {cliente[0]}')
                print(f'Jogo: {jogo[0]}')
                print(f'Valor: R${jogo[1]/100:.2f}')
                print(f'Data: {data}')
                print(f'Estoque restantes de {jogo[0]}: {qntd_atual} unidades')
                break
            except SistemaError as erro:
                print(f'{erro}')
        
    
    def listar_vendas(self):
        print('\n === VENDAS REALIZADAS ===')
        while True:
            try:
                while True:
                    pagina = self._ler_inteiro('Qual pagina das vendas? [0 para sair] ')
                    if pagina == 0:
                        break
                    total = self.banco.contar_vendas()
                    total_paginas, offset = self._paginar(total, pagina)
                    vendas = self.banco.listar_vendas(self.por_pagina, offset)
                    for venda in vendas:
                        id_, cliente_nome, jogo, preco_jogo, data_venda = venda
                        print(f'{id_}. {cliente_nome} comprou {jogo} - R${preco_jogo/100:.2f} - {data_venda}')
                    print(f'Vendas pagina: {pagina}/{total_paginas}')
                break
            except SistemaError as erro:
                print(f'{erro}')
        
    
    def consultar_historico(self):
        print('\n ===HISTORICO DE COMPRAS ===')
        while True:
            try:
                pag_cliente = self._ler_inteiro('Qual pagina do cliente? ')
                self.listar('clientes', pag_cliente)
                id_cliente = self._ler_inteiro('ID do cliente: ')
                cliente = self.banco.encontrar_cliente(id_cliente)
                if not cliente:
                    raise SistemaError('[red]ERRO! ID de cliente nao existe![/]')
                print(f'{cliente[0]} comprou:')
                pag_compras = 1
                while True:
                    total = self.banco.contar_vendas_por_id(id_cliente)
                    if total == 0:
                        print('Nao ha compras existentes.')
                        return
                    total_paginas, offset = self._paginar(total, pag_compras)
                    compras = self.banco.listar_compras(id_cliente, self.por_pagina, offset)
                    gasto_total = self.banco.gasto_total(id_cliente)
                    for compra in compras:
                        jogo, jogo_preco, data = compra
                        print(f' • {jogo} - R${jogo_preco/100:.2f} - {data}')
                    print(f'Pagina de compras do cliente: {pag_compras}/{total_paginas}')
                    print(f'Total gasto: R${gasto_total/100:.2f}')
                    pag_compras = self._ler_inteiro('Qual pagina quer ver? [0 para sair] ')
                    if pag_compras == 0:
                        break
                break
            except SistemaError as erro:
                print(f'{erro}')
    
    def busca_por_nome(self):
        print('\n === BUSCAR NOME CLIENTE ===')
        while True:
            try:
                termo = input('Nome para buscar: ')
                pag_cliente = 1
                while True:
                    total = self.banco.contar_clientes_por_nome(termo)
                    if total == 0:
                        print('Nome nao encontrado.')
                        return
                    total_paginas, offset = self._paginar(total, pag_cliente)
                    nomes_encontrados = self.banco.buscar_nome(termo, self.por_pagina, offset)
                    for nome_resultado in nomes_encontrados:
                        id_, nome = nome_resultado
                        print(f'{id_}. {nome}')
                    print(f'Nome de clientes: {pag_cliente}/{total_paginas}')
                    pag_cliente = self._ler_inteiro('Qual pagina quer ver? [0 para sair] ')
                    if pag_cliente == 0:
                        break
                break
            except SistemaError as erro:
                    print(f'{erro}')
                    
    def listar_jogos_preco(self):
        while True:
            try:
                pag = self._ler_inteiro('Qual pagina quer ver? [0 para sair] ')
                if pag == 0:
                    break
                total = self.banco.contar_jogos_por_preco()
                total_paginas, offset = self._paginar(total, pag)
                dados = self.banco.listar_jogos_acima_preco(self.por_pagina, offset)
                for dado in dados:
                    titulo, preco = dado
                    print(f'{titulo} - R${preco/100:.2f}')
                print(f'Preco de jogos acima da media: {pag}/{total_paginas}')
            except SistemaError as erro:
                print(f'{erro}')