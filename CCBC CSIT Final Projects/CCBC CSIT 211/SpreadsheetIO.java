package application;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.Scanner;

import javafx.collections.ObservableList;

public class SpreadsheetIO {
	public Spreadsheet<Teacher> loadTeachers(String filename) 
			throws FileNotFoundException, DatabaseFormattingException {
		Spreadsheet<Teacher> teacherSheet = new Spreadsheet<Teacher>();
		File file = new File(filename);
		Scanner scan = new Scanner(file);
		
		while (scan.hasNextLine()) {
			String line = scan.nextLine();
			String[] arguments = line.split(" ");
			if (arguments[0].equals("TEACHER")) { //verifies you aren't opening a student file by accident
				Teacher person = new Teacher(arguments[1].replace('_', ' '), arguments[2], 
						Integer.valueOf(arguments[3]), arguments[4].replace('_', ' '), Integer.valueOf(arguments[5]));
				teacherSheet.add(person);
			}
			else {
				scan.close();
				throw new DatabaseFormattingException("The file contents were formatted incorrectly");
			}
		}
		scan.close();
		return teacherSheet;
	}
	
	public Spreadsheet<Student> loadStudents(String filename)
			throws FileNotFoundException, DatabaseFormattingException {
		Spreadsheet<Student> studentSheet = new Spreadsheet<Student>();
		File file = new File(filename);
		Scanner scan = new Scanner(file);
		
		while (scan.hasNextLine()) {
			String line = scan.nextLine();
			String[] arguments = line.split(" ");
			if (arguments[0] == "STUDENT") {
				Student person = new Student(arguments[1], arguments[2], Integer.valueOf(arguments[3]), 
						stringToGrades(arguments[4]), Integer.valueOf(arguments[5]));
				studentSheet.add(person);
			}
			else {
				scan.close();
				throw new DatabaseFormattingException("The file contents were formatted incorrectly");
			}
		}
		scan.close();
		return studentSheet;
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
	
	public <T extends Person> void saveFiles(String filename, ObservableList<T> people) throws IOException {
		FileWriter fw = new FileWriter(filename);
		PrintWriter pw = new PrintWriter(fw);
		int counter = 0;
		for (Person person : people) {
			if (counter == people.size() - 1) { // no newline at end of file
				pw.print(person.toString());
			}
			else {
				pw.println(person.toString());
			}
			counter++;
		}
		pw.close();
	}
}
