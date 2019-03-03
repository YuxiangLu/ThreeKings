# -*- encoding: utf-8 -*-

"""
@Author  :   Yuxiang Lu
 
@License :   (C) Copyright 2013-2018, WTIST
 
@Contact :   luyuxiang@bupt.edu.cn
 
@File    :   Player.py
 
@Time    :   2019-03-02 18:39
 
"""
from Poker import Card, Poker


class Player(object):
    def __init__(self, name, is_banker=False, profit=0, base=1):
        self.name = name
        self.is_banker = is_banker
        self.profit = profit
        self.base = base
        self.cards = []
        self.profit_change_log = []

    def get_name(self):
        return self.name

    def get_is_banker(self):
        return self.is_banker

    def get_profit(self):
        return self.profit

    def set_banker(self, banker):
        self.is_banker = banker

    def change_profit(self, revenue):
        self.profit += revenue
        self.profit_change_log[-1] += revenue

    def receive_card(self, cards):
        for card in cards:
            assert isinstance(card, Card)
        self.cards.extend(cards)

    def get_cards(self):
        return self.cards

    def show_info(self, log_file):
        log_file.write('Player: {}, Role: {}, Cards: {}, Profit: {}, '
                       'Total Profit: {}'.format(self.name,
                                                 'Banker' if self.is_banker else "Leisure",
                                                 [card.info() for card in self.cards],
                                                 self.profit_change_log[-1],
                                                 self.profit))
        print('Player: {}, Role: {}, Cards: {}, Profit: {}, '
              'Total Profit: {}'.format(self.name,
                                        'Banker' if self.is_banker else "Leisure",
                                        [card.info() for card in self.cards],
                                        self.profit_change_log[-1],
                                        self.profit))


if __name__ == '__main__':
    poker = Poker()
    p1 = Player(name='p1', is_banker=False, profit=0)
    p1.receive_card(poker.get_cards_without_drawback(3))
    p1.show_info()
