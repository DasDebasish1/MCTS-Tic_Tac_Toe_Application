# Pre-requisites before running the application: -
1. Make sure you have installed the latest python.
2. Make sure you have insatlled pygame lib.

# Running the Program:-
1. To view tree plotter , 'VISUALIZATION' in the code need to set to True
2. Tree plotter is only available in iteration based. Hence number iteration would be taken as a input from the user when 'VISUALIZATION' is set to True
3. If VISUALIZATION is set to False, the game will work on time based and hence time in seconds will be taken as a input from the user.

## TIC-TAC-TOE Implementation with MCTS

Basic Tic-Tac-Toe was implemented first and then was used to evaluate standard MCTS. The implemented program allows the user to run AI vs AI and gets the option to select human vs human or human vs AI option, as shown in the below figure 1.

![Project Logo](https://github.com/DasDebasish1/MCTS-Tic_Tac_Toe_Application/blob/main/Picture1.png)

* Figure 1 : Demonstrates Tic-Tac-Toe implementation with MCTS

All games are played in the command line interface (CLI). I have also implemented a visualisation option initially kept as False (at line 7 in the code), but when set to True, allows the user to see how MCTS chooses the best move, as shown in Figure 1. Visualisation only works on an iterative basis as it takes additional time to execute. Hence, when Visualisation is set to True, the program will prompt the user to give iterations as the input when executed after selecting an option out of 3, as shown below

![Project Logo](https://github.com/DasDebasish1/MCTS-Tic_Tac_Toe_Application/blob/main/Picture2.png)

* Figure 2 : Executing application through Command Line Interface


