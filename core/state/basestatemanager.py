from helper import log_error

class BaseStateManager:
    _global_active_system_states = []
    _global_active_application_states = []
    _global_active_game_states = []
    _global_active_states = []

    def __init__(self, initial_state, allowed_transitions, log_fn=None, state_name="STATE",type="SYSTEM"):

        self.state = initial_state
        self.previous_state = None
        self.allowed_transitions = allowed_transitions
        self.log_fn = log_fn
        self.state_name = state_name
        self.type = type
        self.all_active_states = BaseStateManager._global_active_states
        self.active_system_states = BaseStateManager._global_active_system_states
        self.active_application_states = BaseStateManager._global_active_application_states
        self.active_game_states = BaseStateManager._global_active_game_states

        if self.type == "SYSTEM":
            if self.state not in self.active_system_states:
                self.active_system_states.append(self.state)
        if self.type == "APPLICATION":
            if self.state not in self.active_application_states:
                self.active_application_states.append(self.state)
        if self.type == "GAME":
            if self.state not in self.active_game_states:
                self.active_game_states.append(self.state)
        if self.state not in self.all_active_states:
            self.all_active_states.append(self.state)

    def set_state(self, new_state):
        if new_state == self.state:
            return

        if new_state not in self.allowed_transitions.get(self.state, []):
            log_error(f"{new_state} not in allowed transitions for {self.state}")
            return

        if self.log_fn:
            self.log_fn(self.state, new_state, self.state_name)

        self.previous_state = self.state
        self.state = new_state

        if self.type == "SYSTEM":
            if self.state not in self.active_system_states:
                self.active_system_states.append(self.state)
        if self.type == "APPLICATION":
            if self.state not in self.active_application_states:
                self.active_application_states.append(self.state)
        if self.type == "GAME":
            if self.state not in self.active_game_states:
                self.active_game_states.append(self.state)
        
        if self.state not in self.all_active_states:
            self.all_active_states.append(self.state)

        if self.previous_state != self.state:
            if self.previous_state in self.active_system_states:
                self.active_system_states.remove(self.previous_state)
            if self.previous_state in self.active_application_states:
                self.active_application_states.remove(self.previous_state)
            if self.previous_state in self.active_game_states:
                self.active_game_states.remove(self.previous_state)
            if self.previous_state in self.all_active_states:
                self.all_active_states.remove(self.previous_state)

    def revert_to_previous(self):
        if self.previous_state is not None:
            self.set_state(self.previous_state)

    def is_state(self, state):
        return self.state == state

    def get_previous_state(self):
        return f"{self.state_name}: {self.previous_state}"

    def get_state(self):
        return f"{self.state_name}: {self.state}"

    @classmethod
    def get_global_active_system_states(cls):
        return cls._global_active_system_states.copy()
    
    @classmethod
    def get_global_active_application_states(cls):
        return cls._global_active_application_states.copy()
    
    @classmethod
    def get_global_active_game_states(cls):
        return cls._global_active_game_states.copy()
    
    @classmethod
    def get_all_global_active_states(cls):
        return cls._global_active_states.copy()