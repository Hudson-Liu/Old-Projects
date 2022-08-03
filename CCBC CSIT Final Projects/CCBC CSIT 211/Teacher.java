package application;

public class Teacher extends Person{
	private String subject;
	private int yearsOfTeaching;
	
	public Teacher(String name, String birthday, int age, String subject, int yearsOfTeaching){
		super(name, birthday, age);
		this.subject = subject;
		this.yearsOfTeaching = yearsOfTeaching;
	}
	
	public String getSubject() {
		return subject;
	}
	
	public int getYearsOfTeaching() {
		return yearsOfTeaching;
	}
	
	public void setSubject(String subject) {
		this.subject = subject;
	}
	
	public void setYearsOfTeaching(int yearsOfTeaching) {
		this.yearsOfTeaching = yearsOfTeaching;
	}
	
	public String toString() {
		return "TEACHER" + " " + super.toString() + " " +
				subject.replace(' ', '_') + " " + String.valueOf(yearsOfTeaching);
	}
}
