package application;

import javafx.event.ActionEvent;
import javafx.scene.Group;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.text.Font;
import javafx.scene.text.FontPosture;
import javafx.scene.text.FontWeight;
import javafx.scene.text.Text;
import javafx.stage.Stage;

public class MenuScene {
	Stage globalStage;
	
	public MenuScene(Stage globalStage) {
		this.globalStage = globalStage;
	}
	
	public Scene returnLayout() {
		globalStage.setTitle("School Account Management System");
		
		Text title = new Text(395, 30, "School Account Management System\n\t\t\t  Menu");
		title.setFont(Font.font("Helvectica", FontWeight.BOLD, FontPosture.REGULAR, 20));
		
		Button studentButton = new Button("Student Account Management");
		studentButton.setFont(Font.font("Helvectica", FontWeight.NORMAL, FontPosture.REGULAR, 15));
		studentButton.setLayoutX(440);
		studentButton.setLayoutY(100);
		studentButton.setPrefWidth(270);
		studentButton.setPrefHeight(50);
		studentButton.setOnAction(this::switchSceneStudent);
		
		Button teacherButton = new Button("Teacher Account Management");
		teacherButton.setFont(Font.font("Helvectica", FontWeight.NORMAL, FontPosture.REGULAR, 15));
		teacherButton.setLayoutX(440);
		teacherButton.setLayoutY(200);
		teacherButton.setPrefWidth(270);
		teacherButton.setPrefHeight(50);
		teacherButton.setOnAction(this::switchSceneTeacher);
		
		Group menu = new Group(title, studentButton, teacherButton);
		
		Scene menuScene = new Scene(menu,1150,450);
		
		return menuScene;
	}
	
	public void switchSceneStudent(ActionEvent event){
		StudentScene studentSceneObj = new StudentScene(globalStage);
		Scene studentScene = studentSceneObj.returnLayout();
		globalStage.setScene(studentScene);
		globalStage.show();
	}
	
	public void switchSceneTeacher(ActionEvent event){
		TeacherScene teacherSceneObj = new TeacherScene(globalStage);
		Scene teacherScene = teacherSceneObj.returnLayout();
		globalStage.setScene(teacherScene);
		globalStage.show();
	}
}
