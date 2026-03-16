# Referencias curriculares por rede

Esta pasta guarda as matrizes curriculares locais da rede ativa do projeto.

## Objetivo
- manter a matriz curricular municipal dentro do repositorio;
- permitir convergencia entre avaliacoes externas, `BNCC` e curriculo local;
- facilitar substituicao futura de `Mendes` por outra rede sem alterar a estrutura do projeto.

## Convencao de estrutura
- `docs/references/redes/<rede>/fundamental_i/`
- `docs/references/redes/<rede>/fundamental_ii/`
- `docs/references/redes/<rede>/README.md`

## Regra de substituicao futura
Quando o projeto passar a operar para outra rede:
1. criar `docs/references/redes/<nova_rede>/`;
2. copiar as matrizes curriculares da nova rede para as subpastas correspondentes;
3. atualizar `docs/CONVERGENCIA_AVALIACOES_BNCC_REDE.md` para apontar a pasta curricular ativa;
4. manter `CNCA`, `SAEB` e demais referencias normativas intactas.

## Estado atual
- rede curricular ativa versionada: `Mendes`
- pasta ativa: `docs/references/redes/mendes/`
