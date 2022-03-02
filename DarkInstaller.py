import curses
import requests
import json
from os import getenv
import os
from curses.textpad import rectangle
from modules.menu import menu
from time import sleep

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
    pass

def main(stdscr):
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(6, 7,-1) # WHITE FG
    curses.init_pair(5, 9,-1) # RED FG
    curses.init_pair(4, 7, 1) # WHITE FG W/ RED BG
    curses.init_pair(3, 7, 6) # WHITE FG W/ CYAN BG
    curses.init_pair(2,-1, 6) # CYAN BG
    curses.init_pair(1,-1, 1) # RED BG
    curses.curs_set(0)
    y, x = stdscr.getmaxyx()
    cy = y//2
    cx = x//2
    stdscr.attron(curses.color_pair(2))
    for i in range((cy+3)-(cy-3)+2):
        for e in range((cx+22)-(cx-22)):
            stdscr.addch((cy-3)+i, (cx-22)+e, 32)
    stdscr.addstr(cy-1, cx-20, "Pinche Dark, alto instalador te hice XD", curses.color_pair(3))
    stdscr.addstr(cy+3, cx-3, "[ OK ]", curses.color_pair(4))
    stdscr.attroff(curses.color_pair(2))
    while True:
        k = stdscr.getch()
        if k == 10: break
    stdscr.move(0,0);stdscr.clrtobot()
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
            "Instalar Alacritty y hacer transparente": exit,
            "Salir": exit
        }
    stdscr.addstr(cy-6,cx-10, "Magia de Darth Venom", curses.color_pair(5))
    while True:
        menu(stdscr, cy-3, cx-25, d)

curses.wrapper(main)
