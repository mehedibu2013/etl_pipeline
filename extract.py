import requests
import pandas as pd


def fetch_users():
    url = "https://jsonplaceholder.typicode.com/users"
    response = requests.get(url)
    data = response.json()

    # Flatten company dictionary
    for user in data:
        user['company_name'] = user['company']['name']
        del user['company']  # Optional: remove original dict column

    df = pd.DataFrame(data)
    return df[['id', 'name', 'email', 'company_name']]