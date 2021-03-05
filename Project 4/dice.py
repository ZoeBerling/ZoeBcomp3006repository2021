import random

"""Zoe Berling DU ID 872608482 count.py
This is a dice betting game between the user and the computer.
First the user defines how many sides the dice will have and how many dice there are.
Then they bet that the sum of their dice will be greater than the sum of the computer's dice.
Then user's dice and the computer's dice are rolled.
If the user's sum is greater, they win their bet.
If it is not, they lose their bet.
There are three classes:
Game class: defines how many sides and how many dice will be played in the game
(will be the same until the player loses their money or cashes out)
Die class: defines the roll and includes methods to compare values of the dice
Cup of Dice class: defines the list of dice rolled and includes methods to compare the values of the lists, and take
the sum of all dice rolled."""


def main():
    bank = 100  # The player will start with a set amount of "money" (you can choose the amount).
    game = Game()
    bet = 1
    gains = 0
    losses = 0

    while bank > 0 and bet != 0:
        bet = amount(bank)  # Choose amount to bet
        if bank == 0:
            break
        if bet == 0:
            break
        player = Cup_Of_Dice(game.sides(), game.quantity())
        computer = Cup_Of_Dice(game.sides(), game.quantity())
        if player > computer:  # you win
            bank += bet
            gains += bet
            print(f"Your dice: {player.sum()} > The computer: {computer.sum()}")
            print(f"You won ${bet}! Your total $ is now ${bank}")

        else:  # you lose
            bank -= bet
            losses += bet
            print(f"Your dice: {player.sum()} < The computer: {computer.sum()}")
            print(f"You lost ${bet}. Your total is now ${bank}")

    if bank == 0:
        print(f"Game Over. You've lost all your $ :( ")
    if bet == 0:
        print(f"Thanks for playing! Your total is ${bank}. Your total gains = ${gains}. Your total losses = ${losses}.")


def amount(bank):
    a = int(input(f"You have ${bank}. Please enter your bet. Or enter 0 to cash out. "))
    while a > bank:
        a = int(input(f"You only have ${bank}. Please enter a new bet. "))
        if a <= bank:
            return a
    return a


class Game:
    """Define the number of sides on the dice and the quantity for the game"""
    def __init__(self):
        self._sides = input("Please enter number of sides on the dice: ")
        self._quantity = input("Please enter the quantity of dice: ")

    def sides(self):
        return int(self._sides)

    def quantity(self):
        return int(self._quantity)


class Die:  # create the die
    def __init__(self, sides):
        self.sides = sides  # number of sides
        self.value = random.randint(1, sides)  # value when die is rolled

    def __str__(self):  # magic string method
        s = f"{self.sides} sided die rolled {self.value}"
        return s

    def __int__(self):
        return self.value

    def __eq__(self, other):
        """=="""
        if self.value == other.value:
            return True
        else:
            return False

    def __ne__(self, other):
        """!="""
        if self.value != other.value:
            return True
        else:
            return False

    def __lt__(self, other):
        """<"""
        if self.value < other.value:
            return True
        else:
            return False

    def __gt__(self, other):
        """>"""
        if self.value > other.value:
            return True
        else:
            return False

    def __le__(self, other):
        """<="""
        if self.value <= other.value:
            return True
        else:
            return False

    def __ge__(self, other):
        """>="""
        if self.value >= other.value:
            return True
        else:
            return False

    def __add__(self, other, sides):
        new_dice = Die(sides)
        return new_dice


class Cup_Of_Dice:  # a "Cup of Dice" class

    def __init__(self, sides, quantity):  # constructor
        self.sides = sides
        self.quantity = quantity
        self.dice = []
        for i in range(quantity):
            die = Die(sides)
            self.dice.append(die)

    def __str__(self):  # string magic method
        # s = f"The {self.sides} sided dice rolled a "
        s = ''
        for value in self.dice:
            s += f"{value}, "
        return s

    def __eq__(self, other):  # All Comparison magic methods
        """=="""
        # lists are the same length
        if len(self.dice) != len(other.dice):
            return False
        # if lists have the same values
        else:
            for i in range(len(self.dice)):
                if sorted(self.dice)[i] == sorted(other.dice)[i]:
                    continue
                else:
                    return False
            return True

    def __ne__(self, other):
        """!="""
        # lists are the same length
        if len(self.dice) != len(other.dice):
            return True
        # if lists have the same values
        else:
            for i in range(len(self.dice)):
                if sorted(self.dice)[i] != sorted(other.dice)[i]:
                    return True
                else:
                    continue
            return False

    def __lt__(self, other):
        """<"""
        if self.sum() < other.sum():
            return True
        else:
            return False

    def __gt__(self, other):
        """>"""
        if self.sum() > other.sum():
            return True
        else:
            return False

    def __le__(self, other):
        """<="""
        if self.sum() <= other.sum():
            return True
        else:
            return False

    def __ge__(self, other):
        """>="""
        if self.sum() >= other.sum():
            return True
        else:
            return False

    def roll(self, sides):  # method to roll the die
        value = random.randint(1, sides)
        return value

    def sum(self):  # method to sum all dice
        sum = 0
        for die in self.dice:
            sum += die.value
        return sum


if __name__ == '__main__':
    main()
