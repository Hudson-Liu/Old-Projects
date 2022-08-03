package application;

import java.lang.String;

public class Student extends Person{
	private int[] grades;
	private String gradesStr;
	private int yearsOfEducation;
	
	public Student(String name, String birthday, int age, int[] grades, int yearsOfEducation) {
		super(name, birthday, age);
		this.grades = grades; //acts purely as a check to make sure that the input is a valid list of grades
		this.gradesStr = gradesToString();
		this.yearsOfEducation = yearsOfEducation;
	}
	
	public int[] getGrades() {
		return grades;
	}
	
	public int getYearsOfEducation() {
		return yearsOfEducation;
	}
	
	public String getGradesStr() {
		return gradesStr;
	}
	
	public void setGrades(int[] grades) {
		this.grades = grades;
		this.gradesStr = gradesToString();
	}
	
	public void setGrade(int yearsOfEducation) {
		this.yearsOfEducation = yearsOfEducation;
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
				grades_str + " " + String.valueOf(yearsOfEducation);
	}
}
