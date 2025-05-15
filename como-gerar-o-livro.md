# Gerando o livro apartir do fonte

## Instale as dependências necessárias.

### Ruby

#### Linux

##### ubuntu

```
sudo apt-get install -y ruby
```

##### arch

```
sudo pacman -S ruby`
```

#### Mac OS

Com o [Homebrew](https://brew.sh/) instalado use o comando abaixo: 

```
brew install ruby
```

#### Windows


Com o [Chocolatey](https://chocolatey.org/) instalado use o comando abaixo: 

```
choco install ruby
```

### Asciidoctor-epub3

```
gem install asciidoctor-epub3
```

### Gerando livro no formato epub.

Na raiz do projeto rode o comando:

```
asciidoctor-epub3 livro.adoc -o 'Python Fluente - Luciano Ramalho, Segunda Edição (2023).epub'
```
