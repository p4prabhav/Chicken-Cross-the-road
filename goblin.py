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

# This is messy; the logic should be split out from the entities sometime.

from character import Character
from colours import *

goblin_names = []
goblins = []
difficulty = 3


def make_goblin(goblin):
    goblin = Character()
    goblin.colour = YELLOW
    goblin.size = 3
    return goblin

for i in range(9):
    i = str(i)
    goblin_name = 'goblin' + i
    goblin_names.append(goblin_name)

for goblin in goblin_names:
    new_goblin = make_goblin(goblin)
    goblins.append(new_goblin)

counter = 1

for goblin in goblins:
    setattr(goblin, 'location', [counter*5, counter*5])
    setattr(goblin, 'movespeed', counter % difficulty+1)  # 3 speeds
    counter += 1
