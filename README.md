# Quantum Noughts and Crosses
Allows the user to play Tic Tac Toe against a quantum computer! This can be done by attatching a Roli board, or just through the UI. There are 3 different modes the quantum computer can use to play:

- Basic - this simply uses gate rotations to choose the best moves
- Grover - this uses the famous Grover's Search Algorithm to select a move
- SVM - this uses a quantum support vector machine to calculate the next move


## Setup
1. Clone this repo
2. Open a terminal and enter `pip install qiskit`
3. Navigate to the folder for the repo and run `python main.py`
4. Play Noughts and Crosses!

If you have a Roli Block you would like to connect, you need to upload the [littlefoot code](https://github.com/maddy-tod/tictactoe-roli/blob/master/UserInput/Roli/QTicTacToe.littlefoot) to it. When you then run the code with your Roli connected to the computer it should be automatically detected. If this still doesn't work, examine the output and check that the correct input/output ids for your device are being selected ([this](https://github.com/maddy-tod/tictactoe-roli/blob/b9efab4b09737c2b0b5f3d2dabdda58bf822f2f1/UserInput/Roli/RoliHandler.py#L33) is where you will need to change the ids being selected).


## The Modes
The idea behind the different players is that they demonstrate the different way quantum computing can currently be used. The Basic player demonstrates the low level ways quantum computers can be used, literally at the gate level. The Grover player exhibts an inherently quantum algorithm and the SVM player uses a hybrid, quantum and classical strategy to play.


### Basic
This mode creates a new circuit everytime the computer needs to make a move. The circuit consists of 9 qubits, one for each space on the board. The general premise of circuit creation is to put all potential moves into an equal superposition, so in the |+> state, apply gates based on how "good" the move is to encourage it towards the |-> state and then reapply the `H` gate so the vector moves to be nearer to |0> or |1> depending on how good the move was considered to be. The more likely a qubit is to be measured as a 1, the better the move. 

The circuit is created as follows :
1. Any spaces that have a move already in them have an `X` gate applied to them. This means that they cannot possibly be used a move.
2. Every avaiable space has an `H` gate applied to it to take it into the equal superposition.
3. All the spaces that are avaliable are iterated over and have T gates applied to then according to some rules.
    * Apply one `T` gate for every move in the same column as the space
    * Apply one `T` gate for every move in the same row as the space
    * Apply one `S` gate if the space is on a diagonal and there are 2 occupied spaces on the same diagonal
4. Apply an `H` gate to all the avaliable spaces. 

We then run this circuit 100 times and get the counts. These are then processed so that the counts of 1's in each position are obtained. The one that is the maximum is then selected as the move the quantum computer should make.
  
All of this can be visualized using the Bloch Sphere by clicking the `Show setup states button`, or if you would like to skip straight to the end states the button `Show final states` can be clicked.


### Grover
*Note: This player takes a long time to run, due to the fact it runs Grover's algorithm locally* 

This player chooses its moves by using Grovers algorithm. It creates a SAT oracle based on the current state of the board and a set of predefined rules. The rules are extracted from the [wikiHow](https://www.wikihow.com/Win-at-Tic-Tac-Toe) page on how to win noughts and crosses! The set of rules then have all the current moves appended as negated variables. This is then run through Grover's algorithm and a valid solution is returned. All the variables that are positive literals in the returned solution are potential moves. These are not necessarily the best moves, just potential valid ones. We then select the move from this list based on more of the advice from the article : if 5 (the number corresponding to the central space)is returned then take that space, else if there is a corner move take that, else choose randomly. 


### SVM

This method uses the SVM (now called VQC) provided by Qiskit Aqua to select its next move. This classifier is trained on a lots of data about different board configurations and where the next move should be played, which is indicated by the classification on the end.

The `Show classical view` button shows which move based on looking at all the data the computer should make. It is called this because classical hardware is currently more advanced, and so it can process all the data. The quantum computer however has to perform PCA, which means it can only see 3 features of the dataset. This is the same as only being able to see the top row of the board. This introduces a lot more uncertainty about where the move should be played, which can be visualised by clicking the `Show quantum view button`. Note how if you don't play in the top row, the view for the quantum computer doesn't change, but when you do it changes it's view. It is also possible that it suggests to play in a space that is already taken, this is because it can't see that there is a move there! If this occurs the player will just choose a random space to play in.




Happy playing!
