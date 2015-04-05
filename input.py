import sys, thread, time, math, os
sys.path.append(os.path.join("~/Documents/Design/Hackathons/LAHacks/LeapCAD"))
import Leap
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
sys.path.append(os.path.join("~/Documents/Design/Hackathons/LAHacks/LeapCAD/myo-python/sdk/myo.framework"))
import myo
from myo.lowlevel import pose_t, stream_emg
from myo.six import print_
import random 

class SampleListener(Leap.Listener, myo.DeviceListener):
    fi = None
    fist = False
    FPS = 100
    translating = False
    trans_axis = 0
    scaling = False
    scaling_axis = 0
    rotating = False
    last_pos = [0, 0, 0]
    last_size = [0, 0, 0]
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']

    def set_run(self, hub, n):
        hub.run(n, self)

    def on_connect(self, *args):
        if len(args) == 2:
            print_("Connected to Myo")
            args[0].vibrate('short')
            args[0].request_rssi()
        elif len(args) == 1:
            print "Connected to Leap"
            args[0].enable_gesture(Leap.Gesture.TYPE_CIRCLE);
            args[0].enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
            args[0].enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
            args[0].enable_gesture(Leap.Gesture.TYPE_SWIPE);

    def on_pose(self, myo, timestamp, pose):
        # print 'on_pose', pose
        if pose == pose_t.fist:
            self.fist = True
        elif pose == pose_t.fingers_spread or pose == pose_t.rest:
            self.fist = False

    def on_sync(self, myo, timestamp, arm, x_direction):
        print_('synced', arm, x_direction)

    def on_init(self, controller):
        print "Initialized"

    def on_disconnect(self, controller):
        print "Disconnected"

    def on_exit(self, controller):
        print "Closing"

    def write(self, n, vector):
        directory = '/Users/raychen/Library/Preferences/Autodesk/maya/2015-x64/prefs/scriptEditorTemp/'

        if os.path.isdir(directory):
            self.fi = open(directory +'command.py', 'w')
            
            self.fi.write("c_type = %d\npVec = %s \n" % (n, vector))
            self.fi.write("import maya.cmds as cmds\n")
            # self.fi.write("import maya.mel as mel\n")
            self.fi.write("import time\n")
            self.fi.write("def scalar_maker(c_type):\n")
            self.fi.write("    if (c_type == 1):\n")
            self.fi.write("        # TRANSLATE SCALAR\n")
            self.fi.write("        return .03\n")
            self.fi.write("    elif (c_type == 2):\n")
            self.fi.write("        # ROTATE SCALAR\n")
            self.fi.write("        return .1\n")
            self.fi.write("    elif (c_type == 3):\n")
            self.fi.write("        # SCALE SCALAR\n")
            self.fi.write("        return .0001\n")
            self.fi.write("    else:\n")
            self.fi.write("        print 'ERROR: cmd not found %d' % c_type \n")
            self.fi.write("        return 1\n")
            self.fi.write("def command(c_type, pVec):\n")
            self.fi.write("    k = scalar_maker(c_type)\n")
            self.fi.write("    if c_type == 1:\n")
            self.fi.write("        cmds.move(k*pVec[0], k*pVec[1], k*pVec[2], relative=True)\n")
            self.fi.write("    elif c_type == 2:\n")
            self.fi.write("        cmds.rotate(k*pVec[0], k*pVec[1], k*pVec[2], relative=True)\n")
            self.fi.write("    elif c_type == 3:\n")
            self.fi.write("        cmds.scale(k*pVec[0] + 1, k*pVec[1] + 1, k*pVec[2] + 1, relative=True)\n")
            # self.fi.write("def __init__():\n")
            # self.fi.write("    pass")
            self.fi.close
            print self.fist
            print "c_type = %d\npVec = %s \n" % (n, vector)
        else:
            print "directory does not exist"


    def on_frame(self, controller):
        frame = controller.frame()
        swept_angles = []

        written = False
        if len(frame.hands) == 1:
            hand = frame.hands[0]
            finger = hand.fingers[0]
            bone = finger.bone(3)

            if hand.pinch_strength > 0.95 and not self.fist:
            # if self.fist:
                if not self.translating:
                    self.translating = True
                    self.last_pos = [bone.next_joint[0], bone.next_joint[1], bone.next_joint[2]]
            else:
                self.translating = False

            if self.translating and not written:
                end = [bone.next_joint[0], bone.next_joint[1], bone.next_joint[2]]
                temp = [end[0] - self.last_pos[0], end[1] - self.last_pos[1], end[2] - self.last_pos[2]]
                self.last_pos = end
                self.write(1, temp)
                written = True

            # swipes[l,r,u,d]
            swipes = [0,0,0,0]
            
            normals = []
            clockwiseness = 1

            for gesture in frame.gestures():
                if gesture.type == Leap.Gesture.TYPE_CIRCLE:
                    circle = CircleGesture(gesture)
                    # Determine clock direction using the angle between the pointable and the circle normal
                    if circle.pointable.direction.angle_to(circle.normal) <= Leap.PI/2:
                        clockwiseness = -1
                    else:
                        clockwiseness = 1

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
                    if swipes[1] > 3:
                        print "Tinder"
                    if swipes[2] > 3:
                        print "Save"
                    if swipes[3] > 3:
                        print "Menu"

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
                    vector[axis] = clockwiseness * avg_swept_angle
                else:
                    vector[axis] = 0

            if sum(vector) != 0 and not written:
                self.write(2, vector)
                written = True
            elif not written:
                self.write(0, [0, 0, 0])
                written = True

        elif len(frame.hands) == 2:
            hand1 = frame.hands[0]
            hand2 = frame.hands[1]
            finger1 = hand1.fingers[0]
            bone1 = finger1.bone(3)
            finger2 = hand2.fingers[0]
            bone2 = finger2.bone(3)
            
            has_ball = False
            has_cube = False
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
                    if swipes[1] > 3:
                        print "Tinder"
                    if swipes[2] > 3:
                        print "Save"
                    if swipes[3] > 6:
                        print "Delete"

                if gesture.type == Leap.Gesture.TYPE_KEY_TAP:
                    keytap = KeyTapGesture(gesture)
                    if has_ball:
                        self.write(4, [])
                    elif has_cube:
                        self.write(5, [])

            if hand1.pinch_strength > 0.95 and hand2.pinch_strength > 0.95 and not self.fist:
                if not self.scaling:
                    self.scaling = True
                    self.last_size = [abs(bone1.next_joint[0] - bone2.next_joint[0]), abs(bone1.next_joint[1] - bone2.next_joint[1]), abs(bone1.next_joint[2] - bone2.next_joint[2])]
            else:
                self.scaling = False

            for axis in range(0, 3):
                if abs(self.last_size[self.scaling_axis]) < abs(self.last_size[axis]):
                    self.scaling_axis = axis

            #Writing
            if self.scaling and not written:
                end = [abs(bone1.next_joint[0] - bone2.next_joint[0]), abs(bone1.next_joint[1] - bone2.next_joint[1]), abs(bone1.next_joint[2] - bone2.next_joint[2])]
                temp = [end[0] - self.last_size[0], end[1] - self.last_size[1], end[2] - self.last_size[2]]
                for axis in range(0, 3):
                    if self.scaling_axis != axis:
                        temp[axis] = 0
                self.write(3, temp)
                last_size = end
                written = True
            elif not written:
                self.write(0, [0, 0, 0])
                written = True

        elif not written:
            self.write(0, [0, 0, 0])
            written = True
        
        time.sleep(1.0/self.FPS)
        # myo.time.sleep(1/self.FPS)

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
    myo.init()
    hub = myo.Hub()
    hub.set_locking_policy(myo.locking_policy.none)

    listener = SampleListener()
    listener.set_run(hub, 1000)
    controller = Leap.Controller()
    controller.add_listener(listener)

    print "Press Enter to quit..."
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        controller.remove_listener(listener)
        hub.stop(True)

if __name__ == "__main__":
    main()
