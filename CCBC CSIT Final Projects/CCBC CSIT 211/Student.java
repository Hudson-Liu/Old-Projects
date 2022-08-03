package application;

import java.lang.String;

public class Student extends Person{
	private int[] grades;
	private int grade;
	
	public Student(String name, String birthday, int age, int[] grades, int grade) {
		super(name, birthday, age);
		this.grades = grades;
		this.grade = grade;
	}
	
	public int[] getGrades() {
		return grades;
	}
	
	public int getGrade() {
		return grade;
	}
	
	public void setGrades(int[] grades) {
		this.grades = grades;
	}
	
	public void setGrade(int grade) {
		this.grade = grade;
	}
	
	/**
	 * The default list toString method includes spaces along with commas,
	 * but that makes it much more difficult to retrieve the data.
	 * @return
	 */
	private String gradesToString() {
		String grades_str = "";
		for (int val : grades) {
			grades_str = grades_str + String.valueOf(val) + ",";
		}
		grades_str = grades_str.substring(0, grades_str.length() - 1);
		return grades_str;
	}
	
	public String toString() {
		String grades_str = this.gradesToString();
		return "STUDENT" + " " + super.toString() + " " + 
				grades_str + " " + String.valueOf(grade);
	}
}
