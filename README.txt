CMPUT313 Assignment 1 Error Simulator
By Xiao Yu Ren and Beikun Yan

Instructions:
To use this simulator the following format must be followed on command line

python3 Assign1.py M A K e B N R 5 x1 x2 x3 x4 x5

M = Error model with two possible inputs "I" or "B"
A = Feedback time all existing data uses a feedback time of 50
K = number of blocks per frame, must be a number that can divide frame size
F = frame size, the number used for all test data was 4000
e = error probability, must be a float
B = Burst length
N = non-burst length

5 is the number of trails, this simulation was built around 5 trails

x1-x5 are the seeds for each trail

The data is outputed in a Output.txt file and an Output.csv file