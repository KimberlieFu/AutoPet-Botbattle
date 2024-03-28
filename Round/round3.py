
    # ROUND 3
    # max of 4 rolls -> from replacing 3 pets, will occur if 3 top-3 pets appear
    
    # 3/3 found case:
        # if you find 3 top-3 pets (duplicates allowed):
            # sell 3 pets
            # buy your top 3
            # if you found them using only one roll:
                # buy 1 food and feed it to your lowest rank pet

        # if after 1 roll you have only found 2 top-3 pets in total (incl. starting selection):
            # roll 3 times
            # if you see a top-3 pet you already have
                # freeze it
                # (only do one freeze, on more powerful pet)
                # if you roll again and see the higher ranked pet of the 2 you already have:
                    # unfreeze the less powerful
                    # freeze the more powerful
                    # (to optimise your chance of seeing your missing top-3 pet)
                # note that unlike in round 1, where the best possible team would have a 1, 2, 2 combo
                # the best possible team of round 3 would have diversity, and include a 1, 2, 3, and tier 1's 1 and 2

        # similar process for if you only find 1 top-3 pet after 1 roll (incl. starting selection)
    '''
    ROUND 3
    '''

    t2_food_ranks = [FoodType.MEAT_BONE, FoodType.APPLE, FoodType.CUPCAKE, FoodType.HONEY]

    def r3_make_move(game_info: 'GameInfo', round_num):
        global team_size
        global horse_acquired
        global rolls_performed
        global rolls_allowed

        # if there are no more shop pets, we need to end turn
        # in future, we need to either reroll or buy food or something
        # if len(game_info.player_info.shop_pets) == 0:
        #     bot_battle.end_turn()
        #     rolls_performed = 0
        #     return

        # look at top 3 for tier 2
        rank_range = len(tier2_ranks)
        shop_pet_ranking = create_range_list(rank_range, tier2_ranks, game_info, game_info.player_info.shop_pets)
        print("Highest value pets index list:", flush = True)
        print(shop_pet_ranking, flush = True)

        print(f"Pets in shop: {game_info.player_info.shop_pets}", flush = True)

        # check that there is actually top 3 rank pet
        # check if the first element in our ranking is in the top 3
        if tier2_dict[game_info.player_info.shop_pets[shop_pet_ranking[0]].type] < 3:
            # need to sell worst pet to buy best pet
            # rank the pets on your own team from best to worst
            team_pet_ranking = create_range_list(rank_range, tier2_ranks, game_info, game_info.player_info.pets)
            worst_pet = game_info.player_info.pets[team_pet_ranking[-1]]
            if game_info.player_info.coins >= 2:
                # sell the worst pet
                bot_battle.sell_pet(worst_pet)
                team_size -= 1
                # after this move, update game info
                game_info = bot_battle.get_game_info()

                # buy the best pet in the shop
                # buy the top 3 pet
                if (attempt_buy_pet(game_info, game_info.player_info.shop_pets[shop_pet_ranking[0]], False) == 0):
                    team_size += 1
                    return
                else:
                    exit()
        elif rolls_performed <= rolls_allowed[round_num - 1]:
            # if rolls_performed == 0:
            # count how many top-3 pets on team
            num_top3_pets = 0
            for team_pet in game_info.player_info.pets:
                if tier2_dict[team_pet.type] <= 3:
                    num_top3_pets += 1
            # if you don't have 3 top-3 pets on your team, try to acquire them
            if num_top3_pets < 3:
                # check the shop for top-3 pets
                rank_range = 3
                shop_pet_ranking = create_range_list(rank_range, tier2_ranks, game_info, game_info.player_info.shop_pets)
                # if there is a pet in the top 3, use it to replace your worst pet
                if len(shop_pet_ranking) != 0:
                    team_rank_range = len(tier2_ranks)
                    team_pet_ranking = create_range_list(team_rank_range, tier2_ranks, game_info, game_info.player_info.pets)
                    worst_pet_index = team_pet_ranking[-1]
                    worst_pet = game_info.player_info.shop_pets[worst_pet_index]

                    if game_info.player_info.coins >= 2:
                        # sell your worst pet
                        bot_battle.sell_pet(worst_pet)
                        # update team_size, game_info
                        team_size -= 1
                        game_info = bot_battle.get_game_info()

                        # buy the best top-3 pet (if there is a choice)
                        best_shop_pet_index = shop_pet_ranking[0]
                        best_shop_pet = game_info.player_info.pets[best_shop_pet_index]
                        if (attempt_buy_pet(game_info, best_shop_pet, False) == 0):
                            # update team_size, game_info
                            team_size -= 1
                            game_info = bot_battle.get_game_info()
                            return
                elif game_info.player_info.coins >= 1:
                    # reroll when there are none left
                    bot_battle.reroll_shop()
                    rolls_performed += 1
                    return

            # once you have 3 top-3 pets, use up your coins
            else:
                # if enough coins, buy food
                if game_info.player_info.coins >= 3:
                    # find the best pet in your team, to feed
                    team_rank_range = len(tier2_ranks)
                    team_pet_ranking = create_range_list(team_rank_range, tier2_ranks, game_info, game_info.player_info.pets)
                    best_team_pet_index = team_pet_ranking[0]
                    # feed food to your best pet
                    if (attempt_buy_food(game_info, 0, best_team_pet_index) == 0):
                        return

                # use remaining coins to reroll and freeze any top-3 pets that aren't dupicates
                if game_info.player_info.coins < 3:
                    # find any pets in the shop that are in the top 3
                    # check the shop for top-3 pets
                    rank_range = 3
                    shop_pet_ranking = create_range_list(rank_range, tier2_ranks, game_info, game_info.player_info.shop_pets)
                    if len(shop_pet_ranking) != 0:
                        # there are some top 3 pets
                        # check each pet on the team to see if the shop pets are already on the team
                        for shop_pet_index, shop_pet in enumerate(game_info.player_info.shop_pets):
                            pet_type_in_team = False
                            for team_pet in game_info.player_info.pets:
                                if team_pet is None or shop_pet is None:
                                    continue
                                if team_pet.type == shop_pet.type:
                                    # duplicate of team pet found
                                    pet_type_in_team = True
                            if pet_type_in_team is False:
                                # for any previously unseen top-3 pet/s ...
                                # freeze them (if not already frozen)
                                pet_to_freeze = game_info.player_info.shop_pets[shop_pet_index]
                                bot_battle.freeze_pet(pet_to_freeze)
                                # update game_info
                                game_info = bot_battle.get_game_info()

                        # if there are any unfrozen spots, reroll where possible
                        for shop_pet in game_info.player_info.shop_pets:
                            if shop_pet.is_frozen is False:
                                if game_info.player_info.coins > 0:
                                    bot_battle.reroll_shop()
                                    rolls_performed += 1
                                    return

                    elif game_info.player_info.coins > 0:
                        # reroll when there are none left
                        bot_battle.reroll_shop()
                        rolls_performed += 1
                        return

        bot_battle.end_turn()
        rolls_performed = 0
        return

