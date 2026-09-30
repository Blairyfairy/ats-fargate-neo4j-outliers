import os
import re
from bs4 import BeautifulSoup
from neo4j import GraphDatabase

NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "Password123!")

def parse_job_skills(html_path):
    with open(html_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    candidate_name = "Blair Page"
    skills = set()
    technologies = [
        "AWS", "Terraform", "Docker", "Kubernetes", "Neo4j", "Python", 
        "Machine Learning", "Cypher", "Fargate", "Graph Database", 
        "CI/CD", "Linux", "DevOps", "Data Science", "SQL", "NoSQL"
    ]

    text_content = soup.get_text()
    for tech in technologies:
        if re.search(r'\b' + re.escape(tech) + r'\b', text_content, re.IGNORECASE):
            skills.add(tech)

    return candidate_name, list(skills)

def ingest_to_neo4j(candidate, skills):
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    with driver.session() as session:
        session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (c:Candidate) REQUIRE c.name IS UNIQUE")
        session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (s:Skill) REQUIRE s.name IS UNIQUE")

        query = """
        MERGE (c:Candidate {name: $candidate_name})
        WITH c
        UNWIND $skills AS skill_name
        MERGE (s:Skill {name: skill_name})
        MERGE (c)-[:POSSESSES {weight: 1.0}]->(s)
        """
        session.run(query, candidate_name=candidate, skills=skills)
    driver.close()
    print(f"Successfully ingested {len(skills)} skills for candidate {candidate}.")

if __name__ == "__main__":
    html_file = "index.html"
    candidate, skills = parse_job_skills(html_file)
    ingest_to_neo4j(candidate, skills)
