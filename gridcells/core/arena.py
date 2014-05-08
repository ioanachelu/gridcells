'''
.. currentmodule:: gridcells.core.arena

The :mod::`~gridcells.core.arena` module provides definitions for all possible
types of arenas in experiments.
'''
from abc import ABCMeta, abstractmethod

import numpy as np

from .common import Pair2D, Position2D

##############################################################################


class Arena(object):
    '''An abstract class for arenas.

    This class is an interface for obtaining discretisations of the arenas and
    masks when the shape is not rectangular.
    '''
    __metaclass__ = ABCMeta


    @abstractmethod
    def getDiscretisation(self):
        '''Obtain the discretisation of this arena.

        Returns
        =======
        d : gridcells.core.Pair2D
            A pair of x and y coordinates for the positions in the arena. Units
            are arbitrary.
        '''
        raise NotImplementedError()


    @abstractmethod
    def getMask(self):
        '''Return mask (a 2D ``np.ndarray``) of where the positions in the
        arena are valid.
        
        For isntance with a circular arena, all positions outside its radius
        are invalid.
        '''
        raise NotImplementedError()


class RectangularArena(Arena):
    '''A rectangular arena.

    Use :class:``~gridcells.core.RectangularArena`` when you need to work with
    rectangular arenas.

    .. note::
        
        The coordinate system in rectangular and derived arenas is centered at
        zero. Any other coordinates must be transformed to match it.
    '''
    def __init__(self, size, discretisation):
        self._sz = size
        self._q = discretisation

    def getDiscretisation(self):
        numX = self._sz.x / self._q.x + 1
        numY = self._sz.y / self._q.y + 1
        xedges = np.linspace(-self._sz.x/2., self._sz.x/2., numX)
        yedges = np.linspace(-self._sz.y/2., self._sz.y/2., numY)
        return Pair2D(xedges, yedges)

    def getMask(self):
        return None



class SquareArena(RectangularArena):
    '''A square arena.'''
    def __init__(self, size, discretisation):
        tmpSz = Pair2D(size, size)
        super(SquareArena, self).__init__(tmpSz, discretisation)
    

class CircularArena(SquareArena):
    '''A circular arena.'''
    def __init__(self, radius, discretisation):
        super(CircularArena, self).__init__(radius*2., discretisation)
        self.radius = radius

    def getMask(self):
        edges = self.getDiscretisation()
        X, Y = np.meshgrid(edges.x, edges.y)
        return np.sqrt(X**2 + Y**2) > self.radius

