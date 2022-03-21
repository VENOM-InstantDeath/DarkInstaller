import curses
import requests
import json
from os import getenv
import os
from os import path, mkdir
from sys import argv
from curses.textpad import rectangle
from modules.menu import menu
from time import sleep
VERSION = '3.0.6'

def listostr(l, c=''):
    if not isinstance(l,list): raise ValueError
    s = ""
    for i in l:
        s += i+c
    return s

def pathcrop(s):
    if not '/' in s: return '.'
    if s.count('/') == 1 and s[0] == '/': return s
    return s[:s.rfind('/')]

def vimplug(stdscr, cy, cx, data):
    if data["vim-plug"]: return
    stdscr.addstr(cy+5, cx-25, "Realizando la operación...", curses.color_pair(2))
    stdscr.refresh()

    HOME=getenv('HOME')
    if not os.path.exists(f"{HOME}/.local/share/nvim"):
        os.mkdir(f"{HOME}/.local/share/nvim")
    if not os.path.exists(f"{HOME}/.local/share/nvim/site"):
        os.mkdir(f"{HOME}/.local/share/nvim/site")
    if not os.path.exists(f"{HOME}/.local/share/nvim/site/autoload"):
        os.mkdir(f"{HOME}/.local/share/nvim/site/autoload")
    F = open(f"{HOME}/.local/share/nvim/site/autoload/plug.vim", "w+")
    resp=requests.get("https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim")
    F.write(resp.content.decode())
    F.close()
    curses.napms(2000)
    stdscr.move(cy+5, cx-25)
    stdscr.clrtoeol()
    data["vim-plug"] = True
    F = open(f"{getenv('HOME')}/.local/share/DarkInstaller/data.json", 'w')
    F.write(json.dumps(data, indent=4))
    F.close()


def vimconf(stdscr, cy, cx, data):
    if data["plugin&config"]: return
    stdscr.addstr(cy+5, cx-25, "Realizando la operación...", curses.color_pair(2))
    stdscr.refresh()

    HOME=getenv('HOME')
    if not os.path.exists(f'{HOME}/.config/nvim'):
        os.mkdir(f'{HOME}/.config/nvim')
    F = open(f'{HOME}/.config/nvim/init.vim','w+')
    resp=requests.get("https://raw.githubusercontent.com/VENOM-InstantDeath/configFiles/main/nvim/init.vim")
    F.write(resp.content.decode())
    F.close()
    curses.napms(2000)
    stdscr.move(cy+5, cx-25)
    stdscr.clrtoeol()
    data["plugin&config"] = True
    F = open(f"{getenv('HOME')}/.local/share/DarkInstaller/data.json", 'w')
    F.write(json.dumps(data, indent=4))
    F.close()
    if data["vim-plug"]:
        win=curses.newwin(6,50,cy-3, cx-25)
        win.touchwin()
        win.bkgd(' ', curses.color_pair(2))
        win.addstr(1,1,"Ahora abre vim en otra terminal y usa el comando",curses.color_pair(3))
        win.addstr(2,18,":PlugInstall",curses.color_pair(3))
        win.addstr(4,22,"[OK]", curses.color_pair(4))
        while True:
            k=win.getch()
            if k == 10: break
        del win
        stdscr.touchwin()
        stdscr.refresh()
    else:
        win=curses.newwin(7,50,cy-3, cx-25)
        win.touchwin()
        win.bkgd(' ', curses.color_pair(2))
        win.addstr(1,1,"Usa la primera opción para instalar vim-plug y luego abre vim en otra terminal y usa el comando",curses.color_pair(3))
        win.addstr(3,18,":PlugInstall",curses.color_pair(3))
        win.addstr(5,22,"[OK]", curses.color_pair(4))
        while True:
            k=win.getch()
            if k == 10: break
        del win
        stdscr.touchwin()
        stdscr.refresh()


def alacop(stdscr, cy, cx, data):
    win=curses.newwin(5,50,cy-3, cx-25)
    win.touchwin()
    win.bkgd(' ', curses.color_pair(2))
    win.addstr(1,1,"Esta función no está disponible aún",curses.color_pair(3))
    win.addstr(3,22,"[OK]", curses.color_pair(4))
    while True:
        k=win.getch()
        if k == 10: break
    del win
    stdscr.touchwin()
    stdscr.refresh()


def interpreter(s):
    s = s.split('\n')
    dir = ''
    base_url = 'https://raw.githubusercontent.com/VENOM-InstantDeath/DarkInstaller/main'
    for i in s:
        if not i: continue
        if i.startswith('::'): continue
        if not dir:
            t = i.split('/')
            if i[0] == '/': t[0] = '/'+t[0]
            if '$insdir' in t: t[t.index('$insdir')] = pathcrop(argv[0])
            dir = listostr(t, '/')[:-1]
            if not path.exists(dir):
                p = ''
                for i in t:
                    p += i+'/'
                    if not path.exists(p): mkdir(p)
            continue
        if i == 'end':
            dir = ''
            continue
        t = i.split()
        if t[0] == "download":
            resp = requests.get(f'{base_url}/{t[1]}')
            F = open(f'{dir}/{t[1]}', 'wb+')
            F.write(resp.content)
            F.close()

def update(stdscr, cy, cx, data):
    """
    Caso 1. No hay update

    tmsg: Buscando actualizaciones...
    msgbox:
        No hay actualizaciones disponibles.

                [ OK ]

    Caso 2. Hay update
    
    tmsg: Buscando actualizaciones...
    msgbox:
        Hay una nueva versión disponible.

        version: 2.1.0
        autor: VENOM-InstantDeath

                [ OK ]

    Formato de instrucciones de updates

    $insdir
    download DarkInstaller.py
    download version
    end

    $insdir/modules
    download ncRead.py
    download menu.py
    download vbox.py
    end

    ::If file exists, replace it.::
    ::If line is empty, ignore it.::
    """
    os.chdir(pathcrop(argv[0]))
    stdscr.addstr(cy+5, cx-25, "Buscando actualizaciones...", curses.color_pair(2))
    stdscr.refresh()
    resp = requests.get("https://raw.githubusercontent.com/VENOM-InstantDeath/DarkInstaller/main/version").text.strip()
    if VERSION != resp:
        win=curses.newwin(7,50,cy-3, cx-25)
        win.touchwin()
        win.bkgd(' ', curses.color_pair(2))
        win.addstr(1,1,"Hay una nueva versión disponible",curses.color_pair(3))
        win.addstr(2,1,f"Version: {resp}",curses.color_pair(3))
        win.addstr(3,1,"Autor: VENOM-InstantDeath",curses.color_pair(3))
        win.addstr(5,22,"[OK]", curses.color_pair(4))
        while True:
            k=win.getch()
            if k == 10: break
        del win
        stdscr.touchwin()
        stdscr.refresh()
        stdscr.move(cy+5, cx-25);stdscr.clrtoeol()
        stdscr.addstr(cy+5, cx-25, "Descargando actualizaciones...", curses.color_pair(2))
        stdscr.refresh()
        order = requests.get("https://raw.githubusercontent.com/VENOM-InstantDeath/DarkInstaller/main/upord").text
        curses.napms(1000)
        stdscr.move(cy+5, cx-25);stdscr.clrtoeol()
        stdscr.addstr(cy+5, cx-25, "Instalando...", curses.color_pair(2))
        stdscr.refresh()
        interpreter(order)
        stdscr.move(cy+5, cx-25);stdscr.clrtoeol()
        win=curses.newwin(6,50,cy-3, cx-25)
        win.touchwin()
        win.bkgd(' ', curses.color_pair(2))
        win.addstr(1,1,"Actualización completada",curses.color_pair(3))
        win.addstr(2,1,"Reinicia el programa para ver los cambios",curses.color_pair(3))
        win.addstr(4,22,"[OK]", curses.color_pair(4))
        while True:
            k=win.getch()
            if k == 10: break
        del win
        stdscr.touchwin()
        stdscr.refresh()
    else:
        win=curses.newwin(5,50,cy-3, cx-25)
        win.touchwin()
        win.bkgd(' ', curses.color_pair(2))
        win.addstr(1,1,"No hay actualizaciones disponibles",curses.color_pair(3))
        win.addstr(3,22,"[OK]", curses.color_pair(4))
        while True:
            k=win.getch()
            if k == 10: break
        del win
        stdscr.touchwin()
        stdscr.refresh()

    stdscr.move(cy+5, cx-25)
    stdscr.clrtoeol()


def main(stdscr):
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(6, 7,-1) # WHITE FG
    curses.init_pair(5, 9,-1) # RED FG
    curses.init_pair(4, 7, 1) # WHITE FG W/ RED BG
    curses.init_pair(3, 7, 27) # WHITE FG W/ BLUE BG
    curses.init_pair(2,-1, 27) # BLUE BG
    curses.init_pair(1,-1, 1) # RED BG
    curses.curs_set(0)
    y, x = stdscr.getmaxyx()
    cy = y//2
    cx = x//2
    stdscr.addstr(y-1,0,f"Version {VERSION}")
    stdscr.refresh()
    win=curses.newwin(5,50,cy-3, cx-25)
    win.touchwin()
    win.bkgd(' ', curses.color_pair(2))
    win.addstr(1,1,"Estimado Zack, págele la renta al señor barriga",curses.color_pair(3))
    win.addstr(3,22,"[OK]", curses.color_pair(4))
    while True:
        k=win.getch()
        if k == 10: break
    del win
    stdscr.touchwin()
    stdscr.refresh()

    if not os.path.exists(f"{getenv('HOME')}/.local/share/DarkInstaller"):
        os.mkdir(f"{getenv('HOME')}/.local/share/DarkInstaller")
    if not os.path.exists(f"{getenv('HOME')}/.local/share/DarkInstaller/data.json"):
        F = open(f"{getenv('HOME')}/.local/share/DarkInstaller/data.json", "w+")
        F.write(json.dumps({"vim-plug": False,
            "plugin&config": False,
            "alacritty_opacity": False}, indent=4))
        F.close()
    F = open(f"{getenv('HOME')}/.local/share/DarkInstaller/data.json")
    data = json.load(F)
    d = {
            "Nvim: Instalar vim-plug": lambda: vimplug(stdscr, cy, cx, data),
            "Nvim: Instalar plugins y config de Darth": lambda: vimconf(stdscr,cy,cx,data),
            "Instalar Alacritty y hacer transparente": lambda: alacop(stdscr,cy,cx,data),
            "Actualizar": lambda: update(stdscr,cy,cx,data),
            "Salir": exit
        }
    stdscr.addstr(cy-6,cx-10, "Magia de Darth Venom", curses.color_pair(5))
    while True:
        menu(stdscr, cy-3, cx-25, d)

curses.wrapper(main)
