from datetime import datetime, timedelta, timezone



class Relations():
    RIGHT_CAUSALITY='->'
    LEFT_CAUSALITY='<-'
    PARALLEL='||'
    NONE='#'


def xes_simple_generator(log_chains, log_filename: str):
    header = """<!-- Created by Me -->
        <!-- (c) 2020  -->
        <log xes.version="1.0" xmlns="http://code.deckfour.org/xes" xes.creator="">
        <extension name="Concept" prefix="concept" uri="http://code.deckfour.org/xes/concept.xesext"/>
        <extension name="Time" prefix="time" uri="http://code.deckfour.org/xes/time.xesext"/>
        <extension name="Organizational" prefix="org" uri="http://code.deckfour.org/xes/org.xesext"/>
        <global scope="trace">
        <string key="concept:name" value="name"/>
        </global>
        <global scope="event">
        <string key="concept:name" value="name"/>
        <date key="time:timestamp" value="2010-04-13T14:02:31.199+02:00"/>
        </global>"""
    trace_start = """<trace>
        <string key="concept:name" value="1"/>
        <string key="creator" value="Me"/>"""
    trace_end = "</trace>"
    event_template = """<event>
        <string key="concept:name" value="{name}"/>
        <date key="time:timestamp" value="{timestamp}"/>
        </event>"""


    log_str = header
    log_str = log_str + '\n'

    for (tr_id, trace) in enumerate(log_chains):
        log_str = log_str + '\n' + trace_start
        timestamp = datetime.now(tz=timezone.utc) - timedelta(weeks=tr_id)
        for (ev_id, event) in enumerate(trace):
            ev_timestamp = timestamp + timedelta(days=ev_id)
            log_str = log_str + '\n' + event_template.format(name=event, timestamp=ev_timestamp.isoformat())
        log_str = log_str + '\n' + trace_end

    log_str = log_str + '\n' + '</log>'

    with open(log_filename, 'w') as f:
        f.write(log_str)