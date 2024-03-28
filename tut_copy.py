from submissionhelper.botbattle import BotBattle
from submissionhelper.info.gameinfo import GameInfo
from submissionhelper.info.pettype import PetType
from submissionhelper.info.foodtype import FoodType


# Core class for the submission helper
# Use this to make moves and get game info
bot_battle = BotBattle()

print("hi world", flush = True)

#initial creating + setting of variables (game start - start of round 1)
horse_acquired = False
# horse should always be placed at the back of the team
HORSE_POS = 4
# horse should be upgraded in round 2
horse_upgraded = False
# macro for error where no free spots (or no pets avail to merge)
NO_FREE_SPOTS = 100
# current team size
team_size = 0


#num rolls allowed for {round 1, round 2, ..., round 150}
#note that for round 8+ (index 7+), rolls_allowed is 1 (same as round 7 / index 6)
rolls_allowed = {1, 1, 4, 5, 2, 2, 1}
rolls_performed = 0 #reset at end of buy stage (once per round)

#RANKS:
tier1_ranks = [PetType.HORSE, PetType.CRICKET, PetType.ANT, PetType.BEAVER, 
PetType.MOSQUITO, PetType.FISH, PetType.PIG]

tier2_ranks = [PetType.PEACOCK, PetType.FLAMINGO, PetType.BEAVER, PetType.KANGAROO, 
PetType.HORSE, PetType.SPIDER, PetType.CRICKET, PetType.ANT, PetType.CRAB, 
PetType.MOSQUITO, PetType.FISH, PetType.PIG, PetType.SWAN, PetType.HEDGEHOG]

tier3_ranks = [PetType.PEACOCK, PetType.FLAMINGO, PetType.KANGAROO, PetType.SHEEP, 
PetType.DOG, PetType.DOLPHIN, PetType.DODO, PetType.SPIDER, PetType.CAMEL, 
PetType.CRAB, PetType.BUNNY, PetType.GIRAFFE, PetType.BEAVER, PetType.HORSE, 
PetType.CRICKET, PetType.ANT, PetType.MOSQUITO, PetType.FISH, PetType.SWAN, 
PetType.PIG, PetType.HEDGEHOG, PetType.ELEPHANT, PetType.BADGER]

tier4_ranks = [PetType.BLOWFISH, PetType.PEACOCK, PetType.HIPPO, PetType.SHEEP, 
PetType.DOG, PetType.PENGUIN, PetType.FLAMINGO, PetType.KANGAROO, PetType.SKUNK, 
PetType.CAMEL, PetType.SPIDER, PetType.DODO, PetType.DOLPHIN, PetType.CRAB, 
PetType.BISON, PetType.BUNNY, PetType.SQUIRREL, PetType.GIRAFFE, PetType.BEAVER, 
PetType.HORSE, PetType.CRICKET, PetType.ANT, PetType.MOSQUITO, PetType.FISH, 
PetType.SWAN, PetType.PIG, PetType.HEDGEHOG, PetType.ELEPHANT, PetType.BADGER]


# make dictionaries for each of the ranking lists for easier lookup
tier1_dict = dict()
i = 0
while i < len(tier1_ranks):
    tier1_dict[tier1_ranks[i]] = i
    i += 1

tier2_dict = dict()
i = 0
while i < len(tier2_ranks):
    tier2_dict[tier2_ranks[i]] = i
    i += 1

tier3_dict = dict()
i = 0
while i < len(tier3_ranks):
    tier3_dict[tier3_ranks[i]] = i
    i += 1

tier4_dict = dict()
i = 0
while i < len(tier4_ranks):
    tier4_dict[tier4_ranks[i]] = i
    i += 1





# Core game loop
# Each iteration you will be expected to make one move
prev_round_num = 0
while True:
    # This function will pause until the game engine
    # is ready for you to make a move. Always call it
    # before making a move. It provides the information
    # required to make a sensible move
    game_info = bot_battle.get_game_info()

    # print("Pets on our team:", flush = True)
    # print(game_info.player_info.pets)
    # print("Pets in shop:", flush = True)
    # print(game_info.player_info.shop_pets)

    # Feel free to uncomment these lines if you want to inspect the info!
    # print(game_info, flush = True)
    # print("", flush = True)

    # How to detect whether it is a new round
    new_round = prev_round_num != game_info.round_num
    if new_round:
        print(f"Round {game_info.round_num}\n\n")
        prev_round_num = game_info.round_num

    '''
    TODO: add a variable "team_size" -->
        starts at 0 and changes when pets are bought/sold/merged
    '''
    '''
    ROUND 1
    '''
    # SOPHIE ROUND 1 DRAFT FUNC HERE:
    '''
    Round 1 structure:
        - buy 3 pets
        - buy 0 food
        - use 1 roll MAX. to aid this process
    '''

    def r1_make_move(game_info: 'GameInfo'):
        # case 1: currently team is empty
        global team_size
        global horse_acquired
        global rolls_performed
        
        if (game_info.player_info.coins < 3):
            bot_battle.end_turn()
            return

        if team_size == 0:
            # 92% chance that >=1 top 4 pet will be present
            # look for top 4 rank pet/s, starting with horse
            for shop_pet in game_info.player_info.shop_pets:
                if shop_pet.type == PetType.HORSE:
                    # buy only a single horse
                    # potentially put BUY in FUNC eg. check if enough coin, pos is free
                    if (attempt_buy_pet(game_info, shop_pet, False) == 0):
                        team_size += 1
                        horse_acquired = True
                        return

            # if there was no horse, look for a top 4 rank pet

            # look at top 4 for tier 1
            rank_range = len(tier1_ranks)
            shop_pet_ranking = create_range_list(rank_range, tier1_ranks, game_info, game_info.player_info.shop_pets)
            print("Highest value pets index list:")
            # print(shop_pet_ranking)

            # check that there is actually top 4 rank pet
            # check if the first element in our ranking is in the top 4
            if tier1_dict[game_info.player_info.shop_pets[shop_pet_ranking[0]].type] < 4:
                # buy the top 4 pet
                if (attempt_buy_pet(game_info, game_info.player_info.shop_pets[shop_pet_ranking[0]], False) == 0):
                    team_size += 1
                    # update game info
                    return
            # buy the (sub-par) top rank pet available and roll
            else:
                # buy the crappy pet
                if (attempt_buy_pet(game_info, game_info.player_info.shop_pets[shop_pet_ranking[0]], False) == 0):
                    team_size += 1
                    print("we had to settle for a sub-par pet", flush = True)
                    # update the game info
                    game_info = bot_battle.get_game_info()
                    # roll the dice
                    bot_battle.reroll_shop()
                    rolls_performed += 1
                    return
    
        elif (rolls_performed > 0):
            # must buy >= 1 pet
            # how many more pets do we need?
            # if team_size == 3:
            #     # end the turn TODO!!!!
            #     # print("r1 ending turn - 162", flush = True)
            #     # bot_battle.end_turn()
            #     return
            
            # calculate the rank range list
            rank_range = len(tier1_ranks)
            shop_pet_ranking = create_range_list(rank_range, tier1_ranks, game_info, game_info.player_info.shop_pets)

            top_pet_index = 0
            # check if the top pet is a horse and there is one already
            for pet_ranking in shop_pet_ranking:
                if tier1_dict[game_info.player_info.shop_pets[pet_ranking].type] == 0:
                    if horse_acquired == True:
                        top_pet_index += 1
                    else:
                        break
                else:
                    break
            
            if (top_pet_index >= len(game_info.player_info.shop_pets)):
                top_pet_index = 0
            

            if (team_size == 2):
                # need to buy 1 pet
                if (attempt_buy_pet(game_info, game_info.player_info.shop_pets[shop_pet_ranking[top_pet_index]], False) == 0):
                    team_size += 1
                    # print("ending turn - 185", flush = True)
                    # bot_battle.end_turn()
                    return

            if (team_size == 1):
                # need to buy 2 more pets total
                if (attempt_buy_pet(game_info, game_info.player_info.shop_pets[shop_pet_ranking[top_pet_index]], False) == 0):
                    team_size += 1
                    return
                    
        else:
            # we have bought a pet, but we have not rolled
            # calculate the rank range list
            rank_range = len(tier1_ranks)
            shop_pet_ranking = create_range_list(rank_range, tier1_ranks, game_info, game_info.player_info.shop_pets)

            top_pet_index = 0
            # check if the top pet is a horse and there is one already
            for pet_ranking in shop_pet_ranking:
                if tier1_dict[game_info.player_info.shop_pets[pet_ranking].type] == 0:
                    if horse_acquired is True:
                        top_pet_index += 1
                    else:
                        break
                else:
                    break
              
            if (top_pet_index >= len(game_info.player_info.shop_pets)):
                top_pet_index = 0
            

            if team_size == 1:
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
                        bot_battle.reroll_shop()
                        rolls_performed += 1
                        return
                else:
                    # no non-horses, roll again
                    bot_battle.reroll_shop()
                    rolls_performed += 1
                    return

            if team_size == 2:
                # we want to look for a third top-4 pet and TODO: FREEZE it before rerolling
                if top_pet_index < len(game_info.player_info.shop_pets):
                    # check for a second top 4 pet in remaining shop selection
                    if tier1_dict[game_info.player_info.shop_pets[shop_pet_ranking[top_pet_index]].type] < 4:
                        # buy the top 4 pet
                        if (attempt_buy_pet(game_info, game_info.player_info.shop_pets[shop_pet_ranking[top_pet_index]], False) == 0):
                            team_size += 1
                            # end turn
                            # bot_battle.end_turn()
                            return
                    else:
                        # roll again
                        bot_battle.reroll_shop()
                        rolls_performed += 1
                        return
                else:
                    # no non-horses, roll again
                    bot_battle.reroll_shop()
                    rolls_performed += 1
                    return

            # if team_size == 3:
            #     bot_battle.end_turn()
            #     return
        print("round 1 turn ended : )", flush = True)
        bot_battle.end_turn()
        return
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
                        # bot_battle.freeze_food(game_info.player_info.shop_foods[0])
                        # game_info = bot_battle.get_game_info()
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
                            # bot_battle.freeze_food(game_info.player_info.shop_foods[0])
                            # game_info = bot_battle.get_game_info()
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
                        # bot_battle.freeze_food(game_info.player_info.shop_foods[0])
                        # game_info = bot_battle.get_game_info()
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
    def r3_make_move(game_info: 'GameInfo'):
        global team_size
        global horse_acquired
        global rolls_performed

    
        # look at top 3 for tier 1
        rank_range = len(tier2_ranks)
        shop_pet_ranking = create_range_list(rank_range, tier2_ranks, game_info, game_info.player_info.shop_pets)
        print("Highest value pets index list:")
        # print(shop_pet_ranking)

        # check that there is actually top 3 rank pet
        # check if the first element in our ranking is in the top 3
        if tier2_dict[game_info.player_info.shop_pets[shop_pet_ranking[0]].type] < 3:
            # need to sell worst pet to buy best PetType
            # rank the pets on your own team from best to worst
            team_pet_ranking = create_range_list(rank_range, tier2_ranks, game_info, game_info.player_info.pets)
            worst_pet = game_info.player_info.pets[team_pet_ranking[-1]]
            # sell the worst pet
            bot_battle.sell_pet(worst_pet)
            team_size -= 1
            # after this move, update game info
            game_info = bot_battle.get_game_info()

            # buy the best pet in the sho
            # buy the top 3 pet
            if (attempt_buy_pet(game_info, game_info.player_info.shop_pets[shop_pet_ranking[0]], False) == 0):
                team_size += 1
                # update game info
                return
            else:
                exit()
        else:
            # in future, reroll shop
            # for now, move to battle
            bot_battle.end_turn()
            return
        
        
    # make dictionary to store the correspondence from higher val. pets to lower ones
    corresponding_dict = dict()

    corresponding_dict[PetType.DOG] = PetType.HORSE
    corresponding_dict[PetType.SHEEP] = PetType.SPIDER
    corresponding_dict[PetType.DODO] = PetType.ANT


    def r5_make_move(game_info: 'GameInfo'):
        global team_size
        global horse_acquired
        global rolls_performed
        

    '''
    FUNCTION
    '''
    def attempt_buy_pet(game_info, shop_pet, merge_allowed):
        if (shop_pet.cost <= game_info.player_info.coins):
            if merge_allowed:
                for i, pet in enumerate(game_info.player_info.pets):
                    if (shop_pet.type == pet.type):
                        print(f"attempt buy: {shop_pet.type} of ID {shop_pet.id} leveled up at pos. {i}", flush = True)
                        bot_battle.level_pet_from_shop(shop_pet, pet)
                        return 0 #success
            for i, pet in enumerate(game_info.player_info.pets):
                if (pet is None):
                    print(f"attempt buy: {shop_pet.type} of ID {shop_pet.id} installed at pos. {i}", flush = True)
                    bot_battle.buy_pet(shop_pet, i)
                    return 0 #success
            print("ERROR: no free spots", flush = True)
            return NO_FREE_SPOTS #cannot place pet
        else:
            print("ERROR: not enough coins!", flush = True)
            return game_info.player_info.coins #not enough coins

    def attempt_buy_food(game_info, shop_food_index, team_pet_index):
        if shop_food_index < len(game_info.player_info.shop_foods):
            # there is a valid food for us to buy
            if team_pet_index < len(game_info.player_info.pets):
                # we do have the pet
                bot_battle.buy_food(game_info.player_info.shop_foods[shop_food_index], game_info.player_info.pets[team_pet_index])
                return 0
            else:
                print("ERROR: pet not in team", flush = True)
                return 1
        else:
            print("ERROR: food not in shop", flush = True)
            return 2

    def create_range_list(rank_range, ranks_list, game_info, pet_collection):
        range_pos = []
        for pet_pos, pet_type in enumerate(ranks_list):
            for pet_index, pet in enumerate(pet_collection):
                # check for pets in rank order
                if pet.type == pet_type:
                    if pet_pos < rank_range:
                        range_pos.append(pet_index)

        return range_pos

    def r2_freeze_food(game_info: 'GameInfo'):
        global horse_acquired
        global horse_upgraded

        # if we have a horse but we haven't upgraded it yet, we want to freeze any apples
        if (horse_acquired is True) and (horse_upgraded is False):
            if game_info.player_info.shop_foods[0].type == FoodType.APPLE:
                return True
        return False

    # Now let's go through a very simple (and poorly written!)
    # example submission
    def make_move(game_info: 'GameInfo'):
        global team_size

        print("We are attempting to make a move", flush = True)
        print(f"Remaining moves: {game_info.remaining_moves}", flush = True)

        if (game_info.round_num == 1):
            print("Round 1:", flush = True)
            r1_make_move(game_info)
            print("r1 move performed", flush = True)
            return
        # if (game_info.player_info.coins > 111):
        #     pass

        elif (game_info.round_num == 2):
            print("Round 2:", flush = True)
            r2_make_move(game_info)
            print("r2 move performed", flush = True)
            return

        elif (game_info.round_num == 3 or game_info.round_num == 4):
            print(f"Round {game_info.round_num}:", flush = True)
            r3_make_move(game_info)
            print(f"r{game_info.round_num} move performed", flush = True)
            return

        else:
            # This loop runs through the available pets in the shop.
            # It then checks whether you have an empty slot in your pet lineup.
            # If you do, then it checks that you can afford to buy the pet from
            # the shop.
            # At a minimum, you will now atleast get a full pet lineup!
            for shop_pet in game_info.player_info.shop_pets:
                for i, pet in enumerate(game_info.player_info.pets):
                    if pet is None and shop_pet.cost <= game_info.player_info.coins:
                        # print(pet.type, flush = True)
                        print(f"we have {game_info.player_info.coins} coins left", flush = True)
                        # Always return after playing a move as
                        # you can only make one move at a time!
                        bot_battle.buy_pet(shop_pet, i)
                        return

            # If we get here, there are two possibilities
            # 1. We're out of cash... yikes. Let's just end if thats the case
            # Note: your bot can be a lot smarter! Why not freeze some shop pets/foods?
            # Potentially rearrange your lineup to be more effective (think ability composition)
            # If you've got one or two coins laying around, do a reroll and freeze the goodies
            if game_info.player_info.coins < 3:
                # Note: you have to end your turn once you're finished otherwise your submission
                # will get banned and you'll have to resubmit to keep playing!
                bot_battle.end_turn()
                return

            # 2. We have a full pet lineup. That's not toooo bad,
            # but why not check if there's a better pet in the shop
            for shop_pet_index, shop_pet in enumerate(game_info.player_info.shop_pets):
                for pet_index, pet in enumerate(game_info.player_info.pets):
                    if pet.health < shop_pet.health and pet.attack < shop_pet.attack and shop_pet.cost <= game_info.player_info.coins:
                        # We can't just immediately buy the pet because we have no free slots :(
                        # First we have to sell the mediocre pet AND THEN we can buy the shop pet

                        # This requires two remaining moves so let's check that first
                        if game_info.remaining_moves < 2:
                            bot_battle.end_turn()
                            return

                        bot_battle.sell_pet(pet)
                        team_size -= 1

                        # We always have to call get_game_info() before making a second move
                        game_info = bot_battle.get_game_info()

                        # We have to get the new shop pet index because the game info has changed and no longer
                        # references the same object. Note: we could also use the shop pet's unique id
                        shop_pet = game_info.player_info.shop_pets[shop_pet_index]
                        if game_info.player_info.pets[pet_index] is None:
                            bot_battle.buy_pet(shop_pet, pet_index)
                            return

            # And, for this simple example, if we get here, there's no more moves to make
            bot_battle.end_turn()

    # Last but not least, don't forget to call the function!
    print("attempt a move", flush = True)
    make_move(game_info)

