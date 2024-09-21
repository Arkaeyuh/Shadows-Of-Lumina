class StateManager:
    def __init__(self):
        self.states = {}
        self.active_state = None

    def set_state(self, new_state):
        """Sets the active state of the game."""
        self.active_state = self.states.get(new_state)

    def add_state(self, state_name, state):
        """Adds a state to the manager."""
        self.states[state_name] = state

    def handle_events(self, event):
        """Delegates event handling to the active state."""
        if self.active_state:
            self.active_state.handle_events(event)

    def update(self, delta_time):
        """Updates the active state."""
        if self.active_state:
            self.active_state.update(delta_time)

    def render(self,screen):
        """Renders the active state."""
        if self.active_state:
            self.active_state.render(screen)