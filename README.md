# apprise-ratos-workaround
A "micro" service that sits between RatOS & Slack Workflows with a few extra features. This is a super overengineered solution created out of frustration but whatever, should work like this

## RatOS Events
### Valid events
started, complete, error, cancelled, paused, resumed

### Template variables
`{event_name}`
`{event_args[1].filename}`

### Example configuration
```
# moonraker.conf

[notifier arw]
url: json://localhost:8001/api/printer?-key=<your-key>
events: started,complete,error,cancelled,paused,resumed
title: {event_name}
body: '{event_args[1].filename}'
attach: http://127.0.0.1/webcam/?action=snapshot
```