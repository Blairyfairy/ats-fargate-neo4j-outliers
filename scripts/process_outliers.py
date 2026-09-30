import os
import pandas as pd
from neo4j import GraphDatabase

NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "Password123!")

BENCHMARK_JOB_REQUIREMENTS = {
    "AWS": 0.99,
    "Python": 0.98,
    "Docker": 0.98,
    "Kubernetes": 0.95,
    "Terraform": 0.95,
    "Neo4j": 0.08,             # Specialized outlier skill
    "Graph Database": 0.06,     # Specialized outlier skill
    "Machine Learning": 0.07,   # Specialized outlier skill
    "Linux": 0.90,
    "CI/CD": 0.92
}

def fetch_candidate_skills():
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    query = """
    MATCH (c:Candidate)-[:POSSESSES]->(s:Skill)
    RETURN c.name AS candidate, collect(s.name) AS skills
    """
    with driver.session() as session:
        result = session.run(query)
        record = result.single()
        candidate = record["candidate"]
        skills = record["skills"]
    driver.close()
    return candidate, skills

def calculate_ats_and_outliers(candidate, candidate_skills):
    df = pd.DataFrame(list(BENCHMARK_JOB_REQUIREMENTS.items()), columns=["Skill", "JobWeight"])
    df["CandidateHas"] = df["Skill"].apply(lambda x: 1 if x in candidate_skills else 0)

    core_df = df[df["JobWeight"] >= 0.90]
    core_match = (core_df["CandidateHas"].sum() / len(core_df)) * 100

    outliers = df[(df["JobWeight"] >= 0.05) & (df["JobWeight"] <= 0.10) & (df["CandidateHas"] == 1)]

    print("=" * 50)
    print(f"Candidate: {candidate}")
    print(f"Core ATS Qualification Score: {core_match:.2f}%")
    print("=" * 50)
    print("\nIdentified 'Nice-to-Have' Outlier Technologies (5%-10% Weight Range):")
    for _, row in outliers.iterrows():
        print(f" - {row['Skill']} (Job Weight: {row['JobWeight']*100:.1f}%)")

if __name__ == "__main__":
    candidate, skills = fetch_candidate_skills()
    calculate_ats_and_outliers(candidate, skills)
