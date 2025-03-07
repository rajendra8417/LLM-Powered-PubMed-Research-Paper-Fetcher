import requests
import openai
import csv
import xml.etree.ElementTree as ET
from typing import List, Dict, Optional

# Constants
PUBMED_API_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
PUBMED_FETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
OPENAI_API_KEY = "your_openai_api_key_here"  # Replace with your OpenAI API key

def classify_affiliation(affiliation: str) -> str:
    """Use OpenAI's LLM to classify affiliations as academic or corporate."""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Classify the following affiliation as 'academic' or 'corporate'."},
            {"role": "user", "content": affiliation}
        ]
    )
    return response["choices"][0]["message"]["content"].strip().lower()

def fetch_pubmed_ids(query: str, debug: bool = False) -> List[str]:
    """Fetch PubMed IDs based on a query."""
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": 50,
    }
    response = requests.get(PUBMED_API_URL, params=params)
    if debug:
        print("PubMed API Response:", response.text)
    response.raise_for_status()
    return response.json().get("esearchresult", {}).get("idlist", [])

def fetch_paper_details(pmid: str, debug: bool = False) -> Optional[Dict]:
    """Fetch details for a specific PubMed paper using efetch."""
    params = {
        "db": "pubmed",
        "id": pmid,
        "retmode": "xml",
    }
    response = requests.get(PUBMED_FETCH_URL, params=params)
    if debug:
        print("Paper Details Response:", response.text)
    response.raise_for_status()
    return parse_paper_details(response.text)

def parse_paper_details(xml_data: str) -> Optional[Dict]:
    """Parse PubMed XML response to extract relevant details."""
    root = ET.fromstring(xml_data)
    title = root.findtext(".//ArticleTitle", default="")
    pub_date = root.findtext(".//PubDate/Year", default="")
    authors = []
    company_authors = []
    corresponding_email = "N/A"
    
    for author in root.findall(".//Author"):
        name = " ".join(filter(None, [author.findtext("ForeName"), author.findtext("LastName")]))
        affiliation = author.findtext("..//AffiliationInfo/Affiliation", default="")
        if affiliation:
            category = classify_affiliation(affiliation)
            authors.append({"name": name, "affiliation": affiliation})
            if category == "corporate":
                company_authors.append(name)
        email = author.findtext("..//AffiliationInfo/Email", default=None)
        if email:
            corresponding_email = email
    
    return {
        "Title": title,
        "Publication Date": pub_date,
        "Authors": authors,
        "Company Authors": company_authors,
        "Corresponding Email": corresponding_email,
    }

def save_to_csv(data: List[Dict], filename: str):
    """Save extracted data to a CSV file."""
    with open(filename, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["PubmedID", "Title", "Publication Date", "Non-academic Author(s)", "Company Affiliation(s)", "Corresponding Author Email"])
        writer.writeheader()
        writer.writerows(data)
