package application;

@SuppressWarnings("serial")
public class DatabaseFormattingException extends Exception {
	public DatabaseFormattingException() {}
	
	public DatabaseFormattingException(String message) {
		super(message);
	}
}
