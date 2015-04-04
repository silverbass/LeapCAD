import Leap, sys, thread, time
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture


class SampleListener(Leap.Listener):
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

        translating = false
        origin = [0, 0, 0]
        end = [0, 0, 0]

        if len(frame.hands) == 1:
            hand = frame.hands[0]
            finger = hand.fingers[0]
            bone = finger.bone(3)

            if hand.pinch_strength > 0.95 and not translating:
                translating = true
                origin = [bone.next_joint[0], bone.next_joint[1], bone.next_joint[2]]
            else:
                translating = false
            
            end = origin = [bone.next_joint[0], bone.next_joint[1], bone.next_joint[2]]

        elif len(frame.hands) == 2:
            hand1 = frame.hands[0]
            hand2 = frame.hands[1]
            if hand1.pinch_strength > 0.95 and hand2.pinch_strength > 0.95:
                print "scaling"
        else:
            print "..."


        # for hand in frame.hands:

            # handType = "Left hand" if hand.is_left else "Right hand"

            # print "  %s, id %d, position: %s" % (
            #     handType, hand.id, hand.palm_position)

            # # Get the hand's normal vector and direction
            # normal = hand.palm_normal
            # direction = hand.direction

            # Get arm bone
            # arm = hand.arm

            # Get fingers
            # x = []
            # y = []
            # z = []
            # distances = []

            # for finger in hand.fingers:
            #     # print self.finger_names[finger.type()]

            #     bone = finger.bone(2)
            #     x = x + [bone.next_joint[0]]
            #     y = y + [bone.next_joint[1]]
            #     z = z + [bone.next_joint[2]]

            # for i in range(0, 5):
            #     for j in range(0, 5):
            #         if i != j:
            #             dx = x[i] - x[j] 
            #             dy = y[i] - y[j] 
            #             dz = z[i] - z[j] 
            #             distances = distances + [(dx**2 + dy**2 + dz**2)**0.5]

            # dx = hand.fingers[0].bone(2).next_joint[0] - hand.fingers[1].bone(3).next_joint[0]
            # dx = hand.fingers[0].bone(2).next_joint[1] - hand.fingers[1].bone(3).next_joint[1]
            # dx = hand.fingers[0].bone(2).next_joint[2] - hand.fingers[1].bone(3).next_joint[2]
            # distances = distances + [(dx**2 + dy**2 + dz**2)**0.5]

            # avg = sum(distances)/10
            # for d in range(0, 10):
            #     distances[d] = distances[d]/avg

            # passes = []
            # for d in range(0, 10):
            #     if (tester[d] * 0.8 < distances[d]) and (tester[d] * 1.2 > distances[d]):
            #         passes = passes + [1]
            #     else:
            #         passes = passes + [0]

            # if sum(passes) > 9:
            #     print "PASS"
            # else:
            #     print "FAIL"

            # print distances

        # # Get tools
        # for tool in frame.tools:

        #     print "  Tool id: %d, position: %s, direction: %s" % (
        #         tool.id, tool.tip_position, tool.direction)

        # # Get gestures
        for gesture in frame.gestures():
            if gesture.type == Leap.Gesture.TYPE_CIRCLE:
                circle = CircleGesture(gesture)

                # Determine clock direction using the angle between the pointable and the circle normal
                if circle.pointable.direction.angle_to(circle.normal) <= Leap.PI/2:
                    clockwiseness = "clockwise"
                else:
                    clockwiseness = "counterclockwise"

                # Calculate the angle swept since the last frame
                swept_angle = 0
                if circle.state != Leap.Gesture.STATE_START:
                    previous_update = CircleGesture(controller.frame(1).gesture(circle.id))
                    swept_angle =  (circle.progress - previous_update.progress) * 2 * Leap.PI

                print "  Circle id: %d, %s, progress: %f, radius: %f, angle: %f degrees, %s" % (
                        gesture.id, self.state_names[gesture.state],
                        circle.progress, circle.radius, swept_angle * Leap.RAD_TO_DEG, clockwiseness)

            if gesture.type == Leap.Gesture.TYPE_SWIPE:
                swipe = SwipeGesture(gesture)
                print "  Swipe id: %d, state: %s, position: %s, direction: %s, speed: %f" % (
                        gesture.id, self.state_names[gesture.state],
                        swipe.position, swipe.direction, swipe.speed)

        #     if gesture.type == Leap.Gesture.TYPE_KEY_TAP:
        #         keytap = KeyTapGesture(gesture)
        #         print "  Key Tap id: %d, %s, position: %s, direction: %s" % (
        #                 gesture.id, self.state_names[gesture.state],
        #                 keytap.position, keytap.direction )

        #     if gesture.type == Leap.Gesture.TYPE_SCREEN_TAP:
        #         screentap = ScreenTapGesture(gesture)
        #         print "  Screen Tap id: %d, %s, position: %s, direction: %s" % (
        #                 gesture.id, self.state_names[gesture.state],
        #                 screentap.position, screentap.direction )

        # if not (frame.hands.is_empty and frame.gestures().is_empty):
        #     print ""

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
