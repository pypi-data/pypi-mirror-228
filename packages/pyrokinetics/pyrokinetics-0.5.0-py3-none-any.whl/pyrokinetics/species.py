import numpy as np

from .units import ureg as units


class Species:
    """
    Contains all species data as a function of psiN

    Charge
    Mass
    Density
    Temperature
    Rotation
    Omega

    Also need r/a (rho) as a function of psi for a/Lt etc.
    May need to add psi_toroidal
    """

    def __init__(
        self,
        species_type=None,
        charge=None,
        mass=None,
        dens=None,
        temp=None,
        rot=None,
        rho=None,
        ang=None,
    ):
        self.species_type = species_type
        self.charge = charge
        self.mass = mass
        self.dens = dens
        self.temp = temp
        self.rotation = rot
        self.omega = ang
        self.rho = rho

    def grad_rho(self, psi_n=None):
        if not hasattr(psi_n, "units"):
            psi_n *= units.dimensionless
        return self.rho(psi_n, derivative=1) if self.rho is not None else None

    def get_mass(self):
        return self.mass

    def get_charge(self, psi_n=None):
        if not hasattr(psi_n, "units"):
            psi_n *= units.dimensionless

        charge = self.charge(psi_n)

        if np.isclose(charge, np.rint(charge)):
            charge = np.rint(charge)

        return charge

    def get_dens(self, psi_n=None):
        if not hasattr(psi_n, "units"):
            psi_n *= units.dimensionless

        return self.dens(psi_n)

    def _norm_gradient(self, field, psi_n):
        r"""Calculate the normalised gradient of field at psi_n:

        .. math::
            -\frac{1}{f}\frac{\partial f}{\partial \rho}

        Parameters
        ----------
        field : InterpolatedUnivariateSpline
            The field to get the gradient of
        psi_n : number
            Normalised flux surface label

        Returns
        -------
        float
            Normalised gradient
        """
        if not hasattr(psi_n, "units"):
            psi_n *= units.dimensionless

        field_value = field(psi_n)
        gradient = field(psi_n, derivative=1)
        if np.isclose(field_value, 0.0):
            return 0.0 / units.lref_minor_radius
        return (-1.0 / field_value) * (gradient / self.grad_rho(psi_n))

    def get_norm_dens_gradient(self, psi_n=None):
        """
        - 1/n dn/rho
        """

        return self._norm_gradient(self.dens, psi_n)

    def get_temp(self, psi_n=None):
        if not hasattr(psi_n, "units"):
            psi_n *= units.dimensionless

        return self.temp(psi_n)

    def get_norm_temp_gradient(self, psi_n=None):
        """
        - 1/T dT/drho
        """

        return self._norm_gradient(self.temp, psi_n)

    def get_velocity(self, psi_n=None):
        if not hasattr(psi_n, "units"):
            psi_n *= units.dimensionless

        if self.rotation is not None:
            return self.rotation(psi_n)
        return 0.0 * units.meter / units.second

    def get_norm_vel_gradient(self, psi_n=None):
        """
        - 1/v dv/drho
        """

        if self.rotation is None:
            return 0.0 / units.lref_minor_radius

        return self._norm_gradient(self.rotation, psi_n)

    def get_angular_velocity(self, psi_n=None):
        if not hasattr(psi_n, "units"):
            psi_n *= units.dimensionless

        if self.omega is not None:
            return self.omega(psi_n)
        return 0.0 * units.vref_nrl / units.lref_minor_radius

    def get_norm_ang_vel_gradient(self, psi_n=None):
        """
        - 1/omega domega/drho
        """

        if self.omega is None:
            return 0.0 / units.lref_minor_radius

        return self._norm_gradient(self.omega, psi_n)
