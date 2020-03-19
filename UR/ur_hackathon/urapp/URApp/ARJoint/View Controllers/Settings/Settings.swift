//
//  Settings.swift
//  URApp
//
//  Created by XavierRoma on 17/03/2019.
//  Copyright © 2019 x.roma_gabriel.cammany. All rights reserved.
//

import Foundation
import UIKit
import ARKit

struct Settings {
    
    var robotSpeed = 90.0
    var robotIP = "192.168.1.40"
    var robotPort = 30100
    var robotCommandPort = 30002
    var webAddress = "urportal.sytes.net"
    var syncQrCode = 10
    var programingMode = false
    var robotWalls = false
    var robotWallsOpacity = 50.0
    var robotJoints = false
    var visualizeProgram = false
    var editModeWalls = false
    
}

struct Operations {
    
    // State booleans for the render function
    var isMonitoring = true
    var isJointMonitoring = false
    var isWallChanging = false
    var placeJointInfo = false
    var isShowingCurrentProgram = false
    var isInProgramMode = false
    var isUpdatingOpacity = false
    var isAddingProgramPoint = false
    var isInitialImageDetected = false
    var stopJointsMonitor = false
    var startJointsMonitor = false
    var isSettingPosition = true
    var robotRunTimeMonitoring = false
    var callibrationEnded = false
    
    var restartExpirience = false
    
}

let MAX_JOINTS = 6

struct RobotData {
    var jointData = [JointData](repeating: JointData(), count: MAX_JOINTS)
    
}

struct JointData {
    var jointTemp = ""
    var jointVolatge = ""
    var jointSpeed = ""
    var jointCurrent = ""
    var jointColor = UIColor.white
    var position = [String](repeating: String(), count: 3)
}



