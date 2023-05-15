from src.settings import *


def check_rank(self, player_id: int):
    """Checks if the current player is in the top 10 players
    
    Parameters:
    rank(int|None): Rank of the current player
    medal(str): Hex of the player's medal
    """
    rank = None
    for i, id in enumerate(self.top_players_ids):
        if player_id == id:
            rank = i+1
            self.on_top_players = True
            break

        elif id == None:
            break
    
    medal = check_medal(rank)
    return rank, medal


def check_medal(rank: int) -> str:
    """Checks if the current player is in the top 3 players
    
    Parameters:
    rank(int): Rank of the current player

    Returns:
    medal(str): Hex code of the color of his medal if he has one
    """
    if rank == 1:
        medal = MEDAL_FIRST
    elif rank == 2:
        medal = MEDAL_SECOND
    elif rank == 3:
        medal = MEDAL_THIRD
    else:
        medal = FG
    return medal
