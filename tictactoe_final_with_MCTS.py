import random
import math
import copy
import time
import pygame

VISUALIZATION=False

if VISUALIZATION:
    Scale=1
    NODE_WIDTH=60
    NODE_HEIGHT=120
    X_OFFSET=30
    Y_OFFSET=50
    FONT_SIZE=20
    X=0
    Y=0
    screen= pygame.display.set_mode()
    pygame.init()

def draw_node(node,x,y):
    if x>-NODE_WIDTH and y>-NODE_HEIGHT and x<screen.get_width()+20 and y<screen.get_height()+20:

        pygame.draw.rect(screen,"black",(x,y,NODE_WIDTH,NODE_HEIGHT),2)
        if NODE_WIDTH>30:
            font=pygame.font.Font(None,int(FONT_SIZE))

            t=font.render(f"V: {node.visits}",True,"black")
            t1=font.render(f"S: {node.score}",True,"black")
            t2=font.render(f"X: {node.selective}",True,"black") 

            screen.blit(t,(x+t.get_height()/4,y+t.get_height()/2))
            screen.blit(t1,(x+t.get_height()/4,y+t.get_height()*1.8))
            screen.blit(t2,(x+t.get_height()/4,y+t.get_height()*2.7))

            for j,row in enumerate(node.board):
                for i,v in enumerate(row):
                    pygame.draw.rect(screen,"black",(NODE_WIDTH/4+x+i*NODE_WIDTH/4-NODE_WIDTH/8,y+NODE_HEIGHT/1.5+j*NODE_WIDTH/4-NODE_WIDTH/8,NODE_WIDTH/4,NODE_WIDTH/4),1)

                    if v!="*":
                        c="red" if v=="O" else "black"
                        t2=font.render(v,True,c)
                        screen.blit(t2,(NODE_WIDTH/4+x+i*NODE_WIDTH/4-t2.get_width()/2,y+NODE_HEIGHT/1.5+j*NODE_WIDTH/4-t2.get_height()/2))





def calculate_width(node):
    W=0
    if node.children:
        for child in node.children:
            if child.visits!=0:

                W+=calculate_width(child)
        if W==0:
            return NODE_WIDTH+X_OFFSET
        return W 
    else:
        return NODE_WIDTH+X_OFFSET


def draw_node_children(node,x,y):
    y+=NODE_HEIGHT+Y_OFFSET
    drawables=[]
    for i,child in enumerate(node.children):
        if child.visits!=0:
            drawables.append(i)
    if node.children:
        for i,child in enumerate(node.children):
            if child.visits!=0:
                w=calculate_width(child)
                draw_node(child,x+w/2,y)
                if i!=drawables[0]:
                    pygame.draw.line(screen,"red",(x+w/2+NODE_WIDTH/2,y-Y_OFFSET/2),(x+NODE_WIDTH/2,y-Y_OFFSET/2))
                if i!=drawables[-1]:
                    pygame.draw.line(screen,"green",(x+w/2+NODE_WIDTH/2,y-Y_OFFSET/2),(x+w+X_OFFSET,y-Y_OFFSET/2))
                if child.children:
                    
                    pygame.draw.line(screen,"black",(x+w/2+NODE_WIDTH/2,y+NODE_HEIGHT),(x+w/2+NODE_WIDTH/2,y+NODE_HEIGHT+Y_OFFSET/2))
                pygame.draw.line(screen,"black",(x+w/2+NODE_WIDTH/2,y),(x+w/2+NODE_WIDTH/2,y-Y_OFFSET/2))
                #pygame.draw.line(screen,"black",(x+NODE_WIDTH+X_OFFSET/2,y+NODE_HEIGHT+Y_OFFSET/2),(x+w-X_OFFSET/2,y+NODE_HEIGHT+Y_OFFSET/2))
                draw_node_children(child,x,y)
                x+=w
            

def draw_tree(root):
    screen.fill("white")
    w=calculate_width(root)
    draw_node(root,X+w/2,Y)
    draw_node_children(root,X,Y)
    if root.children:
        pygame.draw.line(screen,"black",(X+w/2+NODE_WIDTH/2,Y+NODE_HEIGHT),(X+w/2+NODE_WIDTH/2,Y+NODE_HEIGHT+Y_OFFSET/2))
    
dragging=False
draggingx,draggingy=0,0


class MCTSNode:
    def __init__(self, board):
        self.visits = 0
        self.board = board
        self.children = []
        self.parent=None
        self.player="X"
        self.score = 0
        self.done=False
        self.selective=True
        self.expandable=True

class MCTS:
    def __init__(self,time) -> None:
        self.iterationTime=time
        self.m=0
    
    def select(self,root):
        for j in root.children:
            if j.visits == 0:
                return j
        if root.done:
            return root
        else:
            sc=self.best_child(root)

        return self.select(sc)
    
    def expand(self,root,player):
        plays = self.possible_states(root.board, "X" if root.player=="O" else "O")
        if self.is_game_over(root.board,player):
            root.expandable=False
            return
        if not root.done:
            for j in plays:
                j.parent=root
                if root.player=="X":
                    j.player="O"

                root.children.append(j)
        else:
            root.done=True
    def rollout(self, leaf,player):
        current_board = leaf.board
        player_turn = 1 if leaf.player == "O" else 0

        p1 = "O" if leaf.player == "O" else "X"
        p2 = "X" if leaf.player == "O" else "O"
        if self.is_game_over(current_board, "X" if player=="O" else "O"):
            leaf.parent.selective=False
        
        while self.possible_states(current_board, p1) and not self.is_game_over(current_board, p1) and not self.is_game_over(current_board, p2):
            if player_turn == 1:  # "X player" playing the move
                possible_states = [node.board for node in self.possible_states(current_board, p2)]
                if possible_states:
                    choice = random.randrange(0, len(possible_states))
                    current_board = possible_states[choice]

            elif player_turn == 0:  # "O player" playing the move
                possible_states = [node.board for node in self.possible_states(current_board, p1)]
                if possible_states:
                    choice = random.randrange(0, len(possible_states))
                    current_board = possible_states[choice]

            player_turn = 1 - player_turn  # Toggle between 0 and 1
            if self.is_game_over(current_board, p1) or self.is_game_over(current_board, p2):
                break

        score = 0.5
        if self.is_game_over(current_board, "X" if player=="O" else "O"):
            # for i in range(len(current_board)):
            #     for k in range(len(current_board[i])):
            #         if current_board[i][k] == "*":
            #             score-=1
            score -= 1
        elif self.is_game_over(current_board, player):
            score += 1

        return score
    
    # This method backpropagates the result of simulation, up the tree
    def backpropagate(self, leaf, result):
        while 1:
            leaf.score += result
            leaf.visits += 1
            if leaf.parent==None:
                break
            leaf=leaf.parent

    
    def move(self, mx, player):
        global dragging,draggingx,draggingy,X,Y

        root = MCTSNode(mx)
        root.player=player
        leaf=root
        self.starttimestamp=time.time()
        self.timeCounter=0
        paused=False
        if not VISUALIZATION:
            while self.iterationTime>time.time()-self.starttimestamp:
            #for i in range(1000):

                if root.visits == 0:
                    self.expand( root,player)
                leaf = self.select(root)
                self.expand(leaf,player)
                #leaf = self.expand(root.board, player, root)
                result = self.rollout(leaf,"X" if player=="O" else "O")
                self.backpropagate(leaf, result)
        if VISUALIZATION:
            for i in range(int(self.iterationTime)):

                if root.visits == 0:
                    self.expand( root,player)
                leaf = self.select(root)
                self.expand(leaf,player)
                #leaf = self.expand(root.board, player, root)
                result = self.rollout(leaf,"X" if player=="O" else "O")
                self.backpropagate(leaf, result)
                
                draw_tree(root)
                font=pygame.font.Font(None,int(30))
                t2=font.render(f"Iteration: {i+1}",True,"black") 
                screen.blit(t2,(screen.get_width()-t2.get_width(),screen.get_height()-t2.get_height()))
                pygame.display.update()
                # time.sleep(1)

                m=0
                while 1:
                    if m==1:
                        break
                    if dragging:
                        cx,cy=pygame.mouse.get_pos()
                        X+=cx-draggingx
                        Y+=cy-draggingy
                        draggingx=cx
                        draggingy=cy
                    
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN and not dragging:
                            if event.button == 1:
                                dragging=True
                                draggingx,draggingy=pygame.mouse.get_pos()

                        elif event.type == pygame.MOUSEBUTTONUP and dragging:
                            if event.button == 1:
                                dragging=False

                        elif event.type==pygame.KEYDOWN:
                            if event.key==pygame.K_SPACE:
                                paused=not paused
                        
                        elif event.type==pygame.MOUSEWHEEL:
                            global NODE_HEIGHT,NODE_WIDTH,X_OFFSET,Y_OFFSET,Scale,FONT_SIZE
                            if event.y>0:
                                for i in range((event.y)):
                                    
                                    NODE_HEIGHT*=1.1
                                    NODE_WIDTH*=1.1
                                    X_OFFSET*=1.1
                                    Y_OFFSET*=1.1
                                    FONT_SIZE*=1.1
                                    cx,cy=pygame.mouse.get_pos()
                                    ox,oy=cx-X,cy-Y
                                    X-=ox*0.1
                                    Y-=oy*0.1


                            elif event.y<0:
                                for i in range(abs(event.y)):
                                    #Scale*=0.9
                                    NODE_HEIGHT*=0.9
                                    NODE_WIDTH*=0.9
                                    X_OFFSET*=0.9
                                    Y_OFFSET*=0.9
                                    FONT_SIZE*=0.9
                                    cx,cy=pygame.mouse.get_pos()
                                    ox,oy=cx-X,cy-Y
                                    X+=ox*0.1
                                    Y+=oy*0.1
                                   



                    if not paused:     
                        m+=1
                    else:
                        draw_tree(root)
                        font=pygame.font.Font(None,int(30))
                        t2=font.render(f"Iteration: {i+1}",True,"black") 
                        screen.blit(t2,(screen.get_width()-t2.get_width(),screen.get_height()-t2.get_height()))
                        pygame.display.update()

                m=0


        return self.best_child(root).board

    # This method checks whether the game is over for the given player on the given board
   
    def is_game_over(self,board, player):
        # Checks if the specified player has won the game, by checking the rows, columns, and diagonals.
        for i in range(3):
            if all(board[i][j] == player for j in range(3)) or all(board[j][i] == player for j in range(3)):
                return True
        # Check both diagonals
        if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
            return True
        return False
    
    # This method generates next possible state (child nodes) for a given board state and the player
    def possible_states(self, mx, player):
        possible_states = []
        for i in range(len(mx)):
            for k in range(len(mx[i])):
                if mx[i][k] == "*":
                    option = copy.deepcopy(mx)
                    option[i][k] = player
                    child_node = MCTSNode(option)
                    possible_states.append(child_node)
        return possible_states

    # This method chooses the best child node based on the UCB (Upper Confidence Bound)
    def best_child(self, root):
        threshold = -math.inf
        best_child_node = None
        selective_rule=False
        for child_node in root.children:
            if child_node.selective:
                selective_rule=True
                break
        for child_node in root.children:
            if selective_rule and not child_node.selective:
                continue
            if child_node.visits==0:
                potential_score = 0
            else:
                potential_score = child_node.score / child_node.visits +1.41 * math.sqrt(math.log(root.visits) / child_node.visits)

            if potential_score > threshold:
                best_child_node = child_node
                threshold = potential_score
        if best_child_node==None:
            root.done=True
            return root
        return best_child_node




class Game:
    def __init__(self) -> None:
        # Initialize the game with an empty 3x3 board, where '*' represents an empty cell.
        self.board = [['*' for i in range(3) ] for j in range(3) ]
        # Define the human player as 'X'.
        self.human = 'X'
        # Initialize the current player as 'X'.
        self.currnet_player = 'X'
        # Initialize the opponent as None (to be set later based on user input).
        self.oponent = None

    def print_board(self):
        # Print the current state of the game board.
        for row in self.board:
            print(" ".join(row))
        print()

    # def check_winner(self, player):
    #     # Check if the specified player has won the game by examining rows, columns, and diagonals.
    #     for i in range(3):
    #         if all(self.board[i][j] == player for j in range(3)) or all(self.board[j][i] == player for j in range(3)):
    #             return True
    #     if all(self.board[i][i] == player for i in range(3)) or all(self.board[i][2 - i] == player for i in range(3)):
    #         return True
    #     return False
    def check_winner(self, player):
    # Check if the specified player has won the game by examining rows, columns, and diagonals.
        for i in range(3):
            if all(self.board[i][j] == player for j in range(3)) or all(self.board[j][i] == player for j in range(3)):
                return True
        # Check both diagonals
        if all(self.board[i][i] == player for i in range(3)) or all(self.board[i][2 - i] == player for i in range(3)):
            return True
        return False
        
    def check_draw(self):
        # Check if the game has ended in a draw by ensuring there are no empty cells left.
        return all(cell != '*' for row in self.board for cell in row)

    def run(self):
        iter_time= "Iterations" if VISUALIZATION else "Time"
        # Get user input to determine the game mode: Human vs Human or Human vs AI (MCTS algorithm).
        while 1:
            mode = input("1. HUMAN vs HUMAN\n2. HUMAN vs AI\n3. AI vs AI\nSelect Mode")
            if mode == "1":
                self.oponent = "O"
                break
            elif mode == "2":
                # Set the opponent as an instance of the MCTS class (Monte Carlo Tree Search).
                AItime=float(input(f"Enter {iter_time} for AI:"))
                self.oponent = MCTS(AItime)
                self.AIvsAI=False
                break
            elif mode == "3":
                # Set the opponent as an instance of the MCTS class (Monte Carlo Tree Search).
                AItime=float(input(f"Enter {iter_time} for AI 1:"))
                self.player1 = MCTS(AItime)
                AItime2=float(input(f"Enter {iter_time} for AI 2:"))
                self.player2 = MCTS(AItime2)
                self.AIvsAI=True

                break
            print("Invalid Input")

        # Main game loop
        if self.oponent == "O":
            while True:
                self.print_board()

                # Human vs Human or Human vs AI (if the current player is 'O').
                not_valid_move = True
                while not_valid_move:
                    print(self.currnet_player + " Turn")
                    row = input("Enter row position (0, 1, 2): ")
                    if row.isnumeric() and row != "":
                        if int(row) < 0 or int(row) > 2:
                            print("Invalid Input")
                            continue
                    else:
                        print("Invalid Input")
                        continue

                    col = input("Enter column position (0, 1, 2): ")
                    if col.isnumeric() and col != "":
                        if int(col) < 0 or int(col) > 2:
                            print("Invalid Input")
                            continue
                    else:
                        print("Invalid Input")
                        continue

                    row = int(row)
                    col = int(col)
                    not_valid_move = False

                if self.board[row][col] == '*':
                    # Make the move if the selected cell is empty.
                    self.board[row][col] = self.currnet_player

                    # Check if the current player has won.
                    if self.check_winner(self.currnet_player):
                        self.print_board()
                        print(f"Player {self.currnet_player} wins!")
                        break

                    # Check if the game has ended in a draw.
                    if self.check_draw():
                        self.print_board()
                        print("It's a draw!")
                        break

                    # Switch to the next player's turn.
                    if self.currnet_player == self.oponent:
                        self.currnet_player = 'X'
                    else:
                        self.currnet_player = 'O'
                else:
                    print("Cell already occupied. Try again.")

        elif not self.AIvsAI:
            while True:
                self.print_board()

                # Human vs Human or Human vs AI (if the current player is 'X').
                if self.currnet_player == 'X':
                    not_valid_move = True
                    while not_valid_move:
                        row = input("Enter row position (0, 1, 2): ")
                        if row.isnumeric() and row != "":
                            if int(row) < 0 or int(row) > 2:
                                print("Invalid Input")
                                continue
                        else:
                            print("Invalid Input")
                            continue

                        col = input("Enter column position (0, 1, 2): ")
                        if col.isnumeric() and col != "":
                            if int(col) < 0 or int(col) > 2:
                                print("Invalid Input")
                                continue
                        else:
                            print("Invalid Input")
                            continue

                        row = int(row)
                        col = int(col)
                        not_valid_move = False

                    if self.board[row][col] == '*':
                        # Make the move if the selected cell is empty.
                        self.board[row][col] = self.currnet_player

                        # Check if the current player has won.
                        if self.check_winner(self.currnet_player):
                            self.print_board()
                            print("Player X wins!")
                            break

                        # Check if the game has ended in a draw.
                        if self.check_draw():
                            self.print_board()
                            print("It's a draw!")
                            break

                        # Switch to the next player's turn.
                        self.currnet_player = 'O'
                    else:
                        print("Cell already occupied. Try again.")
                else:
                    # AI's turn (if the current player is 'O').
                    print("AI is thinking...")
                    # Get the AI's move using the MCTS algorithm and update the game board.
                    self.board = self.oponent.move(self.board, 'X')

                    # Check if the AI has won.
                    if self.check_winner('O'):
                        self.print_board()
                        print("Player O wins!")
                        break

                    # Check if the game has ended in a draw.
                    if self.check_draw():
                        self.print_board()
                        print("It's a draw!")
                        break

                    # Switch to the next player's turn.
                    self.currnet_player = 'X'
        else:
            n= int(input("Enter Number of Games: "))
            ai1=0
            ai2=0
            draw=0

            for i in range(n):
                self.board = [['*' for i in range(3) ] for j in range(3) ]

                while True:
                    self.print_board()
                    # AI vs AI.
                    if self.currnet_player == 'X':
                        print("AI 1 is thinking...")
                        # Get the AI's move using the MCTS algorithm and update the game board.
                        self.board = self.player1.move(self.board, 'O')

                        # Check if the AI has won.
                        if self.check_winner('X'):
                            self.print_board()
                            print("AI 1 wins!")
                            ai1+=1

                            break

                        # Check if the game has ended in a draw.
                        if self.check_draw():
                            self.print_board()
                            draw+=1

                            print("It's a draw!")
                            break

                        # Switch to the next player's turn.
                        self.currnet_player = 'O'
                        
                    else:
                        # AI's turn (if the current player is 'O').
                        print("AI 2 is thinking...")
                        # Get the AI's move using the MCTS algorithm and update the game board.
                        self.board = self.player2.move(self.board, 'X')

                        # Check if the AI has won.
                        if self.check_winner('O'):
                            self.print_board()
                            print("AI 2 wins!")
                            ai2+=1
                            break

                        # Check if the game has ended in a draw.
                        if self.check_draw():
                            self.print_board()
                            print("It's a draw!")
                            draw+=1

                            break

                        # Switch to the next player's turn.
                        self.currnet_player = 'X'
            print(f"AI 1: {ai1} ,AI 2: {ai2}, Draw: {draw}")
Game().run()
