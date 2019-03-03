# -*- encoding: utf-8 -*-

"""
@Author  :   Yuxiang Lu
 
@License :   (C) Copyright 2013-2018, WTIST
 
@Contact :   luyuxiang@bupt.edu.cn
 
@File    :   Poker.py
 
@Time    :   2019-03-02 18:38
 
"""

import random


class Card(object):
    def __init__(self, index):
        self.index = index
        self.point = index % 13 if index % 13 != 0 else 13
        self.color, self.num = self.get_card_info()

    def get_card_info(self):
        if 1 <= self.index <= 13:
            card_color = '♠️'
        elif 14 <= self.index <= 26:
            card_color = '♥️'
        elif 27 <= self.index <= 39:
            card_color = '♣️'
        else:
            card_color = '♦️'
        if self.index in [1, 14, 27, 40]:
            card_num = 'Ace'
        elif self.index in [11, 24, 37, 50]:
            card_num = 'Jack'
        elif self.index in [12, 25, 38, 51]:
            card_num = 'Queen'
        elif self.index in [13, 26, 39, 52]:
            card_num = 'King'
        else:
            card_num = str(self.index % 13)

        return card_color, card_num

    def info(self):
        return '%s%s' % (self.color, self.num)

    def print_func(self):
        print('{} of {}'.format(self.num, self.color))


class Poker(object):
    def __init__(self):
        self.deck = []
        self.reset()

    def reset(self):
        # print("There are {} cards left before shuffle.".format(len(self.deck)))
        self.deck = [Card(i) for i in range(1, 53)]
        self.shuffle()
        # print("There are {} cards after shuffle.".format(len(self.deck)))

    def shuffle(self):
        random.shuffle(self.deck)

    def get_cards_without_drawback(self, num_of_cards=1):
        cards = []
        for i in range(num_of_cards):
            cards.append(self.deck.pop())
        return cards


if __name__ == '__main__':
    poker = Poker()
    cards = poker.get_cards_without_drawback(5)
    for card in cards:
        card.print_func()
    poker.reset()
