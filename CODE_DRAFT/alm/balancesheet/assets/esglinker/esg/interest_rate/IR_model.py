## Python packages
from abc import ABCMeta, abstractmethod
    
class IR_model:
    """This class is the purely abstract class for all IR models we will implement in the future
    see https://pymotw.com/2/abc/"""

    __metaclass__=ABCMeta

    @abstractmethod
    def get_IR_curve(self):
        """This method returns IR term structures per time steps and trajectories"""
        return

    @abstractmethod
    def get_deflator(self):
        """This method returns deflators per time steps and trajectories"""
        return

    @abstractmethod
    def calibrate(self, asset_data):
        """Calibrate the IR model onto the market environment
            This method returns the IR_curve and deflator"""
        return