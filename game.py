#!/usr/bin/env python

# Copyright 2016 Zara Zaimeche

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from colours import *
try:
    from conf import *
except:
    from sampleconf import *
from goblin import *
import os
from player import player
import pygame
from pygame.locals import *
import random
import sys 

main_clock = pygame.time.Clock()

pygame.init()

window_surface = pygame.display.set_mode((WIDTH, HEIGHT))
window_rect = pygame.Rect(0, 0, WIDTH, HEIGHT)

CELLSIZE = 10

COLUMNS = WIDTH / CELLSIZE
ROWS = HEIGHT / CELLSIZE

ROWS = int(ROWS)
COLUMNS = int(COLUMNS)

grid = []

for row in range(1, ROWS):
    for column in range(1, COLUMNS):
        coordinate = (column, row)
        grid.append(coordinate)

# each coordinate will correspond to one cell in the grid; we will multiply by
# 10

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

pygame.mouse.set_visible(False)

basic_font = pygame.font.SysFont(None, 48)
small_font = pygame.font.SysFont(None, 20)

explanation = "Cross the screen as many times as you can!"
exp_surf = small_font.render(explanation, 1, WHITE)
exp_rect = exp_surf.get_rect()
exp_rect.topleft = (COLUMNS/3 * CELLSIZE, 0)


# moves character as long as they will not end up offscreen
def move_character(chara, direction):
    if direction == UP:
        if chara.location[1] - chara.movespeed > -chara.movespeed:
            chara.location[1] = chara.location[1] - chara.movespeed

    elif direction == DOWN:
        if chara.location[1] + chara.movespeed < ROWS:
            chara.location[1] = chara.location[1] + chara.movespeed

    elif direction == LEFT:
        if chara.location[0] - chara.movespeed > -chara.movespeed:
            chara.location[0] = chara.location[0] - chara.movespeed

    elif direction == RIGHT:
        if chara.location[0] + chara.movespeed < ROWS:
            chara.location[0] = chara.location[0] + chara.movespeed

    return chara.location


def end_game():

    pygame.quit()
    sys.exit()


def main():
    player.location = [COLUMNS/2, ROWS-1]  # player starts at bottom
    player_loc = player.location

    score = 0
    top_toggle = True

    for goblin in goblins:
        goblin.hit_right_wall = False

    direction = ''

    while True:

        player_x = player.location[0]
        player_y = player.location[1]
        player_rect = pygame.Rect(player_x, player_y, player.size, player.size)

        for event in pygame.event.get():
            if event.type == QUIT:
                end_game()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    end_game()
                elif event.key == K_LEFT:
                    direction = LEFT
                elif event.key == K_RIGHT:
                    direction = RIGHT
                elif event.key == K_UP:
                    direction = UP
                elif event.key == K_DOWN:
                    direction = DOWN
            # stop if user releases key. we don't use keyup as they might
            # release a key while holding another down.
            elif 1 not in pygame.key.get_pressed():
                direction = ""
        player_loc = move_character(player, direction)

        for goblin in goblins:
            goblin_x = goblin.location[0]
            goblin_y = goblin.location[1]
            goblin_rect = pygame.Rect(goblin_x, goblin_y, goblin.size, goblin.size)
            if goblin.hit_right_wall is False:
                goblin_dir = RIGHT
                if goblin_x + goblin.movespeed >= COLUMNS:
                    goblin.hit_right_wall = True
                    goblin_dir = LEFT
            elif goblin.hit_right_wall is True:
                goblin_dir = LEFT
                if goblin_x - goblin.movespeed <= 0:
                    goblin.hit_right_wall = False

            goblin.location = move_character(goblin, goblin_dir)

            if goblin_rect.colliderect(player_rect):
                print ('You lose!')
                end_game()

        # give player a point each time they cross screen.
        # increase game speed with each multiple of 10 points.
        # That's just a suggested difficulty mechanic; fine to change or omit.
        if player.location[1] == 0 and top_toggle is True:
            score = score + 1
            if score % 10 == 0:
                for goblin in goblins:
                    goblin.movespeed += 1
            top_toggle = False
        elif player.location[1] == ROWS - 1 and top_toggle is False:
            score = score + 1
            if score % 10 == 0:
                for goblin in goblins:
                    goblin.movespeed += 1
            top_toggle = True

        # draw here so screen isn't far behind logic
        window_surface.fill(BLACK)

        score_surf = basic_font.render('Score: %d' % score, 1, BRIGHTRED)
        score_rect = score_surf.get_rect()
        score_rect.topleft = (1, 1)
        window_surface.blit(score_surf, score_rect)
        window_surface.blit(exp_surf, exp_rect)

        player_x_pos = player_x * CELLSIZE
        player_y_pos = player_y * CELLSIZE
        player_scaled = player.size * CELLSIZE
        player_dimensions = player_x_pos, player_y_pos, player_scaled, player_scaled
        pygame.draw.rect(window_surface, BRIGHTGREEN, (player_dimensions))

        for goblin in goblins:
            goblin_x = goblin.location[0]
            goblin_y = goblin.location[1]
            goblin_x_pos = goblin_x * CELLSIZE
            goblin_y_pos = goblin_y * CELLSIZE
            goblin_scaled = goblin.size * CELLSIZE
            goblin_dimensions = goblin_x_pos, goblin_y_pos, goblin_scaled, goblin_scaled
            pygame.draw.rect(window_surface, YELLOW, (goblin_dimensions))

        pygame.display.update()
        main_clock.tick(FPS)


main()
