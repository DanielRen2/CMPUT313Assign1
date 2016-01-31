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

def readFrame(frame, error, state, burstB, burstN, block_size, checkbits):#reads frame that has been generated and returns false if need to retransmit
    errorCount = 0;
    counter = 0;
    if block_size == 0:
        block_size = len(frame);
    if burstB > 0:
        errorB = error * ((burstB + burstN)/burstB);
    for i in range(len(frame)):
        if state == "I":
            if(frame[i] <= error):
                errorCount += 1;
                if checkbits == 0:
                    return False;
                if errorCount > 2:
                    return False;
        if state == "B":
            if(frame[i] <= errorB):
                errorCount += 1;
                if checkbits == 0:
                    return False;                
                if errorCount > 2:
                    return False;
        counter = counter + 1;
        if(counter >= block_size):
            counter = 0;
            errorCount = 0;
            
    return True;

def calculateFrameSize(blockNum, blockSize, frameSize):#calculates how many total checkbits are added to the frame
    if blockNum == 0:
        return frameSize;
    totalSize = int(math.log2(blockSize));#calculates the number of checkbits for each block
    print("Number of checkbits: " + str(totalSize));
    totalSize = totalSize * blockNum;
    totalSize = totalSize + frameSize;
    return totalSize;

def calculateStandardDevF(frameTransmissionAVG, trail_num, totalGoodFrame, totalFrame):#calculates standard devation of average frame transmission
    s = 0;
    mean_avg = totalFrame/totalGoodFrame;
    #print("this is mean avg: " + str(mean_avg));
    for i in range(trail_num):
        #print("this is frame avg: " + str(frameTransmissionAVG[i]));
        #print(((frameTransmissionAVG[i] - mean_avg)**2));
        s = s + ((frameTransmissionAVG[i] - mean_avg)**2);
    s = s/4;
    s = math.sqrt(s);
    return s;

def calculateStandardDevT(throughputAVG, trail_num, totalGoodFrame, totalTime, frameSize):#calculates standard deviation of throughput
    s = 0;
    mean_avg = (totalGoodFrame*frameSize)/totalTime;
    #print("this is mean avg: " + str(mean_avg));
    for i in range(trail_num):
        #print("this is frame avg: " + str(frameTransmissionAVG[i]));
        #print(((frameTransmissionAVG[i] - mean_avg)**2));
        s = s + ((throughputAVG[i] - mean_avg)**2);
    s = s/4;
    s = math.sqrt(s);
    return s;

def calcCI(mean_avg, standardDev, t_dis):#calculates confidence intervals
    offset = (t_dis*(standardDev/math.sqrt(5)));
    c1 = mean_avg - offset;
    c2 = mean_avg + offset;  
    return c1, c2;

def main():   
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
    if num_blocks > 0:#sets blocksize to 0 if k is 0
        block_size = size_frame/num_blocks;
    else:
        block_size = 0;
    #-------------------------------------------------------- 
    #-----------variables from calculations----------------------
    if block_size > 0:#finds checbits
        checkbits = int(math.log2(block_size));
    else:
        checkbits = 0;
    totalSize = calculateFrameSize(num_blocks, block_size, size_frame);
    frameTransmissionAVG = [];
    throughputAVG = [];
    t_distribution = 2.776;#given by the lab, only works for 5 trails
    #-------------------------------------------------------------
      
    for i in range(trail_num):#adds seeds of trails into a trail array
        trails.append(int(sys.argv[9 + i + 1]));

    #-------temp tracking variables-----------
    totalGoodFrame = 0;
    totalFrame = 0;
    totalTime = 0;
    #---------------------------------------

    for i in range(trail_num):
        random.seed(trails[i]);#sets the seed of the random number generator
        timer = 0;
        finishedFrame = 0;
        while timer <= length_sim:
            
            if error_model == "I":#initializes frames using independent error model
                frame = createFrameSE(totalSize);
            if error_model == "B":#initializes frames using burst error model
                frame = createFrameBE(totalSize, burst_b, burst_n);
                
            result = readFrame(frame, prob_error, error_model, burst_b, burst_n, block_size + checkbits, checkbits);#read frames
            
            if(result == True):#increments frames if succesfull
                finishedFrame += 1;
            timer = timer + totalSize + feedback_time;#adds time to the clock
            
        print("trail " + str(i + 1) + " finished with " + str(finishedFrame) + " received and " + str(timer/(totalSize+feedback_time)) + " total frames transmitted");
        
        if finishedFrame == 0:#if no frames finish
            print("no frames transmitted");
            frameTransmissionAVG.append(0);#appends frame transmission
            throughputAVG.append(0);            
        else:
            frameTransmissionAVG.append((timer/(totalSize+feedback_time))/finishedFrame);#appends frame transmission
            throughputAVG.append((size_frame*finishedFrame)/timer);
        
        totalGoodFrame += finishedFrame;#updates total number of frames finished
        totalFrame += timer/(totalSize+feedback_time);#updates total number of frames transmitted
        totalTime += timer;#updates total time used
        
    #results
    if totalGoodFrame == 0:#deals with a situation where 0 frames are transmited
        print("a total of 0 frames where transmitted");
        exit();
        
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
    print(str(error_model) + " " + str(feedback_time) + " " + str(num_blocks) + " " + str(size_frame) + " " + str(prob_error) + " " + str(burst_b) + " " + str(burst_n) + " " + str(length_sim) + " " + str(trail_num) + " " + str(trails[0]) + " " + str(trails[1]) + " " + str(trails[2]) + " " + str(trails[3]) + " " + str(trails[4]))
        
    s = calculateStandardDevF(frameTransmissionAVG, trail_num, totalGoodFrame, totalFrame);
    c1, c2 = calcCI(totalFrame/totalGoodFrame, s, t_distribution);
    print("Average Frame Transmission: " + str(totalFrame/totalGoodFrame) + " CI: " + str(c1) + " " + str(c2));
    
    s = calculateStandardDevT(throughputAVG, trail_num, totalGoodFrame, totalTime, size_frame);
    c1, c2 = calcCI((totalGoodFrame*size_frame)/totalTime, s, t_distribution);
    print("Throughput Average: " +str((size_frame*totalGoodFrame)/totalTime) + " CI: " + str(c1) + " and: " + str(c2));
    
if __name__ == "__main__":
    main()
