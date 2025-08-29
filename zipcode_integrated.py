import requests
import xml.etree.ElementTree as ET
import pandas as pd
import time

# Lê a lista de cidades com lat e lon de um Excel
cities_df = pd.read_excel('cities.xlsx')  # Colunas: city, state, lat, lon

all_data = []

for index, row in cities_df.iterrows():
    lat = row['lat']
    lon = row['lon']
    radius = 20
    city_name = row['city']
    state = row['state']
    
    url = f"https://www.freemaptools.com/ajax/us/get-all-zip-codes-inside-radius.php?radius={radius}&lat={lat}&lng={lon}&rn=6528&showPOboxes=true"
    
    payload = {}
    headers = {
    'accept': 'application/xml, text/xml, */*; q=0.01',
    'accept-language': 'pt-BR,pt;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'priority': 'u=1, i',
    'referer': 'https://www.freemaptools.com/find-zip-codes-inside-radius.htm',
    'sec-ch-ua': '"Not;A=Brand";v="99", "Microsoft Edge";v="139", "Chromium";v="139"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0',
    'x-requested-with': 'XMLHttpRequest',
    'Cookie': 'PHPSESSID=87b49d22602f0132c693c6bfa174d703; _ga_4HJBJJBR6Z=GS2.1.s1756494008$o1$g0$t1756494008$j60$l0$h0; _ga=GA1.1.504245635.1756494008; __gads=ID=e4a5bb9eb39c907a:T=1756494009:RT=1756494009:S=ALNI_MYGA_px-qm6OGoaKXTg-vOU87LOzg; __gpi=UID=000012761a5acaef:T=1756494009:RT=1756494009:S=ALNI_MZSxfAXjyWG7vxfiI_CMqXDS3sQ8g; __eoi=ID=1abb64eb9ac4fabc:T=1756494009:RT=1756494009:S=AA-AfjYrSZo53g8X-h1S5XnqoupW; FCNEC=%5B%5B%22AKsRol8NK7YPk-PkF2dflScRUMSR5QtG74Y6tk1LBaSUHOBYjn3APTSoFUif6q3b09fgPFi-6bF8QGYpdWucyMK3juiEiDZEfyLS6vzhSFxFWSti2KnPEO33rrA3oMUT3l5OwjQw_V6XuvUYwQKsTe2AShuOAOvu2w%3D%3D%22%5D%5D'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    if response.status_code != 200:
        print(f"Erro ao consultar {city_name}, {state}")
        continue
    
    root = ET.fromstring(response.text)
    
    for postcode in root.findall('postcode'):
        all_data.append({
            'City': city_name,
            'State': state,
            'Zipcode': postcode.get('postcode'),
            'Combined': f"{postcode.get('city')}, {postcode.get('state')}"
        })

    time.sleep(5)

# Cria DataFrame único
final_df = pd.DataFrame(all_data)

# Salva em Excel
final_df.to_excel('all_zipcodes.xlsx', index=False)

print("Arquivo Excel final gerado com sucesso!")
