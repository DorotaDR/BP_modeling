from pm4py.objects.log.importer.xes import factory as xes_import_factory


class LogWrapper():
    def __init__(self, log_file_xes_path):

        self.log = xes_import_factory.apply(log_file_xes_path, parameters={"timestamp_sort": True})

    def get_all_tasks(self):
        """
        Returns set of all names of taks/events stored in log
        Return type: set
        """
        set_TL = set()
        for case in self.log:
            for event in case:
                set_TL.add(event["concept:name"])
        return set_TL

    def get_first_tasks(self):
        """
        Returns set of all names of first  tasks/events per case stored in log
        Return type: set
        """
        set_TI = set()
        [set_TI.add(case[0]["concept:name"]) for case in self.log]
        return set_TI

    def get_last_tasks(self):
        """
        Returns set of all names of last  tasks/events per case stored in log
        Return type: set
        """
        set_TO = set()
        [set_TO.add(case[-1]["concept:name"]) for case in self.log]
        return set_TO

    def show(self):
        for case_index, case in enumerate(self.log):
            print("\n case index: %d  case id: %s" % (case_index, case.attributes["concept:name"]))
            for event_index, event in enumerate(case):
                print("event index: %d  event activity: %s timestamp: %s" % (
                event_index, event["concept:name"], event["time:timestamp"].isoformat()))

    def to_list(self):
        log_list = []
        for case in self.log:
            case_str = ''
            for event in case:
                case_str = case_str + event["concept:name"]

            log_list.append(case_str)

        return log_list