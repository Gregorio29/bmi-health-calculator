class SessionHistory:
    """Historial solo en memoria; nunca persiste datos entre sesiones."""
    def __init__(self): self._entries = []
    def add(self, entry): self._entries.append(dict(entry))
    def items(self): return list(self._entries)
    def latest(self): return self._entries[-1] if self._entries else None
    def clear(self): self._entries.clear()
