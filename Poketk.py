import tkinter as tk
from tkinter import ttk
from io import BytesIO
import requests
from PIL import Image, ImageTk

# Dicionário com as cores das tipagens
tipagensCores = {
    "fire": "#ff5a24",
    "water": "#0db2ff",
    "grass": "#3fa110",
    "electric": "#f1bf00",
    "ice": "#50cfcf",
    "fighting": "#bf2018",
    "poison": "#9b389b",
    "ground": "#cc9f2f",
    "flying": "#9275e7",
    "psychic": "#f63371",
    "bug": "#91a110",
    "rock": "#a18a24",
    "ghost": "#614683",
    "dragon": "#5118cd",
    "dark": "#533e31",
    "steel": "#9fa1ba",
    "fairy": "#ff6ba9",
    "normal": "#949468"
}

# Dicionário para traduzir as tipagens da API/Banco para português
tipagensTrad = {
    "fire": "Fogo",
    "water": "Água",
    "grass": "Planta",
    "electric": "Elétrico",
    "ice": "Gelo",
    "fighting": "Lutador",
    "poison": "Venenoso",
    "ground": "Terrestre",
    "flying": "Voador",
    "psychic": "Psíquico",
    "bug": "Inseto",
    "rock": "Pedra",
    "ghost": "Fantasma",
    "dragon": "Dragão",
    "dark": "Sombrio",
    "steel": "Aço",
    "fairy": "Fada",
    "normal": "Normal"
}

class PokedexInterface(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Comparador Pokemon - Sistema Completo")
        self.geometry("1100x800") 
        self.state("zoomed") 
        self.configure(bg="#bfffe3")

        # Ícone da Pokébola da web
        self.IconeWeb()

        # Título Superior
        self.Titulo()

        # Container Principal (Divide a tela em Esquerda [Card maior] e Direita [Painel])
        self.principal = tk.Frame(self, bg="#bfffe3")
        self.principal.pack(expand=True, fill="both", padx=30, pady=10)

        # Lado Esquerdo: Card do Pokémon
        self.CardPKM()

        # Lado Direito: Painel de Controle e Ações
        self.painelControle()

    def IconeWeb(self):
        iconeURL = "https://thumb.wikimedia.org/wikipedia/commons/thumb/5/53/Pok%C3%A9_Ball_icon.svg/3840px-Pok%C3%A9_Ball_icon.svg.png"
        headers = {"User-Agent": "Mozilla/5.0"}
        
        try:
            resposta = requests.get(iconeURL, headers=headers, timeout=5)
            if resposta.status_code == 200:
                dadosIMG = BytesIO(resposta.content)
                img = Image.open(dadosIMG)
                img = img.resize((32, 32), Image.Resampling.LANCZOS)
                
                self.iconeJan = ImageTk.PhotoImage(img)
                self.iconphoto(False, self.iconeJan)
        except Exception as e:
            print(f"Não foi possível carregar o ícone da web: {e}")

    def Titulo(self):
        tituloFrame = tk.Frame(self, bg="#6f6fff", highlightbackground="#6f6fff", highlightthickness=6)
        tituloFrame.pack(pady=10)
        
        tituloLabel = tk.Label(
            tituloFrame, 
            text="SISTEMA POKÉMON", 
            font=("Arial", 25, "bold"), 
            fg="#fff536", 
            bg="#6f6fff",
            padx= 3000
        )
        tituloLabel.pack()

    def CardPKM(self):
        frame = tk.Frame(self.principal, bg="#bfffe3")
        frame.pack(side="left", padx=(10, 30), anchor="n")

        borda = tk.Frame(frame, bg="#ffcb05", padx=12, pady=12)
        borda.pack()

        card = tk.Frame(borda, bg="#0077ff", padx=30, pady=30, width=440)
        card.pack()

        containerIMG = tk.Frame(card, bg="#e2e8f0", bd=3, relief="solid", padx=10, pady=10)
        containerIMG.pack(fill="x", pady=(0, 18))

        # Variável da Imagem do Pokémon
        self.labelIMG = tk.Label(containerIMG, text="[ Imagem top ]", bg="#e2e8f0", fg="#64748b", font=("Arial", 15, "bold"), height=11)
        self.labelIMG.pack(fill="both")

        # Variável do Nome do Pokémon (pronta para receber valor externo)
        self.labelNome = tk.Label(card, text="", font=("Arial", 24, "bold"), fg="#0f172a", bg="#0077ff")
        self.labelNome.pack(pady=(0, 12))

        # Variável/Frame de Tipagens (alimentado pela função criadorTipagens com lista de tipos em inglês)
        self.frameTipos = tk.Frame(card, bg="#0077ff")
        self.frameTipos.pack(pady=(0, 18))
        self.criadorTipagens([])

        # Variáveis de Informações (Altura, Peso, XP Base)
        infos = tk.Frame(card, bg="#f8fafc", padx=15, pady=15)
        infos.pack(fill="x", pady=(0, 18))

        self.labelAltura = self.criarInfo(infos, "Altura", "", 0)
        self.labelPeso = self.criarInfo(infos, "Peso", "", 1)
        self.labelXp = self.criarInfo(infos, "XP Base", "", 2)

        # Dicionário de Status (HP, Ataque, Defesa) com suas respectivas variáveis e barrinhas
        frameStats = tk.Frame(card, bg="#f1f5f9", padx=15, pady=15)
        frameStats.pack(fill="x")

        self.Stats = {}
        self.Stats['HP'] = self.criarStatus(frameStats, "HP", "", "#ef4444", 0)
        self.Stats['Ataque'] = self.criarStatus(frameStats, "Ataque", "", "#f97316", 1)
        self.Stats['Defesa'] = self.criarStatus(frameStats, "Defesa", "", "#3b82f6", 2)

    def painelControle(self):
        painelControle = tk.Frame(self.principal, bg="#ffffff", bd=3, relief="ridge", padx=15, pady=15)
        painelControle.pack(side="right", fill="both", expand=True, padx=(10, 10))

        tk.Label(painelControle, text="CONTROLE", font=("Arial", 20, "bold"), fg="#0f172a", bg="#ffffff").pack(pady=(0, 10))

        # Consulta ao banco
        tk.Label(painelControle, text="Consultar Pokémon dentro do banco de dados", font=("Arial", 12, "bold"), fg="#2563eb", bg="#ffffff", anchor="w").pack(fill="x", pady=(2, 2))
        
        self.busca = tk.Entry(painelControle, font=("Arial", 11), bd=2, relief="solid")
        self.busca.pack(fill="x", pady=(0, 5))
        self.busca.insert(0,"")

        consultar = tk.Button(
            painelControle, text="CONSULTAR NO BANCO", font=("Arial", 10, "bold"), 
            bg="#2563eb", fg="white", activebackground="#1d4ed8", activeforeground="white",
            cursor="hand2", padx=6, pady=5, command=self.consultarAcao
        )
        consultar.pack(fill="x", pady=(0, 10))

        # API
        tk.Label(painelControle, text="Pegar da API", font=("Arial", 12, "bold"), fg="#d97706", bg="#ffffff", anchor="w").pack(fill="x", pady=(2, 2))
        
        self.enterAPI = tk.Entry(painelControle, font=("Arial", 11), bd=2, relief="solid")
        self.enterAPI.pack(fill="x", pady=(0, 5))
        self.enterAPI.insert(0,"")

        API = tk.Button(
            painelControle, text="BUSCAR DA API", font=("Arial", 9, "bold"), 
            bg="#d97706", fg="white", activebackground="#b45309", activeforeground="white",
            cursor="hand2", padx=6, pady=5, command=self.acaoAPI
        )
        API.pack(fill="x", pady=(0, 10))

        # Botar no banco
        tk.Label(painelControle, text="Colocar no banco de dados", font=("Arial", 12, "bold"), fg="#16a34a", bg="#ffffff", anchor="w").pack(fill="x", pady=(2, 2))
        
        salvar = tk.Button(
            painelControle, text="ARMAZENAR NO BANCO", font=("Arial", 10, "bold"), 
            bg="#22c55e", fg="white", activebackground="#16a34a", activeforeground="white",
            cursor="hand2", padx=6, pady=5, command=self.salvarAcao
        )
        salvar.pack(fill="x", pady=(0, 10))

        # Retirar do banco
        self.frameDeletar = tk.Frame(painelControle, bg="#fee2e2", bd=2, relief="solid", padx=8, pady=8)
        
        tk.Label(self.frameDeletar, text="Registro do banco", font=("Arial", 13, "bold"), fg="#b91c1c", bg="#fee2e2", anchor="w").pack(fill="x", pady=(0, 3))
        
        self.deletar = tk.Button(
            self.frameDeletar, text="EXCLUIR DO BANCO DE DADOS", font=("Arial", 10, "bold"), 
            bg="#dc2626", fg="white", activebackground="#b91c1c", activeforeground="white",
            cursor="hand2", padx=6, pady=5, command=self.deletarAcao
        )
        self.deletar.pack(fill="x")

    def gerenBTNdelet(self, origem):
        if origem == "banco":
            self.frameDeletar.pack(fill="x", pady=(5, 5))
        else:
            self.frameDeletar.pack_forget()

    def consultarAcao(self):
        termo = self.busca.get()
        print(f"Consultando no banco por: {termo}")
        
        origemD = "banco" 
        
        self.gerenBTNdelet(origemD)

    def acaoAPI(self):
        termo = self.enterAPI.get()
        print(f"Buscando da API externa: {termo}")
        
        origemD = "api"
        self.gerenBTNdelet(origemD)

    def salvarAcao(self):
        print("Salvando dados atuais e imagem MEDIUMBLOB na tabela pokemons...")

    def deletarAcao(self):
        print("Executando DELETE no banco de dados para este Pokémon...")
        self.gerenBTNdelet("api")

    def criadorTipagens(self, listatTiposEN):
        """Método para atualizar as tipagens dinamicamente e traduzi-las para português"""
        for widget in self.frameTipos.winfo_children():
            widget.destroy()
            
        for tipoEN in listatTiposEN:
            tipoChave = tipoEN.lower()
            fundo = tipagensCores.get(tipoChave, "#949468")
            NomeBras = tipagensTrad.get(tipoChave, tipoEN.capitalize())
            
            badge = tk.Label(self.frameTipos, text=NomeBras, bg=fundo, fg="white", font=("Arial", 9, "bold"), padx=10, pady=3)
            badge.pack(side="left", padx=4)

    def criarInfo(self, parent, label, valor, linha):
        labelPrinci = tk.Label(parent, text=label, font=("Arial", 10, "bold"), fg="#64748b", bg="#f8fafc", anchor="w")
        labelPrinci.grid(row=linha, column=0, sticky="w", pady=4)
        
        valorLabel = tk.Label(parent, text=valor, font=("Arial", 10, "bold"), fg="#1e293b", bg="#f8fafc", anchor="e")
        valorLabel.grid(row=linha, column=1, sticky="e", pady=4)
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_columnconfigure(1, weight=1)
        return valorLabel

    def criarStatus(self, parent, nomeStat, valorStat, barCor, linha):
        frameLabels = tk.Frame(parent, bg="#f1f5f9")
        frameLabels.grid(row=linha*2, column=0, sticky="ew", pady=(4, 2))
        
        tk.Label(frameLabels, text=nomeStat, font=("Arial", 8, "bold"), fg="#475569", bg="#f1f5f9").pack(side="left")
        
        # Variável do valor numérico do status
        valorLabelStat = tk.Label(frameLabels, text=valorStat, font=("Arial", 8, "bold"), fg="#475569", bg="#f1f5f9")
        valorLabelStat.pack(side="right")

        # Variável da barrinha (Canvas)
        canvasBar = tk.Canvas(parent, height=9, bg="#cbd5e1", highlightthickness=0)
        canvasBar.grid(row=linha*2+1, column=0, sticky="ew", pady=(0, 6))
        
        valInt = int(valorStat) if valorStat.isdigit() else 0
        preenchimento = min(valInt * 2, 300) 
        canvasBar.create_rectangle(0, 0, preenchimento, 9, fill=barCor, width=0, tags="barra")
        
        parent.grid_columnconfigure(0, weight=1)
        
        return {'label': valorLabelStat, 'canvas': canvasBar}

if __name__ == "__main__":
    app = PokedexInterface()
    app.mainloop()