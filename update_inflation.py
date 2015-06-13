# coding: utf-8

"""Script para agregar el valor actualizado de los valores en dólares"""

import pandas as pd

path = "/home/pedro/univs/doctorado/tesis/tesis/material tesis/datasets/modelo_minas/datos/"
update_filename = 'precio_plata_mensual.csv'
inflation_filename = 'inflacion_usa.csv'

def update_inflation_monthly(path, inflation_filename, update_filename):
    """Function to create updated prices"""

    inflation_data = pd.read_csv(path+inflation_filename)
    update_file = pd.read_csv(path+update_filename)

    update_file['Precio act'] = \
            update_file['Precio']*inflation_data['Tasa act']
    update_file['Precio act'] = update_file['Precio act'].apply(lambda x: round(x, 3))

    # generate new csv
    update_file.to_csv(path+update_filename, index=False)

def update_inflation_trimestral(path, inflation_filename, update_filename):
    """Function to create updated prices"""

    inflation_data = pd.read_csv(path+inflation_filename)
    update_file = pd.read_csv(path+update_filename)

    # Create the new column 
    update_file['Precio act'] = update_file['Precio']

    inflation_row = -1
    # Average trimestral depreciation
    for i in range(len(update_file)):
        avg_tasa_act = 0

        # Tasa act for the trimester
        inflation_row += 3
        tasa_act = inflation_data['Tasa act'][inflation_row]

        # The actualized depreciation 
        update_file['Precio act'][i] = \
        round(update_file['Precio'][i]*tasa_act, 2)

    # generate new csv
    update_file.to_csv(path+update_filename, index=False)


update_inflation_monthly(path, inflation_filename, update_filename)


