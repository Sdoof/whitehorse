javac -verbose -cp "../jars/postgresql-9.4-1202.jdbc42.jar:." common/FeedDB.java common/Java_Config.java  common/IQFeed_Socket.java Level1Socket/Level1Socket.java -d Level1Socket/classes
java -cp "../jars/postgresql-9.4-1202.jdbc42.jar:Level1Socket/classes" Level1Socket
