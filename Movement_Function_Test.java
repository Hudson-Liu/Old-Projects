package ueueeu;

import java.util.Scanner;
import java.util.*;

public class aef {
	public static void main(String[] args) {
		
		//Takes Speed, Theta, and Rotation as arguments, used for Autonomous as it's easier to fine-tune (supposedly)
		Scanner sc = new Scanner(System.in);
		System.out.print("Speed: ");
	    	double speed = sc.nextDouble();
	    	System.out.print("Theta: ");
	    	int theta = sc.nextInt();
	    	System.out.print("Rotation: ");
	    	double r = sc.nextDouble();
	    
	    	double rad = Math.toRadians(theta);
	    	double V_h = speed*Math.sin(rad);
	    	double V_v = speed*Math.cos(rad);
	    	double denominator = Math.max(Math.abs(V_v) + Math.abs(V_h) + Math.abs(r), 1);
	    
	    	double t1 = (V_v-V_h+r)/denominator;//Back Left
	    	double t2 = (V_v-V_h-r)/denominator;//Front Right
	    	double t3 = (V_h+V_v-r)/denominator;//Back Right
	    	double t4 = (V_h+V_v+r)/denominator;//Front Left
	    
	    	System.out.println(String.valueOf(t1) + " " + String.valueOf(t2) + " " + String.valueOf(t3) + " " + String.valueOf(t4));
	    	System.out.println(String.valueOf(t1+t2+t3+t4));
		
		/*
		//Uses Horizontal Component and Vertical Components, will be used for Joystick control
		Scanner sc = new Scanner(System.in);

		System.out.print("Horizontal Component: ");
	    	double V_h = sc.nextDouble();
	    	System.out.print("Vertical Component: ");
	    	double V_v = sc.nextDouble();
	    	System.out.print("Rotation :");
	    	double r = sc.nextDouble();
	    	double denominator = Math.max(Math.abs(V_v) + Math.abs(V_h) + Math.abs(r), 1);
	    	double t1 = (V_v-V_h+r)/denominator;//Back Left
	    	double t2 = (V_v-V_h-r)/denominator;//Front Right
	    	double t3 = (V_h+V_v-r)/denominator;//Back Right
	    	double t4 = (V_h+V_v+r)/denominator;//Front Left
	    	System.out.println(String.valueOf(t1) + " " + String.valueOf(t2) + " " + String.valueOf(t3) + " " + String.valueOf(t4));
	    	System.out.println(String.valueOf(t1+t2+t3+t4));
	    	*/
	    
		/*
		//A straight-up broken script that's good for nothing
		Scanner sc = new Scanner(System.in);
		System.out.print("X: ");
	        double x = sc.nextDouble()*1.1;
	        System.out.print("Y: ");
	        double y = -1*sc.nextDouble();
	        System.out.print("Rotate: ");
	        double rx = sc.nextDouble();
		double w_1 = y + x + rx;
		double w_2 = y - x + rx;
		double w_3 = y - x - rx;
		double w_4 = y + x - rx;
		System.out.println(String.valueOf(w_1) + " " + String.valueOf(w_2) + " " + String.valueOf(w_3) + " " + String.valueOf(w_4));
		*/
	}
}
