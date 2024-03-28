    '''
    ROUND 2
    ''' 
    def r2_make_move(game_info: 'GameInfo'):
        global team_size
        global horse_acquired
        global horse_upgraded
        global rolls_performed

        if (game_info.player_info.coins < 3):
            if (game_info.player_info.coins != 1):
                print("Coins", flush = True)
                print(game_info.player_info.coins)
                print("Not enough coins remaining, time for battle!", flush = True)
                print("Goodbye", flush = True)
                # exit()
                bot_battle.end_turn()
                return
            

        if team_size == 3:
            # 92% chance that >=1 top 4 pet will be present
            # look for top 4 rank pet/s, starting with horse
            for shop_pet in game_info.player_info.shop_pets:
                if shop_pet.type == PetType.HORSE:
                    # buy only a single horse
                    # potentially put BUY in FUNC eg. check if enough coin, pos is free
                    if horse_acquired is True:
                        if (attempt_buy_pet(game_info, shop_pet, True) == 0):
                            team_size += 1
                            horse_upgraded = True
                            return
                        else:
                            print("ERROR: HORSE merge unsuccessful!!", flush = True)
                    else:
                        if (attempt_buy_pet(game_info, shop_pet, False) == 0):
                            team_size += 1
                            horse_acquired = True
                            return
                        else:
                            print("ERROR: HORSE acquisition unsuccessful!!", flush = True)

            # if there was no horse, look for a top 4 rank pet

            # look at top 4 for tier 1
            rank_range = len(tier1_ranks)
            shop_pet_ranking = create_range_list(rank_range, tier1_ranks, game_info, game_info.player_info.shop_pets)
            print("Highest value pets index list:")
            print(shop_pet_ranking)

            # check that there is actually top 4 rank pet
            # check if the first element in our ranking is in the top 4
            if tier1_dict[game_info.player_info.shop_pets[shop_pet_ranking[0]].type] < 4:
                # buy the top 4 pet
                if (attempt_buy_pet(game_info, game_info.player_info.shop_pets[shop_pet_ranking[0]], False) == 0):
                    team_size += 1
                    # update game info
                    # print("HOPEFULLY no errors so far. Goodbye.", flush = True)
                    # exit()
                    return
                else:
                    print("ERROR: Failed to buy top-4 pet from selection", flush = True)
                    exit(0)
            # buy the (sub-par) top rank pet available and roll
            else:
                # buy the crappy pet
                if (attempt_buy_pet(game_info, game_info.player_info.shop_pets[shop_pet_ranking[0]], False) == 0):
                    team_size += 1
                    print("we had to settle for a sub-par pet", flush = True)
                    # update the game info
                    game_info = bot_battle.get_game_info()
                    # roll the dice
                    if (r2_freeze_food(game_info) is True):
                        bot_battle.freeze_food(game_info.player_info.shop_foods[0])
                        game_info = bot_battle.get_game_info()
                        bot_battle.reroll_shop()
                        rolls_performed += 1
                        return
                    else:
                        bot_battle.reroll_shop()
                        rolls_performed += 1
                        return
                else:
                    print("ERROR: Failed to buy a crappy pet", flush = True)
                    exit(0)
    
        elif (rolls_performed > 0):
            # calculate the rank range list
            rank_range = len(tier1_ranks)
            shop_pet_ranking = create_range_list(rank_range, tier1_ranks, game_info, game_info.player_info.shop_pets)

            top_pet_index = 0
            # check if the top pet is a horse and there is one already
            for pet_ranking in shop_pet_ranking:
                if tier1_dict[game_info.player_info.shop_pets[pet_ranking].type] == 0:
                    if horse_upgraded is True:
                        top_pet_index += 1
                    else:
                        break
                else:
                    break
              
            if (top_pet_index >= len(game_info.player_info.shop_pets)):
                top_pet_index = 0

            if horse_upgraded is True:
                # we need to buy 2 more pets total
                if team_size == 3:
                    if (attempt_buy_pet(game_info, game_info.player_info.shop_pets[shop_pet_ranking[top_pet_index]], False) == 0):
                        team_size += 1
                        return


            if (team_size == 4):
                # need to buy 1 more pet total
                if (attempt_buy_pet(game_info, game_info.player_info.shop_pets[shop_pet_ranking[top_pet_index]], False) == 0):
                    team_size += 1
                    return

        else:
            # we have bought a pet, but we have not rolled
            # calculate the rank range list
            rank_range = len(tier1_ranks)
            shop_pet_ranking = create_range_list(rank_range, tier1_ranks, game_info, game_info.player_info.shop_pets)

            top_pet_index = 0
            # check if the top pet is a horse (has RANK == 0) and there is one already
            for pet_ranking in shop_pet_ranking:
                if tier1_dict[game_info.player_info.shop_pets[pet_ranking].type] == 0:
                    if horse_upgraded is True:
                        top_pet_index += 1
                    else:
                        break
                else:
                    break
              
            if (top_pet_index >= len(game_info.player_info.shop_pets)):
                top_pet_index = 0

            if team_size == 4:
                # we want to look for a second top-4 pet and then buy it if there is one
                if top_pet_index < len(game_info.player_info.shop_pets):
                    # check for a second top 4 pet in remaining shop selection
                    if tier1_dict[game_info.player_info.shop_pets[shop_pet_ranking[top_pet_index]].type] < 4:
                        # buy the top 4 pet
                        if (attempt_buy_pet(game_info, game_info.player_info.shop_pets[shop_pet_ranking[top_pet_index]], False) == 0):
                            team_size += 1
                            return
                    else:
                        # roll again
                        if (r2_freeze_food(game_info) is True):
                            bot_battle.freeze_food(game_info.player_info.shop_foods[0])
                            game_info = bot_battle.get_game_info()
                            bot_battle.reroll_shop()
                            rolls_performed += 1
                            return
                        else:
                            bot_battle.reroll_shop()
                            rolls_performed += 1
                            return
                else:
                    # no non-horses, roll again
                    if (r2_freeze_food(game_info) is True):
                        bot_battle.freeze_food(game_info.player_info.shop_foods[0])
                        game_info = bot_battle.get_game_info()
                        bot_battle.reroll_shop()
                        rolls_performed += 1
                        return
                    else: 
                        bot_battle.reroll_shop()
                        rolls_performed += 1
                        return

        # now, team size should be 5
        if team_size != 5:
            print("Team size is not 5... round 2 has a bug : /", flush = True)
        # if we have a horse, we want to feed it (if we haven't already upgraded it)
        if (horse_upgraded is False) and (horse_acquired is True):
            # find horse in team
            for i, pet in enumerate(game_info.player_info.pets):
                if pet.type == PetType.HORSE:
                    print("we would like to buy whatever is in the shop...(and feed to horse)", flush = True)
                    print(game_info.player_info.shop_foods)
                    # print(index(game_info.player_info.shop_foods))
                    if len(game_info.player_info.shop_foods) != 0:
                        if (attempt_buy_food(game_info, 0, i)) == 0:
                            horse_upgraded = True
                            return
                        else:
                            print("WARNING: feeding horse failed", flush = True)
                           
        # give food to the pet that will be sticking around the longest i.e. highest ranked
        elif horse_acquired is False:
            rank_range = 7
            team_index_ranking = create_range_list(rank_range, tier1_ranks, game_info, game_info.player_info.pets)
            print("we would like to buy whatever is in the shop (horse not there)...", flush = True)
            if attempt_buy_food(game_info, 0, team_index_ranking[0]) == 0:
                return
            else:
                print("WARNING: feed to other pet failed", flush = True)


        print("Final team", flush = True)
        print(game_info.player_info.pets)
        print("round 2 turn ended : )", flush = True)
        print("Goodbye", flush = True)
        # exit()
        bot_battle.end_turn()
        # exit()
        return


