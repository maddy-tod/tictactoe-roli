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
