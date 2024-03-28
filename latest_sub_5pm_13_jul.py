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

pet_improved = False

#num rolls allowed for {round 1, round 2, ..., round 150}
#note that for round 8+ (index 7+), rolls_allowed is 1 (same as round 7 / index 6)
rolls_allowed = [1, 1, 4, 5, 2, 2, 1]
rolls_performed = 0 #reset at end of buy stage (once per round)

#RANKS:
tier1_ranks = [PetType.HORSE, PetType.CRICKET, PetType.ANT, PetType.BEAVER, 
    PetType.MOSQUITO, PetType.FISH, PetType.PIG]

tier2_ranks = [PetType.PEACOCK, PetType.FLAMINGO, PetType.KANGAROO, 
PetType.HORSE, PetType.SPIDER, PetType.BEAVER, PetType.CRICKET, PetType.ANT, PetType.CRAB, 
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

t2_food_ranks = [FoodType.MEAT_BONE, FoodType.APPLE, FoodType.CUPCAKE, FoodType.HONEY]

t3_food_ranks = [FoodType.GARLIC, FoodType.SALAD_BOWL, 
FoodType.MEAT_BONE, FoodType.APPLE, FoodType.CUPCAKE, FoodType.HONEY]

t4_food_ranks = [FoodType.CANNED_FOOD, FoodType.PEAR, FoodType.GARLIC, FoodType.SALAD_BOWL, 
FoodType.MEAT_BONE, FoodType.APPLE, FoodType.CUPCAKE, FoodType.HONEY]

carried_food = [FoodType.HONEY, FoodType.MEAT_BONE, FoodType.GARLIC]


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


t3_food_dict = dict()
i = 0
while i < len(t3_food_ranks):
    t3_food_dict[t3_food_ranks[i]] = i
    i += 1

t4_food_dict = dict()
i = 0
while i < len(t4_food_ranks):
    t4_food_dict[t4_food_ranks[i]] = i
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
            order_pets(game_info, game_info.player_info.pets)
            print("round 1 turn ended : )", flush = True)
            bot_battle.end_turn()
            rolls_performed = 0
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
                    if horse_acquired is True:
                        top_pet_index += 1
                    else:
                        break
                else:
                    break
            
            if (top_pet_index >= len(game_info.player_info.shop_pets)):
                print("We were forced to buy another horse because we ran out of non-horse pets", flush = True)
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

        order_pets(game_info, game_info.player_info.pets)
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
        if (team_size != 5):
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
            if (attempt_buy_pet(game_info, game_info.player_info.shop_pets[shop_pet_ranking[top_pet_index]], False) == 0):
                print("attempt best", flush = True)
                team_size += 1
                return

   
        order_pets(game_info, game_info.player_info.pets)
        print("round 2 turn ended : )", flush = True)
        bot_battle.end_turn()
        rolls_performed = 0
        return
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
        # if len(shop_pet_ranking) == 0:
        #     if game_info.player_info.coins > 0:
        #         bot_battle.reroll_shop()
        #         return
        #     else:
        #         bot_battle.end_turn()
        #         rolls_performed = 0
        #         return
            
        # check if the first element in our ranking is in the top 3
        if (len(game_info.player_info.shop_pets) > 0 and tier2_dict[game_info.player_info.shop_pets[shop_pet_ranking[0]].type] < 3):

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

        elif rolls_performed <= rolls_allowed[-1 + round_num]:
            if game_info.player_info.coins > 0:
                bot_battle.reroll_shop()
                rolls_performed += 1
                return
 
        order_pets(game_info, game_info.player_info.pets)
        print("round 3 turn ended : )", flush = True)
        bot_battle.end_turn()
        rolls_performed = 0
        return

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

        if game_info.player_info.coins >= 2:
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
                            upgrade = check_upgradable_b4_selling(game_info, game_info.player_info.pets, i)
                            if upgrade is not None and game_info.player_info.coins >= 3:
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

        if game_info.player_info.coins >= 2:
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
                                    upgrade = check_upgradable_b4_selling(game_info, game_info.player_info.pets, i)
                                    if upgrade is not None and game_info.player_info.coins >= 3:
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
            pet_to_feed_index = 0 # initialise
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


    '''
    FUNCTIONS
    '''

    # return a tuple of index to upgrade [from, to] ; else return None
    def check_upgradable_b4_selling(game_info, pets, pet_to_sell_index):
        from_i = None
        to_j = None
        # if there is a pet of the same type you were to sell to:
        pet_to_sell = pets[pet_to_sell_index]
        for pet_index, pet in enumerate(pets):
            if (pet is not None) and (pet_to_sell is not None):
                if (pet_to_sell.type == pet.type) and pet_to_sell_index != pet_index:
                    # work out which has higher level; if equal, sub-level
                    if pet_to_sell.level == pet.level:
                        if pet_to_sell.sub_level < pet.sub_level:
                            from_i = pet_to_sell
                            to_j = pet
                        else:
                            from_i = pet
                            to_j = pet_to_sell
                    elif pet_to_sell.level < pet.level:
                        from_i = pet_to_sell
                        to_j = pet
                    else:
                        from_i = pet
                        to_j = pet_to_sell
                    break
        if from_i is not None and to_j is not None:
            upgrade = [from_i, to_j]
            return upgrade
        else:
            return None

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

    
    def team_pet_feed(game_info, shop_food_index, current_tier_food_ranks):
        food_carry = []
        min_pet = 300
        min_pet_index = None

        # find least value member
        for team_pet_index, team_pet in enumerate(game_info.player_info.pets):
            if team_pet is not None:
                calc = team_pet.level * (team_pet.health + team_pet.attack) 
                if calc < min_pet:
                    min_pet = calc
                    min_pet_index = team_pet_index
                food_carry.append(team_pet.carried_food)
        
        # feed the food based on condition
        food = game_info.player_info.shop_foods[shop_food_index]
        if food not in carried_food and min_pet_index is not None:

            # if min_pet_index is not empty
            if (attempt_buy_food(game_info, shop_food_index, min_pet_index) == 0):
                return 0  # when calling this func, will need to update the game_info if the func returns 0
            else:
                print("ERROR: No pet food optimal", flush = True)
                return game_info.player_info.coins
            

        # all pets have food find the worse food type
        elif (len(food_carry) > 0):
            rank_range = len(food_carry)

            range_pos = []
            for pet_pos, pet_type in enumerate(current_tier_food_ranks):
                for pet_index, pet in enumerate(food_carry):
                    # check for pets in rank order
                    if pet is None:
                        continue
                    elif pet == pet_type:
                        if pet_pos < rank_range:
                            range_pos.append(pet_index)
                        else:
                            print("ERROR: pet position exceed rank pos from function", flush = True)
            
            if len(range_pos) != 0:
                worst_food = range_pos[-1]     
                # find the pet that has the worst food
                for team_pet_index, team_pet in enumerate(game_info.player_info.pets):
                    if team_pet is not None:
                        if team_pet.carried_food == worst_food:
                            if (attempt_buy_food(game_info, shop_food_index, team_pet_index) == 0):
                                return 0  # when calling this func, will need to update the game_info if the func returns 0
                            else:
                                print("ERROR: No pet food optimal", flush = True)
                                return game_info.player_info.coins



    def attempt_buy_pet(game_info, shop_pet, merge_allowed):
        if (shop_pet.cost <= game_info.player_info.coins):
            if merge_allowed:
                for i, pet in enumerate(game_info.player_info.pets):
                    if pet is None:
                        continue
                    if (shop_pet.type == pet.type and pet.level < 3):
                        print(f"attempt buy: {shop_pet.type} of ID {shop_pet.id} leveled up at pos. {i}", flush = True)
                        bot_battle.level_pet_from_shop(shop_pet, pet)
                        #must check that pet is not a level 3 pet already.
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
                if pet is None:
                    continue
                elif pet.type == pet_type:
                    if pet_pos < rank_range:
                        range_pos.append(pet_index)
                    else:
                        print("ERROR: pet position exceed rank pos from function", flush = True)
        return range_pos

    def r2_freeze_food(game_info: 'GameInfo'):
        global horse_acquired
        global horse_upgraded

        # if we have a horse but we haven't upgraded it yet, we want to freeze any apples
        if (horse_acquired is True) and (horse_upgraded is False):
            if game_info.player_info.shop_foods[0].type == FoodType.APPLE:
                return True
        return False

    '''
    MAIN
    '''
    # Now let's go through a very simple (and poorly written!)
    # example submission
    def make_move(game_info: 'GameInfo'):
        global team_size
        print("", flush = True)

        if (game_info.round_num == 1):
            print("Round 1:", flush = True)
            r1_make_move(game_info)
            print("r1 move performed", flush = True)
            return

        elif (game_info.round_num == 2):
            print("Round 2:", flush = True)
            r2_make_move(game_info)
            print("r2 move performed", flush = True)
            return

        elif (game_info.round_num == 3 or game_info.round_num == 4):
            print(f"Round {game_info.round_num}:", flush = True)
            r3_make_move(game_info, game_info.round_num)
            print(f"r{game_info.round_num} move performed", flush = True)
            return
        
        elif (game_info.round_num == 5 or game_info.round_num == 6):
            print(f"Round {game_info.round_num}:", flush = True)
            r5_make_move(game_info, tier3_ranks, tier3_dict, t3_food_ranks, t3_food_dict, game_info.round_num)
            print(f"r{game_info.round_num} move performed", flush = True)
            return

        elif (game_info.round_num >= 7):
            print(f"Round {game_info.round_num}:", flush = True)
            r5_make_move(game_info, tier4_ranks, tier4_dict, t4_food_ranks, t4_food_dict, game_info.round_num)
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
                rolls_performed = 0
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
                            rolls_performed = 0
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
            rolls_performed = 0

    # Last but not least, don't forget to call the function!
    print("attempt a move", flush = True)
    make_move(game_info)

