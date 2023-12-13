Test Introduction
The spatial reasoning test shows images of 3D arrangements of colored cubes and 4 corresponding 2D projections. Participants should identify the 2D projection which can not be made by rotating the arrangements.

There are 10 questions in total, aiming to test 3 dimensions of spatial ability. In questions 1-5, a combination of mental orientation and spatial visualization was involved; in questions 6-10, an extra parameter spatial inference was added to the combination. Questions order in difficulty from low to high.

Participants have about 3 minutes to answer, then the test will automatically stop. As the grade is collected as accuracy, please think carefully and try to answer each question correctly. Don't rush to finish. 

A contract about uploading data (anonymous user_id, gender, age, drink or not, grade, time taken) to the google form will be shown before the display question. Participants are free to accept or reject.

Code Versions
1. Spatial_version1: 
This is the old version that was used to collect samples of reports.

2. Spatial_version2:
This is the refined version of spatial version_1.

First, the code was defined into functions to make the program more readable and simpler to debug and maintain over time. Second, only allowed users to enter 4 uppercase letters as user_id and lowercase male/female as gender. This will increase the efficiency of filtering the same participants from different tests. Third, the grade is collected as final scores in the old version. As mentioned in the report, this was one of the limitations caused by the misestimating of question difficulties. Hence, the grade was now collected as accuracy = final score/attempted questions. In addition, after finishing the test, a table will show the correct answers, users' answers, and time taken for each question, to help participants identify which questions they made mistakes on and which are the most challenge one to them.
