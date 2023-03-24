#!/bin/python3
"""papersnake es un script de cli para establecer
fondos de pantalla con la ayuda de feh en ditribuciones de GNU/Linux"""

import subprocess
import random
import time
import argparse
from pathlib import Path
import imghdr

def cli():
    """ se definenen los argumentos que se pasan por terminal"""
    
    # crear el parser
    parser = argparse.ArgumentParser(
        prog = "papersnake",
        description = """
        principalmente pensado para incorporarce a un entorno de i3wm,
        papersnake sirve para establecer wallpapers que rotan cada sierto timpo.
        """
    )
    # incorporar elementos al parser
    parser.add_argument(
        "directory",
        type = str,
        help = "indicar el directorio con los wallpaper"
    )
    parser.add_argument( 
        "time",
        type = int,
        default = 60,
        help = """
        indicar el tiempo de transicion entre wallpapers en segundos,
        para indicar el tiempo en minutos usar -m or --minuts
        luego de establecer un valor
        """
    )
    # incorporar elementos opcionales al parser
    parser.add_argument(
        "-m", "--minuts",
        action = "store_true",
        help = "indica que el tiempo esta en minutos"
    )
    parser.add_argument(
        "-r", "--random",
        action = "store_true",
        help = "indica que los wallpaper van a rotar de forma aleatoria, de lo contrario lo aran de forma ordenada"
    )
    # retornar los argumentos del parser
    return parser.parse_args()

def wallpepers(dir: Path):
    """crea una lista con los wallpapers dentro de un directorio"""
    
    #list de formatos soportados
    formats = [
        "png",
        "jpeg",
        "bmp"
    ]
    
    # filtrador de archivos
    if not dir.exists():
        print("Error: el directorio no existe")
    elif not dir.is_dir():
        print("Error: no es un directorio")
    else:
        wallpaper_list = []
        for i in dir.iterdir():
            if not i.is_file():
                pass
            else:
                if imghdr.what(i) in formats:
                    wallpaper_list.append(str(i))
        return wallpaper_list
    
    

def main():
    """funcion principal"""
    
    # asignar los argumentos del parser a una variable
    args = cli()
    time_sleep = args.time*60 if args.minuts else args.time
    
    if time_sleep < 0:
        time_sleep *= -1
    
    papers = wallpepers(Path(args.directory))
    count_papers = len(papers) if papers != None else 0
    
    #setea los wallpapers de forma random
    if args.random and count_papers != 0:
        active_random_paper = None
        while True:
            random_paper = random.choice(papers)
            if random_paper != active_random_paper:
                set_wallpaper = ["feh", "--bg-fill", random_paper]

                subprocess.Popen(set_wallpaper).wait()
                
                active_random_paper = random_paper
                
                time.sleep(time_sleep)
    
    #setea los wallpapers de forma ordenada
    if count_papers != 0:
        index = 0
        while True:
            if index >= count_papers:
                index = 0
            
            set_wallpaper = ["feh", "--bg-fill", papers[index]]

            subprocess.Popen(set_wallpaper).wait()
            
            index += 1
            
            time.sleep(time_sleep)

if __name__=="__main__":
    main()
