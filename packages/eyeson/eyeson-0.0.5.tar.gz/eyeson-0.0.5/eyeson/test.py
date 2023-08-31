import argparse
import json
import sys
import requests
import eyeson


def main(argv):
    parser = argparse.ArgumentParser(
        description='Main Test Application')
    parser.add_argument('-f', '--foreground', required=False)
    parser.add_argument('-b', '--background', required=False)
    # parser.add_argument('-a', '--access_token', required=True)
    args = parser.parse_args(argv)


    ec = eyeson.EyesonClient.create_room("jsmith", "MHq3YhoEKWympNuGjTCDi4U4MImSEAkuYwrDuoBA3u")

    # print("access key from room details")
    # print (ec.room_details['access_key'])
    # print("Updating room")
    # ec = eyeson.EyesonClient.get_room('G4Mrs459WW7GjvqHLmWkRWFh')
    # print (ec.room_details)
    # print()


    ec = eyeson.EyesonClient.register_guest('https://app.eyeson.team/?guest=M5kSWGVB7bIInn58KG9Fd0Ri')
    print("Room Details")
    print(ec.room_details)
    print("Access Key")
    print(ec.access_key)

    print('Room2')
    ec2 = eyeson.EyesonClient.get_room('PsuoBoicDLE6tvElheANxmtX')
    print(ec2.room_details)


if __name__ == "__main__":
    main(sys.argv[1:])
