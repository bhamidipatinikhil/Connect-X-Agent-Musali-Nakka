import numpy as np

class config:
    columns = 7
    rows = 6
    inarow = 4

class obs:
    board = np.zeros(config.columns * config.rows)
    mark = 1
    # opp_mark = mark%2 + 1

def my_agent(obs, config):

    #Version 3.4
    import numpy as np
    import random

    


    class MyAgent3:

        def __init__(self):
            self.depth = 10
            self.breadth = 2
            self.moves_left = config.rows * config.columns
            self.grid = np.asarray(obs.board).reshape(config.rows, config.columns)
        
        def get_grid(self):
            self.grid = np.asarray(obs.board).reshape(config.rows, config.columns)
            return self.grid

        def print_grid(self, grid, latest_move):

            [print(i, end=' ') for i in range(config.columns)]
            print()
            if(latest_move != -1):
                print('-'*(latest_move*2), end='|')
                print('-'*(config.columns*2  - latest_move*2))
            else:
                print('-' * (config.columns*2 + 1))
            for r in range(config.rows):
                for c in range(config.columns):
                    if grid[r][c] == 0:
                        print('.', end=' ')
                    else:
                        print(int(grid[r][c]), end=' ')
                print()
            print()

        def drop_piece(self, grid, move, piece):
            result_grid = grid.copy()
            for r in range(config.rows-1, -1, -1):
                if grid[r][move] == 0:
                    result_grid[r][move] = piece
                    return result_grid

        def move(self, grid, piece, depth_ctr=0):
            d_ctr = depth_ctr
            if(d_ctr == 0):
                self.moves_left -= 1
            
            if(d_ctr < min(self.depth, self.moves_left)):
                #Recursive Case
                d_ctr += 1

                current_grid = grid
                valid_moves = [col for col in range(config.columns) if current_grid[0][col]==0]

                # immediate_winning_states = []
                for move in valid_moves:
                    tmp_grid = self.drop_piece(current_grid, move, piece)
                    tmp_result = self.check_if_won(tmp_grid, piece)
                    if tmp_result:
                        return move, 1e7
                
                for move in valid_moves:
                    tmp_grid = self.drop_piece(current_grid, move, piece%2 + 1)
                    tmp_result = self.check_if_won(tmp_grid, piece%2 + 1)
                    if tmp_result:
                        return move, -3*1e7
                    
                scores = []
                scores_move_dict = {}
                for i, move in  enumerate(valid_moves):
                    tmp_grid = self.drop_piece(current_grid, move, piece)
                    tmp_score = self.evaluate_position(tmp_grid, piece)
                    scores.append(tmp_score)
                    scores_move_dict[tmp_score] = move
                
                scores.sort(reverse=True)

                grids = [self.drop_piece(current_grid, scores_move_dict[scores[i]], piece) for i in range(min(self.breadth, len(scores)))]
                new_scores = []
                scores_move_dict_2 = {}
                for i, posn in enumerate(grids):
                    tmp_move, tmp_score = self.move(posn, piece%2 + 1, d_ctr)
                    new_scores.append(tmp_score)
                    scores_move_dict_2[tmp_score] = tmp_move
                
                max_score = max(new_scores)
                max_score_move = scores_move_dict_2[max_score]          

                return max_score_move, max_score
            else:
                #Base Case
                current_grid = grid
                valid_moves = [col for col in range(config.columns) if current_grid[0][col]==0]

                for move in valid_moves:
                    tmp_grid = self.drop_piece(current_grid, move, piece)
                    tmp_result = self.check_if_won(tmp_grid, piece)
                    if tmp_result:
                        return move, 1e7
                
                for move in valid_moves:
                    tmp_grid = self.drop_piece(current_grid, move, piece%2 + 1)
                    tmp_result = self.check_if_won(tmp_grid, piece%2 + 1)
                    if tmp_result:
                        return move, -3*1e7

                scores = []
                scores_ind_dict = {}
                for i, move in enumerate(valid_moves):
                    tmp_score = self.evaluate_position(self.drop_piece(current_grid, move, piece), piece)
                    scores.append(tmp_score)
                    scores_ind_dict[tmp_score] = i

                max_score = max(scores)
                max_score_ind = scores_ind_dict[max_score]

                return valid_moves[max_score_ind], max_score

        def count_windows(self, grid, i, turn):
                #Only 4 directions i guess
                ctr = 0
                for j in range(config.rows):
                    st = 0
                    end = st + config.inarow-1

                    while(end < config.columns):
                        window = list(grid[j, st:end+1])
                        if(window.count(turn) == i):
                            ctr += 1

                        st += 1
                        end = st + config.inarow-1
                
                for j in range(config.columns):
                    st = 0
                    end = st + config.inarow-1

                    while(end < config.rows):
                        window = list(grid[st: end+1, j])

                        if(window.count(turn)==i):
                            ctr+= 1
                        
                        st += 1
                        end = st + config.inarow-1
                

                st_r = 0
                st_c = 0
                end_r = st_r + config.inarow - 1
                end_c = st_c + config.inarow - 1
                while(end_r < config.rows):
                    while(end_c < config.columns):
                        window = []
                        for j in range(0, config.inarow):
                            window.append(grid[st_r + j][st_c + j])
                        
                        if(window.count(turn)==i):
                            ctr+= 1
                        
                        st_c += 1
                        end_c = st_c + config.inarow - 1
                    
                    st_r += 1
                    end_r = st_r + config.inarow - 1
                    st_c = 0
                    end_c = st_c + config.inarow - 1
                
                st_r = 0
                st_c = config.columns-1
                end_r = st_r + config.inarow-1
                end_c = st_c - config.inarow+1
                while(end_r < config.rows):
                    while(end_c >= 0):
                        window = []
                        for j in range(config.inarow):
                            # print(st_r + j)
                            # print(st_c + j)
                            window.append(grid[st_r + j][st_c - j])
                        
                        if(window.count(turn)==i):
                            ctr+= 1
                        
                        st_c -= 1
                        end_c = st_c - config.inarow+1
                    
                    st_r += 1
                    end_r = st_r + config.inarow-1
                    st_c = config.columns-1
                    end_c = st_c - config.inarow+1
                


                return ctr


        def check_if_won(self, grid, piece):
            fours_in_a_row = self.count_windows(grid, 4, piece)
            if fours_in_a_row > 0:
                return True
            else:
                return False

        def evaluate_position(self, grid, piece):

            
            def create_seq_list(grid, turn):
                result_list = []

                for i in range(2, config.inarow+1):
                    result_list.append(self.count_windows(grid, i, turn))
                
                return result_list
            
            def calculate_score(grid, piece):
                my_seqs_list = create_seq_list(grid, piece) 
                opp_seqs_list = create_seq_list(grid, piece%2 + 1) 


                my_mult_consts = [10, 1000, 1000000]
                opp_mult_consts = [-20, -2000, -2000000]

                my_arr = [i*j for i, j in zip(my_seqs_list, my_mult_consts)]
                opp_arr = [i*j for i, j in zip(opp_seqs_list, opp_mult_consts)]

                return sum(my_arr) + sum(opp_arr)

            score = calculate_score(grid, piece)
            # print('\n', score, '\n')
            return score
            
    def watch_agent_vs_agent():

        ag = MyAgent3()
        ag.print_grid(ag.get_grid(), -1)
        turns = 0
        piece = obs.mark
        grid = ag.get_grid()

        while turns !=42:
            next_move,discard_score = ag.move(grid, piece, depth_ctr=0)
            next_grid = ag.drop_piece(grid, next_move, piece)
            ag.print_grid(next_grid, latest_move=next_move)
            if ag.check_if_won(next_grid, piece) == True:
                print("Piece", piece, "has won the game in", turns, "moves")
                break
            piece = (piece)%2 + 1
            grid = next_grid
            turns += 1

    def play_with_agent():
        ag = MyAgent3()
        ag.print_grid(ag.get_grid(), -1)
        turns = 0
        piece = obs.mark%2 + 1
        grid = ag.get_grid()

        agent_move = True
        while turns !=42:
            if agent_move:
                piece = piece%2 + 1
                next_move,discard_score = ag.move(grid, piece, depth_ctr=0)
                next_grid = ag.drop_piece(grid, next_move, piece)
                ag.print_grid(next_grid, latest_move=next_move)
                if ag.check_if_won(next_grid, piece) == True:
                    print("Piece", piece, "has won the game in", turns, "moves")
                    break
                # piece = (piece)%2 + 1
                agent_move = not agent_move
                grid = next_grid
                turns += 1
            else:
                print("Please enter the column you want to drop your move in::")
                piece = piece%2 + 1
                valid_moves = [col for col in range(config.columns) if grid[0][col] == 0]
                player_move = int(input())
                # player_move = -1
                while(player_move not in valid_moves):
                    print("Invalid Move!! Please enter a valid move")
                    player_move = int(input())
                if(player_move in valid_moves):
                    turns += 1
                    next_grid = ag.drop_piece(grid, player_move, piece)
                    ag.print_grid(next_grid, latest_move=player_move)
                    if ag.check_if_won(next_grid, piece) == True:
                        print("Piece", piece, "has won the game in", turns, "moves")
                        break
                
                agent_move = not agent_move
                grid = next_grid
                

    # agent = MyAgent3()
    # # grid = agent.get_grid()
    # move, score = agent.move(agent.get_grid(), obs.mark, depth_ctr=0)
    # return move



    watch_agent_vs_agent()
    # play_with_agent()

my_agent(obs, config).watch_agent_vs_agent()