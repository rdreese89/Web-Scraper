from bs4 import BeautifulSoup
import requests
import time

def get_fighter_pages(URL = "https://www.bjjheroes.com/a-z-bjj-fighters-list") -> list:
    """
    Return a list of unique page IDs that represent each fighter's profile page

    Args:
        URL: str - This is defaulted to the 'A-Z BJJ Fighters List' page on BJJ Heroes
    """    
    response = requests.get(URL)
    soup = BeautifulSoup(response.content, 'html.parser')

    fighter_pages = []

    for link in soup.tbody.find_all('a', href=True):
        if link not in fighter_pages:
            fighter_pages.append(link['href'])

    # Our raw list has links to irrelevant webpages, parts of the desired link that need cleaning up, and duplicate entries (multiple columns within
    # the tbody object have separate links to the same page). We'll fix all of these with a few list comprehensions. 
    fighter_pages = [x for x in fighter_pages if "/?p=" in x]

    fighter_pages = [x.replace('/?p=', '') for x in fighter_pages]

    fighter_pages = list(dict.fromkeys(fighter_pages))

    return fighter_pages

def get_fighter_name(soup) -> str:
    # Gets the webpage's title and returns the fight's name from the meta tag
    title = soup.find("meta", property="og:title")
    fighter = title["content"].removesuffix(" | BJJ Heroes")
    return fighter


def get_table_rows(soup):
    # Returns an object containing all HTML table rows in the 'soup' input
    return soup.tbody.find_all('tr')

def convert_tr_to_list(tr) -> list:
    # Iterate over the 'tr' object, remove HTML tags, strip and separate with a comma, then convert it to a list of elements.
    # Returns a list of lists representing each row of data points.
    list = []
    index = 0
    for iter in tr:
        x = tr[index].get_text(",", strip=True)
        x = x.split(",")
        list.append(x)
        index += 1
    return list

def clean_rows(input, fighter_name):
    for i in input:
        # In some cases, the 'Opponent' column has a reference link to that person's page. The link is returned as it's on 'td' value and should be removed.
        if i[1] == i[2]:
            i.pop(1)

        # The first column comes back with some unknown id that can be removed.
        i.pop(0)

        # The figher's name that is being parsed needs to be added to the 'Fighter' column.
        i.insert(0, fighter_name)

        # Finally, the 'Method' column sometimes contains a string ' Adv' if both fighters tied and results were determined by an advantage.
        # This causes issues with the comma as a separate so let's take it out for now.
        if ' Adv' in i:
            i.remove(' Adv')
    return input

def wait_time(start_time, wait=4) -> float:
    if time.time() - start_time > wait:
        return 0
    else:
        return wait - (time.time() - start_time)
        
def save_to_csv(df, filename) -> None:
    """
    Save a pandas dataframe as a CSV file with the given filename.

    Args:
        df: pandas.DataFrame - The dataframe to be saved.
        filename: str - The name of the CSV file to be saved.
    """
    df.to_csv(filename, index=False)