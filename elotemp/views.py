__author__ = 'zhangjingyuan'
from django.shortcuts import render, redirect
from django.views.generic import ListView, TemplateView
from django.core.urlresolvers import reverse_lazy, reverse
from itertools import combinations
import fileinput

class Player:
    def __init__(self, name, image, rating=100.0):
        self.name = name
        self.image = image
        self.rating = rating

    def update_rating(self, score, opponent):
        K0 = 15
        Q0 = 10 ** (float(self.rating) / 400)
        Q1 = 10 ** (float(opponent.rating) / 400)
        E0 = Q0 / (Q0 + Q1)
        self.rating += (K0 * (score - E0))


class EloView(TemplateView):
    template_name = 'page/elo.html'

    def get_context_data(self, **kwargs):
        player_list = []
        step = int(self.kwargs['step'])
        if step == 0:
            temp_db_file = open('elotemp/elodemo.txt', 'rw')
        else:
            temp_db_file = open('elotemp/update{}.txt'.format(step), 'rw')
        playerdb = temp_db_file.readlines()
        for player in playerdb:
            player = player.strip('\n').split(' ')
            player_list.append(Player(player[0], player[1], player[2]))
        matches = list(combinations(
            player_list, 2))

        player1 = matches[step][0]
        player2 = matches[step][1]
        temp_db_file.close()
        return {'player1': player1, 'player2': player2}


def init_elo(self, **kwargs):
    return redirect(reverse("elo.views", kwargs={'step': '0'}))


def update_rank(self, **kwargs):
    step = int(kwargs['step'])
    player_list = []
    if step == 0:
            temp_db_file = open('elotemp/elodemo.txt', 'rw')
    else:
        temp_db_file = open('elotemp/update{}.txt'.format(step), 'rw')
    playerdb = temp_db_file.readlines()
    for player in playerdb:
        player = player.strip('\n').split(' ')
        player_list.append(Player(player[0], player[1], float(player[2])))
    matches = list(combinations(
        player_list, 2))
    current = matches[step]
    player1 = current[0]
    player2 = current[1]
    result = int(kwargs['result'])
    if result == 0:
        print 'win1'
        player1.update_rating(1, player2)
        player2.update_rating(0, player1)
    elif result == 1:
        print 'win2'
        player2.update_rating(1, player1)
        player1.update_rating(0, player2)
    elif result == 2:
        print 'win3'
        player1.update_rating(.5, player2)
        player2.update_rating(.5, player1)
    step += 1
    if step != len(matches) - 1:
        new_player_db = open('elotemp/update{}.txt'.format(step),'w')
    else:
        new_player_db = open('elotemp/result.txt'.format(step),'w')

    for line in playerdb:
        player = line.strip('\n').split(' ')
        print player
        if player[0] == player1.name:
            print 1
            new_player_db.write(line.replace(player[2],str(player1.rating)))
        elif player[0] == player2.name:
            print 2
            new_player_db.write(line.replace(player[2],str(player2.rating)))
        else:
            new_player_db.write(line)
    temp_db_file.close()
    if step < len(matches) - 1:
        return redirect(reverse_lazy("elo.views", kwargs={'step': step}))
    else:
        return redirect(reverse_lazy("elo.result"))


class EloResult(TemplateView):
    template_name = "page/elo-result.html"
    def get_context_data(self, **kwargs):
        player_list = []
        temp_db_file = open('elotemp/result.txt', 'rw')
        playerdb = temp_db_file.readlines()
        for player in playerdb:
            player = player.strip('\n').split(' ')
            player_list.append(Player(player[0], player[1], float(player[2])))

        player_list = list(sorted(player_list,key=lambda x: x.rating,reverse=True))
        return {'player_list':player_list}