package application;

import javafx.collections.ObservableList;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.Scanner;

import javafx.collections.FXCollections;

public class Spreadsheet {
	private ObservableList<Teacher> teachers = FXCollections.observableArrayList();
	private ObservableList<Student> students = FXCollections.observableArrayList();
	
	public void sortTeachers() {
		teachers = this.<Teacher>bubbleSort(teachers);
	}
	
	public void sortStudents() {
		students = this.<Student>bubbleSort(students);
	}
	
	//Using a generic method + polymorphism lets us use the same function for both Teachers and Students
	private <T extends Person> ObservableList<T> bubbleSort(ObservableList<T> array) {
		int pass = 0;
		int num_swaps = -1;
		while (num_swaps != 0) {
			num_swaps = 0;
			for (int i = 0; i < array.size() - pass - 1; i++) { //-1 since there will always be 1 less pair than the number of elements
				T a = array.get(i);
				T b = array.get(i + 1);
				if (a.getName().compareTo(b.getName()) > 0) {
					array.set(i, b);
					array.set(i + 1, a);
					num_swaps++;
				}
			}
			pass++;
		}
		return array;
	}
	
	public int searchTeachers(String name) {
		int index = this.<Teacher>recursiveSearch(name, 0, teachers);
		return index;
	}
	
	public int searchStudents(String name) {
		int index = this.<Student>recursiveSearch(name, 0, students);
		return index;
	}
	
	private <T extends Person> int recursiveSearch(String name, int index, ObservableList<T> personList) {
		Person currentPerson = personList.get(index);
		if (currentPerson.getName() == name) {
			return index;
		}
		else if (index == personList.size()) {
			return -1;
		}
		else {
			return recursiveSearch(name, ++index, personList);
		}
	}
	
	public void loadFiles(Spreadsheet spreadsheet, String filename) throws FileNotFoundException, IOException {
		File file = new File(filename);
		Scanner scan = new Scanner(file);
		
		while (scan.hasNextLine()) {
			String line = scan.nextLine();
			String[] arguments = line.split(" ");
			if (arguments[0] == "STUDENT") {
				Student person = new Student(arguments[1], arguments[2], Integer.valueOf(arguments[3]), 
						stringToGrades(arguments[4]), Integer.valueOf(arguments[5]));
				students.add(person);
			}
			else if (arguments[0] == "TEACHER") {
				Teacher person = new Teacher(arguments[1], arguments[2], Integer.valueOf(arguments[3]), 
						arguments[4], Integer.valueOf(arguments[5]));
				teachers.add(person);
			}
			else {
				scan.close();
				throw new IOException("File format was incorrect");
			}
		}
		scan.close();
	}
	
	private int[] stringToGrades(String str) {
		String[] str_grades = str.split(",");
		final int GRADE_NUM = str_grades.length;
		
		int[] grades = new int[GRADE_NUM];
		for (int i = 0; i < GRADE_NUM; i++) {
			grades[i] = Integer.valueOf(str_grades[i]);
		}
		return grades;
	}
	
	public void saveFiles(String filename, ObservableList<Person> people) throws IOException {
		FileWriter fw = new FileWriter(filename);
		PrintWriter pw = new PrintWriter(fw);
		for (Person person : people) {
			pw.println(person.toString());
		}
		pw.close();
	}
	
	public void setTeachers(ObservableList<Teacher> teachers) {
		this.teachers = teachers;
	}
	
	public void setStudents(ObservableList<Student> students) {
		this.students = students;
	}
	
	public ObservableList<Teacher> getTeachers(){
		return teachers;
	}
	
	public ObservableList<Student> getStudents(){
		return students;
	}
	
	public void addTeacher(Teacher teacher) {
		teachers.add(teacher);
	}
	
	public void addTeacherAtIndex(int index, Teacher teacher) {
		teachers.add(index, teacher);
	}
	
	public void addStudent(Student student) {
		students.add(student);
	}
	
	public void addStudentAtIndex(int index, Student student) {
		students.add(index, student);
	}
}
