import requests
import json 

data = {
    "code": "CREATE QUERY rr() FOR GRAPH MyGraph API(\"v2\") SYNTAX v2 { PRINT \"Hello World\"\n\n}\n",
    "graph": "MyGraph"
}
response = requests.post("https://f82f2c67cbfc46aa8e43a89d705a0b0e.i.tgcloud.io:14240/gsqlserver/gsql/codecheck", 
                        json=data, auth=('tigergraph', 'Browser123'))
print(response.json()['errors'])