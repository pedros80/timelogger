# TimeLogger - v1.0 Readme
[Peter Somerville](http://www.pedros-stuffs.com) - peterwsomerville@gmail.com

## License.
Standard MIT open source; see LICENSE.txt for more information

## Installation.
`python setup_logger.py` for more information

usage: `python setup_logger.py db_host db_user db_password`

## Usage.
Once installed run `python time_logger.py` to start application.
- New Task

    Type description of task into text field and press 'New Task'
- Start Logging Task

    Select desired task from list and press 'Start'
- Stop Logging Task

    Press 'Stop'
- View Time Logged On Task

    Select desired task from list and press 'Task Details'. 

    Press 'All Tasks' to exit Task Details mode.
- Remove Task From List

    Select desired task from list and press 'Remove Task'

## System Requirements.
[`python 2.x`](http://www.python.org), [`Tkinter`](https://wiki.python.org/moin/TkInter) and [`MySQLdb`](http://mysql-python.sourceforge.net/).


## Known Issues:
If task is started, it *MUST* be stopped before closing app or starting
new task otherwise time spent will not be stored. - Fixed in 1.0.1