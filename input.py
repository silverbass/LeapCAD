import Leap, sys, thread, time, math, command

from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

class SampleListener(Leap.Listener):
    fi = None
    translating = False
    scaling = False
    rotating = False
    init_pos = [0, 0, 0]
    init_size = [0, 0, 0]
    initial_angle = [0, 0, 0]
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']

    def on_init(self, controller):
        print "Initialized"

    def on_connect(self, controller):
        print "Connected"
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

    def on_disconnect(self, controller):
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def write(self, n, vector):
        self.fi = open('line.py', 'w')
        self.fi.write("c_type = " + n + "\npVec = " + vector)
        print "c_type = " + n + "\npVec = " + vector
        self.fi.close


    def on_frame(self, controller):
        frame = controller.frame()
        swept_angles = []

        if len(frame.hands) == 1:
            hand = frame.hands[0]
            finger = hand.fingers[0]
            bone = finger.bone(3)

            if hand.pinch_strength > 0.95:
                if not self.translating:
                    self.translating = True
                    self.init_pos = [bone.next_joint[0], bone.next_joint[1], bone.next_joint[2]]
            else:
                self.translating = False

            if self.translating:
                end = [bone.next_joint[0], bone.next_joint[1], bone.next_joint[2]]
                temp = [end[0] - self.init_pos[0], end[1] - self.init_pos[1], end[2] - self.init_pos[2]]
                self.write(1, temp)

            # swipes[l,r,u,d]
            swipes = [0,0,0,0]
            
            normals = []
            for gesture in frame.gestures():
                if gesture.type == Leap.Gesture.TYPE_CIRCLE:
                    circle = CircleGesture(gesture)

                    # Determine clock direction using the angle between the pointable and the circle normal
                    if circle.pointable.direction.angle_to(circle.normal) <= Leap.PI/2:
                        clockwiseness = "clockwise"
                    else:
                        clockwiseness = "counterclockwise"

                    normals = normals + [circle.normal]
                    # Calculate the angle swept since the last frame
                    # Flawed
                    swept_angle = 0
                    if circle.state != Leap.Gesture.STATE_START:
                        previous_update = CircleGesture(controller.frame(1).gesture(circle.id))
                        swept_angle =  (circle.progress - previous_update.progress) * 2 * Leap.PI
                    swept_angles = swept_angles + [swept_angle]

                if gesture.type == Leap.Gesture.TYPE_SWIPE:
                    swipe = SwipeGesture(gesture)
                    start = swipe.start_position
                    current = swipe.position
                    
                    dx = current.x - start.x
                    dy = current.y - start.y
                    dz = current.z - start.z

                    if( (abs(dx) > abs(3*dy)) and (abs(dx) > abs(3*dz)) and dx < 0):
                        swipes[0] += 1
                    elif( (abs(dx) > abs(3*dy)) and (abs(dx) > abs(3*dz)) and dx > 0):
                        swipes[1] += 1
                    elif( (abs(dy) > abs(3*dx)) and (abs(dy) > abs(3*dz)) and dy > 0):
                        swipes[2]+= 1
                    elif( (abs(dy) > abs(3*dx)) and (abs(dy) > abs(3*dz)) and dy < 0):
                        swipes[3]+= 1

                    if swipes[0] > 3:
                        print "Swiped Left"
                        # self.fi = open('mel_script.mel', 'w')
                        # self.fi.write(?)
                        # self.fi.write('\n')
                        # self.fi.close
                    if swipes[1] > 3:
                        print "Tinder"
                        # self.fi = open('mel_script.mel', 'w')
                        # self.fi.write(?)
                        # self.fi.write('\n')
                        # self.fi.close
                    if swipes[2] > 3:
                        print "Save"
                        # self.fi = open('mel_script.mel', 'w')
                        # self.fi.write(?)
                        # self.fi.write('\n')
                        # self.fi.close
                    if swipes[3] > 3:
                        print "Menu"
                        # self.fi = open('mel_script.mel', 'w')
                        # self.fi.write(?)
                        # self.fi.write('\n')
                        # self.fi.close

                if gesture.type == Leap.Gesture.TYPE_KEY_TAP:
                     keytap = KeyTapGesture(gesture)
                     print "  Key Tap id: %d, %s, position: %s, direction: %s" % (
                             gesture.id, self.state_names[gesture.state],
                             keytap.position, keytap.direction )

            vector = [0, 0, 0]
            for index in range(0, len(normals)):
                vector[0] = vector[0] + (normals[index])[0]
                vector[1] = vector[1] + (normals[index])[1]
                vector[2] = vector[2] + (normals[index])[2]

            working_axis = 0;
            for axis in range(0, 3):
                if abs(vector[working_axis]) < abs(vector[axis]):
                    working_axis = axis

            avg_swept_angle = 0
            for angle in swept_angles:
                avg_swept_angle = avg_swept_angle + angle

            if len(swept_angles) > 0:
                avg_swept_angle = avg_swept_angle * 180.0 / (len(swept_angles) * math.pi)

            for axis in range(0, 3):
                if axis == working_axis:
                    vector[axis] = avg_swept_angle
                else:
                    vector[axis] = 0

            if sum(vector) != 0:
                self.write(2, vector)

        elif len(frame.hands) == 2:
            hand1 = frame.hands[0]
            hand2 = frame.hands[1]
            finger1 = hand1.fingers[0]
            bone1 = finger1.bone(3)
            finger2 = hand2.fingers[0]
            bone2 = finger2.bone(3)
            
            swipes = [0,0,0,0]

            for gesture in frame.gestures():
                if gesture.type == Leap.Gesture.TYPE_SWIPE:
                    swipe = SwipeGesture(gesture)
                    start = swipe.start_position
                    current = swipe.position
                    
                    dx = current.x - start.x
                    dy = current.y - start.y
                    dz = current.z - start.z

                    if( (abs(dx) > abs(3*dy)) and (abs(dx) > abs(3*dz)) and dx < 0):
                        swipes[0] += 1
                    elif( (abs(dx) > abs(3*dy)) and (abs(dx) > abs(3*dz)) and dx > 0):
                        swipes[1] += 1
                    elif( (abs(dy) > abs(3*dx)) and (abs(dy) > abs(3*dz)) and dy > 0):
                        swipes[2]+= 1
                    elif( (abs(dy) > abs(3*dx)) and (abs(dy) > abs(3*dz)) and dy < 0):
                        swipes[3]+= 1

                    if swipes[0] > 3:
                        print "Swiped Left"
                        # self.fi = open('mel_script.mel', 'w')
                        # self.fi.write(?)
                        # self.fi.write('\n')
                        # self.fi.close
                    if swipes[1] > 3:
                        print "Tinder"
                        # self.fi = open('mel_script.mel', 'w')
                        # self.fi.write(?)
                        # self.fi.write('\n')
                        # self.fi.close
                    if swipes[2] > 3:
                        print "Save"
                        # self.fi = open('mel_script.mel', 'w')
                        # self.fi.write(?)
                        # self.fi.write('\n')
                        # self.fi.close
                    if swipes[3] > 6:
                        print "Delete"
                        # self.fi = open('mel_script.mel', 'w')
                        # self.fi.write(?)
                        # self.fi.write('\n')
                        # self.fi.close

            if hand1.pinch_strength > 0.95 and hand2.pinch_strength > 0.95:
                if not self.scaling:
                    self.scaling = True
                    self.init_size = [bone1.next_joint[0] - bone2.next_joint[0], bone1.next_joint[1] - bone2.next_joint[1], bone1.next_joint[2] - bone2.next_joint[2]]
            else:
                self.scaling = False

            if self.scaling:
                end = [bone1.next_joint[0] - bone2.next_joint[0], bone1.next_joint[1] - bone2.next_joint[1], bone1.next_joint[2] - bone2.next_joint[2]]
                temp = [end[0] - self.init_size[0], end[1] - self.init_size[1], end[2] - self.init_size[2]]
                self.write(3, temp)

        #Sleep for 100 milliseconds
        time.sleep(0.10)

    def state_string(self, state):
        if state == Leap.Gesture.STATE_START:
            return "STATE_START"

        if state == Leap.Gesture.STATE_UPDATE:
            return "STATE_UPDATE"

        if state == Leap.Gesture.STATE_STOP:
            return "STATE_STOP"

        if state == Leap.Gesture.STATE_INVALID:
            return "STATE_INVALID"

def main():
    listener = SampleListener()
    controller = Leap.Controller()
    controller.add_listener(listener)

    print "Press Enter to quit..."
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        controller.remove_listener(listener)

if __name__ == "__main__":
    main()
