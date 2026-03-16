let
    BaseUrl = "http://127.0.0.1:8000",
    Endpoint = "bi/v1/hierarquia",
    Source = Json.Document(
        Web.Contents(
            BaseUrl,
            [
                RelativePath = Endpoint
            ]
        )
    ),
    AsTable = Table.FromRecords(
        Source,
        type table [
            municipio_id = text,
            municipio_nome = text,
            municipio_estado = text,
            escola_id = text,
            escola_nome = text,
            turma_id = text,
            turma_nome = text
        ]
    ),
    Typed = Table.TransformColumnTypes(
        AsTable,
        {
            {"municipio_id", type text},
            {"municipio_nome", type text},
            {"municipio_estado", type text},
            {"escola_id", type text},
            {"escola_nome", type text},
            {"turma_id", type text},
            {"turma_nome", type text}
        }
    )
in
    Typed
