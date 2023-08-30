#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy
from dataclasses import dataclass

from PyMieSim.binary.Fibonacci import FIBONACCI
from MPSPlots.Render3D import Scene3D


@dataclass
class FibonacciMesh():
    """
    Class wich represent an angular mesh. The distribution of points inside
    the mesh is similar to a Fibonacci sphere where each point cover an
    equivalent solid angle.
    """
    max_angle: float = 1.5
    """ Angle in radian defined by the numerical aperture of the imaging system. """
    sampling: int = 1000
    """Number of point distrubuted inside the Solid angle defined by the numerical aperture. """
    phi_offset: float = 0.
    """ Angle offset in the parallel direction of the polarization of incindent light. """
    gamma_offset: float = 0.
    """ Angle offset in the perpendicular direction of the polarization of incindent light. """

    def __post_init__(self):
        self.structured = False

        self._para = None
        self._perp = None

        self._parallel_vector_in_plan = None
        self._perpendicular_vector_in_plan = None

        self._vertical_to_perpendicular_vector = None
        self._horizontal_to_perpendicular_vector = None
        self._vertical_to_parallel_vector = None
        self._horizontal_to_parallel_vector = None

        self._phi = None
        self._theta = None

        self._plan = None

        self.vertical_vector = numpy.array([1, 0, 0])
        self.horizontal_vector = numpy.array([0, 1, 0])
        self.generate_ledvedev_mesh()

    @property
    def plan(self):
        if self._plan is None:
            self.cpp_binding.Computeplan()
            self._plan = numpy.asarray([self.cpp_binding.Xplan, self.cpp_binding.Yplan, self.cpp_binding.Zplan])

        return self._plan

    @property
    def perpendicular_vector(self):
        if self._perp is None:
            self.cpp_binding.compute_vector_field()

        return self.cpp_binding.perpVector

    @property
    def parallel_vector(self):
        if self._para is None:
            self.cpp_binding.compute_vector_field()

        return self.cpp_binding.paraVector

    @property
    def horizontal_to_perpendicular(self):
        if self._horizontal_to_perpendicular_vector is None:
            self.cpp_binding.compute_vector_field()

        return self.cpp_binding.horizontal_to_perpendicular_vector

    @property
    def horizontal_to_parallel(self):
        if self._horizontal_to_parallel_vector is None:
            self.cpp_binding.compute_vector_field()

        return self.cpp_binding.horizontal_to_parallel_vector

    @property
    def vertical_to_perpendicular(self):
        if self._vertical_to_perpendicular_vector is None:
            self.cpp_binding.compute_vector_field()

        return self.cpp_binding.perpVector

    @property
    def vertical_to_parallel(self):
        if self._vertical_to_parallel_vector is None:
            self.cpp_binding.compute_vector_field()

        return self.cpp_binding.paraVector

    @property
    def parallel_plan(self):
        if self._parallel_vector_in_plan is None:
            self.cpp_binding.compute_vector_field()

        return self.cpp_binding.paraVectorZplanar

    @property
    def perpendicular_plan(self):
        if self._perpendicular_vector_in_plan is None:
            self.cpp_binding.compute_vector_field()

        return self.cpp_binding.perpVectorZplanar

    def get_phi(self, unit: str = 'radian'):
        if unit.lower() in ['rad', 'radian']:
            return self.cpp_binding.phi

        elif unit.lower() in ['deg', 'degree']:
            return numpy.rad2deg(self.cpp_binding.phi)

    def get_theta(self, unit: str = 'radian'):
        if unit.lower() in ['rad', 'radian']:
            return self.cpp_binding.theta

        elif unit.lower() in ['deg', 'degree']:
            return numpy.rad2deg(self.cpp_binding.theta)

    @property
    def X(self):
        return self.cpp_binding.x

    @property
    def Y(self):
        return self.cpp_binding.y

    @property
    def Z(self):
        return self.cpp_binding.z

    def initialize_properties(self):
        self.cartesian_coordinates = numpy.c_[
            self.cpp_binding.x,
            self.cpp_binding.y,
            self.cpp_binding.z
        ].T

        self.d_omega_radian = self.cpp_binding.d_omega
        self.d_omega_degree = self.cpp_binding.d_omega * (180 / numpy.pi)**2

        self.omega_radian = self.cpp_binding.omega
        self.omega_degree = self.cpp_binding.omega * (180 / numpy.pi)**2

    def projection_HV_vector(self) -> tuple:
        parallel_projection = [
            self.projection_on_base_vector(
                Vector=self.vertical_to_parallel_plan,
                BaseVector=X
            ) for X in [self.vertical_vector, self.horizontal_vector]
        ]

        perpendicular_projection = [
            self.projection_on_base_vector(
                Vector=self.vertical_to_perpendicular_plan,
                BaseVector=X
            ) for X in [self.vertical_vector, self.horizontal_vector]
        ]

        return numpy.array(parallel_projection), numpy.array(perpendicular_projection)

    def projection_HV_scalar(self) -> tuple:
        parallel_projection = [
            self.projection_on_base_scalar(
                Vector=self.vertical_to_perpendicular_in_z_plan,
                BaseVector=X
            ) for X in [self.vertical_vector, self.horizontal_vector]
        ]

        perpendicular_projection = [
            self.projection_on_base_scalar(
                Vector=self.vertical_to_perpendicular_in_z_plan,
                BaseVector=X
            ) for X in [self.vertical_vector, self.horizontal_vector]
        ]

        return numpy.array(parallel_projection), numpy.array(perpendicular_projection)

    def projection_on_base_scalar(self, vector: numpy.ndarray, base_vector: numpy.ndarray) -> numpy.ndarray:
        return vector.dot(base_vector)

    def projection_on_base_vector(self, vector: numpy.ndarray, base_vector: numpy.ndarray) -> numpy.ndarray:
        projection = self.projection_on_base_scalar(vector, base_vector)

        base_projection = numpy.outer(projection, base_vector)

        return base_projection

    def plot(self) -> None:
        figure = Scene3D(shape=(1, 1))
        self._add_mesh_to_ax_(figure=figure, plot_number=(0, 0))

        return figure

    def _add_mesh_to_ax_(self, figure, plot_number: tuple) -> None:
        coordinates = numpy.c_[self.X, self.Y, self.Z]

        figure.add_unstructured_mesh(
            plot_number=plot_number,
            coordinates=coordinates,
        )

        figure.add_unit_sphere_to_ax(plot_number=plot_number)
        figure.add_unit_axes_to_ax(plot_number=plot_number)
        figure.add_theta_vector_field(plot_number=plot_number, radius=1.1)
        figure.add_phi_vector_field(plot_number=plot_number, radius=1.1)

    def generate_ledvedev_mesh(self) -> None:
        self.cpp_binding = FIBONACCI(
            self.sampling,
            self.max_angle,
            numpy.deg2rad(self.phi_offset),
            numpy.deg2rad(self.gamma_offset)
        )

        self.initialize_properties()

# -
