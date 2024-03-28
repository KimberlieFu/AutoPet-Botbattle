









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
                    if (attempt_buy_pet(shop_pet, False) == 0):
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
                if (attempt_buy_pet(game_info.player_info.shop_pets[shop_pet_ranking[0]], False) == 0):
                    team_size += 1
                    # update game info
                    return
            # buy the (sub-par) top rank pet available and roll
            else:
                # buy the crappy pet
                if (attempt_buy_pet(game_info.player_info.shop_pets[shop_pet_ranking[0]], False) == 0):
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
                if (attempt_buy_pet(game_info.player_info.shop_pets[shop_pet_ranking[top_pet_index]], False) == 0):
                    team_size += 1
                    # print("ending turn - 185", flush = True)
                    # bot_battle.end_turn()
                    return

            if (team_size == 1):
                # need to buy 2 more pets total
                if (attempt_buy_pet(game_info.player_info.shop_pets[shop_pet_ranking[top_pet_index]], False) == 0):
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
                        if (attempt_buy_pet(game_info.player_info.shop_pets[shop_pet_ranking[top_pet_index]], False) == 0):
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
                        if (attempt_buy_pet(game_info.player_info.shop_pets[shop_pet_ranking[top_pet_index]], False) == 0):
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
    








from submissionhelper.botbattle import BotBattle
from submissionhelper.info.gameinfo import GameInfo


# Core class for the submission helper
# Use this to make moves and get game info
bot_battle = BotBattle()

# Core game loop
# Each iteration you will be expected to make one move
prev_round_num = 0
while True:
    # This function will pause until the game engine
    # is ready for you to make a move. Always call it
    # before making a move. It provides the information
    # required to make a sensible move
    game_info = bot_battle.get_game_info()

    # Feel free to uncomment these lines if you want to inspect the info!
    # print(game_info, flush = True)
    # print("", flush = True)

    # How to detect whether it is a new round
    new_round = prev_round_num != game_info.round_num
    if new_round:
        print(f"Round {game_info.round_num}\n\n")
        prev_round_num = game_info.round_num

    # Now let's go through a very simple (and poorly written!)
    # example submission
    def make_move(game_info: 'GameInfo'):
        # This loop runs through the available pets in the shop.
        # It then checks whether you have an empty slot in your pet lineup.
        # If you do, then it checks that you can afford to buy the pet from
        # the shop.
        # At a minimum, you will now atleast get a full pet lineup!
        for shop_pet in game_info.player_info.shop_pets:
            for i, pet in enumerate(game_info.player_info.pets):
                if pet == None and shop_pet.cost <= game_info.player_info.coins:
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

                    # We always have to call get_game_info() before making a second move
                    game_info = bot_battle.get_game_info()

                    # We have to get the new shop pet index because the game info has changed and no longer
                    # references the same object. Note: we could also use the shop pet's unique id
                    shop_pet = game_info.player_info.shop_pets[shop_pet_index]
                    bot_battle.buy_pet(shop_pet, pet_index)
                    return

        # And, for this simple example, if we get here, there's no more moves to make
        bot_battle.end_turn()

    # Last but not least, don't forget to call the function!
    make_move(game_info)

    # Now, you might be asking, where do I go from here?
    # Well, here's a few ideas to get you started:

    # 1. We didn't look at what type of pet we were buying AT ALL
    #    How are you going to make the best lineup possible without having some sort of heuristic for which pet is best?
    #    In the game engine, we have a ton of config listed. You could always leverage that!
    
    # 2. What about the shop foods? Eating food is a quick way to get better pets. AND don't forget about garlic + meat bone

    # 3. We didn't even rearrange our pets! bot_battle.swap_pets() is crucial to making an effective lineup

    # 4. What about rerolling!?!!?! Time to start decided when it is most effective to reroll versus eating food

    # 5. LEVEL YOUR PETS UP! Once you start getting a lineup you like, leveling up a pet can gurantee a victory.

    # This only scratches the surface and there's a lot of clever tricks you can do in the game
    # If you have any problems or questions, remember to hit us up on the discord.
