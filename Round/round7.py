    corresponding_dict[PetType.BLOWFISH] = PetType.FLAMINGO
    corresponding_dict[PetType.HIPPO] = PetType.KANGAROO

    def r5_make_move(game_info: 'GameInfo'):
        global team_size
        global horse_acquired
        global rolls_performed

        # if there are no more shop pets, we need to end turn
        # in future, we need to either reroll or buy food or something
        if len(game_info.player_info.shop_pets) == 0:
            bot_battle.end_turn()
            return

        # look through each of the shop pets
        replacement_pet = None
        for shop_pet in game_info.player_info.shop_pets:
            # if there is a pet that is in the corresponding_dict
            # check whether its lower val. equivalent pet is on our team
            if corresponding_dict[shop_pet.type] is not None:
                lower_val_version = corresponding_dict[shop_pet.type]
                replacement_pet = shop_pet
                break
    
        for team_pet in game_info.player_info.pets:
            # if the pet is on our team:
            # check whether it has been leveled up
            if team_pet.type == lower_val_version:
                # if it has NOT been leveled up:
                if team_pet.level < 2:
                    # sell the pet
                    bot_battle.sell_pet(team_pet)
                    team_size -= 1
                    game_info = bot_battle.get_game_info()
                    # buy the correspoding pet
                    if (attempt_buy_pet(game_info, replacement_pet, False) == 0):
                        team_size += 1
                        return

