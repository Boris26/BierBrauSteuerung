from aenum import Enum, NoAlias
class HeatingStates(Enum):
    _settings_ = NoAlias
    ON = True
    OFF = False
    SET = False



