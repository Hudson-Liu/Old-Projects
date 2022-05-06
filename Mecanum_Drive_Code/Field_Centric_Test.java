package aaaaaa;
import java.lang.Math;
public class ohaaa {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		double a = 0; //x
		double b = -0.2; //y
		double yes = 123;
		if (a <= 0 && b >= 0){
			System.out.print("left top quad");
			yes = -1*findJoystickAngle(b,a);
		}
		else if (a >= 0 && b >= 0){
			System.out.print("right top quad");
			yes = 180-findJoystickAngle(b,a);
		}
		else if (a >= 0 && b <= 0){
			System.out.print("right bottom quad");
			yes = 180+(-1*findJoystickAngle(b,a));
		}
		else {
			System.out.print("left bottom quad");
			yes = 360-findJoystickAngle(b,a);
		}
		System.out.println(yes);
		double t1 = 0;
		setMovement(1, 180, 0);
	}
	static double findJoystickAngle(double V_v, double V_h){
        return Math.toDegrees(Math.atan(V_v/V_h));
    }
	static void setMovement(double speed, double angle, double r)
    {
		double rad = Math.toRadians(angle);
		
        double V_h = speed*Math.sin(rad);
        double V_v = speed*Math.cos(rad);
        double denominator = Math.max(Math.abs(V_v) + Math.abs(V_h) + Math.abs(r), 1);
        
        double t1 = (-1*(V_v-V_h)-r)/denominator;//Back Left
        double t2 = ((V_v-V_h)-r)/denominator;//Front Right
        double t3 = (-1*(V_h+V_v)-r)/denominator;//Back Right
        double t4 = ((V_h+V_v)-r)/denominator;//Front Left
        
        System.out.println(t1);
        System.out.println(t2);
        System.out.println(t3);
        System.out.println(t4);
    }

}
