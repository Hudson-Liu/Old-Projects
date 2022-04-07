package states.ducks;

import com.qualcomm.hardware.bosch.BNO055IMU;
import com.qualcomm.robotcore.eventloop.opmode.Autonomous;
import com.qualcomm.robotcore.hardware.CRServo;
import com.qualcomm.hardware.rev.Rev2mDistanceSensor;
import com.qualcomm.hardware.rev.RevColorSensorV3;

import org.firstinspires.ftc.robotcore.external.tfod.Recognition;
import org.firstinspires.ftc.robotcore.external.tfod.TFObjectDetector;
import org.firstinspires.ftc.robotcore.external.navigation.VuforiaLocalizer;
import org.firstinspires.ftc.robotcore.external.hardware.camera.WebcamName;
import org.firstinspires.ftc.robotcore.external.ClassFactory;
import org.firstinspires.ftc.robotcore.external.navigation.DistanceUnit;
import org.firstinspires.ftc.robotcore.external.navigation.AngleUnit;
import org.firstinspires.ftc.robotcore.external.navigation.AxesOrder;
import org.firstinspires.ftc.robotcore.external.navigation.AxesReference;
import org.firstinspires.ftc.robotcore.external.navigation.Orientation;

import java.util.List;
import java.util.ArrayList;

import com.qualcomm.robotcore.eventloop.opmode.LinearOpMode;
import com.qualcomm.robotcore.hardware.Servo;
import com.qualcomm.robotcore.hardware.DcMotor;

import states.Directions;
import states.ServoInstance;

@Autonomous(name = "ducks_blue", group = "auto_ducks")
public class Ducks_Blue extends LinearOpMode {
    BNO055IMU imu;
    @Override
    public void runOpMode() {
        /*
        3 parts:
        1. use camera to detect duck
        2. use distance sensor to align self with shipping hub
        3. use gyro to move in a 'straight' line until sensor gets close enough
         */

        telemetry.addData("Status", "Init");
        telemetry.update();

        Directions dir = initControls();
        Rev2mDistanceSensor ds = hardwareMap.get(Rev2mDistanceSensor.class, "dist");
        CRServo bucket = hardwareMap.crservo.get("bucket");
        DcMotor lift = hardwareMap.dcMotor.get("lift");
        
        RevColorSensorV3 color = hardwareMap.get(RevColorSensorV3.class, "color");

        BNO055IMU.Parameters para = new BNO055IMU.Parameters();
        para.mode = BNO055IMU.SensorMode.IMU;
        para.accelUnit = BNO055IMU.AccelUnit.METERS_PERSEC_PERSEC;
        imu = hardwareMap.get(BNO055IMU.class, "imu");
        imu.initialize(para);

        initVuforia();
        initTfod();
        tfod.activate();

        telemetry.addData("Status", "ready");
        telemetry.update();

        waitForStart();

        duckLocations location = findDuck();
        
        telemetry.addData("location", location);
        telemetry.update();
        
        double angle = -75;
        dir.pointTowardsDegree(angle);
        dir.update();
        sleep(2000);
        dir.setPower(0.25);
        dir.update();

        // try to keep heading at 0
        
        // Notes: Should it be currentAngle > 1, since our IMU might not be that acccurate - might get noise
        // 
        
        int counter = 0;
        long iT = System.currentTimeMillis();
        while (counter < 3) {
            if (location == duckLocations.bottom){
               if (ds.getDistance(DistanceUnit.CM) < 30 || color.getDistance(DistanceUnit.CM) < 10) {
                    counter++;
                } else {
                    counter = 0;
                } 
            }
            else{
                if (ds.getDistance(DistanceUnit.CM) < 25 || color.getDistance(DistanceUnit.CM) < 9) {
                    counter++;
                } else {
                    counter = 0;
                }
            }
            
            if (System.currentTimeMillis() - iT > 7250){
                telemetry.add("Failsafe activated ", counter);
            	break;
            }
        }
        dir.setPower(0);
        dir.update();
        
        
        // move foward slightly so that bucket is aligned
        dir.pointTowardsDegree(0);
        dir.update();
        sleep(1000);
        dir.setPower(0.3);
        dir.update();
        sleep(800);
        dir.setPower(0);
        dir.update();

        // place block in accordance to the level we detect the duck at
        // and yes it looks like this is bc i cant be fucked to figure out dicts/2d lists
        // lift time, bucket time
        Double[] bottom = new Double[] {10d, 500d};
        Double[] middle = new Double[] {130d, 500d};
        Double[] top = new Double[] {1250d, 500d};

        if (location == duckLocations.bottom) placeBlock(bottom, lift, bucket);
        else if (location == duckLocations.middle) placeBlock(middle, lift, bucket);
        else if (location == duckLocations.top) placeBlock(top, lift, bucket);
        
        //align robot to dodge ducks
        dir.pointTowardsDegree(-90);
        dir.update();
        sleep(500);
        dir.setPower(-0.5);
        dir.update();
        sleep(200);
        dir.setPower(0);
        dir.update();
        
        //drive into warehouse, avoid barrier corners
        dir.pointTowardsDegree(10);
        dir.update();
        sleep(1000);
        dir.setPower(-1);
        dir.update();
        sleep(1800);
        dir.setPower(0);
        dir.pointTowardsDegree(0);
        dir.update();
        
    }

    private void placeBlock(Double[] instructions, DcMotor lift, CRServo bucket) {
        
        //move bucket according to duck level
        lift.setPower(-1);
        sleep(instructions[0].longValue());
        lift.setPower(0);
        bucket.setPower(-1);
        sleep(instructions[1].longValue());
        bucket.setPower(0);
        
        // bring the bucket back
        sleep(500);
        bucket.setPower(0.5);
        sleep(600);
        bucket.setPower(0);
    }

    // copied from: https://stemrobotics.cs.pdx.edu/node/7265
    // note: may need to change axises (getAngle() and resetAngle())
    double globalAngle = 0;
    Orientation lastAngles;
    private double getAngle() {
        Orientation angles = imu.getAngularOrientation(AxesReference.INTRINSIC, AxesOrder.ZYX, AngleUnit.DEGREES);

        double deltaAngle = angles.firstAngle - lastAngles.firstAngle;

        if (deltaAngle < -180)
            deltaAngle += 360;
        else if (deltaAngle > 180)
            deltaAngle -= 360;

        globalAngle += deltaAngle;

        lastAngles = angles;

        return globalAngle;
    }

    private double checkDirection() {
        double correction, angle, gain = .05;

        angle = getAngle();

        if (angle == 0) correction = 0;
        else correction = -angle;

        return correction *= gain;
    }

    private void resetAngle() {
        lastAngles = imu.getAngularOrientation(AxesReference.INTRINSIC, AxesOrder.ZYX, AngleUnit.DEGREES);
        globalAngle = 0;
    }

    private duckLocations findDuck() {
        int chance1 = 0;
        int chance2 = 0;
        int chance3 = 0;

        for (int i = 0; i < 20; i++)
        {
            List<Double> xPositions = requestDetection();

            if (xPositions.size() == 0) chance1++;
            else
            {
                for (double d : xPositions)
                {
                    if (d < 320) chance2++;
                    else chance3++;
                }
            }
            
            telemetry.addData("chance1", chance1);
            telemetry.addData("chance2", chance2);
            telemetry.addData("chance3", chance3);
            telemetry.update();

            sleep(75);
        }

        int m = Math.max(Math.max(chance1, chance2), chance3);
        if (m == chance1) return duckLocations.bottom;
        if (m == chance2) return duckLocations.middle;
        return duckLocations.top;
        /*
        int m = Math.max(chance1, chance2)
        if (m <=)
        */
    }

    private Directions initControls() {
        Servo[] servos = new Servo[] {
                hardwareMap.servo.get("s0"),
                hardwareMap.servo.get("s1"),
                hardwareMap.servo.get("s2"),
                hardwareMap.servo.get("s3")
        };

        Servo[] crservos = new Servo[] {
                hardwareMap.servo.get("crs0"),
                hardwareMap.servo.get("crs1"),
                hardwareMap.servo.get("crs2"),
                hardwareMap.servo.get("crs3")
        };

        DcMotor[] motors = new DcMotor[] {
                hardwareMap.dcMotor.get("m0"),
                hardwareMap.dcMotor.get("m1"),
                hardwareMap.dcMotor.get("m2"),
                hardwareMap.dcMotor.get("m3")
        };

        ServoInstance[] ss = new ServoInstance[4];
        for (int i = 0; i < 4; i++) {
            ss[i] = new ServoInstance(servos[i], crservos[i], motors[i]);
        }

        return new Directions(ss[0], ss[1], ss[2], ss[3]);
    }

    private VuforiaLocalizer vuforia;
    private TFObjectDetector tfod;

    private List<Double> requestDetection() {
        if (tfod == null)
        {
            telemetry.addData("Warning: ", "No TFOD found");
            telemetry.update();
        }
        else
        {
            List<Recognition> updatedRecognitions = tfod.getUpdatedRecognitions();
            if (updatedRecognitions != null) {
                List<Double> xPositions = new ArrayList<Double>();

                for (Recognition recognition : updatedRecognitions) {
                    String label = recognition.getLabel();
                    if (label == "Duck")
                    {
                        double averageX = (recognition.getLeft() + recognition.getRight()) / 2.0;
                        //telemetry.addData(String.format("Object %d", averageX), averageX);
                        xPositions.add(averageX);
                    }
                }

                return xPositions;
            }
        }
        return new ArrayList<Double>();
    }

    private void initVuforia() {
        VuforiaLocalizer.Parameters parameters = new VuforiaLocalizer.Parameters();
        parameters.vuforiaLicenseKey = "Adq5D4D/////AAABmdNuUlCksEmesm6DbxOCepVdMIfOfzEaLwYIkUpxQXhRLKA4Kc7Ys9882FOJ8FY8B+pKfDKiQTFywVFMvzIWT2eHpWXd3coJo7TSrUcJsuuyKBzbpTOmEsEdwDBjngfjYuvHWv1hk7b7eqDjg+XHGnZb7pXjrvQsBlFPxG7HgeUDjG3vv/W2IjW6/WEP7x0+T3exI3moU+J8h81KB+qKtfbnhk4AZaxRgdtNfIzmC4jCy+u76UN9hYYYAGztPpT81M4oeoEp7k7sj3EAepia3Etqt2nkTUZX3TJtTlSNHHajc14ZV1B7eXVeIJE5mSL3GDwgnGQzrlsNaB05XWKoKzb1zpQ5qTwit56adFdLCKy7";
        parameters.cameraName = hardwareMap.get(WebcamName.class, "Webcam 1");
        vuforia = ClassFactory.getInstance().createVuforia(parameters);
    }

    private void initTfod() {
        String TFOD_MODEL_ASSET = "FreightFrenzy_BCDM.tflite";
        String[] LABELS = {
                "Ball",
                "Cube",
                "Duck",
                "Marker"
        };

        int tfodMonitorViewId = hardwareMap.appContext.getResources().getIdentifier(
                "tfodMonitorViewId", "id", hardwareMap.appContext.getPackageName());
        TFObjectDetector.Parameters tfodParameters = new TFObjectDetector.Parameters(tfodMonitorViewId);
        tfodParameters.minResultConfidence = 0.50f;
        tfodParameters.isModelTensorFlow2 = true;
        tfodParameters.inputSize = 640;
        tfod = ClassFactory.getInstance().createTFObjectDetector(tfodParameters, vuforia);
        tfod.setZoom(1, 16.0/9.0);
        tfod.loadModelFromAsset(TFOD_MODEL_ASSET, LABELS);
    }

    enum duckLocations {
        bottom, middle, top
    }
}
