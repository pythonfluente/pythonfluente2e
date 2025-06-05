# Procedimentos para preparar .adoc para revisão

## Operações

### Nos arquivos da edição online:

✅ Eliminar duplicação de atributos entre cabeçalhos de `capN.adoc`, `atributos-pt_BR.adoc`, `Livro.adoc`, `Volume1.adoc`...
2. Encurtar links já presentes
3. Quebrar linhas longas (semantic linebreaks)
4. Retirar inline pass macros[^1]
5. Gerar PDF para impressão
6. Revisar PDF, aplicar correções no `.adoc`

[^1]: https://docs.asciidoctor.org/asciidoc/latest/pass/pass-macro/

## Cuidados ao automatizar mudanças

### Não reformatar blocos

Não reformatar ou encurtar URLs em:

* blocos de código
* tabelas

### Proteger legendas de figuras

Uma legenda de figura começa com `.` e não pode ser quebrada em várias linhas.

Exemplo:

```
[[vectors_fig]]
.Soma de vetores bi-dimensionais: `Vector(2, 4) + Vector(2, 1)` devolve `Vector(4, 5)`.
image::images/flpy_0101.png[vetores 2D]
```