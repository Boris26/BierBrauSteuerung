from aenum import enum, NoAlias

class ProcedureStates(enum):
    _settings_ = NoAlias
    HEAT_ON = "Aufheizen wurde gestartet"
    HEAT_OFF = "Aufheizen wurde beendet"
    RUNNING = "läuft"
    FINISHED = "wurde beendet"
    WAITING = "warten"
    BREAWINGFINISHED = "Fertig"

