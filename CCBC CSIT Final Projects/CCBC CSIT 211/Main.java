package application;

import javafx.application.Application;
import javafx.stage.Stage;
import javafx.scene.Scene;

public class Main extends Application {
	Stage globalStage;
	
	@Override
	public void start(Stage primaryStage) throws Exception{
		globalStage = primaryStage;
		
		MenuScene menuSceneObj = new MenuScene(globalStage);
		Scene menuScene = menuSceneObj.returnLayout();
		
		globalStage.setScene(menuScene); //according to most documentation, passing around stage is the standard solution
		globalStage.show();
	}
	
	public static void main(String[] args) {
		launch(args);
	}
}
