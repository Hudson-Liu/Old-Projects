package euueuee;
import java.util.Scanner;
import java.lang.Math;

public class ueueueueue {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		/*
		Scanner sc = new Scanner(System.in);
		System.out.print("Speed: ");
	    int speed = sc.nextInt();
	    System.out.print("Theta: ");
	    int theta = sc.nextInt();
	    double rad = Math.toRadians(theta);
	    double V_h = speed*(Math.sin(rad));
	    double V_v = speed*(Math.cos(rad));
	    double w_1 = 0.25*(V_v-V_h)*Math.sqrt(2);
	    double w_2 = 0.25*(V_v-V_h)*Math.sqrt(2);
	    double w_3 = 0.25*(V_h+V_v)*Math.sqrt(2);
	    double w_4 = 0.25*(V_h+V_v)*Math.sqrt(2);
	    System.out.println(String.valueOf(w_1) + " " + String.valueOf(w_2) + " " + String.valueOf(w_3) + " " + String.valueOf(w_4));
	    System.out.println(Math.sqrt(Math.pow(w_1+w_2, 2) + Math.pow(w_3+w_4, 2)));
	    */
		
		Scanner sc = new Scanner(System.in);
		System.out.print("Speed: ");
	    double speed = sc.nextDouble();
	    System.out.print("Theta: ");
	    int theta = sc.nextInt();
	    double rad = Math.toRadians(theta);
	    double V_h = speed*Math.sin(rad);
	    double V_v = speed*Math.cos(rad);
	    double w_1 = 0.5*(V_v-V_h)*Math.sqrt(2);
	    double w_2 = 0.5*(V_v-V_h)*Math.sqrt(2);
	    double w_3 = 0.5*(V_h+V_v)*Math.sqrt(2);
	    double w_4 = 0.5*(V_h+V_v)*Math.sqrt(2);
	    System.out.println(String.valueOf(w_1) + " " + String.valueOf(w_2) + " " + String.valueOf(w_3) + " " + String.valueOf(w_4));
	    System.out.println(Math.sqrt(Math.pow(w_1+w_2, 2) + Math.pow(w_3+w_4, 2)));
	}
}
