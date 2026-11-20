
from rdflib import Graph

graph = Graph()
graph.parse("oscars_knowledge_graph.ttl", format="turtle")

print("Total RDF triples:", len(graph))

# SPARQL Query 1 - Best Picture Winners
results = graph.query("""
PREFIX ex: <https://example.org/oscars/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?year ?title
WHERE {
    ?ceremony a ex:Ceremony ;
              ex:ceremonyYear ?year ;
              ex:hasWinningFilm ?film .

    ?film rdfs:label ?title .
}
ORDER BY ?year
""")

# Displaying query results
print("\nBest Picture Winners (1965-2025)")
print("-" * 45)

count = 0

for row in results:
    print(row.year, "-", row.title)
    count += 1

print("-" * 45)
print("Total winners found:", count)


# SPARQL Query 2 - Logical and Numerical Filtering
results_q2 = graph.query("""
PREFIX ex: <https://example.org/oscars/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?year ?title
WHERE {
    ?ceremony a ex:Ceremony ;
              ex:ceremonyYear ?year ;
              ex:hasWinningFilm ?film .

    ?film rdfs:label ?title .

    FILTER(
        ?year >= 2000 &&
        ?year <= 2025 &&
        (?year < 2010 || ?year >= 2020)
    )
}
ORDER BY ?year
""")

# Displaying Query 2 results
print("\nQuery 2: Best Picture Winners (2000-2025, excluding 2010-2019)")
print("-" * 65)

count_q2 = 0

for row in results_q2:
    print(row.year, "-", row.title)
    count_q2 += 1

print("-" * 65)
print("Total filtered winners:", count_q2)


# SPARQL Query 3 - OPTIONAL Properties
results_q3 = graph.query("""
PREFIX ex: <https://example.org/oscars/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?year ?title ?runtime ?genreName
WHERE {
    ?ceremony a ex:Ceremony ;
              ex:ceremonyYear ?year ;
              ex:hasWinningFilm ?film .

    ?film rdfs:label ?title .

    OPTIONAL {
        ?film ex:filmRuntimeMinutes ?runtime .
    }

    OPTIONAL {
        ?film ex:hasGenre ?genre .
        ?genre rdfs:label ?genreName .
    }
}
ORDER BY ?year
""")

# Displaying Query 3 results
print("\nQuery 3: Film Runtime and Genre")
print("-" * 75)

for row in results_q3:
    runtime = row.runtime if row.runtime is not None else "N/A"
    genre = row.genreName if row.genreName is not None else "N/A"

    print(row.year, "-", row.title,
          "| Runtime:", runtime,
          "| Genre:", genre)


# SPARQL Query 4 - Aggregation by Decade
results_q4 = graph.query("""
PREFIX ex: <https://example.org/oscars/>

SELECT ?decade (COUNT(DISTINCT ?film) AS ?filmCount)
WHERE {
    ?ceremony a ex:Ceremony ;
              ex:ceremonyYear ?year ;
              ex:hasWinningFilm ?film .

    BIND((FLOOR(?year / 10) * 10) AS ?decade)
}
GROUP BY ?decade
ORDER BY ?decade
""")

# Displaying Query 4 results
print("\nQuery 4: Best Picture Winners by Decade")
print("-" * 45)

total_q4 = 0

for row in results_q4:
    decade = int(row.decade)
    count = int(row.filmCount)

    print(f"{decade}s - {count} winners")
    total_q4 += count

print("-" * 45)
print("Total winners:", total_q4)


# SPARQL Query 5 - Four-Hop Graph Traversal
results_q5 = graph.query("""
PREFIX ex: <https://example.org/oscars/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?year ?title ?directorName
WHERE {
    ?film ex:hasAwardWin ?win .

    ?win ex:atCeremony ?ceremony .

    ?ceremony ex:ceremonyYear ?year ;
              ex:hasWinningFilm ?winningFilm .

    ?winningFilm rdfs:label ?title ;
                 ex:directedBy ?director .

    ?director rdfs:label ?directorName .
}
ORDER BY ?year ?directorName
""")

# Displaying Query 5 results
print("\nQuery 5: Four-Hop Graph Traversal")
print("-" * 75)

count_q5 = 0

for row in results_q5:
    print(row.year, "-", row.title, "| Director:", row.directorName)
    count_q5 += 1

print("-" * 75)
print("Total results:", count_q5)
