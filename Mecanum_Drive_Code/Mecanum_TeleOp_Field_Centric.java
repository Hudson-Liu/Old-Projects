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

import etts.UtilToggle.*;
import com.qualcomm.robotcore.util.ElapsedTime;
import org.firstinspires.ftc.robotcore.external.navigation.DistanceUnit;
import java.util.*;

@TeleOp(name="Mecanum_TeleOp_Field_Centric", group="Testing")
public class Mecanum_TeleOp_Field_Centric extends LinearOpMode {
    //CRServo bucket;    
    DcMotor m0, m1, m2, m3,m4; //, l0, c0, f0, f1
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
        m4 = hardwareMap.dcMotor.get("lift0");
        imu = hardwareMap.get(BNO055IMU.class, "imu"); 
        imu.initialize(parameters);
        
        /*
        l0 = hardwareMap.dcMotor.get("lift0");
        c0 = hardwareMap.dcMotor.get("c0");
        f0 = hardwareMap.dcMotor.get("f0");
        f1 = hardwareMap.dcMotor.get("f1");
        Rev2mDistanceSensor ds = hardwareMap.get(Rev2mDistanceSensor.class, "dist");
        
        bucket.setPower(0);
        
        while (!isStopRequested() && !imu.isGyroCalibrated())
        {
            sleep(50);
            idle();
        }
        
        */
      
        waitForStart();
        double rotateAngle = 0;
        double orientationAngle = 0;
        double joystickAngle = 0;
        double speed = 0;
        
        //double bucketPos = bucket.getPosition();        
        //double bucketPos = 0;
        //double flyWheelMulti = -1;
        //double lastFlyWheelMulti = flyWheelMulti;
        
        /*ElapsedTime stopwatch = new ElapsedTime(); //measure 0.1 sec between checks
        long currentTime = 0;
        double bucketPosMem = 0; //net movement of bucket
        boolean bucketMoving = false; //tells iterator2 to run
        int threshold2 = 0; //too lazy to give a proper name
        int iterator2 = 0; //i sincerely apologize if you're trying to read this code
        double carouselSpeed = 0;
        */
        
        /*
        Gamepad 1 (driving):
            right trigger- move foward
            left trigger- move backwards
            left stick x- rotate left/right
            right stick x- move left/right
            b- move foward (max power)
            a- move backward (max power)
        
        Gamepad 2 (accesories):
            y- lift down
            x- lift up
            dpad up- carousel foward
            dpad down- carousel backward
            dpad left- fly wheel foward
            dpad right- fly wheel backward
            right trigger- bucket foward
            left trigger- bucket backward
            
            ??????- tilts bucket a few degrees
            a- returns the bucket to zero degrees
        */
        
        //UtilToggle utB2 = new UtilToggle();
        
        while (opModeIsActive())
        {
            // init values
            this.setMovement(0.0, 0.0, 0.0);
            //c0.setPower(0);
            
            //stopwatches for 1 second
            //currentTime = stopwatch.time() % 100;
            if(gamepad1.a==true){
                m4.setPower(-10);
            }
            else if (gamepad1.b == true){
                m4.setPower(10);
            }
            else{
                m4.setPower(0);
            }
            
            // gamepad 1
            telemetry.addData("ls", gamepad1.left_stick_x);
            telemetry.addData("rs", gamepad1.left_stick_y);
            telemetry.addData("l2", gamepad1.right_stick_x);
            telemetry.addData("m3", t4);
            telemetry.update();
          
            //field centric shit
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
            /*else {
                telemetry.addData("1", "I don't know what you did or how you did this, but I hate you");
            }*/
            
            speed = Math.sqrt(Math.pow(gamepad1.left_stick_y, 2) + Math.pow(gamepad1.left_stick_x, 2));
            this.setMovement(speed, rotateAngle, gamepad1.right_stick_x);
            
            // gamepad 2
            
            // lift movement
            /*
            if (gamepad2.y) l0.setPower(-0.35);
            else if (gamepad2.x) l0.setPower(0.35);
            else l0.setPower(0);
            
            // bucket
            bucketPos = 0;
            if (!bucketMoving) {
                if (gamepad2.right_trigger > 0) {
                    bucketPos = gamepad2.right_trigger;
                }
                
                else if (gamepad2.left_trigger > 0){
                    bucketPos = -gamepad2.left_trigger;
                }
                
                if (gamepad2.left_bumper) {
                    bucketPos -= 0.1;
                }
                
                if (gamepad2.right_bumper) {
                    bucketPos += 0.1;
                }
                
                /*if (currentTime <= 10 && currentTime - prevTime >= 10) { //if at least 0.09-0.1 seconds have passed
                    prevTime = currentTime;
                    bucketPosMem += bucketPos;
                }
            }
            
            if (utB2.status(gamepad2.b) == UtilToggle.Status.COMPLETE) {
                if (flyWheelMulti == 0) {
                    flyWheelMulti = lastFlyWheelMulti;
                } else {
                    lastFlyWheelMulti = flyWheelMulti;
                    flyWheelMulti = 0;
                }
            }
            
            bucket.setPower(bucketPos);
            
            // carousel direction
            if (gamepad2.dpad_up)
            {
                if (carouselSpeed < 0.5) carouselSpeed = 0.5;
                carouselSpeed += 0.01;
            }
            else if (gamepad2.dpad_down)
            {
                if (carouselSpeed > -0.5) carouselSpeed = -0.5;
                carouselSpeed -= 0.01;
            }
            else carouselSpeed = 0;
            c0.setPower(carouselSpeed);
            // flywheel direction
            if (gamepad2.dpad_left) flyWheelMulti = 0.75;
            if (gamepad2.dpad_right) flyWheelMulti = -1;
            */
            //right bumper
            
            // non-input things
            
            // update motor power
            m0.setPower(t1);
            m1.setPower(t2);
            m2.setPower(t3);
            m3.setPower(t4);
            
            //telemetry.addData("DS", ds.getDistance(DistanceUnit.CM));
            //telemetry.update();
            
            //f0.setPower((float) flyWheelMulti);
            //f1.setPower(-(float) flyWheelMulti);
            
            idle();
        }
    }
  
    private double findJoystickAngle(double V_v, double V_h){
        return Math.atan(V_v/V_h); 
    }
  
    private void setMovement(double speed, double theta, double r)
    {
        double rad = Math.toRadians(theta);
        double V_h = speed*Math.sin(rad);
        double V_v = speed*Math.cos(rad);
        double denominator = Math.max(Math.abs(V_v) + Math.abs(V_h) + Math.abs(r), 1);
        
        t1 = (-1*(V_v-V_h)-r)/denominator;//Back Left
        t2 = ((V_v-V_h)-r)/denominator;//Front Right
        t3 = (-1*(V_h+V_v)-r)/denominator;//Back Right
        t4 = ((V_h+V_v)-r)/denominator;//Front Left
    }
}
