import json
import re
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

class RAGEngine:
    def __init__(self, data_path="employees.json"):
        """
        RAG engine for HR chatbot (Simple Version)
        - FAISS for semantic search
        - SentenceTransformer for embeddings
        - No LLM: Uses template-based responses
        """
        with open(data_path, "r", encoding="utf-8") as f:
            self.data = json.load(f)["employees"]

        self.embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        self.index = faiss.IndexFlatL2(384) 
        self.employee_embeddings = []

        for emp in self.data:
            profile_text = f"{emp['name']} {', '.join(emp['skills'])} {emp['experience_years']} years {', '.join(emp['projects'])} {emp['availability']}"
            embedding = self.embedder.encode(profile_text)
            self.employee_embeddings.append(embedding)

        self.employee_embeddings = np.array(self.employee_embeddings).astype("float32")
        self.index.add(self.employee_embeddings)

    def extract_experience(self, query: str):
        """Extracts years of experience requirement from query."""
        plus_match = re.search(r"(\d+)\s*\+\s*year", query.lower())
        if plus_match:
            return int(plus_match.group(1)), False
        exact_match = re.search(r"(\d+)\s*year", query.lower())
        if exact_match:
            return int(exact_match.group(1)), True
        return None, None

    def extract_skills(self, query: str):
        """Detects skills mentioned in query by matching against known skills."""
        all_skills = {skill for emp in self.data for skill in emp["skills"]}
        query_words = query.lower().replace(",", " ").split()
        detected_skills = [skill for skill in all_skills if skill.lower() in query_words]
        return detected_skills

    def search(self, query, top_k=10):
        """Semantic search on employees."""
        query_emb = self.embedder.encode(query).astype("float32")
        distances, indices = self.index.search(np.array([query_emb]), top_k)
        results = [self.data[i] for i in indices[0]]
        min_exp, exact_flag = self.extract_experience(query)
        if min_exp is not None:
            if exact_flag:
                results = [emp for emp in results if emp["experience_years"] == min_exp]
            else:
                results = [emp for emp in results if emp["experience_years"] >= min_exp]
        detected_skills = self.extract_skills(query)
        if detected_skills:
            results = [emp for emp in results if all(skill in emp["skills"] for skill in detected_skills)]

        return results

    def format_response(self, query, results):
        """Formats response without LLM (template-based)."""
        if not results:
            return f"❌ Sorry, I couldn’t find any employees matching: **{query}**."

        response = f"✅ Based on your request for **{query}**, here are some suitable candidates:\n\n"
        for emp in results[:3]:
            response += (
                f"**{emp['name']}** – {emp['experience_years']} years experience\n"
                f"🛠 Skills: {', '.join(emp['skills'])}\n"
                f"📂 Projects: {', '.join(emp['projects'])}\n"
                f"📌 Availability: {emp['availability']}\n\n"
            )
        response += "Would you like me to provide more details about any of these candidates?"
        return response
