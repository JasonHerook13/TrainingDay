'''
Simulate games of roulette.
Choose a BET amount and the number of ROUNDS you want to play. 
Also choose a STRATEGY. The following values are allowed:
	- always_black
	- always_red
	- random
	- half_and_half
The data from the games is written to the file path defined in DATA_OUT.
A plot will also show at the end of the simulation to show you balance after each round.


To run this script you will need to do:
$ pip install matplotlib
$ pip install pandas

Then you can run it like this:
$ python simulate.py
'''

import random
import pandas as pd
import matplotlib.pyplot as plt

BET = 5
ROUNDS = 1000
STRATEGY = 'random'
DATA_OUT = 'simulation_data.csv'

def build_and_display_chart(x, y, title):
	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1)
	ax.plot(x, y, color = 'tab:blue')
	ax.set_title(title)
	plt.show()

def build_roulette_wheel():
	'''From Wikipedia: The pockets of the roulette wheel are numbered from 0 to 36.
	In number ranges from 1 to 10 and 19 to 28, odd numbers are red and even are black. In ranges from 11 to 18 and 29 to 36, odd numbers are black and even are red.
	There is a green pocket numbered 0 (zero)'''
	number_color = {}
	for i in range(37):
		if i == 0:
			color = 'Green'
		elif i in range(1, 11) or i in range(19, 29):
			if i % 2 == 0:
				color = 'Black'
			else:
				color = 'Red'
		else:
			if i % 2 != 0:
				color = 'Black'
			else:
				color = 'Red'
		number_color.update({i: color})
	return number_color

def spin(bet, choice):
	wheel = build_roulette_wheel()
	game_outcome = wheel[random.randint(0, 36)]
	if game_outcome == choice:
		return bet
	return - bet

def get_user_choice(strategy, current_round, total_rounds):
	if strategy == 'always_black':
		user_choice = 'Black'
	elif strategy == 'always_red':
		user_choice = 'Red'
	elif strategy == 'half_and_half':
		if current_round < total_rounds / 2:
			user_choice = 'Black'
		else:
			user_choice = 'Red'
	elif strategy == 'random':
		user_choice = random.choice(['Red', 'Black'])
	return user_choice

def simulate_roulette(bet, rounds, strategy):
	'''Simulate a game of roulette for `n` players and `k` rounds per simulation.
	Returns the simulation results as a Pandas DataFrame'''
	balance = 100
	round_balance = []
	choices = []
	for r in range(rounds):
		user_choice = get_user_choice(strategy, r, rounds)
		winnings = spin(bet = bet, choice = user_choice)
		balance = balance + winnings
		round_balance.append(balance)
		choices.append(user_choice)
	return round_balance, choices

if __name__ == '__main__':

	results, choices = simulate_roulette(BET, ROUNDS, STRATEGY)
	end_bal = results[-1]
	build_and_display_chart(x = range(ROUNDS), y = results, title = f"Strategy = {STRATEGY}\nEnd balance = {end_bal}")
	data = pd.DataFrame({
		'round': range(ROUNDS),
		'balance': results,
		'choices': choices
	})
	data.to_csv(DATA_OUT, index = False)
	print(f"Wrote simulation results to {DATA_OUT}")











