# GitHub Setup e Fluxo de Versionamento

Guia minimo para manter este projeto versionado localmente e publicado no GitHub.

## Estado esperado
- Repositorio Git inicializado localmente.
- Branch principal: `main`.
- Arquivos locais e segredos fora do versionamento via `.gitignore`.

## 1) Criar o repositorio no GitHub
Crie um repositorio vazio no GitHub com um nome como:
- `educacao-inteligente`

Recomendacao:
- nao inicializar com `README`, `.gitignore` ou licenca no GitHub se este repositorio local ja tiver commit inicial.

## 2) Conectar o remoto
No terminal, na raiz do projeto:

```powershell
git remote add origin https://github.com/SEU-USUARIO/educacao-inteligente.git
git push -u origin main
```

Se preferir SSH:

```powershell
git remote add origin git@github.com:SEU-USUARIO/educacao-inteligente.git
git push -u origin main
```

Alternativa com script do projeto:

```powershell
.\scripts\git_save.ps1 -Message "chore: first github push" -RemoteUrl https://github.com/SEU-USUARIO/educacao-inteligente.git
```

O script:
- faz `git add .`;
- cria o commit;
- cadastra `origin` se ele ainda nao existir;
- executa `push` na branch atual.

## 3) Fluxo diario recomendado
Verificar mudancas:

```powershell
git status
```

Adicionar alteracoes:

```powershell
git add .
```

Criar commit:

```powershell
git commit -m "descreva a alteracao"
```

Enviar ao GitHub:

```powershell
git push
```

Alternativa simplificada:

```powershell
.\scripts\git_save.ps1 -Message "feat: descreva a alteracao"
```

## 4) Estrategia simples de branches
- `main`: estado estavel do projeto.
- `feat/...`: novas funcionalidades.
- `fix/...`: correcoes.
- `docs/...`: mudancas apenas de documentacao.

Exemplo:

```powershell
git checkout -b feat/metabase-filtros
```

## 5) Regras praticas para este projeto
- Nao versionar `.env`, ambientes virtuais, caches e backups SQL.
- Pode versionar `dashboard/MVP_BI_v1.pbix`, mas ele sera tratado como binario.
- Antes de push importante, rodar testes do backend:

```powershell
cd backend
python -m pytest -q
```

## 6) Colaboracao
Se outra pessoa for modificar o projeto:
- clonar o repositorio;
- seguir o `README.md` da raiz;
- usar commits pequenos e descritivos;
- evitar mudar contratos da API sem atualizar `docs/PHASE4_API_CONTRACT.md`.
