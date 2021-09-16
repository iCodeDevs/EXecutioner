'''define Equal Metrics class'''

from .base import BaseMetrics


class Equal(BaseMetrics):
    '''a 0/1 metric, gives full score if equal'''

    def score(self, exp_output, recv_output):
        if exp_output.strip() == recv_output.strip():
            return 1
        return 0
