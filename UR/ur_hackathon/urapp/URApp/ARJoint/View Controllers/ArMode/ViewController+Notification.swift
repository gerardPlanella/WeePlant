//
//  ViewController+Notification.swift
//  URApp
//
//  Created by XavierRoma on 27/03/2019.
//  Copyright © 2019 x.roma_gabriel.cammany. All rights reserved.
//

import Foundation
import ARKit


extension ViewController {

    func setUpNotifications () {
        NotificationCenter.default.addObserver(self, selector: #selector(showWalls), name: .showWalls, object: nil)
        NotificationCenter.default.addObserver(self, selector: #selector(showProgramMode), name: .showProgramMode, object: nil)
        NotificationCenter.default.addObserver(self, selector: #selector(showCurrentProgram), name: .showCurrentProgram, object: nil)
        NotificationCenter.default.addObserver(self, selector: #selector(updateOpacity), name: .updateOpacity, object: nil)
        NotificationCenter.default.addObserver(self, selector: #selector(showRobotJointInfo), name: .showRobotJointInfo, object: nil)
        NotificationCenter.default.addObserver(self, selector: #selector(recalibratePosition), name: .recalibratePosition, object: nil)
        NotificationCenter.default.addObserver(self, selector: #selector(updateNetwork), name: .updateNetwork, object: nil)
    }
    
    @objc func showWalls(notification: Notification) {
        
        if let isOn = notification.object as? Bool {
            settings.robotWalls = isOn
            self.operations.isWallChanging = true
        }
    }
    
    @objc func updateNetwork(notification: Notification) {
        
        if let new_settings = notification.object as? Settings {
            
            settings.robotIP = new_settings.robotIP
            settings.robotPort = new_settings.robotPort
            settings.webAddress = new_settings.webAddress
        }
    }
    
    @objc func showRobotJointInfo(notification: Notification) {
        
        if !isAvailable() {
            return
        }
        
        if let isOn = notification.object as? Bool {
            settings.robotJoints = isOn
            self.operations.isJointMonitoring = isOn
            self.operations.startJointsMonitor = isOn
            self.operations.stopJointsMonitor = !isOn
            
        }
    }
    
    
    @objc func showProgramMode(notification: Notification) {
        
        if !isAvailable() {
            return
        }
        
        if let isOn = notification.object as? Bool {
            self.settings.programingMode = isOn
            self.operations.isInProgramMode = isOn
            undoProgramButton.isHidden = !isOn
            crossHair.isHidden = !isOn
            shooterProgramButton.isHidden = !isOn
            zSlider.isHidden = !isOn
            endefectorButton.isHidden = !isOn
            saveButton.isHidden = !isOn
            sliderProgramView.isHidden = !isOn
            confirmPointButton.isHidden = !isOn
            
        }
    }
    
    @objc func showCurrentProgram(notification: Notification) {
        
        if !isAvailable() {
            return
        }
        
         if let isOn = notification.object as? Bool {
            self.settings.visualizeProgram = isOn
            self.operations.isShowingCurrentProgram = isOn
            
        }
    }
    
    @objc func updateOpacity(notification: Notification) {
        
        if !isAvailable() {
            return
        }
        
         if let opacity = notification.object as? Double {
            self.settings.robotWallsOpacity = opacity
            self.operations.isUpdatingOpacity = true
        }
    }
    
    @objc func recalibratePosition(notification: Notification) {
        self.operations.isSettingPosition = true
        okCalibrateButton.isHidden = false
    }
    
    func isAvailable () -> Bool {
        
        if nodeHolder == nil {
           
            return false
        }
        
        return true
    }
    
    

}

extension Notification.Name {
    static let showWalls = Notification.Name("showWalls")
    static let showProgramMode = Notification.Name("showProgramMode")
    static let showCurrentProgram = Notification.Name("showCurrentProgram")
    static let updateOpacity = Notification.Name("updateOpacity")
    static let showRobotJointInfo = Notification.Name("showRobotJointInfo")
    static let recalibratePosition = Notification.Name("recalibratePosition")
    static let updateNetwork = Notification.Name("updateNetwork")
}

