from fabric.tools.lakehouse import lakehouse_lookup

def test_lakehouse_lookup():
    workspaceName = "ContosoTrek"
    artifactName = "contoso_customers"
    fileName = "customers.csv"
    params = {"customerId": "1"}

    customer = lakehouse_lookup(workspaceName, artifactName, fileName, params)
    assert customer["customerId"] == "1"
    assert customer["firstName"] == "John"
    assert customer["lastName"] == "Smith"