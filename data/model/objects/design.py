from .common_fields import HasAnnualPaid, HasImage
from .intelobject import IntelObject


class Design(HasAnnualPaid, HasImage, IntelObject):

    __mapper_args__ = {
        'polymorphic_identity': 2
    }
