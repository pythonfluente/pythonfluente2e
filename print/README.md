# Procedimentos para preparar volumes para impressão

## Rever ISBN na página de copyright e na contra-capa

Python Fluente, 2ª edição...

|volume| variante  | ISBN              |
|------|-----------|-------------------|
|    1 | standard  | 978-65-988962-1-8 |
|      | dunder    | 978-65-988962-0-1 |
|    2 | standard  | 978-65-989778-3-2 |
|      | dunder    | 978-65-989778-2-5 |
|    3 | standard  | 978-65-989778-1-8 |
|      | dunder    | 978-65-989778-6-3 |


## Formatação dos links

Renderize este markdown para ver a *aparência* dos links.
Aqui eles estão escritos em Markdown, mas o livro é Asciidoc,
então a marcação pode ser diferente.

### Links para a web

Leia o _Tutorial do Python_ [fpy.li/3e]


### Links para outro volume

Como veremos na _Seção 11.3_ [vol.2, fpy.li/3f]


## Operações

### Nos arquivos da edição online:

1. Eliminar duplicação de atributos entre cabeçalhos de `capN.adoc`, `atributos-pt_BR.adoc`, `Livro.adoc`, `vol1.adoc`...
2. Encurtar links já presentes
3. Quebrar linhas longas (semantic linebreaks se possível, hard-wrap como plano B)
4. Retirar inline pass macros[^1]

5. Gerar PDF para impressão
6. Revisar PDF, aplicar correções no `.adoc`

[^1]: https://docs.asciidoctor.org/asciidoc/latest/pass/pass-macro/

### Nos arquivos separados por volume

1. Trocar xrefs para outros volumes: _Título do alvo (v2:c8 fpy.li/xy)_
2. Gerar PDF para impressão
3. Revisar PDF, aplicar correções no `.adoc`

## Para gerar o PDF

Na raiz do repositório:

```
./print/pdf_export.sh vol1/vol1.adoc 
```

## Semantic line breaks

Atenção: legendas de figuras tem que ter apenas uma linha lógica.

A legenda começa com . e não pode ser quebrada em várias linhas. Exemplo:

```
[[vectors_fig]]
.Soma de vetores bi-dimensionais: `Vector(2, 4) + Vector(2, 1)` devolve `Vector(4, 5)`.
image::../images/flpy_0101.png[vetores 2D]
```