//
//  SettingViewController.swift
//  URApp
//
//  Created by XavierRoma on 17/03/2019.
//  Copyright © 2019 x.roma_gabriel.cammany. All rights reserved.
//

import UIKit

class SettingsViewController: UITableViewController {
    
    @IBOutlet weak var robotIP: UITextField!
    @IBOutlet weak var robotPort: UITextField!
    @IBOutlet weak var webURL: UITextField!
    @IBOutlet weak var programingMode: UISwitch!
    @IBOutlet weak var robotWalls: UISwitch!
    @IBOutlet weak var robotWallsOpacity: UISlider!
    @IBOutlet weak var robotWallsOpacityLabel: UILabel!
    @IBOutlet weak var robotJointInfo: UISwitch!
    
    var settings: Settings!
    
    override func viewDidLoad() {
        
        self.navigationController?.isNavigationBarHidden = false
        //self.keyboardDismissMode = UIScrollView.KeyboardDismissMode.onDrag;
    }
    
    override func viewWillDisappear(_ animated: Bool) {
        super.viewWillDisappear(animated)
        settings.robotIP = robotIP.text!
        settings.robotPort = Int(robotPort.text!) ?? settings.robotPort
        settings.webAddress = webURL.text!
        NotificationCenter.default.post(name: .updateNetwork, object: settings)
    }
    
    override func viewWillAppear(_ animated: Bool) {
       
        robotIP.text = settings.robotIP
        robotPort.text = "\(settings.robotPort)"
        webURL.text = settings.webAddress
        programingMode.isOn = settings.programingMode
        robotWalls.isOn = settings.robotWalls
        robotWallsOpacity.value = Float(settings.robotWallsOpacity)
        robotWallsOpacityLabel.text = "\(settings.robotWallsOpacity)"
        robotJointInfo.isOn = settings.robotJoints
       
        
        self.navigationController?.isNavigationBarHidden = false
    }
    
    @IBAction func viewLimitsAction(_ sender: Any) {
        NotificationCenter.default.post(name: .showWalls, object: robotWalls.isOn)
    }
    
    @IBAction func modeProgramingAction(_ sender: Any) {
        NotificationCenter.default.post(name: .showProgramMode, object: programingMode.isOn)
    }
    
    @IBAction func showRobotsJointsInfoAction(_ sender: Any) {
        NotificationCenter.default.post(name: .showRobotJointInfo, object: robotJointInfo.isOn)
    }
    @IBAction func wallsOpacitySlideAction(_ sender: Any) {
        settings.robotWallsOpacity = round(Double(robotWallsOpacity.value))
        robotWallsOpacityLabel.text = "\(settings.robotWallsOpacity)"
        NotificationCenter.default.post(name: .updateOpacity, object: settings.robotWallsOpacity)
    }
    
}
