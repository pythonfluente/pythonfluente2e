# Procedimentos para preparar volumes para impressão

## Operações

### Nos arquivos da edição online:

1. Eliminar duplicação de atributos entre cabeçalhos de `capN.adoc`, `atributos-pt_BR.adoc`, `Livro.adoc`, `Volume1.adoc`...
2. Encurtar links já presentes
3. Quebrar linhas longas (semantic linebreaks)
4. Retirar inline pass macros[^1]
5. Gerar PDF para impressão
6. Revisar PDF, aplicar correções no `.adoc`

[^1]: https://docs.asciidoctor.org/asciidoc/latest/pass/pass-macro/

### Nos arquivos separados por volume

1. Trocar xrefs para outros volumes: _Título do alvo (v2:c8 fpy.li/xy)_
2. Gerar PDF para impressão
3. Revisar PDF, aplicar correções no `.adoc`

## Semantic line breaks

Atenção: legendas de figuras tem que ter apenas uma linha lógica.

A legenda começa com . e não pode ser quebrada em várias linhas. Exemplo:

```
[[vectors_fig]]
.Soma de vetores bi-dimensionais: `Vector(2, 4) + Vector(2, 1)` devolve `Vector(4, 5)`.
image::images/flpy_0101.png[vetores 2D]
```