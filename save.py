import json
from mapa import Bloco

class Salvar:
    def __init__(self, nome_arquivo='savegame.json'):
        self.__nome_arquivo = nome_arquivo

    @property
    def nome_arquivo(self):
        return self.__nome_arquivo

    def salvar_jogo(self, jogador, inimigo, mapa):
        dados_jogo = {
            "Jogador": {
                "x": jogador.rect.x,
                "y": jogador.rect.y,
                "vida": jogador.vida
            },
            "Inimigo": {
                "x": inimigo.rect.x,
                "y": inimigo.rect.y,
                "vida": inimigo.vida,
            },
            "blocos": [
                {
                    "x": bloco.rect.x,
                    "y": bloco.rect.y,
                    "destrutivel": bloco.destrutivel,
                    "imagem": bloco.image_path  # Salvando o caminho da imagem ao invés do objeto Surface
                }
                for bloco in mapa.blocos
            ]
        }

        with open(self.__nome_arquivo, 'w') as arquivo:
            json.dump(dados_jogo, arquivo)

        print('Jogo salvo!') #Debug

    def carregar_jogo(self, jogador, inimigo, mapa):
        try:
            with open(self.__nome_arquivo, 'r') as arquivo:
                dados_jogo = json.load(arquivo)

            # Restaura os dados do jogador
            jogador.rect.x = dados_jogo["Jogador"]["x"]
            jogador.rect.y = dados_jogo["Jogador"]["y"]
            jogador.vida = dados_jogo["Jogador"]["vida"]

            # Restaura os dados do inimigo
            inimigo.rect.x = dados_jogo["Inimigo"]["x"]
            inimigo.rect.y = dados_jogo["Inimigo"]["y"]
            inimigo.vida = dados_jogo["Inimigo"]["vida"]

            # Limpa os blocos existentes e restaura os blocos salvos
            mapa.blocos.empty()
            for dados_bloco in dados_jogo["blocos"]:
                bloco = Bloco(
                    imagem=dados_bloco["imagem"],  # Usando o caminho da imagem salvo
                    x=dados_bloco["x"],
                    y=dados_bloco["y"],
                    tamanho_bloco=mapa.tamanho_bloco,
                    destrutivel=dados_bloco["destrutivel"]
                )
                mapa.blocos.add(bloco)

            print("Jogo carregado com sucesso.") #Debug
        
        except FileNotFoundError:
            print("Nenhum arquivo de salvamento encontrado.")
