from bs4 import BeautifulSoup
import sys
import requests
import json

def main():
    if len(sys.argv) > 2:
        if sys.argv[1] == "search":
            results = google_searcher(sys.argv[2])
            results = json.dumps(results)
            print(results)

def google_searcher(item):
    search_response = requests.get("https://www.google.com/search?q=" + item)
    
    if search_response.status_code == 200:
        soup = BeautifulSoup(search_response.text, 'lxml') 
        search_content = soup.get_text()
        return search_content
    else:
        print("Error: Unable to fetch search results.")
        return None

if __name__ == "__main__":
    main()
