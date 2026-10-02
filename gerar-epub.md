# Como gerar o `epub` a partir dos arquivos fonte

## Pré-requisitos

Para gerar o `.epub` do livro é necessário ter o [Docker](https://docker.com) instalado em sua máquina.

### Docker Ruby Image

Precisamos baixar a [imagem Ruby oficial de Docker](https://hub.docker.com/_/ruby). Podemos fazê-lo com o seguinte comando:

```bash
docker pull ruby
```

Verificando se a imagem Ruby foi baixada.

``` bash
docker images
```

E espera-se o seguinte resultado:

```
REPOSITORY      TAG       IMAGE ID       CREATED         SIZE
ruby            latest    1a74e25729c7   12 days ago     990MB
```

### Clone do repositório

Realize o clone do repositório na sua máquina local.

```bash
git clone https://github.com/pythonfluente/pythonfluente2e.git
cd pythonfluente2e
```

## Executando o build do `epub`

Na raiz do repositório recém clonado, iremos executar um container que irá instalar as dependências para gerar o livro, e gerar o `.epub` na mesma raiz. Basta executar o seguinte comando:

Como a versão 2026 do livro foi divida em 3 partes, iremos executar um comando para cada volume, gerando assim o `.epub` respectivo.
Basta executar os seguintes comandos:

```bash
# Volume 1
docker run -it --rm -v .:/book ruby sh -c "gem install asciidoctor-epub3 && asciidoctor-epub3 /book/vol1/vol1-cor.adoc -o '/book/Python Fluente, Segunda Edição (2026), Volume 1 dados + funções.epub' 2> /dev/null"

# Volume 2
docker run -it --rm -v .:/book ruby sh -c "gem install asciidoctor-epub3 && asciidoctor-epub3 /book/vol2/vol2-cor.adoc -o '/book/Python Fluente, Segunda Edição (2026), Volume 2 classes + protocolos.epub' 2> /dev/null"

# Volume 3
docker run -it --rm -v .:/book ruby sh -c "gem install asciidoctor-epub3 && asciidoctor-epub3 /book/vol3/vol3-cor.adoc -o '/book/Python Fluente, Segunda Edição (2026), Volume 3 controle + metaprogramação.epub' 2> /dev/null"
```

Neste comando:

- `-it`: Permite entrar no modo iterativo.
- `--rm`: Remove o container após a saída.
- `-v .:/book`: Monta o volume com o caminho da pasta raiz no container na em /book.
- `sh -c "gem install asciidoctor-epub3 && asciidoctor-epub3 /book/<vol>.adoc -o '/book/Python Fluente, Segunda Edição.epub' 2> /dev/null"`: Executa o comando especificado dentro do container. O comando faz a instalação do asciidoctor-epub3 dentro do container e realiza o build do livro.

Após isso o container irá executar e salvar automaticamente o livro `.epub` em sua máquina. Basta agora enviar o arquivo para o seu leitor de e-books.
