# coding: utf-8

"""Generate the dataset for test with only the needed data"""

import pandas as pd

# Columns to delete
delete_cols = ['Periodo', 'TM Mineral Cuajone','TM Mineral Toquepala',
               'TM Mineral Toquepala Oxidos', 'TM Mineral Cuajone Oxidos',
               'Con Toquepala', 'Con Cuajone', 'Ley cobre Cuajone', 'Ley cobre Toquepala',
               'Porc Recuperacion Toquepala',
               'Inflacion Usa',
               'Inflacion Peru',
               'Precio Petroleo',
               'Precio Plata',
               'Porc Recuperacion Cuajone', 'Ingresos']


# Path of the data
path = "/home/pedro/univs/doctorado/tesis/tesis/material tesis/datasets/modelo_minas/datos/"
dataset_filename = 'dataset_datos_southern.csv'

test_filename = "test.csv"

# read the dataset
data = pd.read_csv(path+dataset_filename)

# Add the amount of milled material
data['TM Mineral'] = data['TM Mineral Cuajone'] + data['TM Mineral Toquepala']

# Ponderate average of the Ley del cobre
data['Ley Cobre'] = ((data['Ley cobre Toquepala']*data['Con Toquepala']
                     + data['Ley cobre Cuajone']*data['Con Cuajone'])/(
                     data['Con Toquepala']+data['Con Cuajone']))*100
data['Ley Cobre'] = data['Ley Cobre'].apply(lambda x: round(x, 3))

# Add the amount off Concentrados
data['Concentrados'] = data['Con Toquepala']+data['Con Cuajone']

# Ponderate average of Porcentaje de Recuperacion
data['Porc Recup'] = ((data['Porc Recuperacion Toquepala']*data['Con Toquepala']
                     + data['Porc Recuperacion Cuajone']*data['Con Cuajone'])/(
                     data['Con Toquepala']+data['Con Cuajone']))
data['Porc Recup'] = data['Porc Recup'].apply(lambda x: round(x, 3))

# Add the amount of Oxidos
#data['TM Mineral Oxidos'] = data['TM Mineral Toquepala Oxidos'] + \
#                            data['TM Mineral Cuajone Oxidos']

# Ponderate average of the Ley del mineral 
#data['Ley Oxidos'] = ((data['Ley Toquepala Oxidos']*data['TM Mineral Toquepala Oxidos']
#                     + data['Ley Cuajone Oxidos']*data['TM Mineral Cuajone Oxidos'])/(
#                     data['TM Mineral Toquepala Oxidos'] +
#                     data['TM Mineral Cuajone Oxidos']))*100
data['Ley Cuajone Oxidos'] = (data['Ley Cuajone Oxidos']*100).apply(lambda x: round(x, 3))
data['Ley Toquepala Oxidos'] = (data['Ley Toquepala Oxidos']*100).apply(lambda x: round(x, 3))

# Delete columns
data = data.drop(delete_cols, axis=1)

# Replace 

# generate new csv
data.to_csv(path+test_filename, index=False)

