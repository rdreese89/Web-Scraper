from bs4 import BeautifulSoup
import requests
import time
import pandas as pd
import functions as f


df = pd.DataFrame(columns=['Fighter', 'Opponent', 'W/L', 'Method', 'Competition', 'Weight', 'Stage', 'Year'])

error_count = {
    'Append Row Error': 0, 
    'No Table Body Found': 0,
    'Response Error': 0}

ID = f.get_fighter_pages()


for i in ID:
    URL = "https://www.bjjheroes.com/?p=" + str(i)
    ts1 = time.time()
    response = requests.get(URL)

    if response.status_code == 200:
        print("Successful connection to: " + URL)
        soup = BeautifulSoup(response.content, 'html.parser')
    else:
        print("Status Code Error: " + str(response.status_code))
        error_count["Response Error"] += 1
        print("Waiting " + str(f.wait_time(ts1)) + " seconds")
        time.sleep(f.wait_time(ts1))
        continue

    try:
        tr = f.get_table_rows(soup) 
    except:
        print("No TR found in the table body. Breaking loop for ID: " + str(i))
        error_count['No Table Body Found'] += 1
        print("Waiting " + str(f.wait_time(ts1)) + " seconds")
        time.sleep(f.wait_time(ts1))
        continue

    fighter_name = f.get_fighter_name(soup) # Get the fighter's name from the webpage meta title

    list = f.convert_tr_to_list(tr) # Convert the 'tr' object to a list of lists, then clean bad data from the rows
    list = f.clean_rows(list, fighter_name)

    for i in list: # Add each list element as a new row in the dataframe
        try:
            df.loc[len(df)] = i
        except:
            print("Error while appending")
            error_count['Append Row Error'] += 1

    print("Waiting " + str(f.wait_time(ts1)) + " seconds")
    time.sleep(f.wait_time(ts1))

f.save_to_csv(df, "data.csv")
print(error_count)
