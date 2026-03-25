# OpenAlex2VIVO

OpenAlex2VIVO is a Python package designed to fetch author profiles, organizational affiliations, and publication works directly from the [OpenAlex API](https://openalex.org) and translate them into RDF data compliant with the [VIVO-ISF](https://vivoweb.org/) ontology.

## Example: generate and publish RDF

1. Generate the RDF for the given OpenAlex/ORCID ID

```python
# 1. Generate the RDF for the given OpenAlex/ORCID ID
result = openalex_service.process_openalex(request.orcid_id)

# 2. Parse the turtle string back to an rdflib Graph
from rdflib import Graph
graph = Graph()
graph.parse(data=result["vivo_rdf"], format="turtle")

# 3. Publish to VIVO local instance
sparql_insert(graph, VIVO_ENDPOINT, VIVO_USERNAME, VIVO_PASSWORD)
```

Minimum required: Python 3.

