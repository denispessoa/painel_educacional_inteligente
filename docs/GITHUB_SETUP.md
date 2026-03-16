# GitHub Setup

## Objetivo
Documentar o fluxo de versionamento do projeto no Git e no GitHub.

## Baseline oficial
Toda mudanca relevante deve respeitar as referencias oficiais do projeto:
- `README.md`
- `SYSTEM_CONTEXT.md`
- `docs/EDUCATIONAL_DATA_ARCHITECTURE.md`
- `docs/MIGRATION_PLAN_EDUCATIONAL_ARCHITECTURE.md`
- ADRs `007` a `011`

## Regras praticas
- preferir commits pequenos e logicos
- nao misturar mudancas operacionais com refatoracao semantica sem necessidade
- registrar decisoes de arquitetura em ADR ou documento tecnico antes de aplicar mudanca estrutural grande
- manter compatibilidade com o MVP atual

## Publicacao inicial
Adicionar remoto:
```powershell
git remote add origin https://github.com/SEU-USUARIO/SEU-REPO.git
```

Primeiro push:
```powershell
git push -u origin main
```

## Fluxo recomendado
Verificar estado:
```powershell
git status
```

Salvar mudancas:
```powershell
.\scripts\git_save.ps1 -Message "docs: atualiza documentacao tecnica"
```

Ou manualmente:
```powershell
git add .
git commit -m "docs: atualiza documentacao tecnica"
git push
```

## Branches
- manter `main` como linha principal estavel
- usar branches `codex/...` para mudancas maiores quando necessario

## O que registrar com mais rigor
- migrations de banco
- ADRs
- contratos HTTP
- contratos BI
- artefatos de referencia pedagogica
