apprise -vv -b "test.gcode" -t "started" -a ratos.png "json://localhost:8001/api/printer?-key=asdf1234"

sleep 2

apprise -vv -b "test.gcode" -t "complete" -a ratos.png "json://localhost:8001/api/printer?-key=asdf1234"

sleep 2

apprise -vv -b "test2.gcode" -t "started" -a ratos.png "json://localhost:8001/api/printer?-key=asdf1234"

sleep 2

apprise -vv -b "test2.gcode" -t "error" -a ratos.png "json://localhost:8001/api/printer?-key=asdf1234"
