import argparse
import csv
from pubmed_fetcher import fetch_pubmed_ids, fetch_paper_details, save_to_csv

def main():
    parser = argparse.ArgumentParser(description="LLM-Powered PubMed Research Paper Fetcher.")
    parser.add_argument("query", type=str, help="Search query for PubMed.")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode.")
    parser.add_argument("-f", "--file", type=str, help="Filename to save results (default: print to console).")
    args = parser.parse_args()

    pmids = fetch_pubmed_ids(args.query, args.debug)
    results = []

    for pmid in pmids:
        paper = fetch_paper_details(pmid, args.debug)
        if paper:
            results.append({
                "PubmedID": pmid,
                "Title": paper["Title"],
                "Publication Date": paper["Publication Date"],
                "Non-academic Author(s)": ", ".join(paper["Company Authors"]),
                "Company Affiliation(s)": ", ".join(set(a["affiliation"] for a in paper["Authors"] if a.get("affiliation"))),
                "Corresponding Author Email": paper["Corresponding Email"],
            })

    if args.file:
        save_to_csv(results, args.file)
        print(f"Results saved to {args.file}")
    else:
        print(results)

if __name__ == "__main__":
    main()
