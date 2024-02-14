import random
import sys
import nltk
from rich.console import Console
from rich.theme import Theme
from rich.table import Table
from rich.text import Text
from string import ascii_letters, ascii_uppercase
#nltk.download("words")

def get_five_letter_words():
    words = set(nltk.corpus.words.words())  # Get the set of English words from NLTK
    five_letter_words = [word.upper() for word in words if len(word) == 5]
    return five_letter_words

def refresh_page(headline):
    console.clear()
    console.rule(f"[bold blue]:leafy_green: {headline} :leafy_green:[/]\n")

def show_guess(guesses, word):
    letter_status = {letter: letter for letter in ascii_uppercase}
    for guess in guesses:
        styled_guess = []
        for letter, correct in zip(guess,word):
            if letter == correct:
                style = "bold white on green"
            elif letter in word:
                style = "bold white on yellow"
            elif letter in ascii_letters.upper():
                style = "white on #666666"
            else:
                style = "dim"
            styled_guess.append(f"[{style}]{letter}[/]")
            if letter != '_':
                letter_status[letter] = f"[{style}]{letter}[/]"
            
        console.print("".join(styled_guess), justify="center")
    console.print("\n" + "".join(letter_status.values()), justify = "center")
#         correct_letters = {letter for letter,correct in zip(guess,word) if letter == correct }
#         misplaced_letters = set(guess) & set(word) - correct_letters
#         incorrect_letters = set(guess) - set(word)
#         print("correct letters: ", ",".join(sorted(correct_letters)))
#         print("misplaced letters: ", ",".join(sorted(misplaced_letters)))
#         print("incorrect letters: ", ",".join(sorted(incorrect_letters)))


def game_over(guesses,word,guessed_correctly):
    refresh_page(headline="Game Over")
    show_guess(guesses,word)
    print(f"\nThe word is: {word}")
    if guessed_correctly:
        console.print(f"\n[bold white on green]Correct, the word is {word}[/]")
    else:
        console.print(f"\n[bold white on red]Sorry, the word was {word}[/]")
        
def guess_word(previous_guesses):
    guess = console.input(f"\nGuess word: ").upper()
    if guess in previous_guesses:
        console.print(f"You've already guessed {guess}.",style = 'warning')
        return guess_word(previous_guess)
    
    if len(guess) != 5:
        console.print("Your guess must be 5 letters.", style="warning")
        sys.exit()
        return guess_word(previous_guesses)
    
    if any((invalid := letter) not in ascii_letters.upper() for letter in guess):
        console.print(
            f"Invalid letter: '{invalid}'. Please use English letters.",
            style="warning",
        )
        return guess_word(previous_guesses)
    
    return guess

def instructions():

    instructions = Text.from_markup(
    "[bold cyan]Welcome to Wordle![/bold cyan]\n"
    "Guess the secret word in 6 attempts.\n\n"
    "[bold]Instructions:[/bold]\n"
    "1. Enter a 5-letter word and press enter to submit your guess.\n"
    "2. The game will provide feedback on your guess:\n"
    "   - [green]Green letter:[/green] correct letter and position\n"
    "   - [yellow]Yellow letter:[/yellow] correct letter but wrong position\n"
    "   - [grey]Gray letter:[/grey] incorrect letter\n"
    "3. Keep guessing until you find the secret word or run out of attempts.\n"
    "4. [red]To exit the game, simply press Enter without typing anything as the guess word.\n"
    "5. [blue bold]Have fun!"
    )
    # # Create a table to display instructions
    # table = Table(show_header=False)
    # table.add_column(style="bold cyan")
    # table.add_column()

    # # Add instructions rows
    # table.add_row("Welcome to Wordle!", "Guess the secret word in 6 attempts.")
    # table.add_row("Instructions:", "1. Enter a 5-letter word and press enter to submit your guess.")
    # table.add_row("", "2. The game will provide feedback on your guess:")
    # table.add_row("", "   - Green letter: correct letter and position")
    # table.add_row("", "   - Yellow letter: correct letter but wrong position")
    # table.add_row("", "   - Gray letter: incorrect letter")
    # table.add_row("", "3. Keep guessing until you find the secret word or run out of attempts.")
    # table.add_row("", "4. Have fun!")

    # Print the instructions
    console.print(instructions)

def main():
    instructions()
    word = random.choice(get_five_letter_words())
    guesses = ["_" * 5] * 6
    for num in range(6):
        refresh_page(headline=f"Guess {num + 1}")
        
        show_guess(guesses, word)
        
        guesses[num] = guess_word(previous_guesses=guesses[:num])
        guessed_correctly = False
        if guesses[num] ==  word:
            guessed_correctly = True
            break
            
    game_over(guesses, word, guessed_correctly)


if __name__ == "__main__":
    
    console = Console(width=40, theme=Theme({"warning": "red on yellow"}))
    main()

    