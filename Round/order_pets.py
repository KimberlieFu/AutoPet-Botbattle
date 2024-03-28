    # Swap the positions of the two pets within your lineup
    # Note: its totally ok for the indices to point to None
    # def swap_pets(self, pet_a_index: int, pet_b_index: int):

    # start by checking for specific circumstances
    '''
    - flamingo/s should always go the front
    - horse/dog should always go to the back
    - sheep, spider, cricket, ant, should go before horse
    - peacock should go before the kangaroo

    '''

    # if there is a horse/dog, swap it with any pets that do not match its type, to be closer to the back
    # if there is a flamingo, swap it with any pets that do not match its type, to be closer to the back
    # if there is both a peacock and a kangaroo, put the peacock immediately before the kangaroo

   def order_pets(game_info, pets):
        move_made = False
        for index, team_pet in enumerate(pets):
            if team_pet is not None:
                # check if the pet is a flamingo (front-ideal)
                if team_pet.type == PetType.FLAMINGO:
                    # if it is not at the front, swap with the frontmost nonidentical pet
                    if index != 0:
                        for new_index, team_pet in enumerate(pets):
                            if team_pet is not None:
                                # check the pet is not a flamingo (front-ideal)
                                if team_pet.type != PetType.FLAMINGO:
                                    if move_made is True:
                                        print("updating game info to prep for swap", flush = True)
                                        game_info = bot_battle.get_game_info()
                                    bot_battle.swap_pets(index, new_index)
                                    print("swap made", flush = True)
                                    move_made = True
                                    break
                            else:
                                if move_made is True:
                                    print("updating game info to prep for swap", flush = True)
                                    game_info = bot_battle.get_game_info()
                                bot_battle.swap_pets(index, new_index)
                                print("swap made", flush = True)
                                move_made = True
                                break
                # check if the pet is a horse (back-ideal)
                elif team_pet.type == PetType.HORSE:
                    # if it is not at the back, swap with the frontmost non-identical pet
                    back = 4
                    if index != back:
                        while (back >= 0):
                            if pets[back] is not None:
                                # check the pet is not a horse (back-ideal)
                                if team_pet.type != PetType.HORSE:
                                    if move_made is True:
                                        print("updating game info to prep for swap", flush = True)
                                        game_info = bot_battle.get_game_info()
                                    bot_battle.swap_pets(index, new_index)
                                    print("swap made", flush = True)
                                    move_made = True
                                    break
                            else:
                                if move_made is True:
                                    print("updating game info to prep for swap", flush = True)
                                    game_info = bot_battle.get_game_info()
                                bot_battle.swap_pets(index, back)
                                print("swap made", flush = True)
                                move_made = True
                                break
                # check if the pet is a dog (back-ideal)
                elif team_pet.type == PetType.DOG:
                    # if it is not at the back, swap with the frontmost non-identical pet
                    back = 4
                    if index != back:
                        while (back >= 0):
                            if pets[back] is not None:
                                # check the pet is not a dog (back-ideal)
                                if team_pet.type != PetType.DOG:
                                    if move_made is True:
                                        print("updating game info to prep for swap", flush = True)
                                        game_info = bot_battle.get_game_info()
                                    bot_battle.swap_pets(index, new_index)
                                    print("swap made", flush = True)
                                    move_made = True
                                    break
                            else:
                                if move_made is True:
                                    print("updating game info to prep for swap", flush = True)
                                    game_info = bot_battle.get_game_info()
                                bot_battle.swap_pets(index, back)
                                print("swap made", flush = True)
                                move_made = True
                                break

        # check if the team has both a peacock and a kangaroo
        peacock_index = None
        kangaroo_index = None

        for index, pet in enumerate(pets):
            if pet is not None:
                if pet.type == PetType.PEACOCK:
                    peacock_index = index
                elif pet.type == PetType.KANGAROO:
                    kangaroo_index = index

        if peacock_index is not None and kangaroo_index is not None:
            # there are both, should put peacock immediately in front
            # update_reqd = False
            if peacock_index > kangaroo_index:
                if move_made is True:
                    game_info = bot_battle.get_game_info()
                bot_battle.swap_pets(peacock_index, kangaroo_index)
                move_made = True

            if (peacock_index + 1) != kangaroo_index:
                # if update_reqd is True:
                if move_made is True:
                    game_info = bot_battle.get_game_info()
                bot_battle.swap_pets(peacock_index + 1, kangaroo_index)

        if move_made is False:
            return game_info
        else:
            return 0

