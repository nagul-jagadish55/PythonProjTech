import random
import time
import json


class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.attempts = 0
        self.games_played = 0
        self.games_won = 0
        self.best_score = 0


class NumberGuessingGame:

    def __init__(self):
        self.players = []
        self.leaderboard = {}
        self.filename = "leaderboard.json"
        self.load_leaderboard()

    # ---------- FILE HANDLING ----------

    def load_leaderboard(self):
        try:
            with open(self.filename, "r") as file:
                self.leaderboard = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.leaderboard = {}

    def save_leaderboard(self):
        with open(self.filename, "w") as file:
            json.dump(self.leaderboard, file, indent=4)

    # ---------- RULES ----------

    def show_rules(self):
        print("\n========== RULES ==========")
        print("• 2 to 5 players can participate.")
        print("• Each player gets limited attempts.")
        print("• Guess the randomly generated secret number.")
        print("• Too High / Too Low hints are provided.")
        print("• Very Close is shown when the guess is close.")
        print("• Points are reduced for incorrect guesses.")
        print("• A time bonus is given for quick correct answers.")
        print("• Players who run out of attempts get 0 points.")
        print("• Scores are saved in the leaderboard.")

    # ---------- PLAYER SETUP ----------

    def create_players(self):

        while True:
            try:
                count = int(input("Number of players (2-5): "))

                if 2 <= count <= 5:
                    break

                print("Enter a number between 2 and 5.")

            except ValueError:
                print("Please enter a valid number.")

        self.players = []

        for i in range(count):

            while True:
                name = input(f"Enter Player {i + 1} name: ").strip()

                if not name:
                    print("Name cannot be empty.")
                    continue

                if any(
                    p.name.lower() == name.lower()
                    for p in self.players
                ):
                    print("Player name already exists.")
                    continue

                self.players.append(Player(name))
                break

    # ---------- DIFFICULTY ----------

    def choose_difficulty(self):

        print("\n========== DIFFICULTY ==========")
        print("1. Easy   : 1-50")
        print("2. Medium : 1-100")
        print("3. Hard   : 1-500")

        while True:

            choice = input("Choose difficulty: ")

            if choice == "1":
                return "Easy", 50, 5

            elif choice == "2":
                return "Medium", 100, 7

            elif choice == "3":
                return "Hard", 500, 10

            else:
                print("Invalid difficulty choice.")

    # ---------- GAME ----------

    def start_game(self):

        self.create_players()

        difficulty, maximum, max_attempts = (
            self.choose_difficulty()
        )

        secret_number = random.randint(1, maximum)

        # Randomize player order
        random.shuffle(self.players)

        print("\n================================")
        print("Difficulty:", difficulty)
        print("Guess a number from 1 to", maximum)
        print("================================")

        for player in self.players:

            print("\n-----", player.name, "'s Turn -----")

            score = 100
            player.attempts = 0
            won = False

            start_time = time.time()

            for attempt in range(1, max_attempts + 1):

                while True:
                    try:
                        guess = int(
                            input(
                                f"Attempt {attempt}/{max_attempts}: "
                            )
                        )

                        if 1 <= guess <= maximum:
                            break

                        print(
                            f"Enter a number from 1 to {maximum}."
                        )

                    except ValueError:
                        print("Enter numbers only.")

                player.attempts += 1

                # Correct answer
                if guess == secret_number:

                    elapsed = time.time() - start_time

                    if elapsed <= 5:
                        bonus = 30
                    elif elapsed <= 10:
                        bonus = 20
                    else:
                        bonus = 10

                    score += bonus
                    won = True

                    print("\nCorrect! 🎉")
                    print("Time:", round(elapsed, 2), "seconds")
                    print("Time bonus:", bonus)
                    print("Score:", score)

                    break

                score -= 10

                difference = abs(secret_number - guess)

                if difference <= 5:
                    print("Very Close!")

                elif guess > secret_number:
                    print("Too High!")

                else:
                    print("Too Low!")

                print("10 points deducted.")
                print("Current score:", score)

            if not won:
                score = 0
                print("\nNo attempts remaining.")
                print("Score: 0")

            player.score = score
            player.games_played += 1

            if won:
                player.games_won += 1

                if score > player.best_score:
                    player.best_score = score

                print("\n🏆", player.name, "found the number!")
                break

        else:
            print("\nNobody guessed the number.")
            print("The secret number was:", secret_number)

        self.update_leaderboard()
        self.save_leaderboard()

        print("\nLeaderboard updated and saved.")

    # ---------- LEADERBOARD ----------

    def update_leaderboard(self):

        for player in self.players:

            if player.name not in self.leaderboard:

                self.leaderboard[player.name] = {
                    "score": 0,
                    "games_played": 0,
                    "games_won": 0,
                    "best_score": 0
                }

            data = self.leaderboard[player.name]

            data["score"] += player.score
            data["games_played"] += 1
            data["games_won"] += (
                1 if player.games_won > 0 else 0
            )

            if player.score > data["best_score"]:
                data["best_score"] = player.score

    def show_leaderboard(self):

        print("\n========== LEADERBOARD ==========")

        if not self.leaderboard:
            print("No scores available.")
            return

        players = sorted(
            self.leaderboard.items(),
            key=lambda item: item[1]["score"],
            reverse=True
        )

        for position, (name, data) in enumerate(players, 1):

            print(f"\n{position}. {name}")
            print("   Total Score:", data["score"])
            print("   Games Played:", data["games_played"])
            print("   Games Won:", data["games_won"])
            print("   Best Score:", data["best_score"])

    # ---------- PLAYER STATISTICS ----------

    def search_player(self):

        name = input(
            "\nEnter player name: "
        ).strip()

        if name not in self.leaderboard:
            print("Player not found.")
            return

        data = self.leaderboard[name]

        print("\n========== PLAYER STATISTICS ==========")
        print("Name:", name)
        print("Total Score:", data["score"])
        print("Games Played:", data["games_played"])
        print("Games Won:", data["games_won"])
        print("Best Score:", data["best_score"])

    # ---------- MENU ----------

    def menu(self):

        while True:

            print("\n======================================")
            print("   MULTIPLAYER NUMBER GUESSING")
            print("          CHAMPIONSHIP")
            print("======================================")

            print("1. Start New Game")
            print("2. Display Rules")
            print("3. Show Leaderboard")
            print("4. Search Player Statistics")
            print("5. Exit")

            choice = input("Enter choice: ")

            if choice == "1":
                self.start_game()

            elif choice == "2":
                self.show_rules()

            elif choice == "3":
                self.show_leaderboard()

            elif choice == "4":
                self.search_player()

            elif choice == "5":
                print("Thank you for playing!")
                break

            else:
                print("Invalid choice.")


# ---------- PROGRAM START ----------

game = NumberGuessingGame()
game.menu()
