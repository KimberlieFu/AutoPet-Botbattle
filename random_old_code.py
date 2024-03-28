
            # TODO: delete this version, it's now a FUNC yay!
            # # track where they are in the shop
            # rank_range = 4
            # top_range_pos = []

            # for pet_pos, ideal_pet in enumerate(tier1_ranks):
            #     for shop_pet_index, shop_pet in enumerate(game_info.player_info.shop_pets):
            #         # check for pets in rank order
            #         if ideal_pet == shop_pet.type:
            #             if pet_pos < rank_range:
            #                 top_range_pos.append(shop_pet_index)
            









        print(f"Round {game_info.round_num}", flush = True)
        # This loop runs through the available pets in the shop.
        # It then checks whether you have an empty slot in your pet lineup.
        # If you do, then it checks that you can afford to buy the pet from
        # the shop.
        # At a minimum, you will now atleast get a full pet lineup!
        for shop_pet in game_info.player_info.shop_pets:
            for i, pet in enumerate(game_info.player_info.pets):
                if pet is None and shop_pet.cost <= game_info.player_info.coins:
                    # Always return after playing a move as
                    # you can only make one move at a time!
                    print(f"buying {shop_pet} at position {i}", flush = True)
                    bot_battle.buy_pet(shop_pet, i)
                    return

        # If we get here, there are two possibilities
        # 1. We're out of cash... yikes. Let's just end if thats the case
        # Note: your bot can be a lot smarter! Why not freeze some shop pets/foods?
        # Potentially rearrange your lineup to be more effective (think ability composition)
        # If you've got one or two coins laying around, do a reroll and freeze the goodies
        if game_info.player_info.coins < 3:
            # REROLLS + FREEZING (IF 1 or 2 coins)
            # Note: you have to end your turn once you're finished otherwise your submission
            # will get banned and you'll have to resubmit to keep playing!
            print("We have less than 3 coins : ( ending turn...", flush = True)
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
                        print("We have run out of moves : ( ending turn", flush = True)
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
        
        # index_for_ant = 1
        # for pet_index, pet in enumerate(game_info.player_info.pets):
        #     #print("Pet: {pet_index} {pet.pet_name}")
        #     if pet.type == PetType.ANT and index_for_ant != pet_index:
        #         #print("Found an ant")
        #         bot_battle.swap_pets(pet_index, index_for_ant)
        #         index_for_ant += 1
        #         # print("swapping our ants to be cool, ending turn", flush = True)
        #         # bot_battle.end_turn()
        #         return
        # And, for this simple example, if we get here, there's no more moves to make
        print("Nothing more to do, ending turn : )", flush = True)
        bot_battle.end_turn()


