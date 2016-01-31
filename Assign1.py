import sys
import math
import random

def createFrameSE(frameSize):#generate a block of a certain size with possible errors
    frame = [];
    for i in range(frameSize):
        frame.append(random.random());#adds a float between 0-1 to block
    return frame;

def createFrameBE(frameSize, errorLen, nerrLen):#generates a frame with burst error
    frame = [];
    counter = 0;
    state = 1;
    for i in range(frameSize):#switches between states when counter reaches cap
        if(state == 1):
            frame.append(1);
            counter = counter + 1;
            if(counter >= nerrLen):
                state = 0;
                counter = 0;
        if(state == 0):
            frame.append(random.random());
            counter = counter + 1;
            if(counter >= errorLen):
                state = 1;
                counter = 0;
    return frame;

def readFrame(frame, error, state, burstB, burstN, block_size):
    errorCount = 0;
    counter = 0;
    if burstB > 0:
        errorB = error * ((burstB + burstN)/burstB);
    for i in range(len(frame)):
        if state == "I":
            if(frame[i] <= error):
                errorCount += 1;
                if errorCount > 2:
                    return False;
        if state == "B":
            if(frame[i] <= errorB):
                errorCount += 1;
                if errorCount > 2:
                    return False;
        counter = counter + 1;
        if(counter >= block_size):
            counter = 0;
            errorCount = 0;
            
    return True;

def calculateFrameSize(blockNum, blockSize, frameSize):
    totalSize = int(math.log2(blockSize));#calculates the number of checkbits for each block
    print("Number of checkbits: " + str(totalSize));
    totalSize = totalSize * blockNum;
    totalSize = totalSize + frameSize;
    return totalSize;

def calculateStandardDevF(frameTransmissionAVG, trail_num, totalGoodFrame, totalFrame):
    s = 0;
    mean_avg = totalFrame/totalGoodFrame;
    print("this is mean avg: " + str(mean_avg));
    for i in range(trail_num):
        print("this is frame avg: " + str(frameTransmissionAVG[i]));
        print(((frameTransmissionAVG[i] - mean_avg)**2));
        s = s + ((frameTransmissionAVG[i] - mean_avg)**2);
    s = s/4;
    s = math.sqrt(s);
    return s;

def main():
    
    #assume all possible bit time that will be used are used
    #assume receiver reads all bits every time
    #time per cycle assuming no failures is F + r*k + A
    #simulation time means bit unit time for each trail
    
    print("Number of arguments: " + str(len(sys.argv)) + " arguments");
    print("first argument is: " + str(sys.argv[1]));
    
    #------------variables from command line-----------------
    error_model = str(sys.argv[1]);
    feedback_time = int(sys.argv[2]);
    num_blocks = int(sys.argv[3]);
    size_frame = int(sys.argv[4]);
    prob_error = float(sys.argv[5]);
    burst_b = int(sys.argv[6]);
    burst_n = int(sys.argv[7]);
    length_sim = int(sys.argv[8]);
    trail_num = int(sys.argv[9]);
    trails = [];
    block_size = size_frame/num_blocks;
    #--------------------------------------------------------
    
    #-----------variables from calculations----------------------
    checkbits = int(math.log2(block_size));
    totalSize = calculateFrameSize(num_blocks, block_size, size_frame);
    frameTransmissionAVG = [];
    throughputAVG = [];
    t_distribution = 2.776;#given by the lab, only works for 5 trails
    #-------------------------------------------------------------
      
    for i in range(trail_num):#adds seeds of trails into a trail array
        print("this is i : " + str(i))
        trails.append(int(sys.argv[9 + i + 1]));
        print ("this is trail " + str(trails[i]));
    print("Feedback is " + str(feedback_time));
    
    print("block size is : " + str(block_size));
    totalGoodFrame = 0;
    totalFrame = 0;
    totalTime = 0;

    for i in range(trail_num):
        print("Size of transmitted frame : " + str(totalSize));
        random.seed(trails[i]);#sets the seed of the random number generator
        timer = 0;
        finishedFrame = 0;
        while timer <= length_sim:
            if error_model == "I":
                frame = createFrameSE(totalSize);
            if error_model == "B":
                frame = createFrameBE(totalSize, burst_b, burst_n);
            result = readFrame(frame, prob_error, error_model, burst_b, burst_n, block_size + checkbits);#read frames
            if(result == True):
                finishedFrame += 1;
            timer = timer + totalSize + feedback_time;
            
        print("trail " + str(i + 1) + " finished with " + str(finishedFrame) + " sent and " + str(timer/(totalSize+feedback_time)) + " total frames");
        frameTransmissionAVG.append((timer/(totalSize+feedback_time))/finishedFrame);#appends frame transmission
        throughputAVG.append((size_frame*finishedFrame)/timer);
        
        totalGoodFrame += finishedFrame;#updates total number of frames finished
        
        totalFrame += timer/(totalSize+feedback_time);#updates total number of frames transmitted
        totalTime += timer;#updates total time used
        
    print("average number of frame transmissions is " + str(totalFrame/totalGoodFrame))
    s = calculateStandardDevF(frameTransmissionAVG, trail_num, totalGoodFrame, totalFrame);
    print("this is standard deviation: " + str(s));
    print("throughput is " + str((size_frame*totalGoodFrame)/totalTime));
                    
    
if __name__ == "__main__":
    main()
