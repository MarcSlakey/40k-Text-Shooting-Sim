"""Model module
Majority of dice rolling occurs within this module.

Classes:
	Model
"""

import random
from weapon import *

class Model(object):

	"""Model class
	
	Model objects are stored in a list in Unit objects.

	Attributes:
		name (str): model's name
		move (int): maximum move distance in one turn (in inches)
		weapon_skill (int): minimum roll required to successfully hit a target with a melee weapon
		ballistic_skill (int): minimum roll required to successfully hit a target with a ranged weapon
		strength (int): used to determine minimum roll required successfully wound in melee combat
		toughness (int): used to determine minimum roll required to be wounded (melee or ranged)
		wounds (int): health counter
		attacks (int): number of attacks in melee combat
		leadership (int): used to determine outcome of morale tests
		save (int): minimum roll required to successfully save against a wound (melee or ranged)
		invulnerable (int): invulnerable save stat; used instead of regular save if (invulnerable roll) < (save + (armor piercing))
		weapons (Weapon): list of a model's Weapon objects

	"""
	
	def __init__(self, name, move, weapon_skill, ballistic_skill, strength, toughness, wounds, attacks, leadership, save, invulnerable):
		"""The constructor for Model class objects

		All parameter values are pulled from excel workbook/sheets defined in shooting_sim.py.
		"""
		super(Model, self).__init__()
		self.name = name
		self.move = move
		self.weapon_skill = weapon_skill
		self.ballistic_skill = ballistic_skill
		self.strength = strength
		self.toughness = toughness
		self.wounds = wounds
		self.attacks = attacks
		self.leadership = leadership
		self.save = save
		self.invulnerable = invulnerable
		self.weapons = []

	def __str__(self):
		"""Operator overloading: runs this function on print(Model) or str().

		Prints the number of wounds left on a model
		"""
		return "{} has {} wounds".format(self.name, self.wounds)

	def add_weapon(self, weapon):
		"""Adds a weapon to a given model's list of weapons"""
		self.weapons.append(weapon)

	def attack_with_weapon(self, weapon_index, target_unit):
		"""Initiates an attack against the next valid target in the opposing army.

		First determines how many shots the weapon has, then fires those shots one by one at the target. 
		"""
		weapon_used = self.weapons[weapon_index]
		if isinstance(weapon_used, RangedWeapon):
			if weapon_used.shot_dice == 0:
				shot_count = weapon_used.shots
			else:
				shot_count = 0
				for i in range(weapon_used.shot_dice):
					roll = random.randint(1, weapon_used.shots)
					shot_count += roll 
			
		elif isinstance(weapon_used, MeleeWeapon):
			#TODO
			pass

		print('\n{} takes {} shots against {} with {}.'.format(self.name, shot_count, target_unit.name, weapon_used.name))
		for i in range(shot_count):
			print('Taking shot {}'.format(i+1))
			self.single_shot(weapon_used, target_unit)

	def single_shot(self, weapon, target_unit):
		"""Summary."""
		roll = random.randint(1,6)
		if roll < self.ballistic_skill:
			print('  Failed to hit.')
			return

		# target_unit.hit_with_weapon(weapon)

		roll = random.randint(1,6)
		#Target toughness is always homogeneous within a unit
		target_toughness = target_unit.models[0].toughness
		if weapon.strength >= 2*target_toughness:
			wound_roll = 2
		elif weapon.strength > target_toughness:
			wound_roll = 3
		elif weapon.strength == target_toughness:
			wound_roll = 4
		elif weapon.strength < target_toughness:
			wound_roll = 5
		elif weapon.strength <= target_toughness/2:
			wound_roll = 6

		if roll < wound_roll:
			print('  Failed to wound.')
			return

		target_unit.save_against_wound(weapon)

	def model_save_against_wound(self, weapon):
		"""Summary."""
		roll = random.randint(1,6)
		if (self.invulnerable == None) or (self.invulnerable <= self.save):
			if roll >= self.save + weapon.ap:
				print('  {} saved against {} wound.'.format(self.name, weapon.name))
				return
		else:
			if roll >= self.invulnerable:
				print('  {} saved against {} wound.'.format(self.name, weapon.name))
				return

		if weapon.damage_dice == 0:
			self.wounds -= weapon.damage
			print('!  {} took {} damage from {}!'.format(self.name, weapon.damage, weapon.name))
		else:
			for i in range(weapon.damage_dice):
				roll = random.randint(1, weapon.damage)
				self.wounds -= roll
				print('!  {} took {} damage from {}!'.format(self.name, roll, weapon.name))

	def alive(self):
		"""Summary."""
		return self.wounds > 0
