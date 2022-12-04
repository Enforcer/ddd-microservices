class DomainException(Exception):
    pass


class NegotiationConcluded(DomainException):
    pass


class OnlyWaitingSideCanAccept(DomainException):
    pass


class OnlyWaitingSideCanCounteroffer(DomainException):
    pass


class OnlyParticipantsCanBreakOff(DomainException):
    pass
