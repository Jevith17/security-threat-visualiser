

def event_to_features(event):
    
    window_duration = (
        event.window_end - event.window_start
    ).total_seconds()

    return [
        event.signal_count,
        event.total_reports,
        event.max_confidence,
        window_duration,
    ]
