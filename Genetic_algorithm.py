import numpy as np
import random
from copy import deepcopy as cp
from game_2048 import Game_2048

class Population(object):
    def __init__(self, seed):
        self.rand_gen = random.Random()
        self.rand_gen.seed(seed)
        self.game_seed = seed
        self.num_brains = 250
        self.num_limit = 5000
        self.brains = []
        for i in range(0, self.num_brains):
            self.brains.append(Brain(i, self.game_seed, self.num_limit))
        self.generation = 0


    def run_genetic_algorithm(self, lim_generations = 1000):
        for generation in range(0, lim_generations):
            self.simulate_generation()
            self.generation+=1


    def simulate_generation(self):
        #print("=== SIMULATING GENERATION ===")
        for brain in self.brains:
            brain.compute_fitness()
        selected_genome = self.natural_selection()
        genome_brain = self.brains[selected_genome]
        np.save('best_genome.npy', genome_brain.move_array)
        print("The best genome of generation {} is {} and has fitness: {}, with {} steps".format(self.generation, selected_genome, genome_brain.fitness, genome_brain.game.steps))
        print("The resulting board of the best genome")
        print(genome_brain.game)
        self.set_next_generation(selected_genome)


    def set_next_generation(self, selected_genome):
        genome_brain = self.brains[selected_genome]
        genome_vector = genome_brain.move_array
        genome_steps = genome_brain.game.steps
        self.brains[0].move_array = cp(genome_vector)
        self.brains[0].reset_game()
        for i in range(1,self.num_brains):
            self.brains[i].move_array = cp(genome_vector)
            self.brains[i].reset_game()
            self.brains[i].mutate_brain(genome_steps)


    def natural_selection(self):
        best_idx = 0
        best_fitness = self.brains[0].fitness
        best_steps = self.brains[0].game.steps
        #print("Fitness of {} is {}, with {} steps".format(best_idx, best_fitness, best_steps))
        idx = 1
        for brain in self.brains[1:]:
            actual_fitness = brain.fitness
            actual_steps = brain.game.steps
            #print("Fitness of {} is {}, with {} steps".format(idx, actual_fitness, actual_steps))
            if actual_fitness > best_fitness:
                best_idx = idx
                best_fitness = actual_fitness
                best_steps = actual_steps
            elif actual_fitness == best_fitness:
            	if actual_steps < best_steps:
	                best_idx = idx
	                best_fitness = actual_fitness
	                best_steps = actual_steps
            idx += 1
        return best_idx
                



class Brain(object):

    def __init__(self, seed, game_seed, move_limit = 1000):
        self.random_brain = random.Random()
        self.random_brain.seed(seed)
        self.game_seed = game_seed
        self.seed = seed
        self.move_limit = move_limit
        self.move_array = []
        self.random_moves()
        self.fitness = 0
        self.game = Game_2048(game_seed)


    def reset_game(self):
        self.game = Game_2048(self.game_seed)
        self.fitness = 0


    def random_moves(self):
        for i in range(0, self.move_limit):
            self.move_array.append(self.onehot_encode(self.random_brain.randint(0,3)))


    def onehot_encode(self, num):
        onehot_vec = np.zeros((4,1))
        onehot_vec[num] = 1
        return onehot_vec


    def compute_fitness(self):
        self.game.simulate_game(self.move_array)
        self.fitness = self.game.score


    def mutate_brain(self, steps):
        for i in range(0, steps):
            p = self.random_brain.randint(0, sum( range(0, steps) ) ) <= i
            if p: self.move_array[i] = self.onehot_encode(self.random_brain.randint(0,3))

