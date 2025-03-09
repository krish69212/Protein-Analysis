from pypdb.clients.search.search_client import perform_search
from pypdb.clients.search.search_client import ReturnType
from pypdb.clients.search.operators import text_operators


search_operator = text_operators.DefaultOperator(value="ribosome")
return_type = ReturnType.ENTRY

results = perform_search(search_operator, return_type)

print(results)
