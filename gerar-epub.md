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

```bash
docker run --rm \
  -v "$PWD:/book" \
  -w /book \
  ruby \
  sh -c "gem install asciidoctor-epub3 --no-document &&
         asciidoctor-epub3 vol1/vol1-cor.adoc \
           -o '/book/Python Fluente, Segunda Edição (2026), Volume 1 - Dados e Funções.epub' &&
         asciidoctor-epub3 vol2/vol2-cor.adoc \
           -o '/book/Python Fluente, Segunda Edição (2026), Volume 2 - Classes e Protocolos.epub' &&
         asciidoctor-epub3 vol3/vol3-cor.adoc \
           -o '/book/Python Fluente, Segunda Edição (2026), Volume 3 - Controle e Metaprogramação.epub'"
```

Neste comando:

- `--rm`: remove o container automaticamente após a execução;
- `-v "$PWD:/book"`: monta a raiz do repositório no diretório `/book` dentro do container;
- `-w /book`: define a raiz do repositório como diretório de trabalho;
- `gem install asciidoctor-epub3 --no-document`: instala a ferramenta responsável pela geração dos arquivos EPUB sem baixar a documentação das gems;
- `asciidoctor-epub3 vol1/vol1-cor.adoc`: gera o EPUB do Volume 1;
- `asciidoctor-epub3 vol2/vol2-cor.adoc`: gera o EPUB do Volume 2;
- `asciidoctor-epub3 vol3/vol3-cor.adoc`: gera o EPUB do Volume 3;
- os arquivos gerados são salvos na raiz do repositório.

Após a execução, os três arquivos `.epub` serão salvos na raiz do repositório. Basta enviá-los para o seu leitor de e-books.
