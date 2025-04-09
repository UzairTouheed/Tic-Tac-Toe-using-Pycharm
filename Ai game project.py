import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import time
import random

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("AURORA UNIVERSITY Tic Tac Toe")
        self.root.configure(bg='#4CAF90')  # Set background color

        # Initialize game variables
        self.player_turn = 'X'  # 'X' starts the game
        self.moves = 0
        self.ai_mode = False
        self.demo_mode = False
        self.matches_played = 0

        # Initialize statistics
        self.total_games = 0
        self.player_wins = {'X': 0, 'O': 0}

        # Initialize timer variables
        self.start_time = None
        self.timer_label = None

        # Main page UI elements
        self.main_frame = tk.Frame(self.root, bg='#5CAF90')
        self.main_frame.pack(pady=20)

        # Load and place the logo
        self.logo_image = Image.open("C:/Users/UZAIR TAUHID/Downloads/logo.png")
        self.logo_image = self.logo_image.resize((100, 100), Image.LANCZOS)
        self.logo_photo = ImageTk.PhotoImage(self.logo_image)
        self.logo_label = tk.Label(self.main_frame, image=self.logo_photo, bg='#5CAF90')
        self.logo_label.pack(side='top', anchor='n', padx=20, pady=10)

        self.heading_label = tk.Label(self.main_frame, text="AURORA UNIVERSITY", font=('Copperplate Gothic Bold', 45), bg='#9CAF10', fg='blue')
        self.heading_label.pack(pady=10)

        self.heading_label = tk.Label(self.main_frame, text="Tic Tac Toe", font=('Wide Latin', 30), bg='#5CAF50', fg='dark red')
        self.heading_label.pack(pady=20)

        self.play_ai_button = tk.Button(self.main_frame, text="Play with AI", command=self.play_with_ai, font=('Bahnschrift SemiBold SemiConden', 19))
        self.play_ai_button.pack(pady=30)

        self.play_friends_button = tk.Button(self.main_frame, text="Play with Friends", command=self.play_with_friends, font=('Bahnschrift SemiBold SemiConden', 18))
        self.play_friends_button.pack(pady=30)

        self.demo_button = tk.Button(self.main_frame, text="Demo Game", command=self.demo_gameplay, font=('Bahnschrift SemiBold SemiConden', 18))
        self.demo_button.pack(pady=30)

    def play_with_ai(self):
        self.ai_mode = True
        self.demo_mode = False
        self.setup_game()

    def play_with_friends(self):
        self.ai_mode = False
        self.demo_mode = False
        self.setup_game()

    def demo_gameplay(self):
        self.ai_mode = False
        self.demo_mode = True
        self.setup_game()
        self.root.after(1000, self.demo_move)

    def setup_game(self):
        # Destroy main frame and create game frame
        self.main_frame.destroy()

        self.game_frame = tk.Frame(self.root, bg='#4CAF50')
        self.game_frame.pack()

        # Create buttons for the Tic Tac Toe grid
        self.buttons = []
        for i in range(3):
            row_buttons = []
            for j in range(3):
                button = tk.Button(self.game_frame, text='', font=('Helvetica', 20), width=11, height=4,
                                   command=lambda row=i, col=j: self.player_move(row, col))
                button.grid(row=i, column=j, padx=5, pady=5)
                row_buttons.append(button)
            self.buttons.append(row_buttons)

        # Add a Home button to return to the main menu
        self.home_button = tk.Button(self.game_frame, text="Home", command=self.go_to_main_menu, font=('Bahnschrift SemiBold SemiConden', 14))
        self.home_button.grid(row=3, column=1, pady=10)

        # Label to display number of matches played
        self.matches_label = tk.Label(self.game_frame, text=f"Matches Played: {self.matches_played}",
                                      font=('Cascadia Mono SemiBold', 12), bg='#7CAF90', fg='black')
        self.matches_label.grid(row=4, columnspan=3, pady=10)

        # Label to display wins by Player X and Player O
        self.player_wins_label = tk.Label(self.game_frame,
                                          text=f"Player 'X' wins: {self.player_wins['X']}  |  Player 'O' wins: {self.player_wins['O']}",
                                          font=('Times New Roman', 12), bg='#4CAF50', fg='white')
        self.player_wins_label.grid(row=5, columnspan=3, pady=10)

        # Add a Reset button to reset the game board
        self.reset_button = tk.Button(self.game_frame, text="Reset", command=self.reset_game_board, font=('Bahnschrift SemiBold SemiConden', 14))
        self.reset_button.grid(row=6, columnspan=3, pady=10)

        # Add a timer label
        self.timer_label = tk.Label(self.game_frame, text="Time: 00:00", font=('Helvetica', 12), bg='#9CAB10', fg='black')
        self.timer_label.grid(row=7, columnspan=3, pady=10)

        # Start the timer
        self.start_timer()

    def start_timer(self):
        self.start_time = time.time()
        self.update_timer()

    def update_timer(self):
        if self.start_time:
            elapsed_time = time.time() - self.start_time
            timer_str = time.strftime("%M:%S", time.gmtime(elapsed_time))
            self.timer_label.config(text=f"Time: {timer_str}")
            self.timer_label.after(1000, self.update_timer)  # Update every second

    def go_to_main_menu(self):
        # Reset game state and go back to main menu
        self.game_frame.destroy()
        self.__init__(self.root)

    def player_move(self, row, col):
        # Check if the cell is empty
        if self.buttons[row][col]['text'] == '':
            self.buttons[row][col]['text'] = self.player_turn
            self.moves += 1

            # Check for win or draw
            if self.check_win(self.player_turn):
                if self.player_turn == 'X':
                    self.highlight_winning_combo(self.player_turn, 'green')
                    self.game_over(f"Congratulations! You Win the Game!", 'green')
                elif self.player_turn == 'O':
                    self.highlight_winning_combo(self.player_turn, 'red')
                    self.game_over(f"Oh No! You Lose the Game!", 'red')
            elif self.moves == 9:
                self.game_over("It's a Draw!", 'black')
            else:
                # Switch turns
                self.player_turn = 'O' if self.player_turn == 'X' else 'X'

                # If AI mode and it's AI's turn, let AI make a move
                if self.ai_mode and self.player_turn == 'O':
                    self.root.after(500, self.ai_move)  # Delay AI move for smoother gameplay

                # If demo mode, make the next move automatically
                if self.demo_mode:
                    self.root.after(1000, self.demo_move)

    def demo_move(self):
        empty_cells = [(i, j) for i in range(3) for j in range(3) if self.buttons[i][j]['text'] == '']
        if empty_cells:
            row, col = random.choice(empty_cells)
            self.player_move(row, col)

    def ai_move(self):
        # Implement Minimax algorithm for AI move
        best_score = -float('inf')
        best_move = None

        for i in range(3):
            for j in range(3):
                if self.buttons[i][j]['text'] == '':
                    # Make the move for 'O'
                    self.buttons[i][j]['text'] = 'O'
                    score = self.minimax(False, 0)
                    # Undo the move
                    self.buttons[i][j]['text'] = ''

                    if score > best_score:
                        best_score = score
                        best_move = (i, j)

        # Make the best move for 'O'
        if best_move:
            self.buttons[best_move[0]][best_move[1]]['text'] = 'O'
            self.moves += 1

            # Check for win or draw after AI's move
            if self.check_win('O'):
                self.highlight_winning_combo('O', 'red')
                self.game_over("Player O Wins!", 'red')
            elif self.moves == 9:
                self.game_over("It's a Draw!", 'black')
            else:
                self.player_turn = 'X'

    def minimax(self, is_maximizing, depth):
        # Minimax algorithm implementation with alpha-beta pruning
        if self.check_win('O'):
            return 1
        elif self.check_win('X'):
            return -1
        elif self.moves == 9:
            return 0

        if is_maximizing:
            best_score = -float('inf')
            for i in range(3):
                for j in range(3):
                    if self.buttons[i][j]['text'] == '':
                        self.buttons[i][j]['text'] = 'O'
                        self.moves += 1
                        score = self.minimax(False, depth + 1)
                        self.buttons[i][j]['text'] = ''
                        self.moves -= 1
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(3):
                for j in range(3):
                    if self.buttons[i][j]['text'] == '':
                        self.buttons[i][j]['text'] = 'X'
                        self.moves += 1
                        score = self.minimax(True, depth + 1)
                        self.buttons[i][j]['text'] = ''
                        self.moves -= 1
                        best_score = min(score, best_score)
            return best_score

    def check_win(self, player):
        # Check rows, columns, and diagonals for a win
        for row in range(3):
            if all(self.buttons[row][col]['text'] == player for col in range(3)):
                self.winning_combo = [(row, col) for col in range(3)]
                return True
        for col in range(3):
            if all(self.buttons[row][col]['text'] == player for row in range(3)):
                self.winning_combo = [(row, col) for row in range(3)]
                return True
        if all(self.buttons[i][i]['text'] == player for i in range(3)):
            self.winning_combo = [(i, i) for i in range(3)]
            return True
        if all(self.buttons[i][2 - i]['text'] == player for i in range(3)):
            self.winning_combo = [(i, 2 - i) for i in range(3)]
            return True
        return False

    def highlight_winning_combo(self, player, color):
        for row, col in self.winning_combo:
            self.buttons[row][col].config(bg=color)

    def game_over(self, message, color):
        end_time = time.time()
        total_time = end_time - self.start_time
        minutes, seconds = divmod(total_time, 60)
        total_time_str = f"{int(minutes):02}:{int(seconds):02}"

        self.total_games += 1
        self.player_wins[self.player_turn] += 1
        self.matches_played += 1

        # Update the match and win labels
        self.matches_label.config(text=f"Matches Played: {self.matches_played}")
        self.player_wins_label.config(
            text=f"Player 'X' wins: {self.player_wins['X']}  |  Player 'O' wins: {self.player_wins['O']}")

        # Display a message box with the game result
        messagebox.showinfo("Game Over", f"{message}\nTime: {total_time_str}")

        # Reset the game board
        self.reset_game_board()

    def reset_game_board(self):
        for row in self.buttons:
            for button in row:
                button.config(text='', bg='SystemButtonFace')
        self.player_turn = 'X'
        self.moves = 0
        self.winning_combo = []
        self.start_timer()

if __name__ == "__main__":
    root = tk.Tk()
    tictactoe = TicTacToe(root)
    root.mainloop()
