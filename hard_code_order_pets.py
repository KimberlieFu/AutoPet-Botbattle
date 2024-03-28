
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

