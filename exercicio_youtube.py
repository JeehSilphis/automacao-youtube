import os
import sys
from getpass import getpass
import pyautogui as py
import pygetwindow as gw
import time as t
from PIL import Image

# imagens dos botões: ficam na mesma pasta deste arquivo e, no executável (.exe),
# vão dentro dele (o PyInstaller as extrai para a pasta guardada em sys._MEIPASS)
PASTA = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
BOTAO_LOGIN = os.path.join(PASTA, "botao_login.png")        # "Fazer login" do youtube.com
CAIXA_BUSCA = os.path.join(PASTA, "caixa_busca.png")        # caixa "Pesquisar" do youtube.com
PRIMEIRO_VIDEO = os.path.join(PASTA, "primeiro_video.png")  # título do vídeo da música
USAR_OUTRA_CONTA = os.path.join(PASTA, "usar_outra_conta.png")  # tela "Escolha uma conta"

janela = None  # janela do Chrome aberta pelo script 


def procurar_e_clicar(arquivo_imagem, tempo_maximo=15):
    """Procura a imagem na tela por alguns segundos e clica no centro dela."""
    imagem = Image.open(arquivo_imagem)  # Pillow: funciona em pasta com acento
    fim = t.time() + tempo_maximo
    while t.time() < fim:
        try:
            posicao = py.locateCenterOnScreen(imagem, confidence=0.8, grayscale=True)
        except py.ImageNotFoundException:
            posicao = None
        if posicao:
            py.moveTo(posicao)  # move o mouse
            py.click()          # click do mouse
            return True
        t.sleep(0.5)  # ainda não apareceu: tenta de novo
    print("Não encontrei na tela:", arquivo_imagem)
    return False


def titulo_do_chrome():
    """Título da aba aberta na janela do Chrome do script (em minúsculas)."""
    try:
        return janela.title.lower()
    except Exception:
        return ""


def esperar_pagina(condicao, tempo_maximo, aviso):
    """Espera a página do Chrome atender a condição (por exemplo, sair da tela de verificação)."""
    avisou = False
    fim = t.time() + tempo_maximo
    while t.time() < fim:
        if condicao(titulo_do_chrome()):
            return True
        if not avisou and "confirme que é você" in titulo_do_chrome():
            print("O Google pediu verificação: resolva no Chrome e clique em Avançar.")
            avisou = True
        t.sleep(1)
    print(aviso)
    return False


def focar_chrome():
    """Traz a janela do Chrome do script de volta para a frente antes de digitar.

    Se você clicou no VS Code (por exemplo, para ler uma mensagem), sem isso
    o texto seria digitado no VS Code e não no Chrome.
    """
    if janela is None:
        return
    ativa = gw.getActiveWindow()
    if ativa is not None and ativa._hWnd == janela._hWnd:
        return  # o Chrome já está na frente
    janela.minimize()   # minimizar e restaurar faz o Windows
    t.sleep(0.3)        # trazer a janela para a frente
    janela.restore()
    t.sleep(0.3)
    janela.maximize()
    t.sleep(1)


# pede a conta Google ao abrir (nada fica gravado no código nem no executável)
EMAIL = input("E-mail da conta Google: ").strip()
SENHA = getpass("Senha (não aparece enquanto você digita): ")
print("Não mexa no mouse nem no teclado até o fim...")
t.sleep(2)

# 1) abre o Google pelo menu Iniciar
print("1) Abrindo o Google...")
t.sleep(0.5)  # tempo de pausa
py.press("winleft")  # tecla windows
py.write("google")  # abre o navegador
py.press("enter")  # tecla enter, botões de ação única

# espera a janela do Chrome aparecer na frente e guarda qual é ela
fim = t.time() + 15
while t.time() < fim:
    ativa = gw.getActiveWindow()
    if ativa is not None and ativa.title.endswith("Google Chrome"):
        janela = ativa
        break
    t.sleep(0.5)

# maximiza a janela do navegador
print("2) Maximizando a janela...")
if janela is not None:
    janela.maximize()
t.sleep(1)  # pequena pausa para garantir que a janela foi maximizada

# digita youtube.com na barra de endereço
print("3) Abrindo o youtube.com...")
py.hotkey("ctrl", "l")  # coloca o cursor na barra de endereço
py.write("youtube.com")
py.press("enter")
t.sleep(4)

#clica em "Fazer login" dentro do YouTube
print("4) Clicando em Fazer login...")
procurar_e_clicar(BOTAO_LOGIN)
t.sleep(5)  # espera a página de login do Google carregar

# se aparecer a tela "Escolha uma conta", clica em "Usar outra conta"
if procurar_e_clicar(USAR_OUTRA_CONTA, tempo_maximo=5):
    t.sleep(5)  # espera abrir o campo de e-mail

# 5) faz o login
print("5) Digitando o e-mail...")
focar_chrome()
py.write(EMAIL, interval=0.1)  # e-mail informado ao abrir
py.press("enter")  # tecla enter, botões de ação única
t.sleep(3)

# espera sair da tela do e-mail e da verificação (se houver) e chegar na tela da senha
print("   Esperando a tela da senha...")
esperar_pagina(
    lambda titulo: titulo != "" and "fazer login" not in titulo and "confirme que é você" not in titulo,
    tempo_maximo=120,
    aviso="A tela da senha não apareceu.",
)
t.sleep(3)  # espera o campo de senha ficar pronto

print("   Digitando a senha...")
focar_chrome()  # garante que a senha vai ser digitada no Chrome
py.write(SENHA, interval=0.1)  # senha informada ao abrir
py.press("enter")  # tecla enter, botões de ação única

# espera voltar para o YouTube (se o Google pedir código por SMS, espera você digitar)
print("   Esperando voltar para o YouTube...")
esperar_pagina(
    lambda titulo: "youtube" in titulo and "confirme que é você" not in titulo,
    tempo_maximo=180,
    aviso="Não voltou para o YouTube.",
)
t.sleep(3)
focar_chrome()  # garante que a busca vai ser feita no Chrome

# 6) busca a música (só digita se a caixa de busca do YouTube aparecer)
print("6) Buscando a música...")
if procurar_e_clicar(CAIXA_BUSCA, tempo_maximo=30):  # clica na caixa de busca
    py.write("metallica whisky in the jar") #digite aqui o que quer buscar no YouTube
    py.press("enter")
    t.sleep(4)

    # 7) clica no vídeo da música
    print("7) Abrindo o vídeo...")
    if os.path.exists(PRIMEIRO_VIDEO):
        procurar_e_clicar(PRIMEIRO_VIDEO)
    else:
        print("Falta a imagem primeiro_video.png para clicar no vídeo.")
else:
    print("A caixa de busca do YouTube não apareceu: a busca não foi feita.")

print("Fim.")
