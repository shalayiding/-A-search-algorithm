Proper interpretation of input files:
For the program 3 different input files are needed:
1.Orginal image map file as .png
2.mmp.txt which is the file that contains all elevation values for image pixel
3.path.txt which is the file contains all the point that we have to visit
My Program handles the file by reading a file line by line and strip the line ending ‘\n’ and
split the data within the line and read the data to list:
For example :
all the information is stored inside of the eleva_matrix from file 2, the same is applied for file
3.
Map generation :
The case that map is been generated as Width * Height of matrix and store object point
inside of each position.
Make map is used to set the elevation value of the object and find proper terrain type from
pixel values in the image.
A* algorithm :
In the A* algorithm 3 different kinds of scores have been used.
1: Hscore, is simply a manhattan distance from point A to B, since we have elevation I
consider that as 3 point manhattan distance.By testing couple different point and path I
found out that this gives me best result for most of the cases which make sense that from
this equation we are getting 3 dimension distance from point A to point B.
2.Gscore, is calculated by distance/speed(terrain type) where the pixel first moves (
change of x or change of y ) every pixel move as x count as 10.29m, every pixel move as y
count as 7.55m, and then divide the speed from distance will give us the G score. For my
cost function, I was trying to consider if we go from uphill to down our speed will increase, if
we go from down to up our speed should decrease. if we go from higher elevation to lower
our speed will increase by the difference of ele_value multiplied by 0.1, and if we go from a
lower elevation to higher we should get a negative number to reduce our speed.
3.Fscore, Fscore is the final score that we use to decide whether or not to pick that point, it
is simply calculated by Gscore+Hscore.
A* Main:
The function requires 3 inputs which are: start point, endpoint, and the map we build. Two
buffers are used to record our status which is, visited_point which records all the points that
we have been visited, and ready_to_visit which is the point that we want to explore. if we find
that the start point is equal to the endpoint we have to trace back to the start point and
record all the paths.
else we have to generate 4 neighbor values up, down, right, left, and then check if any of the
points are outside of the image. if it is remove the point from the four_point list. Calculate the
point G,H score and do for all the points in the four_point list. Then find the best point in four
values and explore that point. After we have the path simply loop the list and write the path
into the image. Save the image and print the distance on the terminal.
close pixel generator that generates 4 pixels value around the point we select
Test Case :
The Program is good on all the test cases provided, within the time requirement.
redout.png brown.png white.png
Other test case images are in the file, the purple color on the map is just a scaler version of
our start and end points. Distance :
total distance is meter is 7568.36000000004 for red.txt
total distance is meter is 5846.1600000000235 for brown.txt
total distance is meter is: 3287.310000000005 for white.tx
