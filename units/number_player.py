#Определяем номер игрока (1 или 2) по его ID пользователя и данным о игре.
def get_number_player(user_id, game):
    if user_id == game[1]:
        return 1
    elif user_id == game[2]:
        return 2
    else:
        return False