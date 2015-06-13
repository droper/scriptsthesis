# coding: utf-8

"""Generate the datasets for testing"""

import pandas as pd
import subprocess

path = "/home/pedro/univs/doctorado/tesis/tesis/material tesis/datasets/modelo_minas/datos/"
path_dataset = "/home/pedro/univs/doctorado/tesis/tesis/material tesis/datasets/modelo_minas/"
filename = 'dataset_datos_southern.csv'

INCOME = 'income'
CATHODS = 'cathods'

# Load monthly cathods production
monthly_mine_data = pd.read_csv(path+'produccion_catodos_mensual.csv')

monthly_cathods = monthly_mine_data['Catodos Sulfuros']
monthly_cathods_ore = monthly_mine_data['Catodos Oxidos']
monthly_toquepala_concentrate = monthly_mine_data['Concentrados Toquepala']
monthly_cuajone_concentrate = monthly_mine_data['Concentrados Cuajone']

# Load annual material milled and grades of mineral
material_milled_grade = pd.read_csv(path+'material_molido_leyes_anual.csv')

# Load copper prices
copper_prices = pd.read_csv(path+"precio_cobre_mensual.csv")
copper_prices = copper_prices['Price act']

# Load petroleum prices
petroleum_prices = pd.read_csv(path+"precio_petroleo_mensual.csv")
petroleum_prices = petroleum_prices['Precio act']

# Load petroleum prices
silver_prices = pd.read_csv(path+"precio_plata_mensual.csv")
silver_prices = silver_prices['Precio act']

# Load tipo de cambio
tipo_cambio = pd.read_csv(path+"tipo_cambio.csv")
tipo_cambio = tipo_cambio['TC']

# Load southern peru data
southern_income_utilities = pd.read_csv(path+"datos_financieros_southern.csv")

southern_income = southern_income_utilities['Ingreso total act']
southern_utilities = southern_income_utilities['Utilidad act']
southern_interest = southern_income_utilities['Gasto financiero act']
southern_depreciation = southern_income_utilities['Depreciacion act']

# Load inflation data
peru_inflation_data = pd.read_csv(path+"inflacion_peru.csv")
usa_inflation_data = pd.read_csv(path+"inflacion_usa.csv")

peru_inflation_data = peru_inflation_data["Inflacion"]
usa_inflation_data = usa_inflation_data["Inflacion"]

# Slice data since 2001
material_milled_grade_b2001 = material_milled_grade[:7]
#material_milled_grade2001 = material_milled_grade[7:]
material_milled_grade2001 = material_milled_grade


# Columns names
columns = ['Periodo', 'TM Mineral Cuajone', 'Ley cobre Cuajone',
           'Porc Recuperacion Cuajone',
           'TM Mineral Toquepala', 'Ley cobre Toquepala',
           'Porc Recuperacion Toquepala', 'Catodos Sulfuros',
           'TM Mineral Toquepala Oxidos', 'TM Mineral Cuajone Oxidos',
           'Ley Toquepala Oxidos', 'Ley Cuajone Oxidos',
           'Con Toquepala', 'Con Cuajone',
           'Porc Recuperacion Lix','Catodos Oxidos', 'Precio',
           'Gasto financiero',
           'Depreciacion',
           'Ingresos', 'Tipo Cambio',
           'Inflacion Peru','Inflacion Usa',
           'Precio Petroleo',
           'Precio Plata',
           'Utilidad']

data = pd.DataFrame(columns=columns)

period = 4
bias = 0                # Number of months forward in time
cathods_file_count = bias

dataset_type = INCOME

# Iterate over annual material miller
for row in material_milled_grade2001.iterrows():
    # Copy 'period' times the monthly material milled.
    anno = row[1]['Periodo']
    cuajone_mill_mat = row[1]['TM Mineral Cuajone']/period
    toquepala_mill_mat = row[1]['TM Mineral Toquepala']/period
    cuajone_leach_mill_mat = row[1]['TM Mineral Cuajone Oxidos']/period
    toquepala_leach_mill_mat = row[1]['TM Mineral Toquepala Oxidos']/period

    # Assign the new values to the row
    row[1]['TM Mineral Cuajone'] = cuajone_mill_mat
    row[1]['TM Mineral Toquepala'] = toquepala_mill_mat
    row[1]['TM Mineral Cuajone Oxidos'] = cuajone_leach_mill_mat
    row[1]['TM Mineral Toquepala Oxidos'] = toquepala_leach_mill_mat

    # Copy data period times
    for i in xrange(period):
        # In each iteration initialize with cero
        row[1]['Catodos Sulfuros'] = 0
        row[1]['Catodos Oxidos'] = 0
        row[1]['Precio'] = 0
        row[1]['Con Toquepala'] = 0
        row[1]['Con Cuajone'] = 0

        # If dataset to be generated will have income data
        if dataset_type == INCOME:
            row[1]['Ingresos'] = southern_income[len(data)]
            row[1]['Utilidad'] = southern_utilities[len(data)]
            row[1]['Gasto financiero'] = southern_utilities[len(data)]
            row[1]['Depreciacion'] = southern_depreciation[len(data)]

        # Add the Period to the Row
        row[1]['Periodo'] = row[1]['Periodo'] + " " + str(i+1)

        # Add the monthly cathods and prices by the period. If period is one, then add 12
        # months. If period is 2, then add six months and so
        for j in xrange(12/period):
            row[1]['Catodos Sulfuros'] = row[1]['Catodos Sulfuros'] + \
                                          monthly_cathods[cathods_file_count+j]
            row[1]['Catodos Oxidos'] = row[1]['Catodos Oxidos'] + \
                                          monthly_cathods_ore[cathods_file_count+j]
            row[1]['Precio'] = row[1]['Precio'] + copper_prices[cathods_file_count+j]
            row[1]['Precio Petroleo'] = row[1]['Precio Petroleo'] + \
            petroleum_prices[cathods_file_count+j]
            row[1]['Precio Plata'] = row[1]['Precio Plata'] + \
            silver_prices[cathods_file_count+j]
            row[1]['Tipo Cambio'] = row[1]['Tipo Cambio'] + tipo_cambio[cathods_file_count+j]
            row[1]['Inflacion Peru']=row[1]['Inflacion Peru']+peru_inflation_data[cathods_file_count+j]
            row[1]['Inflacion Usa'] = row[1]['Inflacion Usa'] + usa_inflation_data[cathods_file_count+j]
            row[1]['Con Toquepala'] = row[1]['Con Toquepala'] + \
                               monthly_toquepala_concentrate[cathods_file_count+j]
            row[1]['Con Cuajone'] = row[1]['Con Cuajone'] + \
                               monthly_cuajone_concentrate[cathods_file_count+j]


        # The average price
        row[1]['Precio'] = row[1]['Precio']/period
        row[1]['Precio Petroleo'] = round(row[1]['Precio Petroleo']/period, 2)
        row[1]['Precio Plata'] = round(row[1]['Precio Plata']/period, 2)
        # The average exchange rate
        row[1]['Tipo Cambio'] = round(row[1]['Tipo Cambio']/period, 2)
        row[1]['Inflacion Peru'] = round(row[1]['Inflacion Peru']/period, 2)
        row[1]['Inflacion Usa'] = round(row[1]['Inflacion Usa']/period, 2)
        # Add the period number to the counter 
        cathods_file_count += 12/period
        print cathods_file_count

        # Add row to the data DataFrame
        data.loc[len(data)] = row[1]

        row[1]['Periodo'] = anno


data.to_csv(path+filename, index=False)


