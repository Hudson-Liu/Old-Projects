package etts;

import com.qualcomm.robotcore.eventloop.opmode.LinearOpMode;
import com.qualcomm.hardware.rev.Rev2mDistanceSensor;
import com.qualcomm.robotcore.hardware.CRServo;
import com.qualcomm.robotcore.hardware.ColorSensor;
import com.qualcomm.robotcore.hardware.Servo;
import com.qualcomm.robotcore.util.Util;
import com.qualcomm.robotcore.eventloop.opmode.TeleOp;
import com.qualcomm.robotcore.hardware.DcMotor;
import com.qualcomm.robotcore.hardware.Gamepad;
import com.qualcomm.robotcore.hardware.DistanceSensor;
import etts.UtilToggle.*;
import com.qualcomm.robotcore.util.ElapsedTime;
import org.firstinspires.ftc.robotcore.external.navigation.DistanceUnit;


@TeleOp(name="Swerve", group="Testing")
public class Swerve extends LinearOpMode {
    Servo s0, s1, s2, s3;
    CRServo bucket;    
    DcMotor m0, m1, m2, m3, l0, c0, f0, f1;
    float t1, t2, t3, t4;
    
    
    @Override
    public void runOpMode()
    {
        telemetry.addData("Status", "Initialized");
        telemetry.update();
        
        s0 = hardwareMap.servo.get("s0");
        s1 = hardwareMap.servo.get("s1");
        s2 = hardwareMap.servo.get("s2");
        s3 = hardwareMap.servo.get("s3");
        bucket = hardwareMap.crservo.get("bucket");
        
        m0 = hardwareMap.dcMotor.get("motor0");
        m1 = hardwareMap.dcMotor.get("motor1");
        m2 = hardwareMap.dcMotor.get("motor2");
        m3 = hardwareMap.dcMotor.get("motor3");
        l0 = hardwareMap.dcMotor.get("lift0");
        c0 = hardwareMap.dcMotor.get("c0");
        f0 = hardwareMap.dcMotor.get("f0");
        f1 = hardwareMap.dcMotor.get("f1");
        Rev2mDistanceSensor ds = hardwareMap.get(Rev2mDistanceSensor.class, "dist");
        
        bucket.setPower(0);
        
        
        waitForStart();
        
        //double bucketPos = bucket.getPosition();        
        double bucketPos = 0;
        double flyWheelMulti = -1;
        double lastFlyWheelMulti = flyWheelMulti;
        
        ElapsedTime stopwatch = new ElapsedTime(); //measure 0.1 sec between checks
        long currentTime = 0;
        double bucketPosMem = 0; //net movement of bucket
        boolean bucketMoving = false; //tells iterator2 to run
        int threshold2 = 0; //too lazy to give a proper name
        int iterator2 = 0; //i sincerely apologize if you're trying to read this code
        double carouselSpeed = 0;
        
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
        
        UtilToggle utB2 = new UtilToggle();
        
        while (opModeIsActive())
        {
            // init values
            this.setPower(0);
            c0.setPower(0);
            
            //stopwatches for 1 second
            //currentTime = stopwatch.time() % 100;
            
            // gamepad 1
            
            // wheel direction
            if (gamepad1.left_stick_x != 0 && gamepad1.right_stick_x == 0) {
                this.setPos(0.5 * gamepad1.left_stick_x + 0.5, false);    
            }
            else if (gamepad1.left_stick_x == 0 && gamepad1.right_stick_x != 0) {
                this.setPos(0.5 * gamepad1.right_stick_x + 0.5, true);
            }
            else {
                this.setPos(0.5, false);
            }
            
            // driving
            if (gamepad1.right_trigger > 0) this.setPower(gamepad1.right_trigger);
            if (gamepad1.left_trigger > 0) this.setPower(-gamepad1.left_trigger);
            if (gamepad1.a) this.setPower(-10);
            if (gamepad1.b) this.setPower(10);
            
            
            // gamepad 2
            
            // lift movement
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
                }*/
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
            
            //right bumper
            
            // non-input things
            
            // update motor power
            m0.setPower(t1);
            m1.setPower(t2);
            m2.setPower(t3);
            m3.setPower(t4);
            
            telemetry.addData("DS", ds.getDistance(DistanceUnit.CM));
            telemetry.update();
            
            f0.setPower((float) flyWheelMulti);
            f1.setPower(-(float) flyWheelMulti);
            
            idle();
        }
    }
    
    private void setPower(float value)
    {
        t1 = -value;
        t2 = value;
        t3 = -value;
        t4 = value;
    }
    
    private void setPos(double value, boolean sameDir)
    {
        if (!sameDir) {
            double v = -1.0 * value + 1.0;
            s0.setPosition(value);
            s1.setPosition(value);
            s2.setPosition(v);
            s3.setPosition(v); 
        }
        else {
            s0.setPosition(value);
            s1.setPosition(value);
            s2.setPosition(value);
            s3.setPosition(value);
        }
    }
}package etts;

import com.qualcomm.robotcore.eventloop.opmode.LinearOpMode;
import com.qualcomm.hardware.rev.Rev2mDistanceSensor;
import com.qualcomm.robotcore.hardware.CRServo;
import com.qualcomm.robotcore.hardware.ColorSensor;
import com.qualcomm.robotcore.hardware.Servo;
import com.qualcomm.robotcore.util.Util;
import com.qualcomm.robotcore.eventloop.opmode.TeleOp;
import com.qualcomm.robotcore.hardware.DcMotor;
import com.qualcomm.robotcore.hardware.Gamepad;
import com.qualcomm.robotcore.hardware.DistanceSensor;
import etts.UtilToggle.*;
import com.qualcomm.robotcore.util.ElapsedTime;
import org.firstinspires.ftc.robotcore.external.navigation.DistanceUnit;


@TeleOp(name="Swerve", group="Testing")
public class Swerve extends LinearOpMode {
    Servo s0, s1, s2, s3;
    CRServo bucket;    
    DcMotor m0, m1, m2, m3, l0, c0, f0, f1;
    float t1, t2, t3, t4;
    
    
    @Override
    public void runOpMode()
    {
        telemetry.addData("Status", "Initialized");
        telemetry.update();
        
        s0 = hardwareMap.servo.get("s0");
        s1 = hardwareMap.servo.get("s1");
        s2 = hardwareMap.servo.get("s2");
        s3 = hardwareMap.servo.get("s3");
        bucket = hardwareMap.crservo.get("bucket");
        
        m0 = hardwareMap.dcMotor.get("motor0");
        m1 = hardwareMap.dcMotor.get("motor1");
        m2 = hardwareMap.dcMotor.get("motor2");
        m3 = hardwareMap.dcMotor.get("motor3");
        l0 = hardwareMap.dcMotor.get("lift0");
        c0 = hardwareMap.dcMotor.get("c0");
        f0 = hardwareMap.dcMotor.get("f0");
        f1 = hardwareMap.dcMotor.get("f1");
        Rev2mDistanceSensor ds = hardwareMap.get(Rev2mDistanceSensor.class, "dist");
        
        bucket.setPower(0);
        
        
        waitForStart();
        
        //double bucketPos = bucket.getPosition();        
        double bucketPos = 0;
        double flyWheelMulti = -1;
        double lastFlyWheelMulti = flyWheelMulti;
        
        ElapsedTime stopwatch = new ElapsedTime(); //measure 0.1 sec between checks
        long currentTime = 0;
        double bucketPosMem = 0; //net movement of bucket
        boolean bucketMoving = false; //tells iterator2 to run
        int threshold2 = 0; //too lazy to give a proper name
        int iterator2 = 0; //i sincerely apologize if you're trying to read this code
        double carouselSpeed = 0;
        
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
        
        UtilToggle utB2 = new UtilToggle();
        
        while (opModeIsActive())
        {
            // init values
            this.setMovement(0, 0, 0);
        	//this.setPower(0);
            c0.setPower(0);
            
            //stopwatches for 1 second
            //currentTime = stopwatch.time() % 100;
            
            // gamepad 1
            
            // wheel direction
            /*
            if (gamepad1.left_stick_x != 0 && gamepad1.right_stick_x == 0) {
                this.setPos(0.5 * gamepad1.left_stick_x + 0.5, false);    
            }
            else if (gamepad1.left_stick_x == 0 && gamepad1.right_stick_x != 0) {
                this.setPos(0.5 * gamepad1.right_stick_x + 0.5, true);
            }
            else {
                this.setPos(0.5, false);
            }
            
            // driving
            if (gamepad1.right_trigger > 0) this.setPower(gamepad1.right_trigger);
            if (gamepad1.left_trigger > 0) this.setPower(-gamepad1.left_trigger);
            if (gamepad1.a) this.setPower(-10);
            if (gamepad1.b) this.setPower(10);
            */
            this.setMovement(gamepad1.left_stick_x, gamepad1.left_stick_y, gamepad1.right_stick_x);
            
            // gamepad 2
            
            // lift movement
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
                }*/
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
            
            //right bumper
            
            // non-input things
            
            // update motor power
            m0.setPower(t1);
            m1.setPower(t2);
            m2.setPower(t3);
            m3.setPower(t4);
            
            telemetry.addData("DS", ds.getDistance(DistanceUnit.CM));
            telemetry.update();
            
            f0.setPower((float) flyWheelMulti);
            f1.setPower(-(float) flyWheelMulti);
            
            idle();
        }
    }
    
    private void setMovement(double V_v, double V_h, double r)
    {
    	double denominator = Math.max(Math.abs(V_v) + Math.abs(V_h) + Math.abs(r), 1);
    	t1 = (V_v-V_h+r)/denominator;//Back Left
	t2 = (V_v-V_h-r)/denominator;//Front Right
	t3 = (V_h+V_v-r)/denominator;//Back Right
	t4 = (V_h+V_v+r)/denominator;//Front Left
    }
}
