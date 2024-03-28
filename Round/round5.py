
    '''
    ROUND 5
    '''

    # make dictionary to store the correspondence
    #  from higher val. pets to lower ones
    corresponding_dict = dict()

    corresponding_dict[PetType.DOG] = PetType.HORSE
    corresponding_dict[PetType.SHEEP] = PetType.SPIDER
    corresponding_dict[PetType.DODO] = PetType.ANT
    corresponding_dict[PetType.BLOWFISH] = PetType.FLAMINGO
    corresponding_dict[PetType.HIPPO] = PetType.KANGAROO
    
    def r5_make_move(game_info: 'GameInfo', current_tier_pet_ranks, current_tier_pet_dict, current_tier_food_ranks, current_tier_food_dict, round_num):
        global team_size
        global horse_acquired
        global rolls_performed
        global pet_improved

        # if there are no more shop pets, we need to end turn
        # in future, we need to either reroll or buy food or something
        if len(game_info.player_info.shop_pets) == 0:
            bot_battle.end_turn()
            pet_improved = False
            rolls_performed = 0
            return

        # look through each of the shop pets
        replacement_pet = None
        replacement_pet_index = None
        lower_val_version = None
        for i, shop_pet in enumerate(game_info.player_info.shop_pets):
            # if there is a pet that is in the corresponding_dict
            # check whether its lower val. equivalent pet is on our team
            if shop_pet.type in corresponding_dict:
                lower_val_version = corresponding_dict[shop_pet.type]
                replacement_pet_index = i
                break

        for i, team_pet in enumerate(game_info.player_info.pets):
            # if the pet is on our team:
            # check whether it has been leveled up
            if team_pet is not None:
                if team_pet.type == lower_val_version:
                    # if it has NOT been leveled up:
                    if team_pet.level < 2:
                        # sell the pet
                        pet_to_sell = game_info.player_info.pets[i]
                        ugrade = check_upgradable_b4_selling(game_info, game_info.player_info.pets, i)
                        if upgrade is not None:
                            # we should level up within our team instead of selling!!
                            bot_battle.level_pet_from_pets(upgrade[0], upgrade[1])
                            team_size -= 1
                            game_info = bot_battle.get_game_info()
                        else:
                            bot_battle.sell_pet(pet_to_sell)
                            team_size -= 1
                            game_info = bot_battle.get_game_info()
                        # buy the correspoding pet
                        replacement_pet = game_info.player_info.shop_pets[replacement_pet_index]
                        if (attempt_buy_pet(game_info, replacement_pet, False) == 0):
                            team_size += 1
                            return

        # if one of the pets in the shop is a pet that you have on your team, upgrade
        # go through all the pets in the shop
        # if there is a pet that is also on our team, level up
        for shop_pet in game_info.player_info.shop_pets:
            for team_pet in game_info.player_info.pets:
                if team_pet is not None:
                    if team_pet.type == shop_pet.type:
                        if team_pet.level < 3:
                            # bot_battle.level_pet_from_shop(shop_pet, team_pet)
                            if (attempt_buy_pet(game_info, shop_pet, True) == 0):
                                return

        if pet_improved is False:
            # now that we have upgraded our existing pets where possible, we want to improve our lower tier pets
            # pick the highest rank pet from the shop
            rank_range = len(current_tier_pet_ranks)
            shop_pet_ranking = create_range_list(rank_range, current_tier_pet_ranks, game_info, game_info.player_info.shop_pets)
            if len(shop_pet_ranking) != 0:
                best_shop_pet_index = shop_pet_ranking[0]

                # swap it in with the lowest tier pet from the shop that is not leveled up
                # get a ranking of the team pets
                rank_range = len(current_tier_pet_ranks)
                team_pet_ranking = create_range_list(rank_range, current_tier_pet_ranks, game_info, game_info.player_info.pets)
                # iterate through the pets starting at the worst
                i = 1
                while i <= len(team_pet_ranking):
                    # when you find a pet that is not leveled up, sell it and buy the better pet
                    worst_pet_index = team_pet_ranking[- 1 * i]
                    worst_pet = game_info.player_info.pets[worst_pet_index]
                    if worst_pet is not None:
                        if worst_pet.level < 2:
                            # sell the pet
                            pet_to_sell = game_info.player_info.pets[worst_pet_index]

                            # if the pet you are planning to sell is actually worse than its replacement:
                            replacement_pet = game_info.player_info.shop_pets[best_shop_pet_index]
                            if current_tier_pet_dict[pet_to_sell.type] > current_tier_pet_dict[replacement_pet.type]:
                                # you should go through with the upgrade!!
                                ugrade = check_upgradable_b4_selling(game_info, game_info.player_info.pets, i)
                                if upgrade is not None:
                                    # we should level up within our team instead of selling!!
                                    bot_battle.level_pet_from_pets(upgrade[0], upgrade[1])
                                    team_size -= 1
                                    game_info = bot_battle.get_game_info()
                                else:
                                    bot_battle.sell_pet(pet_to_sell)
                                    team_size -= 1
                                    game_info = bot_battle.get_game_info()
                                # buy the correspoding pet
                                replacement_pet = game_info.player_info.shop_pets[best_shop_pet_index]
                                if (attempt_buy_pet(game_info, replacement_pet, False) == 0):
                                    team_size += 1
                                    pet_improved = True
                                    return

                    i += 1

        # if you have 3+ remaining coins:
            # buy food (TODO - we could probably leave this for now)

        if game_info.player_info.coins >= 3:
            # buy food
            # have a rank for the foods
            # create a range list for the foods in the shop by rank

            rank_range = len(current_tier_food_ranks)
            shop_food_ranking = create_range_list(rank_range, current_tier_food_ranks, game_info, game_info.player_info.shop_foods)
            # print("~~~~~~~~~~~~~~~~~~Shop foods:~~~~~~~~~~~~~~~~~~~~~~~~~", flush = True)
            print(game_info.player_info.shop_foods)
            # print("~~~~~~~~~~~~~~~~~~Shop foods ranked:~~~~~~~~~~~~~~~~~~~~~~~~~", flush = True)
            print(shop_food_ranking)

            pet_rank_range = len(current_tier_pet_ranks)
            team_pet_ranking = create_range_list(pet_rank_range, current_tier_pet_ranks, game_info, game_info.player_info.pets)

            # find the pet to feed:
            pet_to_feed_index = 0 #initialise
            if (round_num == 5 or round_num == 6):
                # find the worst pet
                pet_to_feed_index = team_pet_ranking[-1]
            elif (round_num >= 7):
                # find the best pet
                pet_to_feed_index = team_pet_ranking[0]

            # buy the top foods until < 3 coins, or until shop is empty
            if len(game_info.player_info.shop_foods) > 0:
                # print(f"size of ranking list = {len(shop_food_ranking)}", flush = True)
                # print(f"index of food we desire = {shop_food_ranking[0]}", flush = True)
                if (team_pet_feed(game_info, shop_food_ranking[0], current_tier_food_ranks) == 0):
                    return
            # else:
            #     print("Get lost, we don't like you, don't come to the reunion.", flush = True)

        # if you have 1-2 coins, freeze (TODO - we could probably leave this for now)
        else:
            # if the food is in the top 3 for its tier:
            rank_range = len(game_info.player_info.shop_foods)
            shop_food_ranking = create_range_list(rank_range, current_tier_food_ranks, game_info, game_info.player_info.shop_foods)

            for rank in shop_food_ranking:
                if current_tier_food_dict[game_info.player_info.shop_foods[rank].type] < 3:
                    # freeze it if not already frozen
                    if game_info.player_info.shop_foods[rank].is_frozen is False:
                        bot_battle.freeze_food(game_info.player_info.shop_foods[rank])
                        game_info = bot_battle.get_game_info()

        '''
        TODO: re-roll as required
        '''
        order_pets(game_info, game_info.player_info.pets)
        print("round 4/5 turn ended : )", flush = True)
        bot_battle.end_turn()
        rolls_performed = 0
        pet_improved = False
        return

