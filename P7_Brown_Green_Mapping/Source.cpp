#include "opencv2/imgcodecs.hpp"
#include "opencv2/highgui.hpp"
#include "opencv2/imgproc.hpp"
#include <opencv2/highgui/highgui_c.h>
#include "opencv2/stitching.hpp"
#include <iostream>
#include <fstream>
#include <cmath>
#include<climits>   
#include <string>
#include <opencv2/core/utility.hpp>
#include <stdlib.h>

using namespace cv;
using namespace std;

RNG rng(12345);

double points[10000][2];
double points2[10000][2];
double distances[10000][10000];
double textpoint[10000][2];

int shortestdistance = 100000;
int point[10000];
int t = 1;
int boundingboxwidth[100000];
int counter = 1;

int main(int argc, char** argv)
{
    //////////////////////////////////////////////////////////////////Ask user for input regarding altitude and number of pictures/////////////////////////
    cout << "Running brown/green mapping algorithm" << endl;

    //////////////////////////////////////////////////////////If statememnts to sort those input values into ratios to use later //////////////////////////
    double newimageratio = 0.25;
    double pixeltometerratio = 0.019724;
    ///////////////////////////////////////////////////////Loads the images and save them into an array //////////////////////////////////////////////////
    cout << "Load images" << endl;
    vector<cv::String> imgfolder;
    glob("Location of the folder of the desired picture to be analysed\*.png", imgfolder, false);

    vector<Mat> images;
    size_t count = imgfolder.size();
    for (size_t i = 0; i < count; i++)
    {
        Mat img = imread(imgfolder[i]);

        if (img.empty())
        {
            cout << imgfolder[i] << " is invalid" << endl;
            continue;
        }

        /////////////////////////////////////////////////////// Deletes the previous CSV file ///////////////////////////////////////////////////////////////////7
        cout << "Delete CSV file" << endl;

        // Open File pointers
        fstream fin, fout;

        // Open the existing file
        fin.open("centroiddata.csv", ios::in);

        // Close the pointers
        fin.close();
        fout.close();

        // removing the existing 
        remove("centroiddata.csv");

        Mat res = img;

        /////////////////////////////////////////////////////// Toggles contrast///////////////////////////////////////////////////////////////////7
        cout << "Toggle contrast and brightness" << endl;

        Mat imageContrast;
        res.convertTo(imageContrast, -1, 1, -100);

        /////////////////////////////////////////////////////// Toggles brightness ///////////////////////////////////////////////////////////////////7

        Mat imageBrightness;
        imageContrast.convertTo(imageBrightness, -1, 3.3, 0);

        /////////////////////////////////////////////////////// Puts image through color threshold ///////////////////////////////////////////////////////////////////7

        cout << "Turn into binary" << endl;

        // RGB color filter
       
        // Filter for finding purple objects
        Mat OutputImage;
        inRange(imageBrightness, Scalar(70, 0, 70), Scalar(170, 70, 170), OutputImage);

      //Filter for finding green objects
      //  Mat OutputImage;
      //  inRange(imageBrightness, Scalar(10, 10, 10), Scalar(200, 255, 120), OutputImage);

        //HSI color filter
        /*
       // Filter for finding green objects
        Mat imgHSV;
        cvtColor(imageBrightness, imgHSV, COLOR_BGR2HSV);
        Mat OutputImage;
       inRange(imgHSV, Scalar(25, 25, 25), Scalar(70, 255, 255), OutputImage);
       */

       /*
        //Filter for finding brown objects
        Mat imgHSV;
        cvtColor(imageBrightness, imgHSV, COLOR_BGR2HSV); //Convert the captured frame from BGR to HSV
        Mat OutputImage;
        inRange(imgHSV, Scalar(0, 0, 0), Scalar(5, 255, 255), OutputImage); //Threshold the image
        */

        /*
        // Filter for finding brown objects
       Mat imgHSV;
        cvtColor(imageBrightness, imgHSV, COLOR_BGR2HSV); //Convert the captured frame from BGR to HSV
        Mat OutputImage;
        inRange(imgHSV, Scalar(0, 25, 25), Scalar(30, 255, 140), OutputImage); //Threshold the image
        */

        /////////////////////////////////////Morphology//////////////////////////////////////////////////////
        
        cout << "Morphology" << endl;

        Mat morphImg;
        Mat morphImg2;
        Mat elem = getStructuringElement(MORPH_ELLIPSE, Size(10, 10));
        //  Mat elem = getStructuringElement(MORPH_ELLIPSE, Size(25, 25));
        morphologyEx(OutputImage, morphImg, MORPH_CLOSE, elem);
        morphologyEx(morphImg, morphImg2, MORPH_OPEN, elem);

        /////////////////////////////////////Creates contours//////////////////////////////////////////////////////

        cout << "Create contours" << endl;

        Mat canny_output;
        vector<vector<Point>> contours;
        vector<Vec4i> hierarchy;
        findContours(morphImg2, contours, hierarchy, RETR_TREE, CHAIN_APPROX_NONE);
        drawContours(canny_output, contours, -1, Scalar(0, 0, 0), 1);

        /////////////////////////////////////Creates a bounding box out of the contours that are fully closed//////////////////////////////////////////////////////

        cout << "Create bounding boxes" << endl;

        vector<vector<Point> > contours_poly(contours.size());
        vector<Rect> boundRect(contours.size());
        vector<Point2f>centers(contours.size());
        vector<float>radius(contours.size());

        for (size_t i = 0; i < contours.size(); i++)
        {
            approxPolyDP(contours[i], contours_poly[i], 3, true);
            boundRect[i] = boundingRect(contours_poly[i]);
            minEnclosingCircle(contours_poly[i], centers[i], radius[i]);

        }

        Mat drawing = Mat::zeros(canny_output.size(), CV_8UC3);
        for (size_t i = 0; i < contours.size(); i++)
        {
            Scalar color = Scalar(rng.uniform(0, 256), rng.uniform(0, 256), rng.uniform(0, 256));
            drawContours(drawing, contours_poly, (int)i, color);
            rectangle(drawing, boundRect[i].tl(), boundRect[i].br(), color, 20);
        }

        /////////////////////////////////////Finds the center of the bounding box////////////////////////////////////////////////////////
        Mat BoundingBox = Mat(res.size(), CV_8U);
        resize(res, BoundingBox, cv::Size(), newimageratio, newimageratio);

        cout << "Finding bounding box centers" << endl;

        for (int i = 0; i < boundRect.size(); i++)
        {
            //Bounding Box Centroid
            Point center = Point(((boundRect[i].x + (boundRect[i].width) / 2)), ((boundRect[i].y + (boundRect[i].height) / 2)));
            boundingboxwidth[i] = boundRect[i].width;

            ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

            Scalar color = Scalar(rng.uniform(1, 1), rng.uniform(1, 1), rng.uniform(255, 255));
            int radius = 2;
            int t_out = 0;
            std::string win_name = "circle";
            cv::Scalar red(0, 0, 255);
            int boundingboxarea = boundRect[i].width * boundRect[i].height;
            int imagearea = res.size().height * res.size().width;

            ////////////////////////////////////////////////////////////////////////////////////

          //  cout << "Saving center coordinates" << endl;
            if (boundingboxarea / imagearea < 0.7) {

                if (contourArea(contours[i]) > 50) {
                    drawContours(res, contours_poly, (int)i, color);
                    rectangle(res, boundRect[i].tl(), boundRect[i].br(), color, 5);
                    cv::circle(res, cv::Point((boundRect[i].x + (boundRect[i].width) / 2), (boundRect[i].y + (boundRect[i].height) / 2)), radius, red, 5);

                    cv::circle(res, cv::Point(0, 0), 15, red, 25);

                    textpoint[t][0] = center.x;
                    textpoint[t][1] = center.y;

                    //Saves x and y coordinates into an array
                    points2[i][0] = center.x * pixeltometerratio;
                    points2[i][1] = center.y * pixeltometerratio;

                    t++;

                }
            }
            int numberofpoints = boundRect.size();
        }

        points[0][0] = 0;
        points[0][1] = 0;

        for (int i = 0; i < boundRect.size(); i++) {

            if (contourArea(contours[i]) > 50) {

                points[counter][0] = points2[i][0];
                points[counter][1] = points2[i][1];

                counter++;
            }
        }

        ////////////////////////////////////////////////////////////////////////////////////////
        cout << "Finding distance between every point" << endl;

        for (int i = 0; i < counter; i++) {

            for (int j = 0; j < counter; j++)
            {
                distances[i][j] = sqrt(pow(points[j][0] - points[i][0], 2) + pow(points[j][1] - points[i][1], 2));
            }
        }

        //////////////////////////////////////////////////////////////////////////////////////

        cout << "Running path planning algorithm" << endl;
        int newpoint = 0;
        for (int f = 0; f < counter; f++) {

            for (int n = 0; n < counter; n++) {

                if (distances[newpoint][n] != 0) {
                    if (distances[newpoint][n] < shortestdistance) {
                        if (point[0] != n && point[1] != n && point[2] != n && point[3] != n && point[4] != n && point[5] != n && point[6] != n && point[7] != n && point[8] != n && point[9] != n && point[10] != n && point[11] != n && point[12] != n && point[13] != n && point[14] != n && point[15] != n && point[16] != n && point[17] != n && point[18] != n && point[19] != n && point[20] != n && point[21] != n && point[22] != n && point[23] != n && point[24] != n && point[25] != n && point[26] != n && point[27] != n && point[28] != n && point[29] != n && point[30] != n && point[31] != n && point[32] != n && point[33] != n && point[34] != n && point[35] != n && point[36] != n && point[37] != n && point[38] != n && point[39] != n && point[40] != n && point[41] != n && point[42] != n && point[43] != n && point[44] != n && point[45] != n && point[46] != n && point[47] != n && point[48] != n && point[49] != n && point[50] != n && point[51] != n && point[52] != n && point[53] != n && point[54] != n && point[55] != n && point[56] != n && point[57] != n && point[58] != n && point[59] != n && point[60] != n && point[61] != n && point[62] != n && point[63] != n && point[64] != n && point[65] != n && point[66] != n && point[67] != n && point[68] != n && point[69] != n && point[70] != n && point[71] != n && point[72] != n && point[73] != n && point[74] != n && point[75] != n && point[76] != n && point[77] != n && point[78] != n && point[79] != n && point[80] != n && point[81] != n && point[82] != n && point[83] != n && point[84] != n && point[85] != n && point[86] != n && point[87] != n && point[88] != n && point[89] != n && point[90] != n && point[91] != n && point[92] != n && point[93] != n && point[94] != n && point[95] != n && point[96] != n && point[97] != n && point[98] != n && point[99] != n) {

                            shortestdistance = distances[newpoint][n];
                            point[f] = n;
                        }
                    }
                }
            }
            shortestdistance = 100000;
            point[counter] = 0;
            newpoint = point[f];
        }

        //////////////////////////////////////////////////////////////////////////////////////

        stringstream ss;
        string text;
        ss << "Start";
        text = ss.str();
        cv::putText(res,
            text,
            cv::Point(25, 125),
            cv::FONT_HERSHEY_DUPLEX,
            5.0,
            CV_RGB(255, 0, 0),
            5);
        ss.str("");

        int textcounter = 1;

        for (int i = 0; i < counter-1; i++) {

            stringstream ss;
            string text;
            ss << textcounter;
            text = ss.str();
            cv::putText(res,
                text,
                cv::Point(textpoint[point[i]][0] + 25, textpoint[point[i]][1] + 25),
                cv::FONT_HERSHEY_DUPLEX,
                10.0,
                CV_RGB(255, 0, 0),
                10);
            ss.str("");
            textcounter++;
        }

        //////////////////////////////////////////////////////////////////////////////////////

        cout << "Saving shortest path to CSV" << endl;
        fout.open("centroiddata.csv", ios::out | ios::app);

        fout << points[0][0] << "," << points[0][1] << "\n";

        for (int i = 0; i < counter; i++) {

            // Insert the data to CSV file
            fout << points[point[i]][0] << "," << points[point[i]][1] << "\n";
        }
        
                cout << "Final image is done" << endl;

                int finalratiorow = res.rows * pixeltometerratio;
                int finalratiocol = res.cols * pixeltometerratio;

                imwrite("originalimage.jpg", res); 

                Mat final = Mat(res.size(), CV_8U);
                resize(res, final, cv::Size(), 0.55, 0.55);
                imshow("final", final);
                waitKey(0);

                Mat3b simulationimage(2000, 2000, Vec3b(0, 0, 0));

                res.copyTo(simulationimage(Rect(0, 0, res.cols, res.rows)));
                imwrite("testimage.jpg", simulationimage); 

                break;
            }
    }







