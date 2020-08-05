'''defines the base metrics class'''

class BaseMetrics:
    '''base class of Metrics'''
    def score(self, exp_output, recv_output):
        '''abstract score function to get score for given expected , recieved output'''
        raise NotImplementedError

    def __str__(self):
        return self.__class__.__name__
