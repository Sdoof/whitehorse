import java.sql.DriverManager;
import java.sql.Connection;
import java.sql.SQLException;

public class FeedDB {
	String url = "jdbc:postgresql://localhost/tsdp?user=tsdp&password=93768145";
	Connection conn=null;
	
	private static FeedDB instance = null;
	
	public static FeedDB getInstance() {
	      if(instance == null) {
	         instance = new FeedDB();
	      }
	      return instance;
	}
	
	public static Connection getConnection() {
	      if(instance == null) {
	         instance = new FeedDB();
	      }
	      return instance.conn;
	}
	
	
	protected FeedDB() {
		try {

			Class.forName("org.postgresql.Driver");
			conn = DriverManager.getConnection(this.url);

		} catch (Exception e) {

			System.out.println("Where is your PostgreSQL JDBC Driver? "
					+ "Include in your library path!");
			e.printStackTrace();
			return;

		}
	}
	
}
