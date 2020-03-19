//
//  LoginViewController.swift
//  URApp
//
//  Created by XavierRoma on 10/04/2019.
//  Copyright © 2019 x.roma_gabriel.cammany. All rights reserved.
//

import Foundation
import UIKit
import LocalAuthentication
import SwiftSocket
import IJProgressView

class LoginViewController: UIViewController {
    
    @IBOutlet weak var usernameLabel: UITextField!
    
    @IBOutlet weak var passwordLabel: UITextField!
    
    
    var connected = false
  
    override func viewDidLoad() {
       
        
        self.usernameLabel.text = ""
        self.passwordLabel.text = ""
        // Get the local authentication context.
        let context = LAContext()
        
        // Declare a NSError variable.
        var error: NSError?
        
        // Set the reason string that will appear on the authentication alert.
        let reasonString = "Authentication is needed to verify your identity."
        
        // Check if the device can evaluate the policy.
        if context.canEvaluatePolicy(LAPolicy.deviceOwnerAuthenticationWithBiometrics, error: &error) {
            
            [context .evaluatePolicy(LAPolicy.deviceOwnerAuthenticationWithBiometrics, localizedReason: reasonString, reply: { (success: Bool, evalPolicyError: Error?) -> Void in
                if success {
                    DispatchQueue.main.async {
                        self.usernameLabel.text = "xavi"
                        self.passwordLabel.text = "romacastells"
                        self.connected = true
                    }
                }
                else{
                    
                    switch evalPolicyError!._code {
                        
                    case LAError.systemCancel.rawValue:
                        print( "Authentication was cancelled by the user")
                        
                    case LAError.userCancel.rawValue:
                        print( "Authentication was cancelled by the user")
                        
                    default:
                        print("Authentication failed")
                    }
                }
                
            })]
        }
        else{
            
            if (LAError.biometryNotEnrolled.rawValue == 1) {
                print("TouchID not available")
            }
        }
    }
    @IBAction func LogInButtonAction(_ sender: Any) {
        
       
        
        
        if connected {
            //IJProgressView.shared.showProgressView()
             let alexa = TCPClient(address: "192.168.1.40", port: 30102)
             
             switch alexa.connect(timeout: 10) {
             case .success:
             alexa.send(string: "{\"action\":\"login\",\"value\":\"\(String(describing: self.usernameLabel.text))\"}")
             
             alexa.send(string: "{\"action\":\"speak\",\"value\":\"\(String(describing: self.usernameLabel.text)) se ha conectado al Robot\"}")
             alexa.close()
             break
             
             case .failure(let error):
             print("Error: \(error)")
             
             break
             }
            
            performSegue(withIdentifier: "loginOk", sender: nil)
            
        }
        
    }
    
    override func viewWillDisappear(_ animated: Bool) {
        //IJProgressView.shared.hideProgressView()
    }
    
}
