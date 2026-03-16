# Base de Referencia do IMA Medio

## Objetivo
Registrar a base pedagogica e avaliativa que deve orientar a evolucao do `IMA medio`.

## Status atual do produto
- O `IMA medio` implementado no MVP e uma metrica operacional interna.
- Formula atual: `(percentual_leitura + percentual_escrita) / 2`.
- Esses percentuais sao calculados a partir de contagens agregadas por turma e periodo.
- A metrica atual nao representa, por si so, uma escala oficial de proficiencia do Saeb, do CNCA ou do Avalia RJ.
- Matematica ainda nao compoe o `IMA medio` implementado.

## Decisao de referencia
- A evolucao semantica do `IMA medio` deve tomar como referencia oficial:
  - `Saeb` para `5o` e `9o` ano do Ensino Fundamental em `Lingua Portuguesa` e `Matematica`.
  - `Saeb/CNCA` para `2o` ano do Ensino Fundamental, considerando `leitura`, `escrita` e `matematica`.
  - `Alfabetiza RJ` / `Avalia RJ` como camada estadual de aplicacao diagnostica no Rio de Janeiro, vinculada ao regime de colaboracao do `Compromisso Nacional Crianca Alfabetizada`.
- O `CAEd` deve ser tratado como parceiro/plataforma de operacionalizacao de avaliacoes em larga escala, e nao como a referencia normativa principal da metrica.

## Referencias oficiais adotadas

### 1) Saeb: pagina oficial de matrizes e escalas
- O Inep descreve as matrizes como instrumentos norteadores para construcao de itens e analise de resultados.
- O mesmo portal informa que, para preservar comparabilidade, `Lingua Portuguesa` e `Matematica` do `5o` e `9o` ano ainda usam a matriz historica nas aplicacoes comparaveis.
- Fonte oficial:
  - [Matrizes e Escalas - Inep](https://www.gov.br/inep/pt-br/areas-de-atuacao/avaliacao-e-exames-educacionais/saeb/matrizes-e-escalas)

### 2) Saeb: matrizes de referencia para 5o e 9o ano
- `Lingua Portuguesa`:
  - `5o ano`: procedimentos de leitura; implicacoes do suporte, do genero e/ou do enunciador; relacao entre textos; coerencia e coesao; relacoes entre recursos expressivos; variacao linguistica.
  - `9o ano`: mesma estrutura, com maior complexidade e descritores ampliados.
- `Matematica`:
  - `5o ano`: espaco e forma; grandezas e medidas; numeros e operacoes/algebra e funcoes; tratamento da informacao.
  - `9o ano`: espaco e forma; grandezas e medidas; numeros e operacoes/algebra e funcoes; tratamento da informacao, com maior complexidade cognitiva.
- Fonte oficial:
  - [Matriz de Referencia de Lingua Portuguesa e Matematica do Saeb](https://download.inep.gov.br/publicacoes/institucionais/avaliacoes_e_exames_da_educacao_basica/matriz_de_referencia_de_lingua_portuguesa_e_matematica_do_saeb.pdf)

### 3) Saeb: escalas de proficiencia para 5o e 9o ano
- O Inep publica as escalas de proficiencia de `Lingua Portuguesa` e `Matematica` para `5o` e `9o` ano.
- Essas escalas descrevem niveis crescentes de desempenho e exemplos de habilidades dominadas em cada faixa.
- Fonte oficial:
  - [Escalas de proficiencia do Saeb](https://download.inep.gov.br/publicacoes/institucionais/avaliacoes_e_exames_da_educacao_basica/escalas_de_proficiencia_do_saeb.pdf)

## Artefatos ja versionados no repositorio
- O projeto passa a manter copias controladas em `docs/references/saeb/`:
  - `matriz_matematica-base-saeb-2001.pdf`
  - `matriz_linguaportuguesa-base-saeb-2001.pdf`
  - `matriz-de-referencia-de-matematica_BNCC-2018.pdf`
  - `matriz-de-referencia-de-linguagens_BNCC-2018.pdf`
  - `escala_de_proficiencias_saeb_2025.pdf`
- O projeto tambem passa a manter copias controladas em `docs/references/cnca/`:
  - `CNCAGuiadaAvaliaoContnua.pdf`
  - `MEC_2026_CNCA_Av_Cont_Apren_Matriz_Ref.pdf`
- Leitura recomendada para o projeto:
  - `base-saeb-2001`: referencia principal de comparabilidade para `5o` e `9o` ano em `Lingua Portuguesa` e `Matematica`.
  - `BNCC-2018`: referencia de evolucao curricular e de transicao de matriz, util para planejamento semantico e comparacoes futuras.
  - `escala_de_proficiencias_saeb_2025`: referencia de niveis/faixas de desempenho a serem associados a uma futura camada de proficiencia.
- Recomendacao operacional:
  - manter esses arquivos sincronizados com a versao oficial usada em cada decisao semantica;
  - quando houver troca de versao, registrar a mudanca em documentacao e no historico Git.

### 4) Saeb/CNCA: alfabetizacao no 2o ano
- O Inep publicou orientacoes especificas para o `2o ano`:
  - `Lingua Portuguesa`: eixo de apropriacao do sistema de escrita alfabetico, eixo de leitura e eixo de producao textual.
  - `Matematica`: letramento matematico, com habilidades distribuidas em eixos cognitivos e unidades tematicas alinhadas a BNCC.
- Fontes oficiais:
  - [Descricao das habilidades da matriz de Lingua Portuguesa e exemplos de itens | 2o ano](https://download.inep.gov.br/avaliacao_da_alfabetizacao/orientacoes_pedagogicas/descricao_habilidades_lingua_portuguesa_2_ano_ef.pdf)
  - [Orientacoes sobre as habilidades da matriz de Matematica | 2o ano](https://download.inep.gov.br/avaliacao_da_alfabetizacao/orientacoes_pedagogicas/descricao_habilidades_matematica_2_ano_ef.pdf)

### 5) CNCA: guia de avaliacao e niveis nacionais
- O `Compromisso Nacional Crianca Alfabetizada` explicita que:
  - Saeb e CNCA compartilham a referencia para o `2o ano`.
  - As matrizes do CNCA organizam habilidades basicas e prioritarias ao longo dos ciclos avaliativos.
- O Inep tambem publicou o documento preliminar de niveis e metas do CNCA, com `ponto 743` da escala do Saeb como referencia nacional para alfabetizacao ao final do `2o ano`.
- Fontes oficiais:
  - [CNCA - Guia da Avaliacao Continua](https://www.gov.br/mec/pt-br/crianca-alfabetizada/pdf/CNCAGuiadaAvaliaoContnua.pdf)
  - [Niveis de alfabetizacao e definicao de metas para o CNCA](https://download.inep.gov.br/avaliacao_da_alfabetizacao/documentos_tecnicos/niveis_metas.pdf)
  - [Relatorio da Pesquisa Alfabetiza Brasil](https://www.gov.br/inep/pt-br/centrais-de-conteudo/acervo-linha-editorial/publicacoes-institucionais/avaliacoes-e-exames-da-educacao-basica/relatorio-da-pesquisa-alfabetiza-brasil-diretrizes-para-uma-politica-nacional-de-avaliacao-da-alfabetizacao-das-criancas)

### 6) Rio de Janeiro: Alfabetiza RJ / Avalia RJ
- A `Seeduc-RJ` registra oficialmente o `Alfabetiza RJ` como avaliacao diagnostica aplicada aos estudantes do `2o ano` do Ensino Fundamental.
- A mesma documentacao posiciona o programa dentro do `Compromisso Nacional Crianca Alfabetizada` e do regime de colaboracao com os `92 municipios`.
- Fonte oficial:
  - [Seeduc-RJ apresenta resultados da avaliacao Alfabetiza RJ em 2024](https://www.seeduc.rj.gov.br/not%C3%ADcias?fromSearch=true)
  - [Seeduc-RJ - noticias sobre o Compromisso Nacional Crianca Alfabetizada e o programa Alfabetiza RJ](https://www.seeduc.rj.gov.br/mais/mais-not%C3%ADcias)

### 7) Papel do CAEd
- O CAEd informa que os itens de suas avaliacoes sao elaborados com base nas `Matrizes de Referencia` das redes e dos sistemas de ensino.
- Isso reforca que a matriz normativa deve vir da politica avaliativa adotada pela rede, enquanto o `CAEd` atua na elaboracao/calibragem/operacionalizacao.
- Fonte oficial:
  - [Banco de itens - CAEd](https://caeddigital.net/tecnologias-2/banco-de-itens.html)

## Implicacoes para o projeto

### 1) Leitura correta do IMA atual
- O `IMA medio` atual deve ser lido como `proxy operacional de alfabetizacao agregada`.
- Ele nao pode ser rotulado como `proficiencia media Saeb` nem como `indice oficial de proficiencia em matematica e lingua portuguesa`.

### 2) Base para 2o ano
- Para turmas do `2o ano`, a referencia pedagogica deve considerar:
  - `Lingua Portuguesa`: apropriacao do sistema de escrita, leitura e producao textual.
  - `Matematica`: letramento matematico.
  - `CNCA`: ponto de corte nacional e niveis agregados de alfabetizacao.

### 3) Base para 5o e 9o ano
- Para turmas do `5o` e `9o` ano, a referencia deve ser a combinacao de:
  - matriz de `Lingua Portuguesa` do Saeb;
  - matriz de `Matematica` do Saeb;
  - escala de proficiencia correspondente por etapa e componente.

### 4) Efeito de governanca
- Qualquer futura metrica que queira representar `proficiencia` precisa armazenar, no minimo:
  - `ano_escolar_avaliado`
  - `componente` (`portugues`, `matematica`)
  - `fonte_avaliacao` (`saeb`, `cnca`, `alfabetiza_rj`, `avalia_rj`, `outra`)
  - `versao_matriz`
  - `escala` e/ou `nivel_proficiencia`
  - `janela_aplicacao`

## Recomendacao de nomenclatura
- Manter o nome atual apenas se o produto explicitar que se trata de metrica interna.
- Alternativa melhor para o estado atual:
  - `Indice Municipal de Alfabetizacao - operacional`
- Reservar uma futura variante para calibracao externa:
  - `IMA calibrado por proficiencia`

## Proxima evolucao recomendada
1. Renomear no BI as metricas atuais para evitar interpretacao incorreta de proficiencia oficial.
2. Criar um catalogo de metricas com distincao entre:
   - `indicador interno operacional`
   - `indicador de proficiencia externa`
3. Planejar a extensao do modelo para `matematica`.
4. Introduzir `ano_escolar` e `fonte_avaliacao` no modelo de indicadores antes de tentar unificar `2o`, `5o` e `9o` ano em um unico indice.

## Limite identificado nesta pesquisa
- Nao foi localizado, em dominio oficial indexavel da `Seeduc-RJ`, um PDF publico com uma `matriz propria do Avalia RJ` detalhada por descritores.
- Ate que essa matriz seja publicada de forma oficial, o projeto deve tratar `Alfabetiza RJ / Avalia RJ` como avaliacao diagnostica estadual alinhada ao `CNCA` e ao ecossistema `Saeb`, e nao como uma matriz normativa autonoma ja documentada no repositorio.
