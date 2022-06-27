package jp.jaxa.iss.kibo.rpc.defaultapk;


import org.opencv.core.Mat;

import gov.nasa.arc.astrobee.types.Point;
import gov.nasa.arc.astrobee.types.Quaternion;
import gov.nasa.arc.astrobee.Result;
import jp.jaxa.iss.kibo.rpc.api.KiboRpcService;
import org.opencv.calib3d.Calib3d;
import java.util.ArrayList;



import static org.opencv.core.Core.bitwise_and;
import static org.opencv.core.Core.inRange;

import static org.opencv.imgproc.Imgproc.*;


import org.opencv.core.Scalar;
import org.opencv.core.Size;



import static org.opencv.imgproc.Imgproc.COLOR_BGR2HSV;
import static org.opencv.imgproc.Imgproc.MORPH_RECT;

import static org.opencv.imgproc.Imgproc.cvtColor;
import static org.opencv.imgproc.Imgproc.erode;
import static org.opencv.imgproc.Imgproc.getStructuringElement;

/**
 * Class meant to handle commands from the Ground Data System and execute them in Astrobee
 */

public class YourService extends KiboRpcService {


    @Override

    protected void runPlan1() {
        //required line

        api.startMission();


        //min clearance is 22.6 cm or 0.226m since we know that side length for astrobee is
        //32 cm, so to find the radius of the square/astrobee, aka the dist from the corner, we can use
        //pythagorean theorem (we dont have to do 3d euclidian distance because z height doesnt matter)
        //note to self, KOZ 1 & 2 are swapped
        //point is the point for target 1 and quaternion is its corresponding quaternion
        //point 2 is target 2's og position
        Point point = new Point(10.71f, -7.5f-0.2725783682f, 4.48f);
        Quaternion quaternion = new Quaternion(0f, 0.7071068f, 0f, 0.7071068f);
        Point point2=new Point(11.2746f-0.0713120911f,-9.92284f, 5.29881f+0.1626665617f);
        Quaternion quaternion2=new Quaternion( 0f, 0f, -0.707f, 0.707f);

        //Run moveTo until the Astrobee reaches Point 1 and the proper orientation
        //looping for only the required amount of iterations should save a bit of time
        Result result = api.moveTo(point, quaternion, false);
        int counter = 0;
        while (!result.hasSucceeded() && counter < 10) {
            result = api.moveTo(point, quaternion, false);
            counter++;
        }

        // report point1 arrival
        api.reportPoint1Arrival();
        // get a camera image
        Mat image = api.getMatNavCam();
        //just an image for debugging
        api.saveMatImage(image,"URMOM.png");

        // irradiate the laser
        api.laserControl(true);

//         take target1 snapshot
        api.takeTarget1Snapshot();
//         turn the laser off
        api.laserControl(false);
        //Moves past KOZ's over to Point 2
        api.moveTo(new Point(11.1568f, -9.37369f, 4.4f), new Quaternion(0f,0.707f,0f,0.707f),false);

        //Perform Curve to avoid KOZ's
        //Moves to Point 2
        result = api.moveTo(point2, quaternion2, false);
        counter = 0;
        while (!result.hasSucceeded() && counter < 10) {
            result = api.moveTo(point2, quaternion2, false);
            counter++;
        }

        try
        {
            Thread.sleep(10000);
        }
        catch(InterruptedException ex)
        {
            Thread.currentThread().interrupt();
        }        /////////////////////////////////////////////////////////////////////////////////
        //ALL CODE UNTIL THE NEXT BAR OF SLASHES IS MY TARGET CODE. YOU DON'T HAVE TO CHANGE ANYTHING ABOUT THIS. PLEASE CONSULT
        //BEFORE CHANGING ANYTHING ABOUT THIS CODE
        //JUST A REVIEW. THIS FINDS THE UPPER AND LOWER BOUNDS OF THE CIRCLE THEN AVERAGES THE POSITIONS.
        /////////////////////////////////////////////////////////////////////////////////

        double[][] distortion = getNavCamIntrinsics();
        double[] matrix = distortion[0]
        double[] coefficients = distorion[1]
        Mat frameIn = api.getMatNavCam();
        Mat frameOut = new Mat();
        Calib3d.undistort(frameIn,frameout_undist,matrix,coefficients);

        Mat image2=new Mat();
        api.laserControl(true);
        Point point3=new Point();
        point3=point2;

        zmove=.01f*(s-453f)/9.548f;


        xmove = .01f*(a-735f)/9.548f;

        result = api.moveTo(new Point(point2.getX() + xmove, point2.getY(), point2.getZ() + zmove), quaternion2, false);
        counter = 0;
        while (!result.hasSucceeded() && counter < 6) {
            result = api.moveTo(new Point(point2.getX() + xmove, point2.getY(), point2.getZ() + zmove), quaternion2, false);
            counter++;
        }

        //[note to self/future hudson: use "getRobotKinematics" to account for navigation error]

        point2=new Point(point2.getX() + xmove, point2.getY(), point2.getZ() + zmove);
        api.saveMatImage(api.getMatNavCam(),Integer.toString(u)+".png");
        try
        {
            Thread.sleep(10000);
        }
        catch(InterruptedException ep)
        {
            Thread.currentThread().interrupt();
        }


//            api.moveTo(point2, quaternion2, false);
        api.saveMatImage(api.getMatNavCam(),"Target"+Integer.toString(u)+".png");



        api.takeTarget2Snapshot();

        api.laserControl(false);
        //Point point2=new Point(11.2746f,-9.92284f, 5.29881f);
        //DON'T FUCKING TOUCH THESE VALUES

        //move back to goal
        //api.moveTo(new Point(11.02245, -9.38369, 5.4),new Quaternion(0f, 0f, -0.707f, 0.707f),false);
        //api.moveTo(new Point(11.02614, -8.99422, 5.29947),new Quaternion(0f, 0f, -0.707f, 0.707f),false); //09:40:21.271

        api.moveTo(new Point(11, -9.2, 5.4),new Quaternion(0f, 0f, -0.707f, 0.707f),false); //09:40:21.271

        api.moveTo(new Point(11.27460, -7.89178, 4.96538),new Quaternion(0f, 0f, -0.707f, 0.707f),false); //09:40:21.499
        //offset +45 -13
//        /* ******************************************** */
//        /* write your own code and repair the air leak! */
//        /* ******************************************** */
//         send mission completion
        api.reportMissionCompletion();


    }
}
