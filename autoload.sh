while true
do
	../Software/mongodb-osx-x86_64-4.0.4/bin/mongoexport -h *.mlab.com:17834 -d billing -c custEventSource -u test -p * --type=csv --fields="_id,dateTimeConnect,dateTimeDisconnect,origNodeId,destNodeId,callingPartyNumber,originalCalledPartyNumber,callStatus,eventType" -o ../CDR_data/test_CDR.csv
	sleep 5
done
