# Decisões técnicas e backlog

Este documento registra o que já foi decidido na dashboard AvaliaRJ portátil e o que ainda pode ser melhorado.

## Decisões implementadas

- O pacote é offline e portátil.
- A dashboard é um HTML estático, com CSS e JavaScript embutidos.
- A análise usa apenas dados agregados por escola e por turma.
- O pacote não depende da base canônica, do backend, do frontend principal ou de Metabase.
- A versão atual foi construída para o recorte de Língua Portuguesa do 2º ano, bloco principal `H01-H08`.
- Os itens de resposta construída `D09` e `D10` estão cadastrados no dicionário de descritores, mas não aparecem nos arquivos usados neste recorte.
- Os nomes das escolas de Mendes foram padronizados no gerador.
- As habilidades aparecem visualmente como `H xx (Dxx)`.
- O significado do descritor aparece apenas em tooltip, para não poluir os gráficos.
- A seção de escolas usa abas, para separar o contexto de cada unidade.
- A análise de turmas aparece apenas dentro da escola selecionada.
- O heatmap geral da rede aparece na página principal.
- O heatmap por turma aparece apenas dentro do painel da escola.
- Heatmaps largos foram substituídos por cartões responsivos.
- A análise de turmas deixou de usar tabela com rolagem lateral e passou a usar cards.
- Os cards de turma indicam status por cor e destacam a melhor turma e a turma de maior atenção dentro de cada escola.
- O PowerPoint é gerado pelo mesmo contexto analítico da dashboard.
- O workbook Excel é gerado por script separado, mas reaproveita a mesma lógica de leitura e normalização.

## Escopo pedagógico atual

Descritores de Língua Portuguesa cadastrados:

- `D01`: Relacionar elementos sonoros das palavras com sua representação escrita.
- `D02`: Ler palavras.
- `D03`: Ler frases.
- `D04`: Localizar informações explícitas em textos.
- `D05`: Reconhecer a finalidade de um texto.
- `D06`: Inferir o assunto de um texto.
- `D07`: Inferir informações em textos verbais.
- `D08`: Inferir informações em textos que articulam linguagem verbal e não verbal.
- `D09`: Escrever palavras.
- `D10`: Escrever textos.

## Limitações conhecidas

- A matriz de Matemática ainda não está implementada.
- A legenda de habilidades foi tratada para o recorte de AlfabetizaRJ 2º ano disponível no pacote.
- O HTML é standalone; isso facilita o uso offline, mas concentra Python, HTML, CSS e JS em um único gerador.
- Não há testes automatizados específicos para o HTML gerado.
- A responsividade foi validada por estrutura e CSS, mas ainda pode ser refinada com teste visual em vários celulares.
- A comparação temporal ainda não existe, pois o pacote atual trabalha com um par de arquivos por execução.
- A publicação online não está automatizada dentro do pacote portátil.
- A identidade visual oficial da Prefeitura/Secretaria ainda não foi aplicada com logos e manual de marca.

## Backlog recomendado

1. Incluir suporte a Matemática com matriz própria de descritores.
2. Criar um arquivo de configuração simples, por exemplo `config.yml`, para município, ano, componente, nomes oficiais e textos de apresentação.
3. Separar templates HTML/CSS do Python, mantendo a opção de gerar um HTML standalone.
4. Adicionar teste automatizado mínimo para garantir que o HTML gerado contém seções obrigatórias, abas e tooltips.
5. Criar modo de múltiplas escolas ou múltiplos arquivos por rede, para quando chegarem outros dados.
6. Criar visão comparativa entre componentes, por exemplo Língua Portuguesa x Matemática.
7. Criar comparação temporal entre aplicações, caso novos ciclos sejam disponibilizados.
8. Criar exportação por escola em HTML ou PDF, para reuniões individuais com diretores.
9. Incluir identidade visual oficial, se houver autorização e arquivos de marca.
10. Criar opção de publicação estática em GitHub Pages ou Netlify.
11. Revisar acessibilidade com foco em contraste, navegação por teclado e leitores de tela.
12. Adicionar um checklist visual para apresentação em projetor e celular.

## Próximas alterações de maior impacto

- Suporte a Matemática: exige nova matriz de descritores e possível revisão de rótulos, textos e recomendações.
- Comparativo de rede completa: exige consolidar vários arquivos ou múltiplos municípios/escolas em uma estrutura única.
- Publicação online: exige decidir se o HTML continuará standalone ou se haverá uma pasta pública com `index.html`.
- Separação de templates: melhora manutenção, mas aumenta a quantidade de arquivos do pacote portátil.

## Critérios para considerar uma mudança pronta

- A dashboard gera sem erro.
- O PowerPoint gera sem erro quando a mudança afeta conteúdo analítico.
- A análise Excel gera sem erro quando a mudança afeta indicadores.
- A dashboard abre offline.
- Não há rolagem lateral inesperada nas seções principais.
- As abas de escola funcionam.
- Os tooltips das habilidades funcionam.
- O escopo do componente curricular está correto.
- Nenhum microdado de estudante foi adicionado.
