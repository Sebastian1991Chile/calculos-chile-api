import json
from datetime import date
import bcchapi
import os
from dotenv import load_dotenv

def load_data():
    with open("data/ipc.json", "r", encoding="utf-8") as f:
        return json.load(f)

def get_last_period(data):
    if not data:
        return None
    else:
        last_year = '0'
        last_month = '0'
        last_day = '0'
        
        for period in data:
            periodSplit = period.split("-")
            year_period = periodSplit[0]
            month_period = periodSplit[1]
            day_period = periodSplit[2]

            if last_year < year_period:
                last_year = year_period
                last_month = month_period
                last_day = day_period
            elif last_year == year_period and last_month < month_period:
                last_month = month_period
                last_day = day_period
            elif last_year == year_period and last_month == month_period and last_day < day_period:
                last_day = day_period

        return f"{int(last_year):04d}-{int(last_month):02d}-{int(last_day):02d}"

def fetch_ipc_data(start_date, end_date):
    load_dotenv(override=True)
    token = os.getenv("BCCH_TOKEN")

    siete = bcchapi.Siete(token=token)

    if start_date == "1900-01-01":
        datos_historicos = siete.cuadro(
            series=["F074.IPC.IND.Z.200812.C.M"],
            desde="1928-12-01",
            hasta="2009-12-01"
        )

        datos_actuales = siete.cuadro(
            series=["F074.IPC.IND.Z.EP23.C.M"],
            desde="2009-12-01",
            hasta=end_date
        )
    else:
        datos_historicos = None
        datos_actuales = siete.cuadro(
            series=["F074.IPC.IND.Z.EP23.C.M"],
            desde=start_date,
            hasta=end_date
        )

    return datos_historicos, datos_actuales

def normalize_ipc_data(datos_historicos, datos_actuales):
    dic_actuales = dataframe_to_dict(datos_actuales)

    if datos_historicos is None:
        return dic_actuales
    else:
        dic_historicos = dataframe_to_dict(datos_historicos)
        factor = dic_actuales["2009-12-01"] / dic_historicos["2009-12-01"]

        dic_normalizado = {}
        for period in dic_historicos:
            if period != "2009-12-01":
                dic_normalizado[period] = dic_historicos[period] * factor

        return {**dic_normalizado, **dic_actuales}

def dataframe_to_dict(dataframe):
    data = {}

    for period, value in dataframe.iloc[:, 0].items():
        period = period.strftime("%Y-%m-%d")
        data[period] = value

    return data

def update_data(old_data, new_data):
    updated_data = old_data

    for period in new_data:
        updated_data[period] = new_data[period]
    
    return updated_data

def save_data(data):
    with open("data/ipc.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def update_ipc():
    old_data = load_data()
    start_date = get_last_period(old_data)

    if start_date is None:
        start_date = "1900-01-01"

    print(start_date)
    '''
    end_date = date.today().strftime("%Y-%m-%d")
    datos_historicos, datos_actuales = fetch_ipc_data(start_date, end_date)
    new_data_normalized = normalize_ipc_data(datos_historicos, datos_actuales)
    updated_data = update_data(old_data, new_data_normalized)
    save_data(updated_data)
    '''

update_ipc()        