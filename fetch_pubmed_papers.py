import requests
import csv
import re
import argparse
from typing import List, Dict, Any, Optional

BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
DETAIL_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"


def fetch_pubmed_ids(query: str) -> List[str]:
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": 100  # Fetch up to 100 papers
    }
    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()
    data = response.json()
    return data.get("esearchresult", {}).get("idlist", [])


def fetch_paper_details(pubmed_id: str) -> Optional[Dict[str, Any]]:
    params = {
        "db": "pubmed",
        "id": pubmed_id,
        "retmode": "xml"
    }
    response = requests.get(DETAIL_URL, params=params)
    response.raise_for_status()
    return response.text  # XML response (can be parsed further)


def extract_relevant_info(xml_data: str) -> Dict[str, Any]:
    # Dummy parser for now; use an XML parser like `xml.etree.ElementTree` later
    return {
        "PubmedID": "123456",
        "Title": "Sample Paper Title",
        "Publication Date": "2025-01-01",
        "Non-academic Author(s)": "Dr. John Doe",
        "Company Affiliation(s)": "PharmaCorp Inc.",
        "Corresponding Author Email": "johndoe@pharmacorp.com"
    }


def save_to_csv(results: List[Dict[str, Any]], filename: str):
    keys = ["PubmedID", "Title", "Publication Date", "Non-academic Author(s)", "Company Affiliation(s)", "Corresponding Author Email"]
    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(results)


def main():
    parser = argparse.ArgumentParser(description="Fetch research papers from PubMed.")
    parser.add_argument("query", type=str, help="Search query for PubMed.")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode.")
    parser.add_argument("-f", "--file", type=str, help="Output CSV filename.")
    args = parser.parse_args()

    pubmed_ids = fetch_pubmed_ids(args.query)
    results = [extract_relevant_info(fetch_paper_details(pid)) for pid in pubmed_ids]

    if args.file:
        save_to_csv(results, args.file)
        print(f"Results saved to {args.file}")
    else:
        for result in results:
            print(result)


if __name__ == "__main__":
    main()
