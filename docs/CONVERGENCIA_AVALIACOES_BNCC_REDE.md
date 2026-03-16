# Convergencia entre Avaliacoes Externas, BNCC e Matriz Curricular da Rede

## Objetivo
Criar um documento-base para convergencia entre:
- `CNCA/CAEd` (`1o-5o ano`)
- `Avaliacao Continua da Aprendizagem nos Anos Finais` (`6o-9o ano`)
- `Saeb` (matriz historica e matrizes BNCC de referencia)
- habilidades da `BNCC`
- futura matriz curricular da rede municipal

Este artefato nao substitui a matriz curricular da rede. Ele funciona como camada de traducao e governanca para futuras adequacoes a diferentes redes.

## Leitura metodologica
A convergencia pode ocorrer em tres niveis:
- `direta`: quando a propria matriz de avaliacao ja explicita o codigo BNCC
- `mediada`: quando a matriz de avaliacao apresenta uma tarefa de producao ou descritor sem codigo BNCC explicito e a rede precisa fazer a ponte curricular
- `complementar`: quando a referencia `Saeb` ajuda a manter comparabilidade e coerencia sem ser a fonte operacional principal do modelo atual

## Fontes de referencia utilizadas
- `docs/references/cnca/CNCAGuiadaAvaliaoContnua.pdf`
- `docs/references/cnca/MEC_2026_CNCA_Av_Cont_Apren_Matriz_Ref.pdf`
- `docs/references/cnca/MEC_2025-Matriz_Anos_Finais.pdf`
- `docs/references/saeb/matriz_linguaportuguesa-base-saeb-2001.pdf`
- `docs/references/saeb/matriz_matematica-base-saeb-2001.pdf`
- `docs/references/saeb/matriz-de-referencia-de-linguagens_BNCC-2018.pdf`
- `docs/references/saeb/matriz-de-referencia-de-matematica_BNCC-2018.pdf`
- `docs/references/redes/mendes/`
  - base curricular municipal atual versionada no projeto, preparada para futura substituicao por outra rede em `docs/references/redes/<rede>/`

## Regras para uso no projeto
- `1o-5o ano`: usar `CNCA` como referencia operacional principal
- `6o-9o ano`: usar `MEC Anos Finais BNCC` como referencia operacional principal
- `Saeb`: usar como referencia complementar de comparabilidade, especialmente para `2o`, `5o` e `9o`
- `escrita`: tratar como caso especial, porque nem sempre a matriz traz o codigo BNCC explicitamente no mesmo nivel de granularidade de `leitura` e `matematica`
- `fluencia`: tratar como trilha avaliativa futura, separada do modelo atual de componentes

## Projeto previsto - Fluencia em leitura
- `fluencia` passa a ficar registrada como avaliacao prevista para evolucao do projeto
- base documental atual:
  - `CNCA/CAEd` com bloco de `fluencia em leitura`
  - cobertura identificada nos documentos atuais: `2o-5o ano`
- status atual:
  - nao implementada no schema
  - nao implementada na API
  - nao implementada no BI
- orientacao:
  - tratar `fluencia` como projeto proprio de avaliacao
  - nao misturar `fluencia` com `percentual no esperado` de leitura no modelo atual
  - quando evoluir, criar contrato proprio com:
    - `tipo_avaliacao = fluencia`
    - metrica especifica
    - janela de aplicacao
    - regra de interpretacao separada de leitura/escrita/matematica

## Tabela 1 - Estrutura-base de convergencia por etapa e componente
| Etapa | Componente | Fonte principal | Tipo de ancoragem BNCC | Papel do Saeb | Uso recomendado na rede |
| --- | --- | --- | --- | --- | --- |
| 1o-5o | Leitura | CNCA/CAEd | Direta em boa parte da matriz | Complementar | alinhar descritor avaliativo a habilidade BNCC e objeto curricular da rede |
| 1o-5o | Escrita | CNCA/CAEd | Mediada em boa parte da matriz | Complementar/limitado | alinhar genero/tarefa de producao a expectativa curricular da rede |
| 1o-5o | Matematica | CNCA/CAEd | Direta em boa parte da matriz | Complementar | alinhar unidade tematica, habilidade BNCC e progressao da rede |
| 2o-5o | Fluencia em leitura | CNCA/CAEd | Sem ancoragem BNCC explicita por codigo no quadro de fluencia | Sem papel central | tratar como trilha complementar de avaliacao, com governanca propria |
| 6o-9o | Leitura | MEC Anos Finais BNCC | Direta na matriz | Complementar | alinhar habilidade avaliativa a eixo e objeto curricular da rede |
| 6o-9o | Escrita | MEC Anos Finais BNCC | Mediada na matriz de escrita | Complementar/limitado | alinhar tarefa de escrita a genero, finalidade e criterio da rede |
| 6o-9o | Matematica | MEC Anos Finais BNCC | Direta na matriz | Complementar | alinhar habilidade avaliativa a objeto matematico e expectativa da rede |

## Tabela 2 - Crosswalk inicial de referencia
| Etapa | Componente | Fonte | Codigo origem | Descritor/habilidade de avaliacao | Ancoragem BNCC | Tipo | Campo para matriz da rede | Observacoes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1o ano | Leitura | CNCA/CAEd | `1EF11_P` | Localizar informacoes explicitas em textos, recuperadas por repeticao | `EF15LP03` | Direta | Preencher com habilidade equivalente da rede | bom ponto de entrada para eixo de leitura literal |
| 1o ano | Leitura | CNCA/CAEd | `1EF15_P` | Identificar a finalidade de um texto do campo da vida cotidiana | `EF15LP01` | Direta | Preencher | relaciona avaliacao externa ao campo de atuacao da vida cotidiana |
| 1o ano | Escrita | CNCA/CAEd | `1EF02_E` | Escrever palavras, com correspondencias regulares diretas, a partir de uma imagem | Nao explicita no quadro de escrita | Mediada | Preencher com habilidade da matriz da rede ligada a escrita alfabetica | exige definicao curricular local do nivel de dominio esperado |
| 1o ano | Matematica | CNCA/CAEd | `1EF04_M` | Utilizar adicao entre numeros naturais envolvendo juntar ou acrescentar | `EF01MA08` | Direta | Preencher | ancora bem a progressao inicial de numero e operacao |
| 2o ano | Leitura | CNCA/CAEd | `2EF08_P` | Localizar informacoes explicitas em textos, recuperadas por parafrase | `EF15LP03` | Direta | Preencher | util para calibrar progressao entre leitura literal e inferencial |
| 2o ano | Fluencia em leitura | CNCA/CAEd | `D001_D` | Ler palavras oralmente | Nao explicita no quadro de fluencia | Mediada | Preencher com expectativa da rede para fluencia/leitura oral | registrar separadamente de leitura de compreensao |
| 2o ano | Fluencia em leitura | CNCA/CAEd | `D003_D` | Ler textos oralmente | Nao explicita no quadro de fluencia | Mediada | Preencher | exige futura definicao de metrica propria da rede |
| 2o ano | Escrita | CNCA/CAEd | `2EF04_E` | Produzir um bilhete a partir de uma dada situacao | Nao explicita no quadro de escrita | Mediada | Preencher com genero e expectativa da rede | a convergencia deve considerar genero, finalidade e adequacao ao contexto |
| 2o ano | Matematica | Saeb BNCC 2018 | `2N2.1` | Resolver problemas de adicao ou subtracao com numeros naturais de ate 3 ordens | Matriz Saeb BNCC 2018 - Numeros | Direta | Preencher | funciona como referencia complementar de progressao para o 2o ano |
| 2o ano | Leitura | Saeb BNCC 2018 | Sem codigo de descritor legacy | Localizar informacoes explicitas em textos | Matriz Saeb BNCC 2018 - Leitura | Complementar | Preencher | ajuda a aproximar CNCA e referencia nacional do 2o ano |
| 2o ano | Escrita | Saeb BNCC 2018 | Sem descritor operacional equivalente | Escrever texto | Matriz Saeb BNCC 2018 - Producao textual | Complementar/mediada | Preencher | usar apenas como ancora macro, nao como descritor 1:1 |
| 5o ano | Leitura | Saeb base 2001 | `D1` | Localizar informacoes explicitas em um texto | Converge com matriz Saeb BNCC 2018 - Leitura / localizar informacao explicita | Complementar | Preencher | preserva comparabilidade historica da avaliacao externa |
| 5o ano | Leitura | Saeb base 2001 | `D11` | Distinguir um fato da opiniao relativa a esse fato | Converge com matriz Saeb BNCC 2018 - Leitura / distinguir fatos de opinioes | Complementar | Preencher | importante para leitura critica em anos iniciais finais |
| 5o ano | Matematica | Saeb base 2001 | `D26` | Resolver problema envolvendo nocoes de porcentagem | Converge com `5N2.7` da matriz Saeb BNCC 2018 | Complementar | Preencher | bom ponto para alinhar referencia externa e progressao da rede |
| 6o ano | Leitura | MEC Anos Finais BNCC | `6EF02_P` | Localizar informacoes explicitas em textos de nivel 2 recuperando-as por parafrase | `EF69LP03` | Direta | Preencher | ancora a entrada nos anos finais com leitura informacional |
| 6o ano | Leitura | MEC Anos Finais BNCC | `6EF10_P` | Identificar a finalidade de generos publicitarios e jornalisticos | `EF69LP17` | Direta | Preencher | util para alinhar campo jornalistico-midiatico |
| 6o ano | Escrita | MEC Anos Finais BNCC | `6EF02_E` | Produzir uma noticia | Nao explicita no quadro de escrita | Mediada | Preencher com genero, finalidade e criterios da rede | exige rubrica curricular da rede para consolidar a convergencia |
| 6o ano | Matematica | MEC Anos Finais BNCC | `6EF05_M` | Utilizar adicao ou subtracao entre numeros racionais positivos em representacao fracionaria | `EF06MA10` | Direta | Preencher | boa ancora para fracao e racional nos anos finais |
| 9o ano | Leitura | MEC Anos Finais BNCC | `9EF25_P` | Identificar a tese de um texto de nivel 3 a partir da leitura global | `EF89LP04` | Direta | Preencher | importante para textos argumentativos e leitura critica |
| 9o ano | Leitura | MEC Anos Finais BNCC | `9EF20_P` | Reconhecer relacoes logico-discursivas em textos de nivel 3 | `EF09LP11` | Direta | Preencher | convergencia forte com analise linguistica e argumentacao |
| 9o ano | Escrita | MEC Anos Finais BNCC | `9EF02_E` | Produzir um texto de opiniao com introducao, tese, dois ou mais argumentos e conclusao | Nao explicita no quadro de escrita | Mediada | Preencher com habilidade e rubrica da rede | aqui a rede precisa definir claramente padrao de producao e correcao |
| 9o ano | Matematica | MEC Anos Finais BNCC | `9EF01_M` | Utilizar porcentagem, com ou sem percentuais sucessivos, na resolucao de problema | `EF09MA05` e `EF07MA02` | Direta | Preencher | bom elo entre avaliacao externa e objetos da rede sobre porcentagem |
| 9o ano | Matematica | MEC Anos Finais BNCC | `9EF07_M` | Utilizar semelhanca de triangulos na resolucao de problema | `EF09MA12` | Direta | Preencher | ancora geometria com progressao clara para anos finais |
| 9o ano | Matematica | Saeb BNCC 2018 | `9N2.3` | Resolver problemas que envolvam porcentagens, incluindo acrescimos e decrescimos | Matriz Saeb BNCC 2018 - Numeros | Complementar | Preencher | ajuda a manter linguagem comum com referencia nacional |

## Tabela 3 - Casos que exigem convergencia mediada pela rede
| Caso | Motivo | Acao recomendada |
| --- | --- | --- |
| Escrita no CNCA | o quadro de escrita nao explicita codigo BNCC na mesma forma de leitura e matematica | criar rubrica interna da rede por genero, finalidade, nivel de autonomia e convencoes da escrita |
| Escrita nos anos finais | a matriz traz tarefa de producao, mas nao explicita a correspondencia BNCC por codigo no quadro | cruzar genero solicitado, finalidade comunicativa e criterio de correcao com a matriz curricular da rede |
| Fluencia em leitura no CNCA | o bloco de fluencia funciona como trilha propria de leitura oral e nao deve ser confundido com compreensao leitora | criar projeto proprio de fluencia, com metrica, rubrica e periodicidade separadas |
| Saeb base 2001 em Lingua Portuguesa | descritores historicos focam leitura e comparabilidade, nao uma matriz de escrita operacional | usar como referencia complementar, nao como unica ancora para escrita |
| Matriz curricular municipal versionada, mas ainda nao cruzada linha a linha | a documentacao-base da rede agora existe no repo, mas o preenchimento da convergencia ainda depende de trabalho pedagogico | preencher a coluna `Campo para matriz da rede` usando `docs/references/redes/mendes/` como fonte curricular oficial local |

## Como usar esta base na rede municipal
1. Definir a pasta de rede oficial em `docs/references/redes/<rede>/`.
2. Copiar a `Tabela 2` para um artefato operacional da rede.
3. Preencher a coluna `Campo para matriz da rede` com:
   - codigo da habilidade local
   - descricao da expectativa curricular
   - periodo letivo esperado
   - evidencias/instrumentos da rede
4. Validar com equipe pedagogica os casos de convergencia `mediada`.
5. So depois transformar esse crosswalk em regra de BI, analise ou monitoramento.

## Limites assumidos neste documento
- este documento e uma base de convergencia, nao uma rubrica completa de correcao
- `escrita` exige trabalho pedagogico adicional da rede para chegar a uma equivalencia curricular robusta
- `fluencia` esta apenas registrada como projeto futuro e nao compoe o modelo operacional atual
- `Saeb` continua importante para comparabilidade, mas nao substitui as fontes operacionais `CNCA` e `MEC Anos Finais BNCC` no modelo atual do projeto

