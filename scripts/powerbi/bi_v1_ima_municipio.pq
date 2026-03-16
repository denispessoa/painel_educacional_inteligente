let
    BaseUrl = "http://127.0.0.1:8000",
    GroupBy = "municipio",
    Endpoint = "bi/v1/ima",
    Response = Json.Document(
        Web.Contents(
            BaseUrl,
            [
                RelativePath = Endpoint,
                Query = [
                    group_by = GroupBy
                ]
            ]
        )
    ),
    Itens = Record.Field(Response, "itens"),
    AsTable = Table.FromRecords(Itens),
    WithGroupBy = Table.AddColumn(AsTable, "group_by", each Response[group_by], type text),
    Typed = Table.TransformColumnTypes(
        WithGroupBy,
        {
            {"nivel", type text},
            {"id", type text},
            {"nome", type text},
            {"total_registros", Int64.Type},
            {"total_alunos", Int64.Type},
            {"percentual_leitura_medio", type number},
            {"percentual_escrita_medio", type number},
            {"ima_medio", type number},
            {"group_by", type text}
        }
    )
in
    Typed
