package jp.jaxa.iss.kibo.rpc.defaultapk;


import org.opencv.core.Mat;

import gov.nasa.arc.astrobee.types.Point;
import gov.nasa.arc.astrobee.types.Quaternion;
import gov.nasa.arc.astrobee.Result;
import jp.jaxa.iss.kibo.rpc.api.KiboRpcService;

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
        api.moveTo(new Point(11.27f, -8.5f, 4.4f),new Quaternion(0f,0.707f,0f,0.707f),false);
        api.moveTo(new Point(11.27f,-10f,4.4f),new Quaternion(0f,0.707f,0f,0.707f),false);

        //Perform Curve to avoid KOZ's
        //Moves to Point 2
        Result result = api.moveTo(point2, quaternion2, false);
        int counter = 0;
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



        Mat image2=new Mat();
        api.laserControl(true);
        Point point3=new Point();
        point3=point2;
        //x->
        //z|
        float zmove=0f;
        float xmove=0f;
        int q=0;
        int a=0;
        int s=0;
        int g=0;

        for (int u=0;u<5;u++) {

            q=0;

//            while(Math.abs(453-s)>5 && Math.abs(735-a)>5) {

            Mat frame = api.getMatNavCam();

            cvtColor(frame,frame,COLOR_GRAY2BGR);

            double xsize = frame.size().width;
            double ysize = frame.size().height;


            Mat hsv_frame = new Mat();
//        Clock clock = Clock.systemDefaultZone();
//        long smilliSeconds=clock.millis();



            cvtColor(frame, hsv_frame, COLOR_BGR2HSV);
            ArrayList<Integer> low_green = new ArrayList<Integer>() {
                {
                    add(25);
                    add(52);
                    add(72);
                }
            };
            ArrayList<Integer> high_green = new ArrayList<Integer>() {
                {
                    add(102);
                    add(255);
                    add(255);
                }
            };
            Scalar high_green1 = new Scalar(0, 0, 22);
            Scalar low_green1 = new Scalar(0, 0, 21);
            Mat green_mask = new Mat();
            Mat green = new Mat();
            inRange(hsv_frame, low_green1, high_green1, green_mask);
            bitwise_and(frame, frame, green, green_mask);

            Mat element = getStructuringElement(MORPH_RECT, new Size(2, 2));
            erode(green, green, element, new org.opencv.core.Point(-1, -1), 1);
            Mat gran=new Mat();
            gran=green.clone();
            int y = 0;
            int x = 0;
            int sx = 0;
            int sy = 0;
            int m = 0;



            x=0;
            y=0;
            int xTrim=400;
            int yTrim=210;
//        circle(green, new org.opencv.core.Point(xTrim, yTrim),  5,  new Scalar(0, 255, 255), -1);
//        circle(green, new org.opencv.core.Point(xsize-xTrim, ysize-yTrim),  5,  new Scalar(0, 255, 255), -1);

            for (int l = xTrim; l < xsize-xTrim; l++) {
                for (int k = yTrim; k < ysize-yTrim; k++) {
                    if (gran.get(k,l)[0] != 0.0 ||gran.get(k,l)[1] != 0.0 ||gran.get(k,l)[2] != 0.0 && sx == 0) {

                        sx = k;
                        sy = l;
                        break;
                    }

                    x += 1;
                }
                if(sx!=0){
                    break;
                }
                x = 0;
                y += 1;
            }
//        circle(green, new Point(sy, sx), 5, new Scalar(0, 0, 255), -1);
            int ex = 0;
            int ey = 0;
            y = 0;
            x = 0;

            int i = (int) green.size().width - 1-xTrim;
            int n = (int) green.size().height - 1-yTrim;
            while (i > xTrim) {
                while (n > yTrim && ysize-yTrim>n) {
                    if (gran.get(n,i)[0] != 0.0 &&gran.get(n,i)[1] != 0.0 &&gran.get(n,i)[2] != 0.0 && ex == 0) {
                        ex = i;
                        ey = n;
                        break;
                    }
                    x += 1;
                    n -= 1;
                }
                if(ex!=0){
                    break;
                }
                x = 0;
                n = (int) green.size().height - 1-yTrim;
                i -= 1;
                y += 1;
            }

            int z = (int) (((ex + sy) / 2));
            q = (int) ((ey + sx) / 2);


            /////////////////////////////////////////////////////////////////////////
            //YOUR MISSION BEGINS HERE HUDSON. THE X AND Y COORDINATES OF THE TARGET POSITION ARE z and q WHICH ARE RELATIVE
            // TO THE UPPER LEFT CORNER OF THE IMAGE
            //THE COORDS ARE WEIRD AS FUCK
            // IF YOU GET +s values that will mean the target is more +z values relative to the world
            // If you get more +x values, that will mean the target is more +x values relative to the world
            // IG it all works out
            // THE WORLDS *X AND -Z* AXIS. YES THE Z AXIS IS UPSIDE DOWN. I WILL LINK DRAWING OF AXIS HERE
            //https://docs.google.com/document/d/16gjb_33hD5gkhtjClh3fiYJTdbM2_JZ42qZPSlegrxs/edit?usp=sharing
            //THE COORDS OUTPUTTED BY THE PROGRAM ARE PIXEL VALUES BUT THE ROBOT MOVES IN METERS
            //ARGUABLY THE MOST IMPORTANT THING IS THAT THE LASER IS OFFSET AND IT WILL ALWAYS SHINE AT THE POSITION
            //(735,453) RELATIVE TO THE TOP LEFT CORNER OF THE IMAGE. THESE ARE PIXEL VALUES.
            //SO YEAH JUST TRY AND USE THE OUTPUTTED TARGET POSITION TO MOVE THE ASTROBEE TO MAKE THE LASER SHINE AT THE CENTER
            //yeah it's actually harder than it seems lol.
            //good luck
            //////////////////////////////////////////////////////////////////////////


            a = z;
            s = q;
            api.saveMatImage(api.getMatNavCam(),"BeforeMove"+Integer.toString(u)+".png");

            zmove=.01f*(s-453f)/9.548f;


            xmove = .01f*(a-735f)/9.548f;

            //3px=xcm
            //9.4px/cm



            api.moveTo(new Point(point2.getX() + xmove, point2.getY(), point2.getZ() + zmove), quaternion2, false);
            api.moveTo(new Point(point2.getX() + xmove, point2.getY(), point2.getZ() + zmove), quaternion2, false);
            api.moveTo(new Point(point2.getX() + xmove, point2.getY(), point2.getZ() + zmove), quaternion2, false);
            api.moveTo(new Point(point2.getX() + xmove, point2.getY(), point2.getZ() + zmove), quaternion2, false);
            api.moveTo(new Point(point2.getX() + xmove, point2.getY(), point2.getZ() + zmove), quaternion2, false);
            api.moveTo(new Point(point2.getX() + xmove, point2.getY(), point2.getZ() + zmove), quaternion2, false);
            //[note to self/future hudson: use "getRobotKinematics" to account for navigation error]
            g+=1;
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


        }
        api.takeTarget2Snapshot();

        api.laserControl(false);
        //Point point2=new Point(11.2746f,-9.92284f, 5.29881f);
        //DON'T FUCKING TOUCH THESE VALUES

        api.moveTo(new Point(10.35, -9.44f, 5.4f),new Quaternion(0f, 0f, -0.707f, 0.707f),false);
        api.moveTo(new Point(11.27460, -7.89178, 4.96538),new Quaternion(0f, 0f, -0.707f, 0.707f),false);
        //offset +45 -13
//        /* ******************************************** */
//        /* write your own code and repair the air leak! */
//        /* ******************************************** */
//         send mission completion
        api.reportMissionCompletion();


    }
}

//    @Override
//    protected void runPlan2(){
//        // write here your plan 2
//    }
//
//    @Override
//    protected void runPlan3(){
//        // write here your plan 3
//    }
//
//}

