import pygame
import matplotlib.pyplot as plt
import io
import time
from PIL import Image
import psutil
import datetime
import mysql.connector

class Banco():
    def __init__(self, localhost, name, password, database = None):
        self.localhost = localhost
        self.name = name
        self.password = password
        self.database = database

        if database == None:
            self.database_con = mysql.connector.connect(
                host=self.localhost,
                user=self.name,
                password=self.password
            )

        else:
            self.database_con = mysql.connector.connect(
                host=self.localhost,
                user=self.name,
                password=self.password,
                database=self.database
            )

        self.cursor = self.database_con.cursor()

    def criar_banco(self, nome_banco):
        self.criar = f"CREATE DATABASE IF NOT EXISTS {nome_banco};"
        self.cursor.execute(self.criar)

    def use_banco(self, nome_banco):
        self.cursor.execute(f"USE {nome_banco};")

    def insert(self, tabela, lista_dados):
        string_a_ser_montada = f"INSERT INTO '{tabela}' VALUES ("
        for i in lista_dados:
            if type(i) == int or type(i) == float:
                string_a_ser_montada += f"{i},"
            else:
                string_a_ser_montada += f"'{i}',"

        string_a_ser_montada = string_a_ser_montada.rstrip(string_a_ser_montada[-1])
        string_a_ser_montada += ");"

        self.cursor.execute(string_a_ser_montada)
        self.database_con.commit()

    def criar_tabela_auto(self, nome_tabela, lista_campos, lista_tamanhos = None):
        index_lista_tamanhos = 0
        string_a_ser_montada = f"CREATE TABLE IF NOT EXISTS `{nome_tabela}` ("
        for i in lista_campos:
            if i[-1] == "K":
                string_a_ser_montada += f"{i} INT PRIMARY KEY,"
            elif i[-1] == "N":
                string_a_ser_montada += f"{i} INT,"
            elif i[-1] == "V":
                string_a_ser_montada += f"{i} VARCHAR({lista_tamanhos[index_lista_tamanhos]}),"
                index_lista_tamanhos += 1
        string_a_ser_montada = string_a_ser_montada.rstrip(string_a_ser_montada[-1])
        string_a_ser_montada += ");"
        self.cursor.execute(string_a_ser_montada)


class Gerador_Grafico():
    def __init__(self):
        self.atualizador_dados_tempo = 0
        self.lista_cpu = [psutil.cpu_percent()]
        self.lista_ram = [psutil.virtual_memory().percent]
        self.lista_data = [datetime.datetime.now().strftime('%H:%M:%S')]
        time.sleep(1)
        self.update_dados()
        self.atualizar_grafico()
        self.img = self.criar_imagem()

        self.eixo_x = 10
        self.eixo_y = 0

    def update_dados(self):
        if len(self.lista_cpu )< 10:
            self.lista_cpu.append(psutil.cpu_percent())
            self.lista_ram.append(psutil.virtual_memory().percent)
            self.lista_data.append(datetime.datetime.now().strftime('%H:%M:%S'))
        else:
            del self.lista_cpu[0]
            del self.lista_ram[0]
            del self.lista_data[0]
            self.lista_cpu.append(psutil.cpu_percent())
            self.lista_ram.append(psutil.virtual_memory().percent)
            self.lista_data.append(datetime.datetime.now().strftime('%H:%M:%S'))

    def atualizar_grafico(self):
        plt.close('all')
        plt.clf()
        plt.figure(figsize=(9,6))
        plt.plot(self.lista_data, self.lista_cpu)
        plt.plot(self.lista_data, self.lista_ram)

        self.fig = plt.gcf()

    def criar_imagem(self):
        self.buf = io.BytesIO()
        self.fig.savefig(self.buf)
        self.buf.seek(0)
        img = Image.open(self.buf)
        data = img.tobytes("raw", "RGBA")
        return pygame.image.fromstring(data, img.size, 'RGBA')
        

    def mostrar_tela(self, screen, tempo):
        if self.atualizador_dados_tempo + 1000 < tempo:
            self.update_dados()
            self.atualizar_grafico()
            self.img = self.criar_imagem()
            
            self.atualizador_dados_tempo = tempo
        screen.blit(self.img, (self.eixo_x,self.eixo_y))

gerador = Gerador_Grafico()
banco = Banco("localhost", "xxxxxx", "xxxxxx")
banco.criar_banco("teste")
banco.use_banco("teste")
banco.criar_tabela_auto("jonas", ["jonas_K", "CPU_N", "RAM_N"])


pygame.init()
size = (900, 700)
screen = pygame.display.set_mode(size)
 
pygame.display.set_caption("My Game")
 
clock = pygame.time.Clock()


while True:
    tempo = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

    screen.fill((3,3,3))
    
    gerador.mostrar_tela(screen, tempo)

    pygame.display.flip()

    clock.tick(10)