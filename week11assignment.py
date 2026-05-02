class LogError(Exception):
    pass

from dataclasses import dataclass, field
@dataclass
class LogEntry:
    timestamp: str
    level: str
    message: str
    response_time: int
    _status: str = field(init=False, default="PENDING")

    def __post_init__(self):
        levels = ("INFO", "WARNING", "ERROR", "CRITICAL")
        if self.level not in levels:
            raise LogError(f"Unknown level: {self.level}")
        if self.response_time < 0:
            raise LogError("Negative response time")
        
    @property
    def is_slow(self):
        if self.response_time > 500:
            return True
        return False
    
    def __str__(self):
        return f"{self.timestamp} [{self.level}] {self.message} ({self.response_time}ms) -> {self._status}"
    
    def __gt__(self, other):
        return self.response_time > other.response_time
    

class LogScanner:
    def __init__(self, entries, max_ms):
        self.entries = entries
        self.max_ms = max_ms
        self.i = 0

    def __iter__(self):
        return self
    
    def __next__(self):
        if self.i >= len(self.entries):
            raise StopIteration
        
        entry =self.entries[self.i]
        self.i += 1
        if entry.response_time <= self.max_ms:
            entry._status = "OK"
        else:
            entry._status = "ALERT"
        
        return entry
    
def scan_report(scanner):
    ok = 0
    alert = 0

    for entry in scanner:
        if entry._status == "OK":
            ok += 1
        else:
            alert += 1

        yield str(entry)
    yield f"Result: {ok} ok, {alert} alerts"

from contextlib import contextmanager
@contextmanager
def monitoring_session(name):
    logs = []
    print(f"[START] {name}")
    try:
        yield logs
    except LogError as e:
        print(f"[FAIL] {e}")
    finally:
        print(f"[END] {name} ({len(logs)} entries)")





with monitoring_session("Web Server") as logs:
    logs.append(LogEntry("10:00:01", "INFO", "GET /home", 120))
    logs.append(LogEntry("10:00:02", "WARNING", "GET /api", 850))
    logs.append(LogEntry("10:00:03", "ERROR", "POST /login", 1500))

    for line in scan_report(LogScanner(logs, 1000)):
        print(line)

    print(logs[1] > logs[0])

print()

with monitoring_session("DB Server") as logs:
    logs.append(LogEntry("11:00:01", "DEBUG", "Query", 50))
