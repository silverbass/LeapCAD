import Leap, sys, thread, time
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture


class SampleListener(Leap.Listener):
    translating = False
    scaling = False
    origin = [0, 0, 0]
    end = [0, 0, 0]
    base = [0, 0, 0]
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

        if len(frame.hands) == 1:
            hand = frame.hands[0]
            finger = hand.fingers[0]
            bone = finger.bone(3)

            if hand.pinch_strength > 0.95:
                if not self.translating:
                    print "TRANSLATING"
                    self.translating = True
                    self.origin = [bone.next_joint[0], bone.next_joint[1], bone.next_joint[2]]
            else:
                self.translating = False

            if self.translating:
                end = [bone.next_joint[0], bone.next_joint[1], bone.next_joint[2]]
                print [end[0] - self.origin[0], end[1] - self.origin[1], end[2] - self.origin[2]]
            # else:
                # print "1 hand(s)"

        elif len(frame.hands) == 2:
            hand1 = frame.hands[0]
            hand2 = frame.hands[1]
            finger1 = hand1.fingers[0]
            bone1 = finger1.bone(3)
            finger2 = hand2.fingers[0]
            bone2 = finger2.bone(3)
            if hand1.pinch_strength > 0.95 and hand2.pinch_strength > 0.95:
                if not self.scaling:
                    print "SCALING"
                    self.scaling = True
                    self.base = [bone1.next_joint[0] - bone2.next_joint[0], bone1.next_joint[1] - bone2.next_joint[1], bone1.next_joint[2] - bone2.next_joint[2]]
                else:
                    self.scaling = False

            if self.scaling:
                end = [bone1.next_joint[0] - bone2.next_joint[0], bone1.next_joint[1] - bone2.next_joint[1], bone1.next_joint[2] - bone2.next_joint[2]]
                print [end[0] - self.base[0], end[1] - self.base[1], end[2] - self.base[2]]
            # else:
                # print "2 hand(s)"
        # else:

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
