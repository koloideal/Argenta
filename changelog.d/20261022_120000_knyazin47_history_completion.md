### Fixed

- History completion uses the prompt's loaded history instead of rereading
  the history file on every request. Suggestions update as background loading
  progresses and when commands are added during the session. Candidate caches
  also refresh when a history snapshot changes without growing.
