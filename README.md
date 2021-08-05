# <img src="mn2-logo.svg" width="64" style="vertical-align: -0.5em; float: left; margin-right: 10px; margin-top: -0.5em;"> Biblioteca de Métodos Numéricos II

Esta é a biblioteca implementada ao longo do curso da disciplina de Métodos Numércos II. Nela temos códigos para trabalhar com álgebra linear de forma genérica e também formas de tratar e apresentar os dados em vários formatos.

## Instalação da biblioteca no Python

### Instalação em modo de desenvolvimento

O modo desenvolvimento serve para poder instalar a biblioteca no ambiente Python, de forma os arquivos fonte possam ser modificados sem necessitar a reinstalação da biblioteca, ou seja, a instalação mantém referências ao invés de copiar os arquivos de código fonte.

Rode o comando abaixo para instalar a biblioteca em modo de desenvolvimento:

```bash
python setup.py develop
```

No Linux ou Mac, talvez seja necessário usar `sudo`:

```bash
sudo python setup.py develop
```

No Windows um terminal com permissões elevadas terá de ser usado. Para fazer isso pressione <kbd>windows-key</kbd>+<kbd>x</kbd>, e então selecione `Command Prompt (Admin)` ou `Windows Powershell (Admin)`. Navegue até o diretório do projeto e rode o comando indicado anteriormente.

Se quiser instalar o biblioteca em um ambiente virtual, lembre-se de ativar o mesmo antes da instalação, por exemplo:

```bash
conda activate base
```

Ou pelo menos verifique se o ambiente atual é o correto:

- Linux: `which python` ou `which python3`
- Windows: `where python`

### Instalando direto do repositório no GitHub

A instalação pode ser feita diretamente a partir do repositório no GitHub com o comando:

```
pip install git+https://github.com/Metodos-Numericos-II/biblioteca.git
```

Para instalar a partir do Google Colab, basta por um `"!"` antes do comando acima, em uma célula do notebook Jupyter do Colab, e depois executando a célula. Fica assim:

```
!pip install git+https://github.com/Metodos-Numericos-II/biblioteca.git
```

Lembrando que no caso de instalar diretamente a partir do repositório, a branch utilizada será a `main`.

## Usando a biblioteca

Depois de instalar a biblioteca, é possíve importar o pacote `mn2`, e também os seus submódulos:

```python
import mn2
```

Exemplo de importação da classe `Texto` do submódulo `mn2.texto`:

```python
from mn2.texto as Texto
```

## Organização da biblioteca

Os códigos específicos dos tópicos (grupo) podem ser colocados dentro de uma subpasta do tópico dentro de `src/mn2`. Os códigos genéricos vamos arrumar com o tempo, diretamente dentro da pasta `src/mn2`.

### Visual Studio Code

O VSCode pode ter problemas para debugar se houverem múltiplos ambientes virtuais. Isso acontece pois o VSCode não consegue saber qual é o ambiente virtual correto.

Para corrigir isso é possível alterar o ambiente a ser utilizado na configuração `python.pythonPath`.

Digite <kbd>ctrl</kbd>+<kbd>,</kbd> para abrir o painel de configurações, e producre por `python.pythonPath`. Então, na aba `User`, selecione o interpretador Python correto.

Também é possível alterar o interpretador Python do conjunto de trabalho do VSCode (workspace) no arquivo `settings.json`. Mas não se esqueça que essa configuração não pode ser submetida para o repositório pois é algo local do seu computador. Se isso for mandado para o repositório, outros desenvolvedores vão ver um erro sem explicação, o que pode deixar todos bem confusos.

Também é possível alterar o interpretador Python do conjunto de trabalho do VSCode (workspace) no arquivo `settings.json`. Mas não se esqueça que essa configuração não pode ser submetida para o repositório pois é algo local do seu computador. Se isso for mandado para o repositório, outros desenvolvedores vão ver um erro sem explicação, o que pode deixar todos bem confusos.