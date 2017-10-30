"""
Connect-4 using a ``pandas.DataFrame``.
"""
import sys
import itertools
import pandas as pd


def new_board():
    return pd.DataFrame(None, index=range(6), columns=list('abcdefg'))


def check_vert(bools):
    v1 = bools & bools.shift(-1)  # shift up by 1
    vr = v1 & v1.shift(-2)  # shift AND map up by 2
    return True if vr.any().any() else False


def check_horiz(bools):
    h1 = bools & bools.shift(1, axis=1)
    hr = h1 & h1.shift(2, axis=1)
    return True if hr.any().any() else False


def check_diags(bools):
    # / direction
    pos1 = bools & bools.shift(-1).shift(1, axis=1)
    posmask = pos1 & pos1.shift(-2).shift(2, axis=1)
    if posmask.any().any():
        return True

    # \ direction
    neg1 = bools & bools.shift(1).shift(1, axis=1)
    negmask = neg1 & neg1.shift(2).shift(2, axis=1)
    if negmask.any().any():
        return True

    return False


def has_winner(board, player):
    bools = board == player

    if check_vert(bools):
        return True, 'vertical'
    elif check_horiz(bools):
        return True, 'horizontal'
    elif check_diags(bools):
        return True, 'diagonal'

    return False, None


def drop(col, piece):
    colseries = board[col]
    next_row = colseries.index.max() - sum(colseries.notnull())
    colseries[next_row] = piece
    print(board)


if __name__ == '__main__':
    board = new_board()
    print(board)
    player1 = raw_input("\nPlayer 1 name: ")
    player2 = raw_input("Player 2 name: ")
    print("\n")
    players = itertools.cycle([player1, player2])

    player = next(players)
    while True:
        col = raw_input("Player '{}' select column: "
                        .format(player))
        try:
            drop(col, player)
            print("\n")
        except KeyError:
            print("\n{} is not valid column!?\n".format(col))
            continue

        win, patt = has_winner(board, player)
        if win:
            print("Player {} has won by {}...yey".format(player, patt))
            break

        player = next(players)

    sys.exit(0)
