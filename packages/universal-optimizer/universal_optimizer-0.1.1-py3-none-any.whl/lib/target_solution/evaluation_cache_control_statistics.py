import path
import sys 

directory = path.Path(__file__).abspath()
sys.path.append(directory.parent)

class EvaluationCacheControlStatistics:
    """
    Class that represents control statistics for evaluation caching.
    """
    
    def __init__(self)->None:
        """
        Create new EvaluationCacheControlStatistics instance
        """
        self.__is_caching:bool = False
        self.__cache:dict[str] = {}
        self.__cache_hit_count:int = 0
        self.__cache_request_count:int = 0

    @property
    def is_caching(self)->bool:
        """
        Property getter for is_caching 
        :return: if caching is used during evaluation, or not 
        :rtype: bool
        """
        return self.__is_caching

    @is_caching.setter
    def is_caching(self, value:bool)->None:
        """
        Property setter for is_caching

        :param bool value: value for determining if caching is activated
        """
        self.__is_caching = value

    @property
    def cache(self)->dict[str]:
        """
        Property getter for cache 
        
        :return: cache that is used during evaluation 
        :rtype: dict[str]
        """
        return self.__cache

    @cache.setter
    def cache(self, value:dict[str])->None:
        """
        Property setter for cache

        :param dict[str] value: value for cache
        """
        self.__cache = value

    @property
    def cache_hit_count(self)->int:
        """
        Property getter for cache_hit_count 

        :return: number of cache hits during evaluation
        :rtype: int
        """
        return self.__cache_hit_count

    def increment_cache_hit_count(self)->None:
        """
        Increments number of cache hits during evaluation 
        """
        self.__cache_hit_count += 1

    @property
    def cache_request_count(self)->int:
        """
        Property getter for cache_request_count 

        :return: overall number of evaluations 
        :rtype: int
        """
        return self.__cache_request_count

    def increment_cache_request_count(self)->None:
        """
        Increments overall number of evaluations 
        """
        self.__cache_request_count += 1

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
        s += '__is_caching=' + str(self.__is_caching) + delimiter
        for i in range(0, indentation):
            s += indentation_symbol      
        s += '__cache_hit_count=' + str(self.__cache_hit_count) + delimiter
        for i in range(0, indentation):
            s += indentation_symbol      
        s += '__cache_request_count=' + str(self.__cache_request_count) + delimiter
        for i in range(0, indentation):
            s += indentation_symbol  
        s += group_end 
        return s
