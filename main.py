from tkinter import *
import random

class App:
    def __init__(self, master=None):
        # Define a cor que será usada
        self.preto = "#090909"
        master["background"] = self.preto
        # Carrega as imagens
        self.vazio = PhotoImage(file="assets/vazio.png")
        self.x = PhotoImage(file="assets/x.png")
        self.bola = PhotoImage(file="assets/bola.png")
        self.quit = PhotoImage(file="assets/quit.png")

        ## Tela inicial

        # Interface principal da página inicial
        self.inicio = Frame(master, pady=10, padx=30, background=self.preto)
        self.inicio.pack()
        self.inicio_titulo = Label(self.inicio, text="Jogo da velha", font=("Calibre", "16"), background=self.preto)
        self.inicio_titulo.pack()

        # Interface principal da leitura do nome do jogador1
        self.master_jogador1 = Frame(self.inicio, pady=5, background=self.preto)
        self.master_jogador1.pack()
        # Entrada do nome do primeiro jogador
        self.jogador1_entry_label = Label(self.master_jogador1, width=15, text="Jogador1(X)", background=self.preto)
        self.jogador1_entry_label.pack(side=LEFT)
        self.jogador1_entry = Entry(self.master_jogador1, width=20, background=self.preto)
        self.jogador1_entry.pack(side=RIGHT)

        # Interface principal da leitura do nome do jogador2
        self.master_jogador2 = Frame(self.inicio, pady=5, background=self.preto)
        self.master_jogador2.pack()
        # Entrada do nome do segundo jogador
        self.jogador2_entry_label = Label(self.master_jogador2, width=15, text="Jogador2(O)", background=self.preto)
        self.jogador2_entry_label.pack(side=LEFT)
        self.jogador2_entry = Entry(self.master_jogador2, width=20, background=self.preto)
        self.jogador2_entry.pack(side=RIGHT)

        # Botão para iniciar o jogo
        # O botão chama uma função para verificar os nomes
        self.iniciar_button = Button(self.inicio, text="Iniciar jogo", width=15, background=self.preto)
        self.iniciar_button["command"] = self.verifica_user
        self.iniciar_button.pack()
        # Caso o nome seja igual ou inexistente imprime um erro
        self.verificacao = Label(self.inicio, text="", pady=3, background=self.preto)
        self.verificacao.pack()

        ## Tela do jogo

        # Define os jogadores
        self.jogador1, self.jogador2 = self.jogador1_entry.get(), self.jogador2_entry.get()
        self.jogador_atual = "Apenas declara a variável"

        # Tela que recebe os 9 quadrados
        self.tela_de_fundo = Frame(master, background=self.preto)

        # Título que mostra quem começa
        # Durante a execução ele é alterado para mostrar o jogador atual
        self.tela_de_fundo_titulo = Label(master, text=f"{self.jogador_atual} começa", pady=6, background=self.preto)
        self.tela_de_fundo_titulo["font"] = ("Calibre", "12")

        # Botão para fechar o jogo
        self.quit_button = Button(master, width="30", image=self.quit, background=self.preto, highlightthickness = 0, bd=0)
        self.quit_button.bind("<Button-1>", lambda event, tela="sair": self.gerenciador(event, tela))

        # Matrizes auxiliares
        self.quadrados = [['W', 'e', 's'], ['l', 'l', 'e'], ['y', '4', '1']]
        self.jogo_map = [['vazio', 'vazio', 'vazio'], ['vazio', 'vazio', 'vazio'], ['vazio', 'vazio', 'vazio']]
        # Situação do jogo
        self.situacao_do_jogo, self.vencedor = self.fim_de_jogo(self.jogo_map)

        # Cria 9 quadrados(botoẽs) com a imagem "vazio.png"
        for linha in range(3):
            for coluna in range(3):
                # Quadrado 100x100 com background preto e imagem vazia
                self.quadrados[linha][coluna] = (Button(self.tela_de_fundo, image=self.vazio, background=self.preto))
                # Quando for clicado chama a função para trocar a imagem
                self.quadrados[linha][coluna].bind("<Button-1>", lambda 
                                                    event, linha=linha, coluna=coluna: 
                                                    self.quadrado_troca(event, linha, coluna))
                # Exibe na tela em uma matriz 3x3
                self.quadrados[linha][coluna].grid(row=linha, column=coluna)


    def gerenciador(self, event, tela):
        # A função remove/imprime telas
        if (tela == "iniciar jogo"):
            self.inicio.destroy()
            self.tela_de_fundo.pack(side=BOTTOM)
            self.tela_de_fundo_titulo["text"] = f"{self.jogador_atual} começa"
            self.tela_de_fundo_titulo.pack(side=TOP)
        elif (tela == "sair"):
            self.tela_de_fundo.quit()

    def quadrado_troca(self, event, linha, coluna):
        # Enquato houver espaços vazios ou alguém ganhar
        if (self.situacao_do_jogo == "continua"):
            # Se o quadrado escolhido estiver vazio:
            if (self.jogo_map[linha][coluna] == "vazio"):
                # Verifica quem é o jogador da vez para efetuar a jogada
                # informa a jogada na matriz auxiliar
                if (self.jogador_atual == self.jogador1):
                    self.quadrados[linha][coluna].config(image=self.x)
                    self.jogo_map[linha][coluna] = "x"
                    self.jogador_atual = self.troca_jogador(self.jogador_atual, self.jogador1, self.jogador2)
                else:
                    self.quadrados[linha][coluna].config(image=self.bola)
                    self.jogo_map[linha][coluna] = "bola"
                    self.jogador_atual = self.troca_jogador(self.jogador_atual, self.jogador1, self.jogador2)

            # Atualiza as informações do jogo
            self.situacao_do_jogo, self.vencedor = self.fim_de_jogo(self.jogo_map)
            # Caso alguém vença:
            if (self.situacao_do_jogo == "venceu"):
                self.tela_de_fundo_titulo["text"] = f"{self.jogador_atual} venceu!"
                self.quit_button.place(x=0, y=0)
            # Caso acabe os espaços disponíveis
            elif (self.situacao_do_jogo == "velha"):
                self.tela_de_fundo_titulo["text"] = "Fim de jogo! Deu velha"
                self.quit_button.place(x=0, y=0)
            # Ou simplesmente segue o jogo
            else:
                self.tela_de_fundo_titulo["text"] = (f"Vez de {self.jogador_atual}")

    def verifica_user(self):
        # Recebe os nomes lidos no menu principal
        self.jogador1, self.jogador2 = self.jogador1_entry.get(), self.jogador2_entry.get()
        # Define o jogador inicial de forma aleatória
        self.jogador_atual = random.choice([self.jogador1, self.jogador2])
        # Verifica se a combinação de nomes é válida
        # São recusados: Nomes iguais, nomes com mais de 16 caracteres ou campos de nome vazios.
        if (self.jogador1 == self.jogador2):
            self.verificacao["text"] = "Insira nomes diferentes para os jogadores"
        elif (self.jogador1 > "" and self.jogador2 > ""):
            if (len(self.jogador1) > 16 or len(self.jogador2) > 16):
                self.verificacao["text"] = "Insira nomes com até 16 caracterers"
            else:
                # Quando o nome for válido inicia o jogo pela função "gerenciador"
                self.gerenciador("<Button-1>", "iniciar jogo")
        else:
            self.verificacao["text"] = "Insira o nome dos jogadores"

    def fim_de_jogo(self, jogo_map):
        # Possibilidades de vitória
        self.diagonal1 = [jogo_map[0][0], jogo_map[1][1], jogo_map[2][2]]
        self.diagonal2 = [jogo_map[0][2], jogo_map[1][1], jogo_map[2][0]]
        self.sequencia_x = ["x", "x", "x"]
        self.sequencia_bola = ["bola", "bola", "bola"]

        # Verifica vitória na horizontal
        for linha in range(3):
            if (self.jogo_map[linha] == self.sequencia_x or self.jogo_map[linha] == self.sequencia_bola):
                self.jogador_atual = self.troca_jogador(self.jogador_atual, self.jogador1, self.jogador2)
                return "venceu", self.jogador_atual

        # Verifica vitória na diagonal
        if (self.diagonal1 == self.sequencia_x or self.diagonal1 == self.sequencia_bola):
            self.jogador_atual = self.troca_jogador(self.jogador_atual, self.jogador1, self.jogador2)
            return "venceu", self.jogador_atual
        elif (self.diagonal2 == self.sequencia_x or self.diagonal2 == self.sequencia_bola):
            self.jogador_atual = self.troca_jogador(self.jogador_atual, self.jogador1, self.jogador2)
            return "venceu", self.jogador_atual

        # Verifica vitória na vertical
        else:
            for linha in range(3):
                self.coluna_atual = []
                for coluna in range(3):
                    self.coluna_atual.append(self.jogo_map[coluna][linha])
                if (self.coluna_atual == self.sequencia_x or self.coluna_atual == self.sequencia_bola):
                    self.jogador_atual = self.troca_jogador(self.jogador_atual, self.jogador1, self.jogador2)
                    return "venceu", self.jogador_atual

            # Verifica continuidade do jogo ou VELHA
            if (("vazio" not in self.jogo_map[0]) and ("vazio" not in self.jogo_map[1]) and ("vazio" not in self.jogo_map[2])):
                return "velha", None

        # Ou simplesmente segue o jogo
        return "continua", None

    def troca_jogador(self, jogador_atual, jogador1, jogador2):
        # Verifica o jogador atual e o troca
        if (jogador_atual == jogador1):
            return jogador2
        else:
            return jogador1

def iniciar_jogo():
    # Função para iniciar a interface
    jogo = Tk()
    App(jogo)
    jogo.title("Jogo da velha")
    jogo.mainloop()

if (__name__ == "__main__"):
    iniciar_jogo()
