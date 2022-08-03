package application;

import java.io.FileNotFoundException;
import java.io.IOException;
import java.time.DateTimeException;
import java.util.Arrays;

import javafx.event.ActionEvent;
import javafx.scene.Group;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.TableColumn;
import javafx.scene.control.TableView;
import javafx.scene.control.TextField;
import javafx.scene.control.cell.PropertyValueFactory;
import javafx.scene.paint.Color;
import javafx.scene.text.Font;
import javafx.scene.text.FontPosture;
import javafx.scene.text.FontWeight;
import javafx.scene.text.Text;
import javafx.stage.Stage;

public class TeacherScene {
	TextField enterName, enterBirthdate, enterAge, enterSubject, 
	enterYearsOfTeaching, enterSearch, saveFilename, loadFilename,
	enterIndex;
	
	Text status, locatedIndex;
	
	Spreadsheet<Teacher> teachers = new Spreadsheet<Teacher>();
	
	TableView<Teacher> teacherTable;
	
	Stage globalStage;
	
	public TeacherScene(Stage globalStage) { //now this class has control over the stage
		this.globalStage = globalStage;
	}
	
	public Scene returnLayout(){
		Text title = new Text(460, 30, "Teacher Management System");
    	title.setFont(Font.font("Helvectica", FontWeight.BOLD, FontPosture.REGULAR, 20));
    	
		teacherTable = new TableView<Teacher>();
		
		teacherTable.setEditable(false);
		teacherTable.setLayoutX(0);
		teacherTable.setLayoutY(120);
		teacherTable.setMaxSize(800, 300);
		teacherTable.setMinSize(800, 300);
		
		TableColumn<Teacher, String> nameCol = new TableColumn<Teacher, String>("Name");
		TableColumn<Teacher, String> birthdateCol = new TableColumn<Teacher, String>("Birthdate");
		TableColumn<Teacher, Integer> ageCol = new TableColumn<Teacher, Integer>("Age");
		TableColumn<Teacher, String> subjectCol = new TableColumn<Teacher, String>("Subjects");
		TableColumn<Teacher, Integer> yearsOfTeachingCol = new TableColumn<Teacher, Integer>("Years Of Teaching");

		nameCol.setResizable(false);
		birthdateCol.setResizable(false);
		ageCol.setResizable(false);
		subjectCol.setResizable(false);
		yearsOfTeachingCol.setResizable(false);
		
		nameCol.setSortable(false);
		birthdateCol.setSortable(false);
		ageCol.setSortable(false);
		subjectCol.setSortable(false);
		yearsOfTeachingCol.setSortable(false);
		
		nameCol.setPrefWidth(200);
		birthdateCol.setPrefWidth(80);
		ageCol.setPrefWidth(80);
		subjectCol.setPrefWidth(320);
		yearsOfTeachingCol.setPrefWidth(119);
		
		teacherTable.getColumns().addAll(Arrays.asList(nameCol, birthdateCol, 
				ageCol, subjectCol, yearsOfTeachingCol));
		
		nameCol.setCellValueFactory(new PropertyValueFactory<>("name"));
		birthdateCol.setCellValueFactory(new PropertyValueFactory<>("birthday"));
		ageCol.setCellValueFactory(new PropertyValueFactory<>("age"));
		subjectCol.setCellValueFactory(new PropertyValueFactory<>("subject"));
		yearsOfTeachingCol.setCellValueFactory(new PropertyValueFactory<>("yearsOfTeaching"));
		
		teacherTable.setItems(teachers.getFaculty());
		
		Button addTeacher = new Button("Add Teacher");
    	addTeacher.setFont(Font.font("Helvectica", FontWeight.NORMAL, FontPosture.REGULAR, 15));
    	addTeacher.setLayoutX(850);
    	addTeacher.setLayoutY(50);
    	addTeacher.setPrefWidth(270);
    	addTeacher.setPrefHeight(50);
    	addTeacher.setOnAction(this::addTeacherFunc);
    	
    	Button saveList = new Button("Save List");
    	saveList.setFont(Font.font("Helvectica", FontWeight.NORMAL, FontPosture.REGULAR, 15));
    	saveList.setLayoutX(850);
    	saveList.setLayoutY(120);
    	saveList.setPrefWidth(100);
    	saveList.setPrefHeight(30);
    	saveList.setOnAction(this::saveListFunc);
    	
    	Button loadList = new Button("Load List");
    	loadList.setFont(Font.font("Helvectica", FontWeight.NORMAL, FontPosture.REGULAR, 15));
    	loadList.setLayoutX(850);
    	loadList.setLayoutY(170);
    	loadList.setPrefWidth(100);
    	loadList.setPrefHeight(30);
    	loadList.setOnAction(this::loadListFunc);
    	
    	Button sortList = new Button("Sort List");
    	sortList.setFont(Font.font("Helvectica", FontWeight.NORMAL, FontPosture.REGULAR, 15));
    	sortList.setLayoutX(850);
    	sortList.setLayoutY(220);
    	sortList.setPrefWidth(100);
    	sortList.setPrefHeight(30);
    	sortList.setOnAction(this::sortListFunc);
    	
    	Button searchList = new Button("Search List");
    	searchList.setFont(Font.font("Helvectica", FontWeight.NORMAL, FontPosture.REGULAR, 15));
    	searchList.setLayoutX(850);
    	searchList.setLayoutY(270);
    	searchList.setPrefWidth(100);
    	searchList.setPrefHeight(30);
    	searchList.setOnAction(this::searchListFunc);
    	
    	Button addAtIndex = new Button("Add At Index");
    	addAtIndex.setFont(Font.font("Helvectica", FontWeight.NORMAL, FontPosture.REGULAR, 13));
    	addAtIndex.setLayoutX(850);
    	addAtIndex.setLayoutY(320);
    	addAtIndex.setPrefWidth(100);
    	addAtIndex.setPrefHeight(30);
    	addAtIndex.setOnAction(this::addAtIndexFunc);
    	
    	Button removeAtIndex = new Button("Remove Index");
    	removeAtIndex.setFont(Font.font("Helvectica", FontWeight.NORMAL, FontPosture.REGULAR, 13));
    	removeAtIndex.setLayoutX(850);
    	removeAtIndex.setLayoutY(370);
    	removeAtIndex.setPrefWidth(100);
    	removeAtIndex.setPrefHeight(30);
    	removeAtIndex.setOnAction(this::removeAtIndexFunc);
    	
    	Button backButton = new Button("Return to Menu");
    	backButton.setFont(Font.font("Helvectica", FontWeight.NORMAL, FontPosture.REGULAR, 13));
    	backButton.setLayoutX(10);
    	backButton.setLayoutY(10);
    	backButton.setPrefWidth(150);
    	backButton.setPrefHeight(30);
    	backButton.setOnAction(this::backButtonFunc);
    	
    	enterName = new TextField("Enter Teacher's Name");
    	enterName.setFont(Font.font("Helvectica", FontWeight.NORMAL, FontPosture.REGULAR, 12));
        enterName.setLayoutX(0);
        enterName.setLayoutY(65);
    	
    	enterBirthdate = new TextField("Enter Teacher's Birthday");
    	enterBirthdate.setFont(Font.font("Helvectica", FontWeight.NORMAL, FontPosture.REGULAR, 12));
        enterBirthdate.setLayoutX(170);
        enterBirthdate.setLayoutY(65);
        
        enterAge = new TextField("Enter Teacher's Age");
    	enterAge.setFont(Font.font("Helvectica", FontWeight.NORMAL, FontPosture.REGULAR, 12));
        enterAge.setLayoutX(340);
        enterAge.setLayoutY(65);
        
        enterSubject = new TextField("Enter Teacher's Subject");
    	enterSubject.setFont(Font.font("Helvectica", FontWeight.NORMAL, FontPosture.REGULAR, 12));
        enterSubject.setLayoutX(510);
        enterSubject.setLayoutY(65);
        
        enterYearsOfTeaching = new TextField("Enter Years Of Teaching");
    	enterYearsOfTeaching.setFont(Font.font("Helvectica", FontWeight.NORMAL, FontPosture.REGULAR, 12));
        enterYearsOfTeaching.setLayoutX(680);
        enterYearsOfTeaching.setLayoutY(65);
		
        saveFilename = new TextField("Enter Filename to Save");
    	saveFilename.setFont(Font.font("Helvectica", FontWeight.NORMAL, FontPosture.REGULAR, 12));
        saveFilename.setLayoutX(970);
        saveFilename.setLayoutY(123);
        
        loadFilename = new TextField("Enter Filename to Load");
    	loadFilename.setFont(Font.font("Helvectica", FontWeight.NORMAL, FontPosture.REGULAR, 12));
        loadFilename.setLayoutX(970);
        loadFilename.setLayoutY(173);
        
        enterSearch = new TextField("Enter Name to Search");
    	enterSearch.setFont(Font.font("Helvectica", FontWeight.NORMAL, FontPosture.REGULAR, 12));
        enterSearch.setLayoutX(970);
        enterSearch.setLayoutY(263);
        
        locatedIndex = new Text(970, 303, "Located Index: ");
        locatedIndex.setFont(Font.font("Helvectica", FontWeight.NORMAL, FontPosture.REGULAR, 13));
        
        enterIndex = new TextField("Enter Index");
    	enterIndex.setFont(Font.font("Helvectica", FontWeight.NORMAL, FontPosture.REGULAR, 12));
        enterIndex.setLayoutX(970);
        enterIndex.setLayoutY(335);
        enterIndex.setMinHeight(50);
        
        status = new Text(780, 30, "");
        status.setFont(Font.font("Helvectica", FontWeight.NORMAL, FontPosture.REGULAR, 15));
        status.setStroke(Color.RED);
        
		Group root = new Group(teacherTable, addTeacher, enterName, enterBirthdate, 
				enterAge, enterSubject, enterYearsOfTeaching, status, title,
				sortList, searchList, enterSearch, saveList, loadList, saveFilename,
				loadFilename, addAtIndex, removeAtIndex, enterIndex, locatedIndex,
				backButton);
		
		Scene scene = new Scene(root,1150,450);
		
		return scene;
	}
	
	public void addTeacherFunc(ActionEvent event) {
		addTeacherGeneral(false);
    }
	
	public void saveListFunc(ActionEvent event){
		SpreadsheetIO ioSheet = new SpreadsheetIO();
		String filename = saveFilename.getText();
		try {
			ioSheet.<Teacher>saveFiles(filename, teachers.getFaculty());
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
	
	public void loadListFunc(ActionEvent event){
		SpreadsheetIO ioSheet = new SpreadsheetIO();
		String filename = loadFilename.getText();
		try {
			teachers = ioSheet.loadTeachers(filename);
			teacherTable.setItems(teachers.getFaculty());
		} catch (FileNotFoundException e) {
			status.setText("File Not Found");
			status.setX(940);
			status.setY(30);
			return;
		} catch (DatabaseFormattingException e) {
			status.setText("File Formatted Incorrectly; Check if file was altered");
			status.setX(810);
			status.setY(30);
			return;
		}
		status.setText("");
	}
	
	public void sortListFunc(ActionEvent event) {
		teachers.sort();
	}
	
	public void searchListFunc(ActionEvent event) {
		String name = enterSearch.getText();
		int index = teachers.search(name);
		if (index == -1) {
			locatedIndex.setText("Located Index: None");
		}
		else {
			locatedIndex.setText("Located Index: " + String.valueOf(index));
		}
	}
	
	public void addAtIndexFunc(ActionEvent event) {
		addTeacherGeneral(true);
	}
	
	private void addTeacherGeneral(boolean addAtIndex) {
		int age;
		try {
			age = Integer.parseInt(enterAge.getText());
		} catch (NumberFormatException e){
			status.setText("Invalid Age; Enter an integer");
			status.setX(880);
			status.setY(30);
			return;
		}
		
		int yearsOfTeaching;
		try {
			yearsOfTeaching = Integer.parseInt(enterYearsOfTeaching.getText());
		} catch (NumberFormatException e) {
			status.setText("Invalid Years Of Teacher; Enter an integer");
			status.setX(840);
			status.setY(30);
			return;
		}
		
		try {
			Teacher teacher = new Teacher(
					enterName.getText(),
					enterBirthdate.getText(),
					age,
					enterSubject.getText(),
					yearsOfTeaching);
			if (addAtIndex) {
				try {
					int index = Integer.parseInt(enterIndex.getText());
					teachers.addAtIndex(index, teacher);
				}
				catch (NumberFormatException e) {
					status.setText("Invalid Index; Enter an integer");
					status.setX(870);
					status.setY(30);
					return;
				}
				catch (IndexOutOfBoundsException e) {
					status.setText("Invalid Index; Out of bounds");
					status.setX(880);
					status.setY(30);
					return;
				}
			}
			else {
				teachers.add(teacher);
			}
		} catch (DateTimeException e){
			status.setText("Invalid Date Of Birth; Enter a date in mm/dd/yyyy \n\t\t\tformat, e.g. 06/02/1995");
			status.setX(810);
			status.setY(20);
			return;
		}
		status.setText("");
	}
	
	public void removeAtIndexFunc(ActionEvent event) {
		try {
			int index = Integer.parseInt(enterIndex.getText());
			teachers.removeAtIndex(index);
		} catch (NumberFormatException e){
			status.setText("Invalid Index; Enter an integer");
			status.setX(870);
			status.setY(30);
			return;
		} catch (IndexOutOfBoundsException e) {
			status.setText("Invalid Index; Out Of Bounds");
			status.setX(880);
			status.setY(30);
			return;
		}
		status.setText("");
	}
	
	public void backButtonFunc(ActionEvent event) {
		MenuScene menuSceneObj = new MenuScene(globalStage);
		Scene menuScene = menuSceneObj.returnLayout();
		globalStage.setScene(menuScene);
		globalStage.show();
	}
}
