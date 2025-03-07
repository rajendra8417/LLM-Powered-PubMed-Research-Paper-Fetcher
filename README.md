Overview
This Python tool fetches research papers from PubMed based on a user query, identifies authors affiliated with pharmaceutical or biotech companies using an LLM (Large Language Model), and saves the results to a CSV file.

It consists of:

A module (pubmed_fetcher.py) that handles PubMed API requests and LLM classification.
A command-line interface (CLI) (pubmed_cli.py) that allows users to search and save results.

Features
✅ Fetches research papers from PubMed using the Entrez API.
✅ Uses OpenAI's LLM (GPT-4) to classify affiliations as academic or corporate.
✅ Extracts details like authors, company affiliations, and corresponding author email.
✅ Saves results as a CSV file or prints to the console.
✅ Supports command-line options for flexible usage.
✅ Packaged with Poetry and can be published on TestPyPI.


Installation
1. Clone the Repository
bash
Copy
Edit
git clone https://github.com/yourusername/llm-pubmed-fetcher.git
cd llm-pubmed-fetcher
2. Install Dependencies with Poetry
Ensure you have Poetry installed. Then, run:

bash
Copy
Edit
poetry install
3. Set Up Your OpenAI API Key
Create a .env file or set an environment variable:

bash
Copy
Edit
export OPENAI_API_KEY="your_openai_api_key_here"
Usage
Basic Command
To fetch PubMed papers for a given query:

bash
Copy
Edit
poetry run get-papers-list "cancer treatment"
This prints results to the console.

Save Results to CSV
bash
Copy
Edit
poetry run get-papers-list "diabetes research" -f results.csv
This saves the results to results.csv.

Enable Debug Mode
bash
Copy
Edit
poetry run get-papers-list "gene therapy" -d
Prints API responses for troubleshooting.

Command-Line Options
Option	Description
query	(Required) The search term for PubMed.
-f, --file	(Optional) Save results to a CSV file.
-d, --debug	(Optional) Enable debug mode to see API responses.
-h, --help	Show usage instructions.
Output Format
The tool outputs a CSV file with the following columns:

PubmedID	Title	Publication Date	Non-academic Author(s)	Company Affiliation(s)	Corresponding Author Email
12345678	Research on X	2024-01-15	John Doe	Pfizer, Inc.	johndoe@pfizer.com
Development & Contribution
Run Tests
If tests are added, run them using:

bash
Copy
Edit
pytest tests/
Publish to TestPyPI
Build the package:
bash
Copy
Edit
poetry build
Publish to TestPyPI:
bash
Copy
Edit
poetry publish --repository testpypi
Install from TestPyPI for testing:
bash
Copy
Edit
pip install --index-url https://test.pypi.org/simple/ llm-pubmed-fetcher
Technologies Used
Python 3.8+
PubMed API (Entrez Utilities)
OpenAI GPT-4 (for affiliation classification)
Requests (for API calls)
Poetry (for dependency management)
