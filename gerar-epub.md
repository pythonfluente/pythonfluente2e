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
docker run -it --rm \
  -v "$PWD:/book" \
  -w /book/online \
  ruby \
  sh -c "gem install asciidoctor-epub3 --no-document &&
         asciidoctor-epub3 Livro.adoc \
           -o '/book/Python Fluente, Segunda Edição (2023).epub'"
```

Neste comando:

- `-it`: executa o container em modo interativo;
- `--rm`: remove o container automaticamente após a execução;
- `-v "$PWD:/book"`: monta a raiz do repositório no diretório `/book` dentro do container;
- `-w /book/online`: define `/book/online` como diretório de trabalho, onde está localizado o arquivo mestre `Livro.adoc`;
- `gem install asciidoctor-epub3 --no-document`: instala a ferramenta responsável pela geração do EPUB sem baixar a documentação das gems;
- `asciidoctor-epub3 Livro.adoc`: processa o arquivo `/book/online/Livro.adoc`;
- `-o '/book/Python Fluente, Segunda Edição (2023).epub'`: salva o EPUB gerado na raiz do repositório.


Após isso o container irá executar e salvar automaticamente o livro `.epub` em sua máquina. Basta agora enviar o arquivo para o seu leitor de e-books.
