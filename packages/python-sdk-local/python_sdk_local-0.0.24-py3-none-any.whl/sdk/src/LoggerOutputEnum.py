from enum import Enum


class LoggerOutputEnum(Enum):
    """
    LoggerOutputEnum

    Attributes:
        CONSOLE
        MySQLDatabase
        Logzio
    """
    Console = "Console"
    MySQLDatabase = "MySQLDatabase"
    Logzio = "Logzio"