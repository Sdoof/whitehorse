javac -verbose -cp "../jars/postgresql-9.4-1202.jdbc42.jar:." common/FeedDB.java common/Java_Config.java  common/IQFeed_Socket.java DBFeed/DBFeed.java -d DBFeed/classes
java -cp "../jars/postgresql-9.4-1202.jdbc42.jar:DBFeed/classes" DBFeed
