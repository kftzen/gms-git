import pandas as pd
import numpy as np
import os
import re


def get_files():
    pth_files = os.path.abspath("../request-asa/files")
    lst_files = os.listdir(pth_files)
    return lst_files

def get_df(nm_file):
    pth_files = os.path.abspath("../request-asa/files")
    pth_file = os.path.join(pth_files,nm_file)
    with open(pth_file,encoding="latin1") as f:
        dt_ace = [f.readline() for n in range(0,47)].\
            pop().split("/")[1:]
        dt_ace = [float(dt) for dt in dt_ace \
            if float(dt) != 0].pop()
    df_ace = pd.read_csv(
        pth_file,
        sep="\s+",
        skiprows=[x for x in range(0,109) if x != 107],
        header=0,
        engine="python",
        dtype=np.float64,
        encoding="latin1"
        )
    print(df_ace.head(1))
    len_ace = len(df_ace)

    # Las siguientes ordenes reducen el diferencial de tiempo
    # a 0.02, normalizando nuestra base de datos a dt = 0.02.
    # Esto es debido a que para el alcance del proyecto, solo
    # se necesita este nivel de precisión.

    o_index = np.arange(0,len_ace,0.02/dt_ace,dtype=np.int16)
    df_ace = df_ace[df_ace.index.isin(o_index)]
    df_ace = df_ace.reset_index(drop=True)

    # Regresa un objeto tipo DataFrame, para el manejo de los
    # datos.

    return df_ace


def save_feather(df,nm_file):
    pth_files = os.path.abspath("../process-asa/files/acce")
    pth_file = os.path.join(pth_files,nm_file+".feather")
    df.to_feather(pth_file)

def print_acce(pth_file):
    print(pd.read_feather(pth_file))

class Newmark():
    def __init__(self,damping=0.05):
        # Ignora la división entre cero en la primera
        # iteración.
        np.seterr(divide="ignore",invalid="ignore")
        pth_ps = os.path.\
            abspath("../process-asa/files/ps_acce")
        # Calcula las variables necesarias para el
        # ánalisis de Newmark.
        dt = 0.02
        t = np.arange(0,5+dt,dt)
        omega = (2*np.pi)/t
        c = damping * 2 * omega
        k = omega ** 2
        a1 = 4/(dt**2)+2*c/dt
        a2 = 4/dt+c
        k = k + a1
        st_t = t.size
        # Asigna las variables a los atributos de la
        # clase Newmark.
        self.pth_ps = pth_ps
        self.dt = dt
        self.omega = omega
        self.a1 = a1
        self.a2 = a2
        self.k = k
        self.st_t = st_t

    def retrive_files(self):
        # Genera una lista de la dirección de cada uno
        # de los archivos disponibles.
        pth_acce = os.path.abspath("../process-asa/files/acce")
        lst_acce = os.listdir(pth_acce)
        pth_acce = [os.path.join(pth_acce,f) for f in lst_acce]        
        return pth_acce

    def newmark_b(self,pth):
        pth_ps = self.pth_ps
        dt = self.dt
        omega = self.omega
        a1 = self.a1
        a2 = self.a2
        k = self.k
        st_t = self.st_t       
        df_acce = pd.read_feather(pth)
        df_ps_acce = pd.DataFrame()
        for label,content in df_acce.items():
            i = content.to_numpy()
            st_i = i.size
            # Preasignación de espacio en la memoria para
            # las matrices de la iteración.
            a = np.empty([st_i,st_t],dtype=np.float64)
            v = np.empty([st_i,st_t],dtype=np.float64)
            d = np.empty([st_i,st_t],dtype=np.float64)
            p = np.empty([st_i,st_t],dtype=np.float64)
            # Asignación de condiciones iniciales del
            # sistema.
            a[0,:] = i[0]
            v[0,:] = 0
            d[0,:] = 0
            p[0,:] = 0
            # Realiza las siguientes iteraciones para
            # el calculo de la pseudo-aceleración.
            for n in range(1,st_i):
                p[n,:] = i[n]+a1[:]*d[n-1,:] \
                    +a2[:]*v[n-1,:]+a[n-1,:]
                d[n,:] = p[n,:]/k[:]
                v[n,:] = (2*(d[n,:]-d[n-1,:])/dt) \
                    -v[n-1,:]
                a[n,:] = (4*(d[n,:]-d[n-1,:])/(dt**2)) \
                    - 4*v[n-1,:]/dt - a[n-1,:]
            # Obtiene los desplazamientos máximos para cada
            # periodo de vibrar y calcula la pseudo-aceleración.
            ps_acce = np.amax(np.absolute(d),axis=0)*omega**2
            df_ps_acce[label] = ps_acce
        fl_name = os.path.split(pth)[-1]
        pth_ps = os.path.join(pth_ps,fl_name)
        print(df_ps_acce.head(2))
        print("Procesando el archivo {}"\
            .format(fl_name)) 
        df_ps_acce.to_feather(pth_ps)
