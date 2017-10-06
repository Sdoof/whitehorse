javac -verbose -cp "." common/Java_Config.java common/IQFeed_Socket.java HistorySocket/HistorySocket.java -d HistorySocket/classes
java -cp "HistorySocket/classes" HistorySocket
