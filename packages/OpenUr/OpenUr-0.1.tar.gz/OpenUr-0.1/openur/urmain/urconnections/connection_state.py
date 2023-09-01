__author__ = "Beck Isakov"
__copyright__ = "Copyright 2023, Beck Isakov, Japan"
__license__ = "GPL v3"

class ConnectionState:
    ERROR: int = 0
    DISCONNECTED: int = 1
    CONNECTED: int = 2
    PAUSED: int = 3
    STARTED: int = 4

    @staticmethod
    def change_connection_state(state: int):
        if state == ConnectionState.ERROR:
            return "ERROR"
        elif state == ConnectionState.DISCONNECTED:
            return "DISCONNECTED"
        elif state == ConnectionState.CONNECTED:
            return "CONNECTED"
        elif state == ConnectionState.PAUSED:
            return "PAUSED"
        elif state == ConnectionState.STARTED:
            return "STARTED"
        else:
            return "UNKNOWN"


# print(ConnectionState.change_connection_state(ConnectionState.ERROR))
