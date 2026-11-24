from classes import Pokemon,Gerenciadorbd,PokedexInterface,Gerenciadorbd
pokemonvazio=Pokemon('',0,'','',0,0,0,0,0)
evento={
    'acao':'',
    'pokemon':pokemonvazio,
    'termo':'',
    'nome_original':''
    }
banco=Gerenciadorbd('banco/pokedex.db')
interface=PokedexInterface(evento,banco)
interface.mainloop()
interface.banco.fechar()
