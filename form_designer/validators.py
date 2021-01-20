import datetime

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _


phone_number_validator = RegexValidator(re.compile(r"^\+?\d[-\d\s]{7,13}$"), message=_("Invalid Phone Number"))


class EGN(str):
    """
    Object representing Bulgarian unique citizenship number (EGN)
    More details https://en.wikipedia.org/wiki/Unique_citizenship_number
    Information in Bulgarian for this can be found here
    http://www.grao.bg/esgraon.html#section2
    """

    def get_birth_date(self):
        """Extract persons birth date from EGN"""
        try:
            year, month, day = int(self[0:2]), int(self[2:4]), int(self[4:6])
        except (ValueError, TypeError):
            raise ValueError('First six characters must be numbers')

        if month >= 40:
            month -= 40
            year += 2000
        elif month >= 20:
            month -= 20
            year += 1800
        else:
            year += 1900

        return datetime.date(year, month, day)

    def _get_checksum(self):
        weights = (2, 4, 8, 5, 10, 9, 7, 3, 6)
        return sum(weight * int(digit) for weight, digit in zip(weights, self)) % 11 % 10

    def has_valid_checksum(self):
        """Check if the last digit is the same with the calculated checksum"""
        try:
            return int(self[-1]) == self._get_checksum()
        except ValueError:
            return False

    def is_valid(self):
        try:
            return bool(len(self) == 10 and self.has_valid_checksum() and self.get_birth_date())
        except ValueError:
            return False


def egn_validator(egn):
    egn = EGN(egn)
    if not egn.is_valid():
        raise ValidationError(_('Invalid EGN'))
    return egn


def eik_validator(eik):
    """
    Check Bulgarian EIK/BULSTAT codes for validity
    full information about algoritm is available here
    http://bulstat.registryagency.bg/About.html
    """
    error_message = _('EIK/BULSTAT is not valid')

    def get_checksum(weights, digits):
        checksum = sum([weight * digit for weight, digit in zip(weights, digits)])
        return checksum % 11

    def check_eik_base(eik):
        checksum = get_checksum(range(1, 9), eik)
        if checksum == 10:
            checksum = get_checksum(range(3, 11), eik)
        return eik[-1] == checksum % 10

    def check_eik_extra(eik):
        digits = eik[9:13]
        checksum = get_checksum([2, 7, 3, 5], digits)
        if checksum == 10:
            checksum = get_checksum([4, 9, 5, 7], digits)
        return digits[-1] == checksum % 10

    try:
        eik = list(map(int, eik))
    except ValueError:
        raise ValidationError(error_message)

    if not (len(eik) in [9, 13] and check_eik_base(eik)):
        raise ValidationError(error_message)

    if len(eik) == 13 and not check_eik_extra(eik):
        raise ValidationError(error_message)
