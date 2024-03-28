
    def order_pets(game_info, pets):
        move_made = False
        for index, team_pet in enumerate(pets):
            if team_pet is not None:

                # if horse is available
                if team_pet.type == PetType.HORSE:
                    ideal_pos = 4
                    curr = index
                    # check if correct position
                    actual_pos = ideal_pos - index
                    if index == actual_pos:
                        continue
                    bot_battle.swap_pets(curr, ideal_pos)
                    game_info = bot_battle.get_game_info()
                    move_made = True

                # if flamingo is available
                elif team_pet.type == PetType.FLAMINGO:
                    ideal_pos = 0
                    curr = index
                    
                    # check if correct position
                    actual_pos = ideal_pos - index
                    if index == actual_pos:
                        continue
                    
                    bot_battle.swap_pets(curr, ideal_pos)
                    game_info = bot_battle.get_game_info()
                    move_made = True
                

                elif team_pet.type == PetType.KANGAROO:
                    ideal_pos = 2
                    curr = index
                    
                    # check if correct position
                    actual_pos = ideal_pos - index
                    if index == actual_pos:
                        continue

                    bot_battle.swap_pets(curr, ideal_pos)
                    game_info = bot_battle.get_game_info()
                    move_made = True
                
                elif team_pet.type == PetType.PEACOCK:
                    ideal_pos = 1
                    curr = index
                    
                    # check if correct position
                    actual_pos = ideal_pos - index
                    if index == actual_pos:
                        continue

                    bot_battle.swap_pets(curr, ideal_pos)
                    game_info = bot_battle.get_game_info()
                    move_made = True
                
                elif team_pet.type == PetType.DOG:
                    ideal_pos = 4
                    curr = index
                    
                    # check if correct position
                    actual_pos = ideal_pos - index
                    if index == actual_pos:
                        continue

                    bot_battle.swap_pets(curr, ideal_pos)
                    game_info = bot_battle.get_game_info()
                    move_made = True

                elif team_pet.type == PetType.SHEEP:
                    ideal_pos = 3
                    curr = index
                    
                    # check if correct position
                    actual_pos = ideal_pos - index
                    if index == actual_pos:
                        continue

                    bot_battle.swap_pets(curr, ideal_pos)
                    game_info = bot_battle.get_game_info()
                    move_made = True


        if move_made is False:
            return 1
        return 0

    def order_pets(game_info, pets):
        move_made = False
        for index, team_pet in enumerate(pets):
            if team_pet is not None:

                # if horse is available
                if team_pet.type == PetType.HORSE:
                    ideal_pos = 4
                    curr = index
                    # check if correct position
                    actual_pos = ideal_pos - index
                    if index == actual_pos:
                        continue
                    bot_battle.swap_pets(curr, ideal_pos)
                    game_info = bot_battle.get_game_info()
                    move_made = True

                # if flamingo is available
                elif team_pet.type == PetType.FLAMINGO:
                    ideal_pos = 0
                    curr = index
                    
                    # check if correct position
                    actual_pos = ideal_pos - index
                    if index == actual_pos:
                        continue
                    
                    bot_battle.swap_pets(curr, ideal_pos)
                    game_info = bot_battle.get_game_info()
                    move_made = True
                

                elif team_pet.type == PetType.KANGAROO:
                    ideal_pos = 2
                    curr = index
                    
                    # check if correct position
                    actual_pos = ideal_pos - index
                    if index == actual_pos:
                        continue

                    bot_battle.swap_pets(curr, ideal_pos)
                    game_info = bot_battle.get_game_info()
                    move_made = True
                
                elif team_pet.type == PetType.PEACOCK:
                    ideal_pos = 1
                    curr = index
                    
                    # check if correct position
                    actual_pos = ideal_pos - index
                    if index == actual_pos:
                        continue

                    bot_battle.swap_pets(curr, ideal_pos)
                    game_info = bot_battle.get_game_info()
                    move_made = True
                
                elif team_pet.type == PetType.DOG:
                    ideal_pos = 4
                    curr = index
                    
                    # check if correct position
                    actual_pos = ideal_pos - index
                    if index == actual_pos:
                        continue

                    bot_battle.swap_pets(curr, ideal_pos)
                    game_info = bot_battle.get_game_info()
                    move_made = True

                elif team_pet.type == PetType.SHEEP:
                    ideal_pos = 3
                    curr = index
                    
                    # check if correct position
                    actual_pos = ideal_pos - index
                    if index == actual_pos:
                        continue

                    bot_battle.swap_pets(curr, ideal_pos)
                    game_info = bot_battle.get_game_info()
                    move_made = True


        if move_made is False:
            return 1
        return 0

    def r2_make_move(game_info: 'GameInfo'):
        global team_size
        global horse_acquired
        global horse_upgraded
        global rolls_performed

        print(f"horse acq: {horse_acquired}", flush = True)
        print(f"horse upgraded: {horse_upgraded}", flush = True)
        print(f"coins: {game_info.player_info.coins}", flush = True)

        # in future, reroll
        if game_info.player_info.coins < 3:
            order_pets(game_info, game_info.player_info.pets)
            print("round 2 turn ended : )", flush = True)
            bot_battle.end_turn()
            rolls_performed = 0
            return

        # do we not already have a horse?
        if horse_acquired is False:
            # we should be trying to buy a horse if there is space on our team
            if team_size != 5:
                # look through pets in the shop
                for shop_pet in game_info.player_info.shop_pets:
                    # if there is a horse, buy it : )
                    if shop_pet.type == PetType.HORSE:
                        # if purchase is successful, move over : )
                        if (attempt_buy_pet(game_info, shop_pet, False) == 0):
                            team_size += 1
                            horse_acquired = True
                            return

        # do we have a horse in need of an upgrade?
        elif horse_upgraded is False:
            # we should either level it up or feed it an apple
            for shop_pet in game_info.player_info.shop_pets:
                # if there is a horse, buy it : )
                if shop_pet is None:
                    continue
                elif shop_pet.type == PetType.HORSE:
                    # if purchase is successful, move over : )
                    if (attempt_buy_pet(game_info, shop_pet, True) == 0):
                        horse_upgraded = True
                        return

            # find the horse in our team
            horse_index = None
            for i, team_pet in enumerate(game_info.player_info.pets):
                # save the index of the horse
                if team_pet is None:
                    continue
                if team_pet.type == PetType.HORSE:
                    horse_index = i
                    # print(f"Horse index: {horse_index}", flush = True)
                    break

            # no horse in shop? perhaps there is an apple?
            for food_index, shop_food in enumerate(game_info.player_info.shop_foods):
                # if there is an apple, feed it to the horse : )
                # print(f"Shop food: {food_index}, {shop_food}", flush = True)
                if shop_food.type == FoodType.APPLE:
                    # print("Apple found!", flush = True)
                    # if purchase is successful, move over : )
                    if (attempt_buy_food(game_info, food_index, horse_index) == 0):
                        horse_upgraded = True
                        return
                    print("Failed to buy apple", flush = True)

        # so either, we failed to upgrade/acquire
        # or we have successfully upgraded/acquired
        # lets fill our team
        if team_size != 5:
            # find the best non-horse pet in the shop
            rank_range = len(tier1_ranks)
            shop_pet_ranking = create_range_list(rank_range, tier1_ranks, game_info, game_info.player_info.shop_pets)
    
            top_pet_index = 0
            # check if the top pet is a horse and there is one already
            for pet_ranking in shop_pet_ranking:
                if tier1_dict[game_info.player_info.shop_pets[pet_ranking].type] == 0:
                    if horse_acquired is True:
                        top_pet_index += 1
                        # print(f"top_pet_index: {top_pet_index}", flush = True)
                    else:
                        break
                else:
                    break

            if (top_pet_index >= len(game_info.player_info.shop_pets)):
                if rolls_performed == 0:
                    # roll again in the hopes of finding some non-horse pets for diversity
                    bot_battle.reroll_shop()
                    rolls_performed += 1
                    return

            # buy the best pet to fill our team, end turn : )
            if (team_size != 5):
                if (attempt_buy_pet(game_info, game_info.player_info.shop_pets[shop_pet_ranking[top_pet_index]], False) == 0):
                    print("attempt best", flush = True)
                    team_size += 1
                    return
        elif game_info.player_info.coins > 3:
            bot_battle.reroll_shop()
            rolls_performed += 1
            return
        elif game_info.player_info.coins == 3:
            rank_range = len(tier2_ranks)
            team_pet_ranking = create_range_list(rank_range, tier2_ranks, game_info, game_info.player_info.pets)
            i = 0
            if game_info.player_info.pets[team_pet_ranking[i]].type == PetType.HORSE and game_info.player_info.shop_foods[0].type == FoodType.HONEY:
                while (game_info.player_info.pets[team_pet_ranking[i]].type == PetType.HORSE):
                    i += 1 #shift to next best pet
            if (attempt_buy_food(game_info, 0, team_pet_ranking[i]) == 0):
                print("trying to buy food {game_info.player_info.shop_food[0].type} for {game_info.player_info.pets[team_pet_ranking[0]]}", flush = True)
            return

        order_pets(game_info, game_info.player_info.pets)
        print("round 2 turn ended : )", flush = True)
        bot_battle.end_turn()
        rolls_performed = 0
        return
