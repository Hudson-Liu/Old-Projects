package application;

import java.time.DateTimeException;
import java.lang.String;

public class Person {
	private String name, birthday;
	private int age;
	
	public String toString() {
		return name.replace(' ', '_') + " " + birthday + " " + String.valueOf(age);
	}
	
	public Person(String name, String birthday, int age) {
		this.name = name;
		setBirthday(birthday);
		this.age = age;
	}
	
	public String getName() {
		return name;
	}
	
	public String getBirthday() {
		return birthday;
	}
	
	public int getAge() {
		return age;
	}
	
	public void setName(String name) {
		this.name = name;
	}
	
	public void setBirthday(String birthday) {
		if (birthday.charAt(2) != '/' ||
			birthday.charAt(5) != '/' ||
			birthday.length() > 10){
			throw new DateTimeException("The entered date was not in mm/dd/yyyy format.");
		}
		else {
			this.birthday = birthday;
		}
	}
	
	public void setAge(int age) {
		this.age = age;
	}
}
