class plasz_events:
    def __init__(self):
        self.event_handlers = {}

    def on(self, event_name):
        def decorator(handler):
            if event_name not in self.event_handlers:
                self.event_handlers[event_name] = []
            self.event_handlers[event_name].append(handler)
            return handler
        return decorator

    def trigger(self, event_name, *args, **kwargs):
        handlers = self.event_handlers.get(event_name, [])
        for handler in handlers:
            handler(*args, **kwargs)
            
