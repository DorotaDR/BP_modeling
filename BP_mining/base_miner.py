import bpmn_python.bpmn_diagram_visualizer as visualizer

from .log_wrapper import LogWrapper


class BaseMiner():
    def __init__(self, log_file_xes_path):
        self.log = LogWrapper(log_file_xes_path)
        self.TL = self.log.get_all_tasks()
        self.TI = self.log.get_first_tasks()
        self.TO = self.log.get_last_tasks()

        self.bpmn_graph = None

    def execute_algorithm(self):
        raise NotImplemented

    def is_task_next_connected(self, task_name):
        task_id = self._get_node_id_by_name(task_name)
        task_details = self.bpmn_graph.get_node_by_id(task_id)[1]
        if 'outgoing' in task_details and len(task_details['outgoing']) >= 1:
            return True
        else:
            return False

    def _get_node_id_by_name(self, name):
        nodes_list = self.bpmn_graph.get_nodes()
        node_id = None
        for node in nodes_list:
            try:
                if node[1]['node_name'] == name:
                    node_id = node[1]['id']
            except KeyError as e:
                pass
        return node_id

    def _add_sequence_flow_by_names(self, process_id, start_node_name, end_node_name, flow_name=" "):
        start_id = self._get_node_id_by_name(start_node_name)
        end_id = self._get_node_id_by_name(end_node_name)
        if self.bpmn_graph and start_id and end_id:  # if not None
            self.bpmn_graph.add_sequence_flow_to_diagram(process_id, start_id, end_id, flow_name)
        else:
            print("bpmn_graph or start_id={} or end_id={} is/are None".format(start_id, end_id))

    def save_to_png(self, filename="bpmn_graph.png"):
        visualizer.bpmn_diagram_to_png(self.bpmn_graph, file_name=filename)
