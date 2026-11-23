import tkinter as tk
from tkinter import messagebox
from io import BytesIO
import requests
from PIL import Image, ImageTk
from Pokemon import Pokemon

# Dicionário com as cores das tipagem
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


class PokedexInterface(tk.Tk):
    def __init__(self, retornoMain=None):
        super().__init__()

        # Função/callback do main que recebe os retornos disparados pelos botões
        self.retornoMain = retornoMain
        self.pkmAtual = None
        self.nomeOriginalBD = None
        self.imgTKAtual = None

        self.title("Comparador Pokemon")
        self.geometry("1100x800")
        self.state("zoomed")
        self.configure(bg="#bfffe3")

        # ícone da Pokébola da web
        self.IconeWeb()

        # Título Superior
        self.Titulo()

        # Container Principal (Divide a tela em Esquerda sendo o Card maior e Direita o Painel)
        self.principal = tk.Frame(self, bg="#bfffe3")
        self.principal.pack(expand=True, fill="both", padx=30, pady=10)

        # Lado Esquerdo: Card do Pokémon (Aumentado)
        self.CardPKM()

        # Lado Direito: Painel de Controle e Ações
        self.painelControle()

    def IconeWeb(self):
        # URL e cabeçalho para baixar o ícone da janela
        iconeURL = "https://thumb.wikimedia.org/wikipedia/commons/thumb/5/53/Pok%C3%A9_Ball_icon.svg/3840px-Pok%C3%A9_Ball_icon.svg.png"
        headers = {"User-Agent": "Mozilla/5.0"}

        try:
            resposta = requests.get(iconeURL, headers=headers, timeout=5)
            if resposta.status_code == 200:
                dadosIMG = BytesIO(resposta.content)
                img = Image.open(dadosIMG)
                img = img.resize((32, 32), Image.Resampling.LANCZOS)

                # Mantém referência da imagem para o Tkinter não descartar
                self.iconeJan = ImageTk.PhotoImage(img)
                self.iconphoto(False, self.iconeJan)
        except Exception as e:
            print(f"Não foi possível carregar o ícone da web: {e}")

    def Titulo(self):
        # Faixa superior do sistema
        tituloFrame = tk.Frame(self, bg="#6f6fff", highlightbackground="#6f6fff", highlightthickness=6)
        tituloFrame.pack(pady=10)

        tituloLabel = tk.Label(
            tituloFrame,
            text="SISTEMA POKÉMON",
            font=("Arial", 25, "bold"),
            fg="#fff536",
            bg="#6f6fff",
            padx=3000
        )
        tituloLabel.pack()

    def CardPKM(self):
        # Moldura externa do card à esquerda
        frame = tk.Frame(self.principal, bg="#bfffe3")
        frame.pack(side="left", padx=(10, 30), anchor="n")

        borda = tk.Frame(frame, bg="#ffcb05", padx=12, pady=12)
        borda.pack()

        card = tk.Frame(borda, bg="#0077ff", padx=30, pady=30, width=440)
        card.pack()

        containerIMG = tk.Frame(card, bg="#e2e8f0", bd=3, relief="solid", padx=10, pady=10)
        containerIMG.pack(fill="x", pady=(0, 18))

        # Cartinha
        self.labelIMG = tk.Label(containerIMG, text="[ Imagem top ]", bg="#e2e8f0", fg="#64748b", font=("Arial", 15, "bold"), height=11)
        self.labelIMG.pack(fill="both")

        # Nomezinho dos bicho
        self.labelNome = tk.Label(card, text="Pikachu", font=("Arial", 24, "bold"), fg="#0f172a", bg="#0077ff")
        self.labelNome.pack(pady=(0, 12))

        # Tipagens (a elétrica é de defalt só)
        self.frameTipos = tk.Frame(card, bg="#0077ff")
        self.frameTipos.pack(pady=(0, 18))
        self.criadorTipagens(["electric"])

        # Todas as informações
        infos = tk.Frame(card, bg="#f8fafc", padx=15, pady=15)
        infos.pack(fill="x", pady=(0, 18))

        self.labelAltu = self.criarInfo(infos, "Altura", "0.4 m", 0)
        self.labelPeso = self.criarInfo(infos, "Peso", "6.0 kg", 1)
        self.labelXP = self.criarInfo(infos, "Nº Pokédex", "#025", 2)

        # Seção de Status (HP, Ataque, Defesa)
        frameStats = tk.Frame(card, bg="#f1f5f9", padx=15, pady=15)
        frameStats.pack(fill="x")

        # Guarda canvas, label do valor e cor de cada status separadamente
        self.Stats = {}
        self.Stats['HP'] = self.criarStatus(frameStats, "HP", "35", "#ef4444", 0)
        self.Stats['Ataque'] = self.criarStatus(frameStats, "Ataque", "55", "#f97316", 1)
        self.Stats['Defesa'] = self.criarStatus(frameStats, "Defesa", "40", "#3b82f6", 2)

    def painelControle(self):
        # Painel lateral com busca, formulário e botões de ação
        painelControle = tk.Frame(self.principal, bg="#ffffff", bd=3, relief="ridge", padx=15, pady=15)
        painelControle.pack(side="right", fill="both", expand=True, padx=(10, 10))

        tk.Label(painelControle, text="CONTROLE", font=("Arial", 20, "bold"), fg="#0f172a", bg="#ffffff").pack(pady=(0, 8))

        # Consulta ao banco
        tk.Label(painelControle, text="Consultar Pokémon no banco", font=("Arial", 11, "bold"), fg="#2563eb", bg="#ffffff", anchor="w").pack(fill="x")

        frameBusca = tk.Frame(painelControle, bg="#ffffff")
        frameBusca.pack(fill="x", pady=(2, 8))

        self.busca = tk.Entry(frameBusca, font=("Arial", 10), bd=2, relief="solid")
        self.busca.pack(side="left", fill="x", expand=True, padx=(0, 6))

        consultar = tk.Button(
            frameBusca, text="CONSULTAR", font=("Arial", 9, "bold"),
            bg="#2563eb", fg="white", activebackground="#1d4ed8", activeforeground="white",
            cursor="hand2", padx=8, pady=4, command=self.consultarAcao
        )
        consultar.pack(side="right")

        # Formulário digitado pelo usuário (sem pegar dados da API, só imagem no cadastro)
        tk.Label(painelControle, text="Entrada dos dados do Pokémon", font=("Arial", 11, "bold"), fg="#0f172a", bg="#ffffff", anchor="w").pack(fill="x", pady=(2, 4))

        formGrid = tk.Frame(painelControle, bg="#f8fafc", bd=1, relief="solid", padx=8, pady=8)
        formGrid.pack(fill="x", pady=(0, 8))

        # Campos do formulário em grade
        self.entradaNome = self.criarCampoForm(formGrid, "Nome:", 0, 0)
        self.entradaNumPkm = self.criarCampoForm(formGrid, "Nº Pokédex:", 0, 2)
        self.entradaTipo1 = self.criarCampoForm(formGrid, "Tipo 1:", 1, 0)
        self.entradaTipo2 = self.criarCampoForm(formGrid, "Tipo 2:", 1, 2)
        self.entradaHP = self.criarCampoForm(formGrid, "HP:", 2, 0)
        self.entradaAtaque = self.criarCampoForm(formGrid, "Ataque:", 2, 2)
        self.entradaDefesa = self.criarCampoForm(formGrid, "Defesa:", 3, 0)
        self.entradaAltura = self.criarCampoForm(formGrid, "Altura:", 3, 2)
        self.entradaPeso = self.criarCampoForm(formGrid, "Peso:", 4, 0)

        # Botão Cadastrar (baixa imagem pela API e retorna para o main)
        cadastrar = tk.Button(
            painelControle, text="CADASTRAR POKÉMON", font=("Arial", 10, "bold"),
            bg="#16a34a", fg="white", activebackground="#15803d", activeforeground="white",
            cursor="hand2", padx=6, pady=5, command=self.cadastrarAcao
        )
        cadastrar.pack(fill="x", pady=(0, 6))

        # Botão Alterar (atualiza informações do Pokémon e retorna para o main)
        self.alterar = tk.Button(
            painelControle, text="ALTERAR INFORMAÇÕES", font=("Arial", 10, "bold"),
            bg="#d97706", fg="white", activebackground="#b45309", activeforeground="white",
            cursor="hand2", padx=6, pady=5, command=self.alterarAcao
        )
        self.alterar.pack(fill="x", pady=(0, 8))

        # Frame Excluir (aparece quando o Pokémon vem do banco)
        self.frameDeletar = tk.Frame(painelControle, bg="#fee2e2", bd=2, relief="solid", padx=8, pady=8)

        tk.Label(self.frameDeletar, text="Registro do banco", font=("Arial", 12, "bold"), fg="#b91c1c", bg="#fee2e2", anchor="w").pack(fill="x", pady=(0, 3))

        self.deletar = tk.Button(
            self.frameDeletar, text="EXCLUIR DO BANCO DE DADOS", font=("Arial", 10, "bold"),
            bg="#dc2626", fg="white", activebackground="#b91c1c", activeforeground="white",
            cursor="hand2", padx=6, pady=5, command=self.deletarAcao
        )
        self.deletar.pack(fill="x")

    def criarCampoForm(self, parent, rotulo, linha, coluna):
        # Cria rótulo e campo de entrada alinhados na grade do formulário
        tk.Label(parent, text=rotulo, font=("Arial", 9, "bold"), fg="#334155", bg="#f8fafc", anchor="w").grid(
            row=linha, column=coluna, sticky="w", padx=(2, 4), pady=2
        )
        campo = tk.Entry(parent, font=("Arial", 9), bd=1, relief="solid", width=12)
        campo.grid(row=linha, column=coluna + 1, sticky="ew", padx=(0, 8), pady=2)
        parent.grid_columnconfigure(1, weight=1)
        parent.grid_columnconfigure(3, weight=1)
        return campo

    def emitirRetorno(self, payload):
        """Envia o retorno da ação do botão para o main e devolve o payload."""
        if callable(self.retornoMain):
            self.retornoMain(payload)
        return payload

    def montarPokemonForm(self, imgExistente=None):
        """Valida os inputs do usuário e instancia a classe Pokemon."""
        nome = self.entradaNome.get().strip()
        tipo1 = self.entradaTipo1.get().strip().lower()
        tipo2 = self.entradaTipo2.get().strip().lower()

        if not nome:
            messagebox.showerror("Erro de Validação", "Digite o nome do Pokémon.")
            return None

        if not tipo1:
            messagebox.showerror("Erro de Validação", "Digite pelo menos o Tipo 1 do Pokémon.")
            return None

        # Converte e valida campos numéricos (aceitando vírgula em altura e peso)
        try:
            numpokedex = int(self.entradaNumPkm.get().strip())
            hp = int(self.entradaHP.get().strip())
            ataque = int(self.entradaAtaque.get().strip())
            defesa = int(self.entradaDefesa.get().strip())
            altura = float(self.entradaAltura.get().strip().replace(",", "."))
            peso = float(self.entradaPeso.get().strip().replace(",", "."))
        except ValueError:
            messagebox.showerror(
                "Erro de Dados",
                "Verifique os campos numéricos: Nº Pokédex, HP, Ataque e Defesa devem ser inteiros; Altura e Peso devem ser números."
            )
            return None

        pkm = Pokemon(
            nome=nome,
            numpokedex=numpokedex,
            tipo1=tipo1,
            tipo2=tipo2,
            hp=hp,
            defesa=defesa,
            ataque=ataque,
            altura=altura,
            peso=peso
        )

        if imgExistente is not None:
            pkm.adicionar_imagem(imgExistente)

        return pkm

    def preencherFormComPokemon(self, pkm: Pokemon):
        """Preenche os campos do formulário a partir de um objeto Pokemon."""
        campos = [
            (self.entradaNome, pkm.nome),
            (self.entradaNumPkm, str(pkm.numpokedex)),
            (self.entradaTipo1, pkm.tipo1 or ""),
            (self.entradaTipo2, pkm.tipo2 or ""),
            (self.entradaHP, str(pkm.hp)),
            (self.entradaAtaque, str(pkm.ataque)),
            (self.entradaDefesa, str(pkm.defesa)),
            (self.entradaAltura, str(pkm.altura)),
            (self.entradaPeso, str(pkm.peso)),
        ]
        for campo, valor in campos:
            campo.delete(0, tk.END)
            campo.insert(0, valor)

    def exibirPokemonNoCard(self, pkm: Pokemon):
        """Atualiza o card visual com os dados e a imagem do objeto Pokemon."""
        self.pkmAtual = pkm
        self.labelNome.config(text=pkm.nome.capitalize())
        self.labelAltu.config(text=f"{pkm.altura} m")
        self.labelPeso.config(text=f"{pkm.peso} kg")
        self.labelXP.config(text=f"#{int(pkm.numpokedex):03d}")

        tipos = [t for t in [pkm.tipo1, pkm.tipo2] if t]
        self.criadorTipagens(tipos if tipos else ["normal"])

        # Atualiza cada status individualmente usando os dados salvos em self.Stats
        valoresStats = {
            "HP": int(pkm.hp),
            "Ataque": int(pkm.ataque),
            "Defesa": int(pkm.defesa),
        }
        for chave, infoStat in self.Stats.items():
            valor = valoresStats[chave]
            self.atualizarStatVisual(infoStat, valor)

        # Renderiza a imagem do Pokémon ou exibe aviso se não houver imagem
        imgBytes = getattr(pkm, "imagem", None)
        if imgBytes:
            try:
                dadosIMG = BytesIO(imgBytes)
                img = Image.open(dadosIMG)
                img = img.resize((160, 160), Image.Resampling.LANCZOS)
                self.imgTKAtual = ImageTk.PhotoImage(img)
                self.labelIMG.config(image=self.imgTKAtual, text="", height=160)
            except Exception as e:
                messagebox.showerror("Erro de Imagem", f"Não foi possível renderizar a imagem do Pokémon: {e}")
        else:
            self.imgTKAtual = None
            self.labelIMG.config(image="", text="[ Sem imagem ]", height=11)

    def atualizarStatVisual(self, infoStat, valorStat):
        # Atualiza somente o label e a barra do status correspondente
        canvasBar = infoStat["canvas"]
        labelValor = infoStat["label"]
        corBarra = infoStat["cor"]

        labelValor.config(text=str(valorStat))

        canvasBar.delete("barra")
        preenchimento = min(int(valorStat) * 2, 300)
        canvasBar.create_rectangle(0, 0, preenchimento, 9, fill=corBarra, width=0, tags="barra")

    def gerenBTNdelet(self, origem):
        # Exibe ou oculta o bloco de exclusão conforme a origem do registro
        if origem == "banco":
            self.frameDeletar.pack(fill="x", pady=(4, 4))
        else:
            self.frameDeletar.pack_forget()

    def consultarAcao(self):
        # Valida o termo de busca e notifica o main
        termo = self.busca.get().strip()
        if not termo:
            messagebox.showerror("Erro de Consulta", "Digite um nome ou número para consultar no banco.")
            return self.emitirRetorno(None)

        self.gerenBTNdelet("banco")
        return self.emitirRetorno({"acao": "consultar", "termo": termo})

    def cadastrarAcao(self):
        # Monta o Pokémon, busca a arte oficial na API e envia o cadastro para o main
        pkm = self.montarPokemonForm()
        if pkm is None:
            return self.emitirRetorno(None)

        try:
            baixouIMG = pkm.buscar_imagem()
        except Exception as e:
            messagebox.showerror("Erro na API de Imagens", f"Falha ao conectar na API de imagens: {e}")
            return self.emitirRetorno(None)

        if not baixouIMG or not getattr(pkm, "imagem", None):
            messagebox.showerror(
                "Imagem Não Encontrada",
                f"Não foi possível baixar a imagem de '{pkm.nome}' na API."
            )
            return self.emitirRetorno(None)

        self.nomeOriginalBD = pkm.nome
        self.exibirPokemonNoCard(pkm)
        self.gerenBTNdelet("banco")
        return self.emitirRetorno({"acao": "cadastrar", "pokemon": pkm})

    def alterarAcao(self):
        # Preserva a imagem atual caso não haja nova busca e envia a alteração
        imgAtual = getattr(self.pkmAtual, "imagem", None) if self.pkmAtual else None
        pkmAlterado = self.montarPokemonForm(imgExistente=imgAtual)
        if pkmAlterado is None:
            return self.emitirRetorno(None)

        chaveAlvo = self.nomeOriginalBD or (self.pkmAtual.nome if self.pkmAtual else pkmAlterado.nome)
        self.nomeOriginalBD = pkmAlterado.nome
        self.exibirPokemonNoCard(pkmAlterado)
        return self.emitirRetorno({
            "acao": "alterar",
            "nome_original": chaveAlvo,
            "pokemon": pkmAlterado
        })

    def deletarAcao(self):
        # Identifica o alvo da exclusão, limpa referência atual e notifica o main
        alvo = self.nomeOriginalBD or (self.pkmAtual.nome if self.pkmAtual else self.entradaNome.get().strip())
        if not alvo:
            messagebox.showerror("Erro ao Excluir", "Nenhum Pokémon selecionado ou informado para exclusão.")
            return self.emitirRetorno(None)

        self.pkmAtual = None
        self.nomeOriginalBD = None
        self.gerenBTNdelet("api")
        return self.emitirRetorno({"acao": "excluir", "nome": alvo})

    def criadorTipagens(self, listatTiposEN):
        # Recria as     tipagem no card
        for widget in self.frameTipos.winfo_children():
            widget.destroy()

        for tipoEN in listatTiposEN:
            fundo = tipagensCores.get(tipoEN, "#949468")
            NomeBras = tipoEN.capitalize()

            badge = tk.Label(self.frameTipos, text=NomeBras, bg=fundo, fg="white", font=("Arial", 9, "bold"), padx=10, pady=3)
            badge.pack(side="left", padx=4)

    def criarInfo(self, parent, label, valor, linha):
        # Cria uma linha de informação (rótulo à esquerda e valor à direita)
        labelPrinci = tk.Label(parent, text=label, font=("Arial", 10, "bold"), fg="#64748b", bg="#f8fafc", anchor="w")
        labelPrinci.grid(row=linha, column=0, sticky="w", pady=4)

        valorLabel = tk.Label(parent, text=valor, font=("Arial", 10, "bold"), fg="#1e293b", bg="#f8fafc", anchor="e")
        valorLabel.grid(row=linha, column=1, sticky="e", pady=4)
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_columnconfigure(1, weight=1)
        return valorLabel

    def criarStatus(self, parent, nomeStat, valorStat, barCor, linha):
        # Cria cabeçalho e barra de progresso para um atributo específico
        frameLabels = tk.Frame(parent, bg="#f1f5f9")
        frameLabels.grid(row=linha * 2, column=0, sticky="ew", pady=(4, 2))

        tk.Label(frameLabels, text=nomeStat, font=("Arial", 8, "bold"), fg="#475569", bg="#f1f5f9").pack(side="left")
        valorLabelStat = tk.Label(frameLabels, text=valorStat, font=("Arial", 8, "bold"), fg="#475569", bg="#f1f5f9")
        valorLabelStat.pack(side="right")

        canvasBar = tk.Canvas(parent, height=9, bg="#cbd5e1", highlightthickness=0)
        canvasBar.grid(row=linha * 2 + 1, column=0, sticky="ew", pady=(0, 6))

        preenchimento = min(int(valorStat) * 2, 300)
        canvasBar.create_rectangle(0, 0, preenchimento, 9, fill=barCor, width=0, tags="barra")

        parent.grid_columnconfigure(0, weight=1)
        return {"canvas": canvasBar, "label": valorLabelStat, "cor": barCor}


if __name__ == "__main__":
    def receberRetorno(dadosRetorno):
        if dadosRetorno:
            print("Retorno para o main:", dadosRetorno["acao"], dadosRetorno)

    app = PokedexInterface(retornoMain=receberRetorno)
    app.mainloop()