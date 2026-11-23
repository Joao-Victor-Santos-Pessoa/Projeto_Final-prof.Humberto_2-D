import requests
class Pokemon:
    def __init__(self,nome:str,numpokedex:int,tipo1:str,tipo2:str,hp:int,defesa:int,ataque:int,altura:float,peso:float):
        self.nome=nome
        self.numpokedex=numpokedex
        self.tipo1=tipo1
        self.tipo2=tipo2
        self.hp=hp
        self.defesa=defesa
        self.ataque=ataque
        self.altura=altura
        self.peso=peso
    def buscar_imagem(self)->bool:
        url=f'https://pokeapi.co/api/v2/pokemon/{self.nome.lower().strip()}'
        resposta=requests.get(url)
        if resposta.status_code!=200:
            return False
        dados=resposta.json()
        urlimagem=dados['sprites']['other']['official-artwork']['front_default']
        resposta=requests.get(urlimagem)
        self.imagem=resposta.content
        return True
    def adicionar_imagem(self,img):
        self.imagem=img