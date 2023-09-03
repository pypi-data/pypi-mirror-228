from enum import Enum


class LoggerOutputEnum(Enum):
    """
    LoggerOutputEnum

    Attributes:
        CONSOLE
        MySQLDatabase
        Logz.io
    """
    Console = "Console"
    MySQLDatabase = "MySQLDatabase"
    Logzio = "Logz.io"