import path
import sys 

directory = path.Path(__file__).abspath()
sys.path.append(directory.parent)

from copy import deepcopy
from collections import namedtuple
from abc import ABCMeta, abstractmethod

from target_problem.target_problem import TargetProblem
from target_solution.evaluation_cache_control_statistics import EvaluationCacheControlStatistics

ObjectiveFitnessFeasibility = namedtuple('ObjectiveFitnessFeasibility', ['objective_value', 
                'fitness_value', 
                'is_feasible'])

class TargetSolution(metaclass=ABCMeta):
    
    """
    Cache that is used during evaluation for previously obtained solutions
    """
    evaluation_cache_cs:EvaluationCacheControlStatistics = EvaluationCacheControlStatistics()
    
    @abstractmethod
    def __init__(self, name:str, fitness_value:float, objective_value:float, is_feasible:bool)->None:
        """
        Create new TargetSolution instance
        :param str name: name of the target solution
        :param float fitness_value: fitness value of the target solution
        :param float objective_value: objective value of the target solution
        :param bool is_feasible: if the target solution is feasible, or not
        """
        self.__name = name
        self.__fitness_value = fitness_value
        self.__objective_value = objective_value
        self.__is_feasible = is_feasible

    @abstractmethod
    def __copy__(self):
        """
        Internal copy of the current target solution

        :return:  new `TargetSolution` instance with the same properties
        :rtype: TargetSolution
        """
        ts = deepcopy(self)
        return ts

    @abstractmethod
    def copy(self):
        """
        Copy the current target solution

        :return: new `TargetSolution` instance with the same properties
        :rtype: TargetSolution
        """
        return self.__copy__()

    @abstractmethod
    def copy_to(self, destination)->None:
        """
        Copy the current target solution to the already existing destination target solution

        :param destination: destination target solution
        :type destination: `TargetSolution`
        """
        destination =  copy(self)

    @property
    def name(self)->str:
        """
        Property getter for the name of the target solution

        :return: name of the target solution instance 
        :rtype: str
        """
        return self.__name

    @property
    def fitness_value(self)->float:
        """
        Property getter for fitness value of the target solution

        :return: fitness value of the target solution instance 
        :rtype: float
        """
        return self.__fitness_value

    @fitness_value.setter
    def fitness_value(self, value:float)->None:
        """
        Property setter for fitness value of the target solution

        :param value: value of the `fitness` to be set
        :type value: float
        """
        if value < 0:
            raise ValueError("Fitness value less than 0 is not possible.")
        self.__fitness_value = value

    @property
    def objective_value(self)->float:
        """
        Property getter for objective value of the target solution

        :return: objective value of the target solution instance 
        :rtype: float
        """
        return self.__objective_value

    @objective_value.setter
    def objective_value(self, value:float)->None:
        """
        Property setter for objective value of the target solution

        :param value: value of the `objective_value` to be set
        :type value: float
        """
        self.__objective_value = value

    @property
    def is_feasible(self)->bool:
        """
        Property getter for feasibility of the target solution

        :return: feasibility of the target solution instance 
        :rtype: bool
        """
        return self.__is_feasible

    @is_feasible.setter
    def is_feasible(self, value:bool)->None:
        """
        Property setter for feasibility of the target solution

        :param value: value to be set for the `is_feasible`
        :type value: bool
        """
        self.__is_feasible = value

    @abstractmethod
    def solution_code(self)->str:
        """
        Solution code of the target solution

        :return: solution code 
        :rtype: str
        """
        raise NotImplementedError

    @abstractmethod
    def calculate_objective_fitness_feasibility(self, problem:TargetProblem)->ObjectiveFitnessFeasibility:
        """
        Fitness calculation of the target solution

        :param TargetProblem problem: problem that is solved
        :return: objective value, fitness value and feasibility of the solution instance 
        :rtype: `ObjectiveFitnessFeasibility`
        """
        raise NotImplementedError

    @abstractmethod
    def recalculate_solution_code(self)->None:
        """
        Recalculation of the solution code for the target solution
        """
        raise NotImplementedError

    @abstractmethod
    def random_init(self)->None:
        """
        Random initialization of the target solution
        """
        raise NotImplementedError

    @staticmethod
    def calculate_objective_fitness_feasibility_try_consult_cache(target_solution, target_problem:TargetProblem):
        """
        Calculate fitness of the argument with optional cache consultation

        :param TargetSolution target_solution: target solution whose fitness should be 
        :param TargetProblem target_problem: problem that is solved
        :return: solution with calculated objection value, fitness value and feasibility
        :rtype: `TargetSolution`
        """
        eccs = target_solution.evaluation_cache_cs 
        eccs.increment_cache_request_count()
        if eccs.is_caching:
            code = target_solution.solution_code()
            if code in eccs.cache:
                eccs.increment_cache_hit_count()
                return eccs.cache[code]
            triplet:ObjectiveFitnessFeasibility = target_solution.calculate_objective_fitness_feasibility(
                    target_problem)
            target_solution.objective_value = triplet.objective_value
            target_solution.fitness_value = triplet.fitness_value
            target_solution.is_feasible = triplet.is_feasible
            eccs.cache[code] = target_solution
            return target_solution
        else:
            triplet:ObjectiveFitnessFeasibility = target_solution.calculate_objective_fitness_feasibility(
                    target_problem)
            target_solution.objective_value = triplet.objective_value
            target_solution.fitness_value = triplet.fitness_value
            target_solution.is_feasible = triplet.is_feasible
            return target_solution

    def evaluate(self, target_problem:TargetProblem)->None:
        """
        Evaluate current target solution

        :param TargetProblem target_problem: problem that is solved
        """        
        solution = TargetSolution.calculate_objective_fitness_feasibility_try_consult_cache(self, target_problem)
        self.objective_value = solution.objective_value;
        self.fitness_value = solution.fitness_value;
        self.is_feasible = solution.is_feasible;

    @abstractmethod
    def best_1_change(self, problem:TargetProblem)->bool:
        """
        Change the best one within solution 

        :param TargetProblem problem: problem that is solved
        :return: if the best one is changed, or not
        :rtype: bool
        """        
        raise NotImplementedError

    @abstractmethod
    def solution_code_distance(solution_code_1:str, solution_code_2:str)->float:
        """
        Calculate distance between two solutions determined by its code

        :param str solution_code_1: solution code for the first solution
        :param str solution_code_2: solution code for the second solution
        """
        raise NotImplementedError

    def string_representation(self, delimiter:str, indentation:int=0, indentation_symbol:str='', group_start:str ='{', 
        group_end:str ='}')->str:
        """
        String representation of the target solution instance

        :param delimiter: delimiter between fields
        :type delimiter: str
        :param indentation: level of indentation
        :type indentation: int, optional, default value 0
        :param indentation_symbol: indentation symbol
        :type indentation_symbol: str, optional, default value ''
        :param group_start: group start string 
        :type group_start: str, optional, default value '{'
        :param group_end: group end string 
        :type group_end: str, optional, default value '}'
        :return: string representation of instance that controls output
        :rtype: str
        """         
        s = delimiter
        for i in range(0, indentation):
            s += indentation_symbol  
        s += group_start + delimiter
        for i in range(0, indentation):
            s += indentation_symbol     
        s += 'name=' + self.name + delimiter
        for i in range(0, indentation):
            s += indentation_symbol     
        s += 'fitness_value=' + str(self.fitness_value) + delimiter
        for i in range(0, indentation):
            s += indentation_symbol     
        s += 'objective_value=' + str(self.objective_value) + delimiter
        for i in range(0, indentation):
            s += indentation_symbol     
        s += 'is_feasible=' + str(self.is_feasible) + delimiter
        for i in range(0, indentation):
            s += indentation_symbol     
        s += 'solution_code=' + self.solution_code() + delimiter
        for i in range(0, indentation):
            s += indentation_symbol     
        s += 'evaluation_cache_cs(static)=' + self.evaluation_cache_cs.string_representation(
                delimiter, indentation+1, indentation_symbol, '{', '}')  
        for i in range(0, indentation):
            s += indentation_symbol  
        s += group_end 
        return s

    @abstractmethod
    def __str__(self)->str:
        """
        String representation of the target solution instance

        :return: string representation of the target solution instance
        :rtype: str
        """
        return self.string_representation('|')

    @abstractmethod
    def __repr__(self)->str:
        """
        Representation of the target solution instance

        :return: string representation of the target solution instance
        :rtype: str
        """
        return self.string_representation('\n')

    @abstractmethod
    def __format__(self, spec:str)->str:
        """
        Formatted the target solution instance

        :param spec: str -- format specification
        :return: formatted target solution instance
        :rtype: str
        """
        return self.string_representation('|')

