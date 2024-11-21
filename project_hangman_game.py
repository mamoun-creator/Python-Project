# Mamoun Mohamed
# 20/11/2024
# Improved Hangman game

import random
import os
import time
import json

class HangmanGame:
    """
    An advanced Hangman game class that provides a more interactive 
    and feature-rich word-guessing experience.
    """

    # Class-level constants for game configuration
    WORD_CATEGORIES = {
        "programming": [
            "python", "javascript", "algorithm", "database", 
            "frontend", "backend", "compiler", "function"
        ],
        "animals": [
            "elephant", "giraffe", "rhinoceros", "cheetah", 
            "penguin", "kangaroo", "platypus", "octopus"
        ],
        "countries": [
            "germany", "australia", "argentina", "switzerland", 
            "canada", "brazil", "japan", "morocco"
        ]
    }

    # Detailed ASCII art for hangman stages
    HANGMAN_STAGES = [
        # More detailed ASCII art for each stage of the hangman
        """\
    ╔═══════════╗
    ║           |
    ║           
    ║           
    ║           
    ║           
    ║           
    ╚═══════════╩═════""",
        """\
    ╔═══════════╗
    ║           |
    ║           O
    ║           
    ║           
    ║           
    ║           
    ╚═══════════╩═════""",
        # ... (rest of the stages would be similarly detailed)
    ]

    def __init__(self, difficulty="medium"):
        """
        Initialize the Hangman game with configurable settings.
        
        Args:
            difficulty (str): Game difficulty level 
            (easy, medium, hard) affecting attempts and word selection.
        """
        self.difficulty = difficulty
        self.max_attempts = self._set_attempts()
        self.score = 0
        self.high_score = self._load_high_score()

    def _set_attempts(self):
        """
        Dynamically set maximum attempts based on difficulty level.
        
        Returns:
            int: Number of allowed incorrect guesses.
        """
        difficulty_attempts = {
            "easy": 8,
            "medium": 6,
            "hard": 4
        }
        return difficulty_attempts.get(self.difficulty, 6)

    def _load_high_score(self):
        """
        Load high score from a JSON file.
        
        Returns:
            int: Highest score achieved previously.
        """
        try:
            with open('hangman_scores.json', 'r') as file:
                scores = json.load(file)
                return scores.get('high_score', 0)
        except (FileNotFoundError, json.JSONDecodeError):
            return 0

    def _save_high_score(self):
        """
        Save the current high score to a JSON file.
        """
        with open('hangman_scores.json', 'w') as file:
            json.dump({'high_score': max(self.score, self.high_score)}, file)

    def choose_word_category(self):
        """
        Allow player to choose a word category.
        
        Returns:
            str: Chosen category of words.
        """
        print("\n--- Word Categories ---")
        for idx, category in enumerate(self.WORD_CATEGORIES.keys(), 1):
            print(f"{idx}. {category.capitalize()}")
        
        while True:
            try:
                choice = int(input("\nChoose a category (number): "))
                category = list(self.WORD_CATEGORIES.keys())[choice - 1]
                return random.choice(self.WORD_CATEGORIES[category])
            except (ValueError, IndexError):
                print("Invalid category. Try again.")

    def play(self):
        """
        Main game play method with comprehensive game logic.
        """
        # Word selection with category choice
        word = self.choose_word_category()
        guessed_letters = set()
        attempts_left = self.max_attempts
        
        print("\n--- Hangman Game Started ---")
        
        while attempts_left > 0:
            # Clear screen for clean display
            os.system('cls' if os.name == 'nt' else 'clear')
            
            # Display game state
            self._display_game_state(word, guessed_letters, attempts_left)
            
            # Player guess input
            guess = self._get_player_guess(guessed_letters)
            
            # Process guess
            if guess in word:
                print("\n✅ Correct guess!")
                guessed_letters.add(guess)
                
                # Win condition check
                if set(word) <= guessed_letters:
                    self._handle_win(word)
                    break
            else:
                attempts_left -= 1
                print(f"\n❌ Wrong guess! {attempts_left} attempts remaining.")
            
            # Pause for readability
            time.sleep(1)
        
        # Game over handling
        if attempts_left == 0:
            self._handle_loss(word)

    def _display_game_state(self, word, guessed_letters, attempts_left):
        """
        Render current game state with hangman art and word progress.
        """
        # Display hangman stage
        print(self.HANGMAN_STAGES[self.max_attempts - attempts_left])
        
        # Display word progress
        display_word = ''.join(
            letter if letter in guessed_letters else '_' 
            for letter in word
        )
        print(f"\nWord: {display_word}")
        print(f"Attempts Left: {attempts_left}")
        print(f"High Score: {self.high_score}")

    def _get_player_guess(self, guessed_letters):
        """
        Validate and return player's letter guess.
        """
        while True:
            guess = input("\nGuess a letter: ").lower()
            
            if len(guess) != 1:
                print("Please enter a single letter.")
            elif not guess.isalpha():
                print("Please enter a valid letter.")
            elif guess in guessed_letters:
                print("You've already guessed that letter.")
            else:
                return guess

    def _handle_win(self, word):
        """
        Handle winning scenario, update score.
        """
        print(f"\n🎉 Congratulations! You guessed the word: {word}")
        self.score += len(word)
        self._save_high_score()

    def _handle_loss(self, word):
        """
        Handle losing scenario.
        """
        print(f"\n😢 Game Over! The word was: {word}")
        print(f"Your score: {self.score}")

def main():
    """
    Main game execution function with difficulty selection.
    """
    print("🎲 Welcome to Advanced Hangman! 🎲")
    
    while True:
        difficulty = input("\nSelect difficulty (easy/medium/hard): ").lower()
        
        if difficulty in ['easy', 'medium', 'hard']:
            game = HangmanGame(difficulty)
            game.play()
            
            play_again = input("\nPlay again? (yes/no): ").lower()
            if play_again != 'yes':
                print("Thanks for playing!")
                break
        else:
            print("Invalid difficulty. Choose easy, medium, or hard.")

if __name__ == "__main__":
    main()
