# Calango

Processador de referências cruzadas para a publicação do 
_Python Fluente Segunda Edição_ impresso em três columes.

## Objetivo

Encontrar e substituir as referências cruzadas que apontam
para volumes diferentes.

Por exemplo, no Capítulo 1, próximo da linha 744 há essa referência:

````adoc
Como implementar [...] será visto no <<ch_seq_methods>>,
````

Como aponta para um capítulo do volume 2, precisa ser reescrita assim:

```adoc
Como implementar [...] será visto no Capítulo 12 [vol.2, fpy.li/xyz],
```

Onde fpy.li/xyz direciona para:

https://pythonfluente.com/2/#ch_seq_methods

