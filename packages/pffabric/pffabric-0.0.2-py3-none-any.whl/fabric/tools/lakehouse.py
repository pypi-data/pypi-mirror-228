import json
from promptflow import tool
from azure.storage.filedatalake import (
    DataLakeServiceClient,
    DelimitedJsonDialect, 
    DelimitedTextDialect
)
from azure.identity import DefaultAzureCredential


@tool
def lakehouse_lookup(workspaceName: str, artifactName: str, fileName: str, params: dict[str, any]):
    storage_account_name = "dxt-onelake"
    artifact_type = "Lakehouse"

    token_credential = DefaultAzureCredential()
    service_client = DataLakeServiceClient(account_url=f"https://{storage_account_name}.dfs.fabric.microsoft.com", 
                                           credential=token_credential)
    file_system_client = service_client.get_file_system_client(file_system=workspaceName)
    file_client = file_system_client.get_file_client(f"{artifactName}.{artifact_type}/Files/{fileName}")

    query_expression = "SELECT * from DataLakeStorage"

    if params is not None and len(params) > 0:
        p = 0
        query_expression += " WHERE "
        for key, value in params.items():
            query_expression += f"{key} = " + (f"'{value}'" if isinstance(value, str) else f"{value}")
            if p < len(params) - 1:
                query_expression += " AND "
            p += 1

    input_format = DelimitedTextDialect(has_header=True)
    output_format = DelimitedJsonDialect(delimiter='\n')
    reader = file_client.query_file(query_expression, file_format=input_format, output_format=output_format)
    content = reader.readall()
    
    return json.loads(content)
