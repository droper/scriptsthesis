# Directorios origen de la data
DIRECTORIO_DATA = "/home/pedro/univs/doctorado/tesis/tesis/material tesis/data_estados_financieros/"
PREDICCIONES_PAISES = "/home/pedro/univs/doctorado/tesis/tesis/material tesis/predicciones/imf/crecimiento_paises.csv"
PREDICCIONES_COMMODITIES = "/home/pedro/univs/doctorado/tesis/tesis/material tesis/predicciones/wb_commodities/predicciones_commodities.csv"
DIRECTORIO_PRUEBAS = "/home/pedro/univs/doctorado/tesis/tesis/material tesis/datasets/data_ratios/"

columnas_dataset = c("ROA","VAR_ROA","ROE","VAR_ROE","FLUJO_CAJA","VAR_CUENTAS_COBRAR",
                     "VAR_GM","DIV_UTIL","INV_CAP","LIQUID","EMISION", "UTILIDAD")

prom_inv_cap = 0

# Lee los nombres de los archivos con la data de los estados financieros
archivos_data = list.files(DIRECTORIO_DATA)

# Se leen las predicciones de crecimiento económico y de precios de los
# commodities
commodities = read.table(file=PREDICCIONES_COMMODITIES, header=TRUE, sep=",")
paises = read.table(file=PREDICCIONES_PAISES, header=TRUE, sep=",")

# Vector donde se guardan los promedios de inversión de capital en un año
promedios_inv = matrix(0,nrow(commodities))

# Se suman las inversiones de capital de las empresas en cada periodo
# Luego se promediaran
for (archivo in archivos_data){
  # Se lee un archivo de información financiera
  empresa = read.csv(file=paste(DIRECTORIO_DATA, archivo, sep=""),
                     header=TRUE, sep=",")
  
  for (i in 1:nrow(empresa)){
    promedios_inv[i] = promedios_inv[i] + empresa[i,"inv_capital"]
  }
}

# Se obtienen los promedios
promedios_inv = promedios_inv/length(archivos_data)

# Se itera sobre cada archivo para generar los ratios
for (archivo in archivos_data){
    commodities_aux = commodities
    paises_aux      = paises
    promedios_inv_aux = promedios_inv

    # Se lee un archivo de información financiera
    empresa = read.csv(file=paste(DIRECTORIO_DATA, archivo, sep=""),
                         header=TRUE, sep=",")
    
    # Se eliminan las filas que no tienen data
    i = 1
    while (i <= nrow(empresa)){
      if (empresa[["activos"]][i] == 0) {
        empresa = empresa[-(i),]
        commodities_aux = commodities_aux[-(i),]
        paises_aux      = paises_aux[-(i),]
        promedios_inv_aux = promedios_inv_aux[-(i)]
        i = i - 1
      }
      
      i = i + 1
    }
    
    # Se crea un dataset para guardar toda la data
    dataset = matrix(nrow = nrow(empresa), ncol = NROW(columnas_dataset), 
                    dimnames = list(c(1:nrow(empresa)),columnas_dataset))
     
    for (i in 1:nrow(empresa)){
       print(i)
       dataset[i,"ROA"] = round(empresa[i,"ing_act_ord"]/empresa[i,"activos"],3)
       dataset[i,"ROE"] = round(empresa[i,"ing_act_ord"]/empresa[i,"valor_libros"],3)
       dataset[i,"FLUJO_CAJA"] = round(empresa[i,"flujo_efectivo"]/empresa[i,"activos"],3)
       dataset[i,"DIV_UTIL"] = round(empresa[i,"dividendos"]/empresa[i,"utilidades"],3)  
       dataset[i,"UTILIDAD"] = empresa[i,"utilidades"]
               
       # Si se emiten acciones es 1, caso contrario es 0
       if (empresa[i,"emision_acciones"] != 0){
         dataset[i,"EMISION"] = 1
       } 
       else{
         dataset[i,"EMISION"] = 0
       }
       
       # Se calculan las variaciones que utilizan ratios previamente calculados
       if (i > 1){
         dataset[i,"INV_CAP"] = round(promedios_inv_aux[i] - promedios_inv_aux[i-1],3)
         dataset[i,"VAR_ROA"] = dataset[i,"ROA"] - dataset[i-1,"ROA"]
         dataset[i,"VAR_ROE"] = dataset[i,"ROE"] - dataset[i-1,"ROE"]
         dataset[i,"VAR_CUENTAS_COBRAR"] = round((empresa[i,"ventas"]-empresa[i-1,"ventas"])/empresa[i-1,"ventas"] -
                   (empresa[i,"cuentas_cobrar"]-empresa[i-1,"cuentas_cobrar"])/empresa[i-1,"cuentas_cobrar"],3)  
         dataset[i,"VAR_GM"] = round(empresa[i,"ing_act_ord"]-empresa[i,"costo_operacion"],3) -
                               round(empresa[i-1,"ing_act_ord"]-empresa[i-1,"costo_operacion"],3)
         dataset[i,"LIQUID"] = round(empresa[i,"act_circulante"]/empresa[i,"deuda_corto_plazo"],3) -
                           round(empresa[i-1,"act_circulante"]/empresa[i-1,"deuda_corto_plazo"],3)
         
         # Para las variaciones de la primera instancia donde no hay data previa se utiliza el mismo
         # número de la siguiente instancia
         if (i == 2) {
           dataset[i-1,"INV_CAP"] = dataset[i,"INV_CAP"]
           dataset[i-1,"VAR_ROA"] = dataset[i,"VAR_ROA"]
           dataset[i-1,"VAR_ROE"] = dataset[i,"VAR_ROE"]
           dataset[i-1,"VAR_CUENTAS_COBRAR"] = dataset[i,"VAR_CUENTAS_COBRAR"]
           dataset[i-1,"VAR_GM"] = dataset[i,"VAR_GM"]
           dataset[i-1,"LIQUID"] = dataset[i,"LIQUID"]
         }
       }
              
    }

    # Se terminan los ratios para la data de prueba juntando todos los sets de datos
    prueba = data.frame(dataset, commodities_aux[,-1], paises_aux[,-1])

    # Se escribe el data frame de datos para las pruebas en un archivo cuyo prefijo es
    # pruebas
    write.csv(prueba, file=paste(DIRECTORIO_PRUEBAS, "prueba_",
          archivo, sep=""), sep=",")
}
