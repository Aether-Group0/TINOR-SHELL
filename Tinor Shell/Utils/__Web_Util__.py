import webbrowser as Web
from urllib.parse import quote_plus

def Lookup(Command_input):
    query = Command_input.strip()[2:].strip()

    if not query:
        print("Usage: lp <search query>")
        return False

    # If it's already a URL, open it directly
    if query.startswith(("http://", "https://")):
        Web.open_new_tab(query)
    else:
        # Otherwise, search the web
        search_url = "https://www.google.com/search?q=" + quote_plus(query)
        Web.open_new_tab(search_url)

    return True