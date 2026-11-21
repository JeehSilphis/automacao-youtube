# Automação do YouTube com PyAutoGUI

Script em **Python** que controla o mouse e o teclado para abrir o navegador, entrar no YouTube,
fazer login, buscar uma música e abrir o vídeo, sozinho, como se fosse uma pessoa usando o computador.

Exercício da disciplina de **Sistemas de Informação**.

## O que o script faz

1. Pede o **e-mail** e a **senha** da conta Google (a senha não aparece enquanto você digita)
2. Abre o **Google Chrome** pelo menu Iniciar e **maximiza** a janela
3. Digita **youtube.com** na barra de endereço
4. Clica em **Fazer login** (e em **Usar outra conta**, se o Google mostrar a escolha de contas)
5. Digita o e-mail
6. Se o Google pedir a confirmação **"Não sou um robô"**, espera você resolver (até 2 minutos)
7. Digita a senha
8. Se o Google pedir outra verificação (por exemplo, um **código por SMS**), espera você concluir (até 3 minutos)
9. Clica na caixa **Pesquisar** do YouTube e busca *metallica whisky in the jar*
10. Clica no vídeo da música

Os botões são encontrados **pela imagem**, não por coordenadas fixas: o script procura na tela
os recortes `.png` e clica no centro deles. Assim ele continua funcionando mesmo que o botão
mude de lugar na tela.

## Como executar

### Opção 1: executável (sem instalar nada)

Dê dois cliques em **`exercicio_youtube.exe`**, informe o e-mail e a senha e **não mexa no mouse
nem no teclado** até o fim. As imagens dos botões já estão dentro do executável.

> Na primeira vez, o Windows Defender pode mostrar um alerta. Clique em
> **Mais informações → Executar assim mesmo**.

### Opção 2: pelo código Python

Instale as bibliotecas (uma vez só):

```
pip install pyautogui pygetwindow pillow opencv-python
```

Depois execute, na pasta do projeto:

```
python exercicio_youtube.py
```

O andamento aparece no terminal, passo a passo (`1) Abrindo o Google...`, `2) Maximizando a janela...` etc.).

## Verificação do Google

Como o login é digitado por um programa, o Google pode pedir uma confirmação:
**"Não sou um robô"** ou um **código por SMS**. Essas telas existem para barrar automação e
precisam ser resolvidas por você. O script **espera** você resolver no Chrome e continua sozinho
em seguida.

## Arquivos

| Arquivo | Conteúdo |
|---|---|
| `exercicio_youtube.py` | Código do script |
| `exercicio_youtube.exe` | Executável gerado com PyInstaller |
| `exercicio_youtube.spec` | Configuração do PyInstaller usada para gerar o executável |
| `botao_login.png` | Botão "Fazer login" do YouTube |
| `usar_outra_conta.png` | Opção "Usar outra conta" do Google |
| `caixa_busca.png` | Caixa "Pesquisar" do YouTube |
| `primeiro_video.png` | Título do vídeo da música nos resultados |

## Como gerar o executável novamente

```
pip install pyinstaller
python -m PyInstaller exercicio_youtube.spec
```

O novo executável fica na pasta `dist`.

## Dicas

- As imagens foram recortadas numa tela de **1366×768** com o zoom do navegador em **100%**.
  Em outra resolução ou zoom, recorte os botões de novo (**Win + Shift + S**) e salve com os mesmos nomes.
- Para buscar outra música, troque o texto em `py.write("metallica whisky in the jar")` e
  recorte o título do vídeo nos resultados como `primeiro_video.png`.
- Nenhum e-mail ou senha fica gravado no código ou no executável: eles são pedidos toda vez que o script abre.

## Tecnologias

- Python 3
- [PyAutoGUI](https://pyautogui.readthedocs.io/): mouse, teclado e busca de imagens na tela
- PyGetWindow: controle das janelas (trazer para a frente e maximizar)
- Pillow e OpenCV: leitura e comparação das imagens
- PyInstaller: geração do executável

## Autoria

Desenvolvido por [Jéssica Soares](https://github.com/JeehSilphis).
