// Pixy Camera Proof Of Concept Vehicle

// Include Libraries
    #include <SPI.h>
    #include <Pixy2.h>

// Define Pins
    #define in1 5
    #define in2 6
    #define in3 7
    #define in4 8
    #define enA 9
    #define enB 10
    #define greenLed 4
// Define bitmasks for setting output values of the pins
    #define IN1_MASK 0b00100000
    #define IN2_MASK 0b01000000
    #define IN3_MASK 0b10000000
    #define IN4_MASK 0b00000100


// Variables
    uint8_t rotateSpeed = 150;
    uint8_t turnSpeed = 180;
    uint8_t driveSpeed = 255;
    uint8_t tennisBallsCollected = 0;
    static int8_t index;
    Pixy2 pixy; //Setup Pixy Camera
    bool drivingStart = false;
    int objectXPosition;

void setup() {		
    Serial.begin(9600);
    pinMode(enA, OUTPUT);
    pinMode(in1, OUTPUT);
    pinMode(in2, OUTPUT);
    pinMode(enB, OUTPUT);
    pinMode(in3, OUTPUT);
    pinMode(in4, OUTPUT); 
    pinMode(greenLed, OUTPUT); 
    pixy.init();        // Initialise Pixy Camera
    driveRobot("stop"); // Set Initial Motor Controls
}

void loop() {
    
    // Find and collect tennis balls
    while (tennisBallsCollected < 3) {
        pixy.ccc.getBlocks();
        findClosestObject();
        rotateToObject();
        driveToObject();
        findClosestObject();
        if(index == -1) {
            driveRobot("stop");
        }
    }
   


}


// Make a clean away to direct robot.
void driveRobot(String command) {
    if (command == "forward") {
        digitalWrite(in1, HIGH);
        digitalWrite(in2, LOW);
        digitalWrite(in3, HIGH);
        digitalWrite(in4, LOW);
    } else if (command == "backward") {
        digitalWrite(in1, LOW);
        digitalWrite(in2, HIGH);
        digitalWrite(in3, LOW);
        digitalWrite(in4, HIGH);
    } else if (command == "right") {
        digitalWrite(in1, LOW);
        digitalWrite(in2, HIGH);
        digitalWrite(in3, HIGH);
        digitalWrite(in4, LOW);
    } else if (command == "left") {
        digitalWrite(in1, HIGH);
        digitalWrite(in2, LOW);
        digitalWrite(in3, LOW);
        digitalWrite(in4, HIGH);
    } else if (command == "stop") {
        digitalWrite(in1, LOW);
        digitalWrite(in2, LOW);
        digitalWrite(in3, LOW);
        digitalWrite(in4, LOW);
    } else {
        // Invalid Command
    }
}


int16_t acquireBlock() {
    pixy.changeProg("color_connected_components");
    if (pixy.ccc.numBlocks && pixy.ccc.blocks[0].m_age>30)
        return pixy.ccc.blocks[0].m_index;

    return -1;
}

Block *trackBlock(uint8_t index) {
    uint8_t i;

    for (i=0; i<pixy.ccc.numBlocks; i++) {
        if (index==pixy.ccc.blocks[i].m_index)
            return &pixy.ccc.blocks[i];
    }
    return NULL;
}

Block *block=NULL;

void findClosestObject() {
    index = -1; 
    if (index==-1) { //search...
        Serial.println("Searching for block...");
        index = acquireBlock();
        if (index>=0)
        Serial.println("Found block!");
    }
    // If we've found a block, find it, track it
    if (index>=0)
        block = trackBlock(index);
}

void rotateToObject() {
    if (block && drivingStart ==  false) {
        objectXPosition  = block->m_x; // fixed line
        analogWrite(enA, rotateSpeed);
        analogWrite(enB, rotateSpeed);
        // Rotate the robot until it faces the object
        while (abs(objectXPosition - 160) > 10) { // 10 pixel tolerance 
            pixy.ccc.getBlocks();
            if (objectXPosition < 150) {
            driveRobot("right");
            } else if (objectXPosition > 170) {
            driveRobot("left");
            }  
            block = trackBlock(block->m_index); // update block position
            objectXPosition = block->m_x; // update object position
        }
        //driveRobot("stop");
        drivingStart = true; 
    }
}

void driveToObject() {
    if (drivingStart == true) {
        int objectYPosition  = block->m_y;
        driveRobot("forward");
        while (pixy.ccc.numBlocks) {
            if (objectXPosition < 150){
                analogWrite(enA, turnSpeed);
                analogWrite(enB, driveSpeed);
            } else if (objectXPosition > 170) {
                analogWrite(enA, driveSpeed);
                analogWrite(enB, turnSpeed);
            } else {
                analogWrite(enA, driveSpeed);
                analogWrite(enB, driveSpeed);
            }
            pixy.ccc.getBlocks();
            block = trackBlock(block->m_index); // update block position
            objectYPosition = block->m_y;   
            objectXPosition = block->m_x;
        }
        driveRobot("stop");
        tennisBallsCollected ++;
        digitalWrite(greenLed, HIGH);
        delay(100);
        digitalWrite(greenLed, LOW);
        delay(100);
        digitalWrite(greenLed, HIGH);
        delay(100);
        digitalWrite(greenLed, LOW);
        drivingStart = false;
    }
}
