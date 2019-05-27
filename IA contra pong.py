#importação das bibliotecas
import pygame
import random
from pybrain3.supervised.trainers import BackpropTrainer
from pybrain3.datasets.supervised import SupervisedDataSet
from pybrain3.tools.shortcuts import buildNetwork

#Criação da classe que faz a criação da Rede Neural.
class IA:
    #Cria uma rede com 2 entradas, 7 neuronios na camada oculta e 1 saida
    rede = buildNetwork (2,7, 1)

    #Crio uma "base" de dados onde coloco possiveis resultados corretos para comparação
    base = SupervisedDataSet(2, 1)
    #Adiciona exemplos a essa base de dados
    base.addSample((1, 0),(0, ))
    base.addSample((50,343),(1, ))
    base.addSample((77,344),(1, ))
    base.addSample((894,344),(0, ))
    #Crio um objeto que contem o resultado do treinamento feito com base nos exemplos
    treinamento = BackpropTrainer(rede, dataset = base , learningrate = 0.01 ,
                                    momentum = 0.01)

#treino 5 gerações iniciais
for i in range(1, 5):
    #mostro o diferencial do erro obtido
    erro = IA.treinamento.train()
    print("erro : %s" %erro)

#_________________________________________________________________#

#Cores usadas no jogo
PRETO = 0,0,0
BRANCO = 255,255,255
VERDE = 0,255,0
VERMELHO= 255,0,0
#Criação dos objetos que contem a tela
tamanho=800,600
tela=pygame.display.set_mode(tamanho)
tela_retangulo = tela.get_rect()
tempo = pygame.time.Clock()
pygame.display.set_caption("pong zinho")

#classe contendo informações da raquete
class Raquete:
    #inicializa as variaveis da raquete
    def __init__(self, tamanho):
        self.imagem = pygame.Surface(tamanho)
        self.imagem.fill(VERDE)
        self.imagem_retangulo=self.imagem.get_rect()
        self.velocidade = 16
        self.imagem_retangulo[0] = 2
        self.imagem_retangulo[1] = 50

    #Atualiza as informações da raquete na tela
    def realiza(self):
        tela.blit(self.imagem,self.imagem_retangulo)

    #define o movimento da raquete e adiciona a velocidade
    def move(self ,x ,y):
        self.imagem_retangulo[0] += x * self.velocidade
        self.imagem_retangulo[1] += y * self.velocidade

    #objetos de movimentação
    def cima(self):
        self.move(0, -1)

    def baixo(self):
        self.move(0, 1)

    #Atualiza o retangulo na tela e ler a ação do teclado
    def atualiza(self , tecla):
       # IA.rede.activate([bola.imagem_retangulo[1], raquete.imagem_retanguloy[1]])

        if tecla[pygame.K_UP]:
            raquete.cima()

        if tecla[pygame.K_DOWN]:
            raquete.baixo()

        self.imagem_retangulo.clamp_ip(tela_retangulo)

#Classe que contem informações da bola
class Bola :
    #Define variaveis da bola
    def __init__(self, tamanho):
        self.altura, self.largura = tamanho
        self.imagem = pygame.Surface(tamanho)
        self.imagem.fill(VERMELHO)
        self.imagem_retangulo=self.imagem.get_rect()
        self.velocidade = 15
        self.set_bola()

    #Define um local de surgimento aleatorio para a bola
    def aleatorio(self):
        while True:
            num=random.uniform(-1.0,1.0)
            if num > -0.5 and num< 0.5:
                continue
            else:
                return num
    #Define o surgimento da bola e o movimento
    def set_bola(self):
        x= self.aleatorio()
        y= self.aleatorio()
        self.imagem_retangulo.x = tela_retangulo.centerx
        self.imagem_retangulo.y = tela_retangulo.centery
        self.velo=[x, y]
        self.pos = list(tela_retangulo.center)

    #Cria o evento que le quando a bola colide com a parede e faz o somatorio dos pontos
    #e treinamendo de novas geraçoes
    def colide_parede(self):
        gen =0
        if self.imagem_retangulo.y < 0 or self.imagem_retangulo.y > tela_retangulo.bottom - self.altura:
            self.velo[1] *= -1

        if self.imagem_retangulo.x < 0 or self.imagem_retangulo.x > tela_retangulo.right - self.largura:
            self.velo[0] *= -1
            if self.imagem_retangulo.x < 0:
                placar.pontos -= 1
                if placar.pontos <= 0:
                    IA.treinamento.train()
                    if raquete.imagem_retangulo[1] >= bola.pos[1]:
                        print("1/1 =1")
                        IA.base.addSample((raquete.imagem_retangulo[1], bola.pos[1]),(1, ))
                    elif raquete.imagem_retangulo[1] < bola.pos[1]:
                        print("1/1 =0")
                        IA.base.addSample((raquete.imagem_retangulo[1], bola.pos[1]), (0 , ))
                    gen += 1
                    geracao.gen += gen
                    print("Re Treinado Greração", gen)
                    placar.pontos = 2

                print("bateu")



    #Realiza o movimento na tela
    def realiza(self):
        tela.blit(self.imagem,self.imagem_retangulo)

    #Verifica a ação de colidir com a raquete
    def colide_raquete(self, raquete_rect):
        if self.imagem_retangulo.colliderect(raquete_rect):
            self.velo[0] *= -1
            placar.pontos += 1
            print("oloquinho meu")

    #define os movimentos da bola
    def move(self):
        self.pos[0] += self.velo[0] * self.velocidade
        self.pos[1] += self.velo[1] * self.velocidade
        self.imagem_retangulo.center = self.pos

    #Atualiza as açoes da bola
    def atualiza(self, raquete_rect):
        self.colide_raquete(raquete_rect)
        self.colide_parede()
        self.move()

#cria a classe co placar
class Placar:
    def __init__(self):
        pygame.font.init()
        self.fonte = pygame.font.Font(None, 36)
        self.pontos = 1

    def contagem(self):
        self.text=self.fonte.render("pontos = " + str(self.pontos),1,(255,255,255))
        self.textpos = self.text.get_rect()
        self.textpos.centerx = tela.get_width() / 2
        tela.blit(self.text, self.textpos)
        tela.blit(tela, (0,0))

#Cria um placar de gerações
class Geracao:
    def __init__(self):
        pygame.font.init()
        self.fonte = pygame.font.Font(None, 19)
        self.gen = 0000

    def contagem(self):
        self.text=self.fonte.render("Geração = " + str(self.gen),1,(255,255,255))
        self.textpos = self.text.get_rect()
        self.textpos.centerx = tela.get_width() / 3
        tela.blit(self.text, self.textpos)
        tela.blit(tela, (0,0))

#Inicializa os objetos
raquete = Raquete((10,50))
bola = Bola((15,15))
placar= Placar()
geracao = Geracao()

#Cria um objeto para rodar o programa
def iniciar():
    tecla = pygame.key.get_pressed()
    if set(tecla) == {0, 1}:
            print(tecla.index(1))

    tela.fill(PRETO)
    raquete.atualiza(tecla)
    bola.atualiza(raquete.imagem_retangulo)
    bola.realiza()
    raquete.realiza()
    tempo.tick(30)
    placar.contagem()
    geracao.contagem()
    result = IA.rede.activate([raquete.imagem_retangulo[1], bola.pos[1]])
    print( IA.rede.activate([raquete.imagem_retangulo[1], bola.pos[1]]))
    print(bola.pos[1])
    print(erro)
    if   result >= 0.5:
        raquete.cima()
    elif result < 0.5:
        raquete.baixo()
    pygame.display.update()

fim = False

#loop para manter a tela aberta e rodando
while not fim:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            fim = True
    iniciar()

