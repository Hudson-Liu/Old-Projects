package etts;

import com.qualcomm.robotcore.eventloop.opmode.LinearOpMode;
import com.qualcomm.hardware.bosch.BNO055IMU;
import com.qualcomm.hardware.rev.Rev2mDistanceSensor;
import com.qualcomm.robotcore.hardware.CRServo;
import com.qualcomm.robotcore.hardware.ColorSensor;
import com.qualcomm.robotcore.hardware.Servo;
import com.qualcomm.robotcore.util.Util;
import com.qualcomm.robotcore.eventloop.opmode.TeleOp;
import com.qualcomm.robotcore.hardware.DcMotor;
import com.qualcomm.robotcore.hardware.Gamepad;
import com.qualcomm.robotcore.hardware.DistanceSensor;
import org.firstinspires.ftc.robotcore.external.navigation.AngleUnit;
import org.firstinspires.ftc.robotcore.external.navigation.AxesOrder;
import org.firstinspires.ftc.robotcore.external.navigation.AxesReference;
import org.firstinspires.ftc.robotcore.external.navigation.Orientation;
import org.firstinspires.ftc.robotcore.external.navigation.Position;
import org.firstinspires.ftc.robotcore.external.navigation.Velocity;

import com.qualcomm.robotcore.util.ElapsedTime;
import org.firstinspires.ftc.robotcore.external.navigation.DistanceUnit;
import java.util.*;

@TeleOp(name="Mecanum_TeleOp_Field_Centric", group="Testing")
public class Mecanum_TeleOp_Field_Centric extends LinearOpMode {
    //CRServo bucket;    
    DcMotor m0, m1, m2, m3;
    double t1, t2, t3, t4;
    BNO055IMU imu;
    
    @Override
    public void runOpMode()
    {
        telemetry.addData("Status", "Initialized");
        telemetry.update();
     
        //bucket = hardwareMap.crservo.get("bucket");
        //initialize gyro stuff
        BNO055IMU.Parameters parameters = new BNO055IMU.Parameters();
        parameters.angleUnit           = BNO055IMU.AngleUnit.DEGREES;
        parameters.accelUnit           = BNO055IMU.AccelUnit.METERS_PERSEC_PERSEC;
        parameters.calibrationDataFile = "BNO055IMUCalibration.json"; // see the calibration sample opmode
        parameters.loggingEnabled      = true;
        parameters.loggingTag          = "IMU";
        
        
        m0 = hardwareMap.dcMotor.get("motor0");
        m1 = hardwareMap.dcMotor.get("motor1");
        m2 = hardwareMap.dcMotor.get("motor2");
        m3 = hardwareMap.dcMotor.get("motor3");
        imu = hardwareMap.get(BNO055IMU.class, "imu"); 
        imu.initialize(parameters);
        
      
        waitForStart();
        double rotateAngle = 0;
        double orientationAngle = 0;
        double joystickAngle = 0;
        double speed = 0;
        
        while (opModeIsActive())
        {
            // init values
            this.setMovement(0.0, 0.0, 0.0);
            
            // gamepad 1
            telemetry.addData("ls", gamepad1.left_stick_x);
            telemetry.addData("rs", gamepad1.left_stick_y);
            telemetry.addData("l2", gamepad1.right_stick_x);
            telemetry.addData("m3", t4);
            telemetry.update();
          
            //field centric stuff
            Orientation orientation = imu.getAngularOrientation(AxesReference.INTRINSIC, AxesOrder.ZYX, AngleUnit.DEGREES);
            orientationAngle = orientation.firstAngle;
            telemetry.addData("Orientation: ", Double.toString(orientationAngle));
          
            joystickAngle = this.findJoystickAngle(gamepad1.left_stick_y, -1*gamepad1.left_stick_x);
            if (joystickAngle > orientationAngle){
                rotateAngle = joystickAngle - orientationAngle;
            }
            else if (orientationAngle > joystickAngle){
                rotateAngle = orientationAngle - joystickAngle;
            }
            else if (-1.0 * orientationAngle == joystickAngle){
                rotateAngle = joystickAngle - orientationAngle;
            }
            
            else {
                telemetry.addData("1", "I don't know what you did or how you did this, but I hate you");
            }
            
            speed = Math.sqrt(Math.pow(gamepad1.left_stick_y, 2) + Math.pow(gamepad1.left_stick_x, 2));
            this.setMovement(speed, rotateAngle, gamepad1.right_stick_x);
            
            // update motor power
            m0.setPower(t1);
            m1.setPower(t2);
            m2.setPower(t3);
            m3.setPower(t4);
            
            idle();
        }
    }
  
    private double findJoystickAngle(double V_v, double V_h){
        return Math.atan(V_v/V_h); 
    }
  
    private void setMovement(double speed, double rad, double r)
    {
        double V_h = speed*Math.sin(rad);
        double V_v = speed*Math.cos(rad);
        double denominator = Math.max(Math.abs(V_v) + Math.abs(V_h) + Math.abs(r), 1);
        
        t1 = (-1*(V_v-V_h)-r)/denominator;//Back Left
        t2 = ((V_v-V_h)-r)/denominator;//Front Right
        t3 = (-1*(V_h+V_v)-r)/denominator;//Back Right
        t4 = ((V_h+V_v)-r)/denominator;//Front Left
    }
}
