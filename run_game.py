# -*- encoding: utf-8 -*-

"""
@Author  :   Yuxiang Lu
 
@License :   (C) Copyright 2013-2018, WTIST
 
@Contact :   luyuxiang@bupt.edu.cn
 
@File    :   run_game.py
 
@Time    :   2019-03-02 18:39
 
"""
from Player import Player
from ThreeKings import ThreeKings
from utils import draw
import time

if __name__ == '__main__':
    p1 = Player(name='Lu', is_banker=False, profit=0, base=1)
    p2 = Player(name='Li', is_banker=False, profit=0, base=1)
    p3 = Player(name='Liu', is_banker=False, profit=0, base=1)
    p4 = Player(name='Ding', is_banker=False, profit=0, base=1)
    players = [p1, p2, p3, p4]
    turns = 10000
    game = ThreeKings(players=players)
    time = time.strftime("%Y%m%d%H%M", time.localtime())
    log_file = open('log/' + time + '.log', 'a+')
    for i in range(turns):
        print("#" * 40 + " Turn " + str(i + 1) + " " + "#" * 40)
        game.play(log_file)
    draw(players)
    log_file.close()
