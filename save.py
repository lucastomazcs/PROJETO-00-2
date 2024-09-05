import json
from mapa import Bloco
from inimigoexplosivo import InimigoExplosivo
from poderes import Poder

class Salvar:
   def __init__(self, nome_arquivo='savegame.json'):
        self.__nome_arquivo = nome_arquivo

   @property
   def nome_arquivo(self):
        return self.__nome_arquivo

   def salvar_jogo(self, jogador, inimigo, inimigo_explosivo, mapa):
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
            "InimigoExplosivo": {
                "x": inimigo_explosivo.rect.x,
                "y": inimigo_explosivo.rect.y,
                "vida": inimigo_explosivo.vida,
                "raio_explosao": inimigo_explosivo.raio_explosao
            },
            "poderes": [
                {
                "x": poder.rect.x,
                "y": poder.rect.y,
                "tipo": poder.tipo
                }
                for poder in mapa.poderes
            ],
            "blocos": [
                {
                "x": bloco.rect.x,
                "y": bloco.rect.y,
                "destrutivel": bloco.destrutivel,
                "imagem": bloco._image_path  # Usando o caminho da imagem correto
                }
                for bloco in mapa.blocos
            ]
        }

        with open(self.__nome_arquivo, 'w') as arquivo:
            json.dump(dados_jogo, arquivo)

        print('Jogo salvo!')

   def carregar_jogo(self, jogador, inimigo, inimigo_explosivo, mapa):
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

        # Restaura os dados do inimigo explosivo
        inimigo_explosivo.rect.x = dados_jogo["InimigoExplosivo"]["x"]
        inimigo_explosivo.rect.y = dados_jogo["InimigoExplosivo"]["y"]
        inimigo_explosivo.vida = dados_jogo["InimigoExplosivo"]["vida"]
        inimigo_explosivo.raio_explosao = dados_jogo["InimigoExplosivo"]["raio_explosao"]

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

        # Limpa os poderes existentes e restaura os poderes salvos
        mapa.poderes.empty()
        for dados_poder in dados_jogo["poderes"]:
            poder = Poder(
                posicao=(dados_poder["x"], dados_poder["y"]),
                tamanho=dados_poder["tamanho"],
                tipo=dados_poder["tipo"]
            )
            mapa.poderes.add(poder)

        print("Jogo carregado com sucesso.")

    except FileNotFoundError:
        print("Nenhum arquivo de salvamento encontrado.")
