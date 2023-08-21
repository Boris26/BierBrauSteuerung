from aenum import enum, NoAlias

class ProcedureTyps(enum):
    _settings_ = NoAlias
    MASHING_IN = "Einmaischen"
    MASHING_OUT = "Abmaischen"
    RAST = "Rast"
    COOKING = "Kochen"
