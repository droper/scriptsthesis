# Directorios origen de la data
DATA_TIPO_CAMBIO = "/home/pedro/univs/doctorado/tesis/tesis/material tesis/data_economica/"
TIPO_CAMBIO_CSV = "tipo_cambio.csv"
TIPO_CAMBIO_TRIM_CSV = "tipo_cambio_trimestral.csv"
TIPO_CAMBIO_ANUAL_CSV = "tipo_cambio_anual.csv"



# Se lee un archivo de información financiera
tipo_cambio = read.csv(file=paste(DATA_TIPO_CAMBIO, TIPO_CAMBIO_CSV, sep=""),
                         header=TRUE, sep=",", colClasses = c("character", "numeric"))

tc_trim  = numeric(0)
per_trim = character(0)
anno     = 1992

i = 3
per = 1

# Se generan los promedios trimestrales
while (i <= nrow(tipo_cambio)){
  promedio = (tipo_cambio[["TC"]][i] + tipo_cambio[["TC"]][i-1] + tipo_cambio[["TC"]][i-2])/3
  tc_trim = c(tc_trim, promedio)
  per_trim =  c(per_trim, paste(anno,'-',per, sep="" ))
  
  i = i + 3
  
  # Si periodo es igual a cuatro, lo regresamos a uno
  # y aumentamos en uno el año
  if (per == 4){
    per = 1
    anno = anno + 1
  }  
  else {
    per = per + 1
  }
}


tc_anual  = numeric(0)
per_anual = character(0)
anno      = 1992
i = 12

# Se generan los promedios anuales
while (i <= nrow(tipo_cambio)){
  promedio = (tipo_cambio[["TC"]][i] + tipo_cambio[["TC"]][i-1] + tipo_cambio[["TC"]][i-2] + tipo_cambio[["TC"]][i-3] 
              + tipo_cambio[["TC"]][i-4] + tipo_cambio[["TC"]][i-5] + tipo_cambio[["TC"]][i-6] + tipo_cambio[["TC"]][i-7]
              + tipo_cambio[["TC"]][i-8] + tipo_cambio[["TC"]][i-9] + tipo_cambio[["TC"]][i-10] + tipo_cambio[["TC"]][i-11])/12
  tc_anual = c(tc_anual, promedio)
  per_anual =  c(per_anual, anno)
  
  i = i + 12
  anno = anno + 1
}


# Se generan los promedios trimestrales del tipo de cambio juntando los vectores
tipo_cambio_trim = data.frame(per_trim, tc_trim)
    
# Se generan los promedios anuales del tipo de cambio juntando los vectores
tipo_cambio_anual = data.frame(per_anual, tc_anual)    

# Se escribe el data frame de datos para las pruebas en un archivo cuyo prefijo es
# pruebas
write.csv(tipo_cambio_trim, file=paste(DATA_TIPO_CAMBIO, 
          TIPO_CAMBIO_TRIM_CSV, sep=""), sep=",", row.names=FALSE)
write.csv(tipo_cambio_anual, file=paste(DATA_TIPO_CAMBIO, 
          TIPO_CAMBIO_ANUAL_CSV, sep=""), sep=",", row.names=FALSE)

