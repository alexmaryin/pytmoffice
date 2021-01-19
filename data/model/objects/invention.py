from .common_fields import HasAnnualPaid
from .intelobject import IntelObject


class Invention(HasAnnualPaid, IntelObject):

    __mapper_args__ = {
        'polymorphic_identity': 1
    }
