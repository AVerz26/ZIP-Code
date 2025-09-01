import requests
import xml.etree.ElementTree as ET
import pandas as pd
import time
import streamlit as st
from io import BytesIO

st.title("Zip Codes Finder")


# Input múltiplo de cidades
cities_input = st.text_area("Enter city names (one per line):")
radius = st.number_input("Enter the radius (miles):", min_value=1, value=20)

df_princ = []

if st.button("Get Zip Codes"):

    with st.status("Downloading data...", expanded=True) as status:
        
        all_data = []

        # Processa cada cidade
        for city_input in cities_input.splitlines():
            city_input = city_input.strip()
            if not city_input:
                continue

            # HEADERS GEOCODE
            geocode_headers = {
            'accept': '*/*',
            'accept-language': 'pt-BR,pt;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJtYXBzYXBpIiwidGlkIjoiMk01MzgyRkRKTiIsImFwcGlkIjoiMk01MzgyRkRKTi5tYXBzLm9yZy5ncHMtY29vcmRpbmF0ZXMiLCJpdGkiOmZhbHNlLCJpcnQiOmZhbHNlLCJpYXQiOjE3NTY1MDg3MjAsImV4cCI6MTc1NjUxMDUyMCwib3JpZ2luIjoiaHR0cHM6Ly9ncHMtY29vcmRpbmF0ZXMub3JnIn0.wIWtc6tCNOEJI8G82e86xD2CBosAA7LmCekt5zcvtHcKpwMDU7ejgcMCjJXQpsfi5gVCp0cGUxcNC_PnLtNybw',
            'origin': 'https://gps-coordinates.org',
            'priority': 'u=1, i',
            'referer': 'https://gps-coordinates.org/',
            'sec-ch-ua': '"Not;A=Brand";v="99", "Microsoft Edge";v="139", "Chromium";v="139"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0'
            }

            geocode_url = f"https://nominatim.openstreetmap.org/search?city={city_input}&format=json"
            geo_resp = requests.get(geocode_url, headers=geocode_headers)

            st.write(f"Searching for {city_input} geo data...")

            if geo_resp.status_code != 200 or not geo_resp.json():
                st.error(f"Could not geocode city {city_input}")
                continue

            
            geo_data = geo_resp.json()[0]
            lat, lon = geo_data["lat"], geo_data["lon"]

            lista = [city_input, lat, lon]

            df_princ.append(lista)

            # HEADERS ZIP
            zip_headers = {
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

            
            zip_url = f"https://www.freemaptools.com/ajax/us/get-all-zip-codes-inside-radius.php?radius={radius}&lat={lat}&lng={lon}&rn=6528&showPOboxes=true"
            zip_resp = requests.get(zip_url, headers=zip_headers)

            st.write(f"Searching for {city_input} zip codes data...")

            if zip_resp.status_code != 200:
                st.error(f"Erro ao consultar {city_input}")
                continue

            root = ET.fromstring(zip_resp.text)

            for postcode in root.findall("postcode"):
                all_data.append({
                    "City": city_input,
                    "Zipcode": postcode.get("postcode"),
                    "Combined": f"{postcode.get('city')}, {postcode.get('state')}"
                })

            time.sleep(1)

        df_map = pd.DataFrame(df_princ, columns=["City", "lat", "lon"])
        df_map["lat"] = df_map["lat"].astype(float)
        df_map["lon"] = df_map["lon"].astype(float)

        status.update(
        label="Download complete!", state="complete", expanded=False
    )

    if all_data:
        final_df = pd.DataFrame(all_data)

        st.write(f'Total found zip codes: {len(final_df)}')
        a, b = st.columns()
        with a:
            st.map(df_map)
    
                # Salva em excel direto na memória
        with b:
            output = BytesIO()
            with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
                final_df.to_excel(writer, index=False)
            output.seek(0)
    
            st.download_button(
                label="Download File",
                data=output,
                file_name="data_formatted.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )
    
            st.dataframe(final_df)
    else:
        st.warning("Nenhum zip code encontrado.")

