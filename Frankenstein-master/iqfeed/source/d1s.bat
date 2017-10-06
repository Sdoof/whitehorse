javac -verbose -cp "..\jars\postgresql-42.0.0.jar;." common\FeedDB.java common\Java_Config.java  common\IQFeed_Socket.java  DBFeed\DBFeed.java  -d target
java -verbose -cp "..\jars\postgresql-42.0.0.jar;target" DBFeed
