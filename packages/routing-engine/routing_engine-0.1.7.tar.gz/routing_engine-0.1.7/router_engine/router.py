from . import rules_parser as parser
from . import rule_executor as executer
from . import rules_updater as updater
import threading

class routerClass:
    rules = None
    rules_file = None
    rules_json = None
    db_settings = None
    rules_source = ""
    rules_lock = threading.Lock()

    def __init__(self,file_path=None,rules_json=None,db_settings=None) -> None:
        if file_path is not None:
            self.load_rules_from_file(file_path)
            self.rules_source = "file"
        elif rules_json is not None:
                self.load_rules_from_json(rules_json)
                self.rules_source = "json"
        elif db_settings is not None:
            self.db_settings = db_settings
            self.load_rules_from_postgres()
            self.rules_source = "postgres_db"
        else:
            raise Exception("cannot initialize router, check rules")
        
    def activate_notification_rules_update(self):
        if (self.rules_source is not None) and self.rules_source == "postgres_db":
            t = threading.Thread(target=updater.activate_notification_rules_update, args=(self,))
            t.start()

    def load_rules_from_file(self,file_path):
        with self.rules_lock:
            self.rules = parser.load_rules_from_file(file_path)
            self.rules_file = file_path

    def load_rules_from_json(self,rules_json):
        with self.rules_lock:
            self.rules = parser.load_rules_from_json(json_data=rules_json)

    def load_rules_from_postgres(self):
        with self.rules_lock:
            self.rules = parser.load_rules_from_postgres(self.db_settings)
 

    def apply_rules(self,context, actions, **kwargs):
        with self.rules_lock:
            sorted_rules = sorted(self.rules, key=lambda r: -r['priority']) # Sorting by descending priority
        rules_status = {} 
        for rule in sorted_rules:
            if executer.evaluate_condition(rule['condition'], context):
                try:
                    # context will always be passed to the actions, so context is not needed in kwargs, and 'context' is reserved in kwargs
                    result,status = executer.execute_actions(rule['actions'],actions,context=context,**kwargs)
                    rules_status[str(rule)] = status
                    if not result is None:
                        return True,result,rule,rules_status # Return if action is successfully executed
                except executer.ExecutionFailed as e:
                    rules_status[str(rule)] = e
                    pass # Continue to the next rule if execution failed
            else:
                rules_status[str(rule)] = "rule doesn't apply"

        return False,None,None,rules_status # Return False if no rules were successfully executed
    












