# -*- encoding: utf-8 -*-

"""
@Author  :   Yuxiang Lu
 
@License :   (C) Copyright 2013-2018, WTIST
 
@Contact :   luyuxiang@bupt.edu.cn
 
@File    :   ThreeKings.py
 
@Time    :   2019-03-02 22:34
 
"""

from Poker import Poker
from Player import Player
import random


class ThreeKings(object):
    def __init__(self, players, if_change_banker=True):
        if len(players) < 2 or players is None:
            "It takes at least 2 players to play this GAME!"
        self.poker = Poker()
        self.if_change_banker = if_change_banker
        self.players = players
        self.banker_index = random.randint(0, len(self.players) - 1)
        self.set_banker()

    def deal(self):
        """
        发牌
        :return:
        """
        self.poker.reset()
        for player in self.players:
            player.cards = []
        # 每人发三张牌
        for _ in range(3):
            for player in self.players:
                card = self.poker.get_cards_without_drawback(1)
                player.receive_card(card)

    def show(self, log_file=None):
        """
        打印本轮结果
        :return:
        """
        for player in self.players:
            player.show_info(log_file)

    def set_banker(self):
        """
        设置庄家
        :return:
        """
        for player in self.players:
            player.set_banker(False)
        self.players[self.banker_index].set_banker(True)

    def compare(self, banker, leisure):
        """
        点数       倍数
        8点        2倍
        9点        3倍
        三公       4倍
        豹子八点    7倍
        豹子九点    8倍
        豹子三公    9倍
        其余豹子    6倍
        其余       1倍
        :return:
        """
        banker_win = None
        banker_deck = banker.get_cards()
        leisure_deck = leisure.get_cards()
        banker_multiple, banker_point = self.get_deck_info(banker_deck)
        leisure_multiple, leisure_point = self.get_deck_info(leisure_deck)
        if banker_multiple > leisure_multiple:  # 先比较倍数
            banker_win = True
        elif banker_multiple < leisure_multiple:
            banker_win = False
        else:  # 倍数一样的情况
            if banker_point > leisure_point:  # 先比点数
                banker_win = True
            elif banker_point < leisure_point:
                banker_win = False
            else:  # 点数一样的情况, 从最大的开始比
                banker_cards_point = [card.index % 13 if card.index % 13 != 0 else 13 for card in banker_deck]
                leisure_cards_point = [card.index % 13 if card.index % 13 != 0 else 13 for card in leisure_deck]
                banker_cards_point.sort()
                leisure_cards_point.sort()
                i = len(banker_deck) - 1
                while i >= 0:
                    if banker_cards_point[i] == leisure_cards_point[i]:
                        if i == 0:
                            banker_win = True
                            break
                        i -= 1
                        continue
                    elif banker_cards_point[i] > leisure_cards_point[i]:
                        banker_win = True
                        break
                    else:
                        banker_win = False
                        break
        if banker_win:
            profit = leisure.base * banker_multiple
            self.account(banker, profit)
            self.account(leisure, -1 * profit)
        else:
            profit = leisure.base * leisure_multiple
            self.account(banker, -1 * profit)
            self.account(leisure, profit)
        #
        # return (banker_multiple, banker_point), (leisure_multiple, leisure_point)

    def get_deck_info(self, deck):
        """
        计算一副牌的倍数
        :param deck:
        :return:
        """
        point = self.get_deck_point(deck)
        is_leopard = self.is_leopard(deck)
        is_three_king = self.is_three_king(deck)
        if point == 8:
            if is_leopard:
                multiple = 7
            else:
                multiple = 2
        elif point == 9:
            if is_leopard:
                multiple = 8
            else:
                multiple = 3
        elif is_three_king:
            if is_leopard:
                multiple = 9
            else:
                multiple = 4
        elif is_leopard:
            multiple = 6
        else:
            multiple = 1

        return multiple, point

    @staticmethod
    def get_card_point(card):
        """
        计算每张牌的点数
        :param card:
        :return:
        """
        if card.index in [10, 11, 12, 13, 23, 24, 25, 26, 36, 37, 38, 39, 49, 50, 51, 52]:
            point = 0
        else:
            point = card.index % 13 % 10
        return point

    def get_deck_point(self, deck):
        """
        计算三张牌的点数
        :param deck:
        :return:
        """
        return sum([self.get_card_point(card) for card in deck]) % 10

    @staticmethod
    def is_three_king(deck):
        """
        三公
        :param deck:
        :return:
        """
        king_indexes = [11, 12, 13, 24, 25, 26, 37, 38, 39, 50, 51, 52]
        return deck[0].index in king_indexes and deck[1].index in king_indexes and deck[2].index in king_indexes

    @staticmethod
    def is_leopard(deck):
        """
        豹子
        :param deck:
        :return:
        """
        return deck[0].index % 13 == deck[1].index % 13 and deck[1].index % 13 == deck[2].index % 13

    @staticmethod
    def account(player, profit):
        """
        发放收益
        :param player:
        :param profit:
        :return:
        """
        player.change_profit(profit)

    def change_banker(self):
        """
        换庄家
        :return:
        """
        candidates = []
        for i, player in enumerate(self.players):
            _, point = self.get_deck_info(player.cards)
            if point == 9:
                candidates.append(i)
        if len(candidates) == 0:
            return
        else:
            tmp_banker_index = candidates[0]
            if len(candidates) == 1:
                if tmp_banker_index == self.banker_index:
                    return
            else:
                for candidate_index in range(1, len(candidates)):
                    tmp_banker_deck = self.players[tmp_banker_index].get_cards()
                    candidate_banker_deck = self.players[candidate_index].get_cards()

                    tmp_banker_cards_point = [card.index % 13 if card.index % 13 != 0 else 13 for card in
                                              tmp_banker_deck]
                    candidate_cards_point = [card.index % 13 if card.index % 13 != 0 else 13 for card in
                                             candidate_banker_deck]
                    tmp_banker_cards_point.sort()
                    candidate_cards_point.sort()
                    i = len(tmp_banker_deck) - 1
                    while i >= 0:
                        if tmp_banker_cards_point[i] == candidate_cards_point[i]:
                            if i == 0:
                                break
                            i -= 1
                            continue
                        elif tmp_banker_cards_point[i] > candidate_cards_point[i]:
                            break
                        else:
                            tmp_banker_index = candidate_index
                            break

            if tmp_banker_index != self.banker_index:
                print(
                    "{} Banker has been changed from {} to {} {}".format("#" * 5, self.players[self.banker_index].name,
                                                                         self.players[tmp_banker_index].name, "#" * 5))
            self.banker_index = tmp_banker_index
            self.set_banker()

    def get_banker(self):
        """
        返回庄家
        :return:
        """
        return self.players[self.banker_index]

    def play(self, log_file=None):
        """
        玩一轮游戏
        :return:
        """
        self.deal()
        banker = self.get_banker()
        banker.profit_change_log.append(0)
        for player in self.players:
            if not player.is_banker:
                player.profit_change_log.append(0)
                self.compare(banker, player)
        if log_file is not None:
            self.show(log_file=log_file)
        else:
            self.show(log_file=None)
        if self.if_change_banker:
            self.change_banker()


if __name__ == '__main__':
    pass
