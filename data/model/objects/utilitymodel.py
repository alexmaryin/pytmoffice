from .common_fields import HasImage, HasAnnualPaid
from .intelobject import IntelObject


class UtilityModel(HasAnnualPaid, HasImage, IntelObject):

    __mapper_args__ = {
        'polymorphic_identity': 4
    }
