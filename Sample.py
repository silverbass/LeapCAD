import Leap, sys, thread, time, math
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture


class SampleListener(Leap.Listener):
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

        # Enable gestures
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def on_frame(self, controller):
        # Get the most recent frame and report some basic information
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
                print ['t', end[0] - self.init_pos[0], end[1] - self.init_pos[1], end[2] - self.init_pos[2]]
 
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
                    swept_angle = 0
                    if circle.state != Leap.Gesture.STATE_START:
                        previous_update = CircleGesture(controller.frame(1).gesture(circle.id))
                        swept_angle =  (circle.progress - previous_update.progress) * 2 * Leap.PI
                    swept_angles = swept_angles + [swept_angle]

                # if gesture.type == Leap.Gesture.TYPE_SWIPE:
                #     swipe = SwipeGesture(gesture)
                #     print "  Swipe id: %d, state: %s, position: %s, direction: %s, speed: %f" % (
                #             gesture.id, self.state_names[gesture.state],
                #             swipe.position, swipe.direction, swipe.speed)

                # if gesture.type == Leap.Gesture.TYPE_KEY_TAP:
                #     keytap = KeyTapGesture(gesture)
                #     print "  Key Tap id: %d, %s, position: %s, direction: %s" % (
                #             gesture.id, self.state_names[gesture.state],
                #             keytap.position, keytap.direction )


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
                print ['r'] + vector

        #hand gesture for sphere

               # Testing

            tester = [1.0, 44.91178318267466, 57.743819704059696, 70.16927919895994, 34.65348355212118, 10.354287804394628, 23.30137470487314, 36.34202635507951, 44.91178318267466, 10.354287804394628, 13.658626200471023, 27.451934454176808, 57.743819704059696, 23.30137470487314, 13.658626200471023, 15.55379317705879, 70.16927919895994, 36.34202635507951, 27.451934454176808, 15.55379317705879]
            for hand in frame.hands:

                handType = "Left hand" if hand.is_left else "Right hand"

                # print "  %s, id %d, position: %s" % (
                    # handType, hand.id, hand.palm_position)

                # Get the hand's normal vector and direction
                normal = hand.palm_normal
                direction = hand.direction

                # Get arm bone
                arm = hand.arm

                # Get fingers
                x = []
                y = []
                z = []
                distances = []

                for finger in hand.fingers:
                    # print self.finger_names[finger.type()]

                    bone = finger.bone(2)
                    x = x + [bone.next_joint[0]]
                    y = y + [bone.next_joint[1]]
                    z = z + [bone.next_joint[2]]

                for i in range(0, 5):
                    for j in range(0, 5):
                        if i != j:
                            dx = x[i] - x[j] 
                            dy = y[i] - y[j] 
                            dz = z[i] - z[j] 
                            distances = distances + [(dx**2 + dy**2 + dz**2)**0.5]

                dx = hand.fingers[0].bone(2).next_joint[0] - hand.fingers[1].bone(3).next_joint[0]
                dy = hand.fingers[0].bone(2).next_joint[1] - hand.fingers[1].bone(3).next_joint[1]
                dz = hand.fingers[0].bone(2).next_joint[2] - hand.fingers[1].bone(3).next_joint[2]
                distances = distances + [(dx**2 + dy**2 + dz**2)**0.5]

                for d in range(0, 11):
                    distances[d] = distances[d]/distances[0]

                passes = []
                for d in range(0, 10):
                    if (tester[d] * 0.5 < distances[d]) and (tester[d] * 2 > distances[d]):
                        passes = passes + [1]
                    else:
                        passes = passes + [0]

                if sum(passes) > 9:
                    print "PASS"
                else:
                    print "FAIL"

        elif len(frame.hands) == 2:
            hand1 = frame.hands[0]
            hand2 = frame.hands[1]
            finger1 = hand1.fingers[0]
            bone1 = finger1.bone(3)
            finger2 = hand2.fingers[0]
            bone2 = finger2.bone(3)
            if hand1.pinch_strength > 0.95 and hand2.pinch_strength > 0.95:
                if not self.scaling:
                    self.scaling = True
                    self.init_size = [bone1.next_joint[0] - bone2.next_joint[0], bone1.next_joint[1] - bone2.next_joint[1], bone1.next_joint[2] - bone2.next_joint[2]]
            else:
                self.scaling = False

            if self.scaling:
                end = [bone1.next_joint[0] - bone2.next_joint[0], bone1.next_joint[1] - bone2.next_joint[1], bone1.next_joint[2] - bone2.next_joint[2]]
                print ['s', end[0] - self.init_size[0], end[1] - self.init_size[1], end[2] - self.init_size[2]]

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
    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        # Remove the sample listener when done
        controller.remove_listener(listener)


if __name__ == "__main__":
    main()
