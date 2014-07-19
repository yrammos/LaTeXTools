#! /bin/bash
# cd " + self.caller.file_path + " && echo lat > .lytexerr.log && " + make_cmd_str + self.caller.file_name + " && echo ok > .lytexerr.log"

trap "echo 'STOPPED' > ~/.lytexstat.log" SIGHUP SIGINT SIGTERM EXIT

echo "$1"
echo "$2"
echo "$3"
echo "RUNNING" > ~/.lytexstat.log && cd "$1" && echo lil > ~/.lytexerr.log && lilypond-book -f latex --pdf "$3.lytex" && echo lat > .lytexerr.log && eval "$2 $3" && echo ok > .lytexerr.log && echo "STOPPED" > ~/.lytexstat.log
