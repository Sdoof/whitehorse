javac -verbose -cp "." common/Java_Config.java  common/IQFeed_Socket.java Level1Socket/Level1Socket.java -d Level1Socket/classes
java -cp "Level1Socket/classes" Level1Socket
