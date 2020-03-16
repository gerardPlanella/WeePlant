//
//  RobotMonitoring.swift
//  URApp
//
//  Created by XavierRoma on 27/03/2019.
//  Copyright © 2019 x.roma_gabriel.cammany. All rights reserved.
//

import Foundation
import SwiftSocket


enum information: String {
    typealias RawValue = String
    case timestamp = "timestamp";
    case target_q = "target_q";
    case target_qd = "target_qd";
    case target_qdd = "target_qdd";
    case target_current = "target_current";
    case target_moment = "target_moment";
    case actual_q = "actual_q";
    case actual_qd = "actual_qd";
    case actual_current =  "actual_current";
    case joint_control_output = "joint_control_output";
    case actual_TCP_pose = "actual_TCP_pose";
    case actual_TCP_speed = "actual_TCP_speed";
    case actual_TCP_force = "actual_TCP_force";
    case target_TCP_pose = "target_TCP_pose";
    case target_TCP_speed = "target_TCP_speed";
    case actual_digital_input_bits = "actual_digital_input_bits";
    case joint_temperatures = "joint_temperatures";
    case actual_execution_time = "actual_execution_time";
    case robot_mode = "robot_mode";
    case joint_mode = "joint_mode";
    case safety_mode = "safety_mode";
    case actual_tool_accelerometer = "actual_tool_accelerometer";
    case speed_scaling = "speed_scaling";
    case target_speed_fraction = "target_speed_fraction";
    case actual_momentum = "actual_momentum";
    case actual_main_voltage = "actual_main_voltage";
    case actual_robot_voltage = "actual_robot_voltage";
    case actual_robot_current = "actual_robot_current";
    case actual_joint_voltage = "actual_joint_voltage";
    case actual_digital_output_bits = "actual_digital_output_bits";
    case runtime_state = "runtime_state";
    case get_all_joint_positions = "get_all_joint_positions";
    case joint_temperatures_json = "joint_temperatures_json";
    case get_all_joint_positions_json = "get_all_joint_positions_json";
    case actual_current_json = "actual_current_json";
    case get_walls_json = "get_walls_json";
    case safety_status_bits = "safety_status_bits";
    case safety_status_bits_json = "safety_status_bits_json";
    case get_all_json = "get_all_json";
    case actual_joint_voltage_json = "actual_joint_voltage_json";
    case get_info_json = "get_info_json";
    case get_all_joint_target_positions_json = "get_all_joint_target_positions_json";

}

class RobotMonitoring {
    
    var client: TCPClient
    
    var init_succeed = false
    var isOpen = false
    
    init(_ ip: String,_ port: Int32) {
        client = TCPClient(address: ip, port: port)
        //server = TCPServer(address: ip, port: Int32(serverPort))
        connect()
        
    }
    
    func close() {
        client.close()
        isOpen = false
    }
    
    func connect(){
        switch client.connect(timeout: 10) {
        case .success:
            init_succeed = true
            isOpen = true
            break
            
        case .failure(let error):
            print("Error: \(error)")
            init_succeed = false
            client.close()
            break
        }
    }
    
    func read(_ what: information) -> NSData {
        
        switch client.send(string: what.rawValue) {
        case .success:
            guard let bytes = client.read(4096) else {return NSData()}
            return NSData(bytes: bytes, length: bytes.count)
        case .failure:
            //print("Error \(error)")
            break
        }
        return NSData()
    }
    
    func send(_ msg: String) -> Bool {
        switch client.send(string: msg) {
        case .success:
            return true
        case .failure:
            return false
        }
        return false
    }
    
    func movel_to(_ position: Position) {
        send("move = False\n")
        send("movel(\(position.position), a=\(position.acc), v=\(position.vel), t=\(position.time), r=\(position.radius))\n")
    }
    
    
    
    
}
