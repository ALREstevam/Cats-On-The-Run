# Resolução de Problemas - Trabalho II (Catcher)

## Grupo

* André L. R. Estevam RA: 166348
* Caroline Lucas Calheirani RA: 168926
* Mayara Naomi Fustaino Ramos RA: 184517


## Execução

O pegador é ativado pela execução do arquivo `my_catcher.py`. O mesmo diretório deve conter o arquivo `HexDistance.py`.


### Outros códigos desenvolvidos/modificados
* `game.py`
	* alterado para:
		* Gerar arquivos `.gif` coloridos
		* Modficar o desenho do gato
		* Testar se o catcher devolveu uma posição fora do tabuleiro
		* Mostrar no modo debug quais coordenadas enviadas pelo catcher que causaram o erro

* `confs.py` - armazena os dados do teste, é importado por `multithread_tester.py`
* `multithread_tester.py` - código para testar os 100 inputs usando multithreading

## Estrutura básica do projeto

        │   `confs.bat` - arquivo que testa 100 tabuleiros 
        │   `game.py` - arquivo que controla um jogo
        │   `gato.py` - gato
        │   `multithread_tester.py` - testa jogos usando mais de uma thread
        │   `my_catcher.py` - catcher desenvolvido
        │   `pegador.py` - catcher fornecido pelo professor
        │   `plano.pdf` - arquivo com a explicação do trabalho
        │
        ├───`games` - armazena arquivos .gif com a execução
        │       `game_0.gif`
        │
        └───`tabuleiros` - armazena tabuleiros vazios em diversos formatos
                `tabuleiro.bmp`
                `tabuleiro.eps`
                `tabuleiro.gif`
                `tabuleiro.jpg`
                `tabuleiro.png`
                `tabuleiro.tga`
                `tabuleiro.tif` 


# Acesso no GitHub

[Todos os projetos da disciplina](https://github.com/ALREstevam/Cats-On-The-Run)
[Projeto II](https://github.com/ALREstevam/Cats-On-The-Run/tree/master/project2)