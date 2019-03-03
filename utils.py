# -*- encoding: utf-8 -*-

"""
@Author  :   Yuxiang Lu
 
@License :   (C) Copyright 2013-2018, WTIST
 
@Contact :   luyuxiang@bupt.edu.cn
 
@File    :   utils.py
 
@Time    :   2019-03-03 14:46
 
"""
import matplotlib.pyplot as plt


def draw(players):
    plt.title('Result Plot')
    turns = [i + 1 for i in range(len(players[0].profit_change_log))]
    for player in players:
        var = trans_log_to_var(player.profit_change_log)

        plt.plot(turns, var, label=player.name)
    plt.plot(turns, [0]*len(turns), color='black')
    plt.xlabel('turn')
    plt.ylabel('profit')
    plt.legend()
    plt.show()


def trans_log_to_var(changes):
    var = [changes[0]]
    for i in range(1, len(changes)):
        var.append(var[-1] + changes[i])
    return var


if __name__ == '__main__':
    pass
