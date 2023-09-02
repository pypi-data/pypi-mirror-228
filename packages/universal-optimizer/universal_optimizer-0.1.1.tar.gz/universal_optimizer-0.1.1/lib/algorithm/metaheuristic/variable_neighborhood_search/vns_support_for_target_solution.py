import path
import sys
directory = path.Path(__file__).abspath()
sys.path.append(directory.parent.parent)

from abc import ABCMeta, abstractmethod

from target_problem.target_problem import TargetProblem

class VnsSupportForTargetSolution(metaclass=ABCMeta):
    
    @abstractmethod
    def vns_randomize(k:int, problem:TargetProblem, solution_codes:list[str])->bool:
        """
        Random VNS shaking of several parts such that new solution code does not differ more than supplied from all solution codes inside collection

        :param TargetProblem problem: problem that is solved
        :param int k:int parameter for VNS
        :param list[str] solution_codes: solution codes that should be randomized
        :return: if randomization is successful
        :rtype: bool
        """        
        raise NotImplemented

