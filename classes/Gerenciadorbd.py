import sqlite3 as sql
from classes.Pokemon import Pokemon
import os
class Gerenciadorbd:
    def __init__(self,caminhobanco:str):
        self.caminhobanco=caminhobanco
    def conectar(self):
        if os.path.exists(self.caminhobanco):
            self.con=sql.connect(self.caminhobanco)
            self.cur=self.con.cursor()
        else:
            self.con=sql.connect(self.caminhobanco)
            self.cur=self.con.cursor()
            self.cur.execute('CREATE TABLE pokemon(id INT AUTO_INCREMENT PRIMARY KEY, nome VARCHAR(50) NOT NULL, numero_pokedex INT UNIQUE NOT NULL, tipo1 VARCHAR(20) NOT NULL, tipo2 VARCHAR(20), hp INT, defesa INT, ataque INT, altura FLOAT, peso FLOAT, img MEDIUMBLOB);')
    def fechar(self):
        self.con.close()
    def inserir_pokemon(self,pokemon:Pokemon):
        if pokemon.tipo2==None:
            comando="INSERT INTO pokemon(nome,numero_pokedex,tipo1,hp,defesa,ataque,altura,peso,img) VALUES(?,?,?,?,?,?,?,?,?)"
            valores=(pokemon.nome,pokemon.numpokedex,pokemon.tipo1,pokemon.hp,pokemon.defesa,pokemon.ataque,pokemon.altura,pokemon.peso,pokemon.imagem)
        else:
            comando="INSERT INTO pokemon(nome,numero_pokedex,tipo1,tipo2,hp,defesa,ataque,altura,peso,img) VALUES(?,?,?,?,?,?,?,?,?,?)"
            valores=(pokemon.nome,pokemon.numpokedex,pokemon.tipo1,pokemon.tipo2,pokemon.hp,pokemon.defesa,pokemon.ataque,pokemon.altura,pokemon.peso,pokemon.imagem)
        self.cur.execute(comando,valores)
        self.con.commit()
    def consultar_pokemon(self,nome:str)->Pokemon:
        resp=self.cur.execute('SELECT FROM pokemon WHERE nome=?',(nome,))
        dados=resp.fetchone()
        pokemon=Pokemon(dados[0],dados[1],dados[2],dados[3],dados[4],dados[5],dados[6],dados[7],dados[8])
        pokemon.adicionar_imagem(dados[9])
        return pokemon
    def deletar_pokemon(self,nome:str):
        self.cur.execute('DELETE FROM pokemon WHERE nome=?',(nome,))
        self.con.commit()
