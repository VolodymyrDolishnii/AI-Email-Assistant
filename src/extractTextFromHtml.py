from bs4 import BeautifulSoup

def extractTextFromHtml(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    text = soup.get_text()

    clean_text = '\n'.join(line.strip() for line in text.splitlines() if line.strip())
    
    return clean_text
