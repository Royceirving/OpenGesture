import argparse
from opengesture import OpenGesture

if __name__ == "__main__":

    parser = argparse.ArgumentParser("OpenGesture",description="Tool that uses your computers camera to input gestures to your computer and create action shortcuts")
    parser.add_argument("--verbose","-v",action=argparse._StoreTrueAction,required=False,help="Enable verbose output")
    parser.add_argument("--camera","-c",required=False,default=0,help="Index of camera to use",type=int)
    args = parser.parse_args()
    print(args)
    OpenGesture(verbose=args.verbose,capture_device=args.camera).run()