package org.firstinspires.ftc.teamcode;

import com.qualcomm.robotcore.eventloop.opmode.Autonomous;
import com.qualcomm.robotcore.hardware.Servo;
import com.qualcomm.robotcore.eventloop.opmode.LinearOpMode;
import com.qualcomm.robotcore.hardware.DcMotor;
import java.util.*;

@Autonomous(name = "RedCarouselSideParking", group = "Testing")
public class RedCarouselSideParking extends LinearOpMode {
    DcMotor m0, m1, m2, m3;

    @Override
    public void runOpMode() {
        m0 = hardwareMap.dcMotor.get("motor0");
        m1 = hardwareMap.dcMotor.get("motor1");
        m2 = hardwareMap.dcMotor.get("motor2");
        m3 = hardwareMap.dcMotor.get("motor3");

        telemetry.addData("Status: ", "Ready to start");
        telemetry.update();

        waitForStart();

        setPos(0.3);

        sleep(2000);

        m0.setPower(1);
        m1.setPower(-1);
        m2.setPower(1);
        m3.setPower(-1);

        sleep(1400);

        m0.setPower(0);
        m1.setPower(0);
        m2.setPower(0);
        m3.setPower(0);
    }

    private void setMovement(double speed, double theta, double r)
    {
    	double rad = Math.toRadians(theta);
	double V_h = speed*Math.sin(rad);
	double V_v = speed*Math.cos(rad);
	double denominator = Math.max(Math.abs(V_v) + Math.abs(V_h) + Math.abs(r), 1);
	   
	m0.setPower((V_v-V_h+r)/denominator);//Back Left
	m1.setPower((V_v-V_h-r)/denominator);//Front Right
	m2.setPower((V_h+V_v-r)/denominator);//Back Right
	m3.setPower((V_h+V_v+r)/denominator);//Front Left
    }
}
