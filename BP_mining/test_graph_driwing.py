
import bpmn_python.bpmn_diagram_visualizer as visualizer
import bpmn_python.bpmn_diagram_rep as diagram



if __name__ == "__main__":


    bpmn_graph = diagram.BpmnDiagramGraph()
    bpmn_graph.create_new_diagram_graph(diagram_name="diagram1")
    process_id = bpmn_graph.add_process_to_diagram()
    [start_id, _] = bpmn_graph.add_start_event_to_diagram(process_id, start_event_name="start_event",
                                                          start_event_definition="timer")

    [task1_id, _] = bpmn_graph.add_task_to_diagram(process_id, task_name="task1")

    bpmn_graph.add_sequence_flow_to_diagram(process_id, start_id, task1_id, "start_to_one")

    [task2_id, _] = bpmn_graph.add_task_to_diagram(process_id, task_name="task2")

    [flow_id, _] = bpmn_graph.add_sequence_flow_to_diagram(process_id,
                                                           source_ref_id=task2_id,
                                                           target_ref_id=task1_id,
                                                           sequence_flow_name="two_to_one")

    visualizer.bpmn_diagram_to_png(bpmn_graph, "./../test_png/graph_incorrect")



