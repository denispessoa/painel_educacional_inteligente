let
    BaseUrl = "http://127.0.0.1:8000",
    Ano = "2026",
    Trimestre = "1",
    Endpoint = "bi/v1/indicadores-trimestrais",
    Source = Json.Document(
        Web.Contents(
            BaseUrl,
            [
                RelativePath = Endpoint,
                Query = [
                    ano = Ano,
                    trimestre = Trimestre
                ]
            ]
        )
    ),
    AsTable = Table.FromRecords(Source),
    Typed = Table.TransformColumnTypes(
        AsTable,
        {
            {"indicador_id", type text},
            {"ano", Int64.Type},
            {"trimestre", Int64.Type},
            {"turma_id", type text},
            {"turma_nome", type text},
            {"escola_id", type text},
            {"escola_nome", type text},
            {"municipio_id", type text},
            {"municipio_nome", type text},
            {"municipio_estado", type text},
            {"total_alunos", Int64.Type},
            {"alfabetizados_leitura", Int64.Type},
            {"alfabetizados_escrita", Int64.Type},
            {"percentual_leitura", type number},
            {"percentual_escrita", type number},
            {"ima", type number}
        }
    )
in
    Typed
