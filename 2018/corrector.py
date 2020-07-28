import argparse
import os
import shutil
from subprocess import run

from probar_entrega1 import probar

import pandas as pd

BASE_PATH = os.path.realpath(os.path.join(os.path.dirname(__file__)))


def bajar_repositorio(info_grupo):
    print("Cloning", info_grupo['grupo'])
    grupo_path = os.path.join(BASE_PATH, info_grupo.grupo)
    if os.path.exists(grupo_path):
        shutil.rmtree(grupo_path)
    if info_grupo.cvs == 'git':
        cmd = '{cvs} clone {cvs}@{servicio}:{url} {grupo}'.format(**info_grupo.to_dict())
    elif info_grupo.cvs == 'hg':
        cmd = '{cvs} clone ssh://{cvs}@{servicio}/{url} {grupo}'.format(**info_grupo.to_dict())

    print("About to execute:", cmd)
    run(cmd, shell=True)


def correr_pruebas(info_grupo):
    probar(grupo=info_grupo.grupo)


def main(grupo=None, mantener_repositorio=False):
    grupos = pd.read_csv('repos.config', sep='|')
    if grupo is not None:
        grupos = grupos[grupos.grupo == grupo]

    for _, info_grupo in grupos.iterrows():
        print("#"*160)
        print("#"*160)
        print("Grupo ", info_grupo.grupo)
        if mantener_repositorio:
            print("Se saltea la actualización del repositorio")
        else:
            bajar_repositorio(info_grupo)
        correr_pruebas(info_grupo)
        print("#"*160)
        print("#"*160)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--grupo', help='Grupo en particular')
    parser.add_argument('--mantener_repositorio', action='store_true', help='Evita volver a clonar el repo')
    args = parser.parse_args()

    main(args.grupo, args.mantener_repositorio)
