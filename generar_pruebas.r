# Directorios origen de la data
DIRECTORIO_DATA = "/home/pedro/univs/doctorado/tesis/tesis/material tesis/data_estados_financieros/"
PREDICCIONES_PAISES = "/home/pedro/univs/doctorado/tesis/tesis/material tesis/predicciones/imf/crecimiento_paises.csv"
PREDICCIONES_COMMODITIES = "/home/pedro/univs/doctorado/tesis/tesis/material tesis/predicciones/wb_commodities/predicciones_commodities.csv"
DIRECTORIO_PRUEBAS = "/home/pedro/univs/doctorado/tesis/tesis/material tesis/datasets/data_original/"

# Lee los nombres de los archivos con la data de los estados financieros
archivos_data = list.files(DIRECTORIO_DATA)

# Se itera sobre cada archivo 
for (archivo in archivos_data){
    
    print(archivo)
    # Se lee un archivo de información financiera
    empresa = read.table(file=paste(DIRECTORIO_DATA, archivo, sep=""),
                         header=TRUE, sep=",")

    # Se elimina las tres últimas filas debido a que no se necesita esa data 
    empresa = empresa[1:(nrow(empresa)-2),]

    # Se leen las predicciones de crecimiento económico y de precios de los
    # commodities
    commodities = read.table(file=PREDICCIONES_COMMODITIES, header=TRUE, sep=",")
    paises = read.table(file=PREDICCIONES_PAISES, header=TRUE, sep=",")

    # Se genera la data de prueba juntando todos los sets de datos
    prueba = data.frame(empresa, commodities[,-1], paises[,-1])
    
    # Se eliminan las dos primeras columnas (número y periodo)
    # prueba$periodo = NULL
    

    # Se eliminan las filas que no tienen data
    i = 1
    while (i <= nrow(prueba)){
        if (prueba[["activos"]][i] == 0) {
           prueba = prueba[-(i),]
           i = i - 1
        }

        i = i + 1
    }
    

    # Se escribe el data frame de datos para las pruebas en un archivo cuyo prefijo es
    # pruebas
    write.csv(prueba, file=paste(DIRECTORIO_PRUEBAS, "prueba_",
          archivo, sep=""), sep=",", row.names=FALSE)
}
