from chordian._sse import parse_sse


def test_parse_basic_events():
    lines = [
        "event: progress",
        'data: {"n": 1}',
        "",
        "event: done",
        "data: bye",
        "",
    ]
    events = list(parse_sse(lines))
    assert len(events) == 2
    assert events[0].event == "progress"
    assert events[0].json == {"n": 1}
    assert events[1].event == "done"
    assert events[1].data == "bye"
    assert events[1].json is None  # not valid JSON


def test_multiline_data_is_joined():
    lines = ["data: line1", "data: line2", ""]
    events = list(parse_sse(lines))
    assert events[0].data == "line1\nline2"


def test_default_event_type_is_message():
    lines = ['data: {"x": 1}', ""]
    events = list(parse_sse(lines))
    assert events[0].event == "message"


def test_comments_and_trailing_event():
    lines = [": this is a comment", "event: tick", "data: 1"]  # no trailing blank line
    events = list(parse_sse(lines))
    assert len(events) == 1
    assert events[0].event == "tick"
    assert events[0].data == "1"
