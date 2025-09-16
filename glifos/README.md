# Tofu, ou glifos fantando

Glifos são as figuras dos caracteres. Na falta de um glifo,
o software usado para exibir o texto mostra um caractere alternativo,
geralmente um retângulo branco apelidado de "tofu".

As fontes padrão do `asciidoctor-pdf` não têm os glifos de
todos os caracteres que usei no *Python Fluente Segunda Edição*.
Por isso inicialmente o PDF para imprimir exibia dúzias de tofu.

> O problema não acontece nos navegadores exibindo o livro em HTML:
> https://pythonfluente.com.

## Diagnosticar o problema

Para diagnosticar o problema, escrevi o script `list_symbols.py` que lê
`stdin` ou arquivos de uma lista de argumentos na linha de comando,
e gera no `stdout` um arquivo `.adoc` com cada um dos caracteres
não-ASCII que aparecem nos arquivos de entrada, bem como sua contagem.

## Solução

### Plano A

O ideal seria configurar o `asciidoctor-pdf` para usar o conceito
de *fallback font*: uma ou mais fonte alternativas onde encontrar
os glifos faltando.
Em tese, todos os glifos necessários existem na coleção de fontes Noto.

Mas a fonte Noto usada pelo `asciidoctor-pdf` não tem todos os glifos,
e minhas tentativas de usar fallback fracassaram.

### Plano B

Eu poderia editar a fonte Noto que vem com o `asciidoctor-pdf` para
incluir algumas dúzias de glifos necessários para o *Python Fluente*,
mas a documentação do Asciidoctor alerta que há vários truques necessários
para que uma fonte moderna como a Noto funcionem com a biblioteca
`prawn` em Ruby, usada pelo `asciidoctor-pdf`.

Como não sou especialista em fontes, esse plano ficou inviável.

### Plano C

Descobri que a maioria dos tofus estão no capítulo 4 cujo tema é Unicode.
Alguns símbolos de operações de conjunto aparecem no capítulo 3, sobre
dicts e sets.

Com o prazo acabando, removi os caracteres que apareciam como tofu
no capítulo 2, e coloquei notas explicando o problema no capítulo 4.