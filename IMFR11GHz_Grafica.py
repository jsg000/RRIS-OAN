import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

micrasdato = pd.read_csv("datos.csv")# Archivo csv

micrasdato['uV']=micrasdato*(-1) # se multiplica por -1 a causa de que el diodo invierte la senal
micrasdato= micrasdato[micrasdato.uV > 0] # elimina los datos inconsistentes
micrasdato['W']= (pow((micrasdato['uV']*1e-6),2))/50 #escalado en Watts
n=np.arange(micrasdato.shape[0])*0.0261 # escala en grados acorde la velocidad del barrido
micrasdato['grados']=n
micrasdato.plot(x='grados', y='W',fontsize=16)
#print(micrasdato['W'].min(),micrasdato['W'].max())
plt.title('IMFR11GHz Sol d=0.55m')
plt.ylabel('watts',fontsize=16)
plt.xlabel('grados',fontsize=16)
plt.grid()
plt.show()
