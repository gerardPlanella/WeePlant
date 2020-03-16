//
//  ProgramOperation.swift
//  URApp
//
//  Created by XavierRoma on 04/04/2019.
//  Copyright © 2019 x.roma_gabriel.cammany. All rights reserved.
//

import Foundation
import ARKit


enum OperationType {
    
    case update
    case create
    case remove
    case confirm
    
}

struct RobotPos {
    var x = ""
    var y = ""
    var z = ""
    var tcpx = "0"
    var tcpy = "-3.14"
    var tcpz = "0"
    var grab = false
    var release = false
    
    
    
    init(x: String, y: String, z: String) {
        self.x = x
        self.y = y
        self.z = z
    }
    
    init(x: String, y: String, z: String, grab: Bool, release: Bool) {
        self.x = x
        self.y = y
        self.z = z
    }
    
    func clone() -> RobotPos {
        return RobotPos(x: x, y: y, z: z, grab: grab, release: release)
    }
    
    func toSCNVector3() -> SCNVector3 {
        return SCNVector3(x: Float(x) ?? 0.0, y: Float(y) ?? 0.0, z: Float(z) ?? 0.0)
    }
    
    func toPosition() -> Position {
        let robpos = Position("p[\(x), \(y), \(z), \(tcpx), \(tcpy), \(tcpz)]")
        robpos.vel = "0.5"
        robpos.acc = "0.5"
        
        return robpos
    }
    
    func reproducePosition(com: RobotMonitoring) {
        let robpos = Position("p[\(x), \(y), \(z), \(tcpx), \(tcpy), \(tcpz)]")
        robpos.vel = "0.5"
        robpos.acc = "0.5"
        
        com.send("def M():\n")
        com.send("  move = True\n")
        com.send("  while move:\n")
        
        
        com.movel_to(robpos)
        
        if grab || release {
            com.send("  while is_steady() == False:\n")
            com.send("      sleep(0.01)\n")
            com.send("  end\n")
        }
        
        if grab {
            com.send("  set_tool_digital_out(1, False)\n")
            com.send("  sleep(0.5)\n")
            com.send("  set_tool_digital_out(0, True)\n")
            com.send("  sleep(0.5)\n")
        }
        
        if release {
            com.send("  set_tool_digital_out(0, False)\n")
            com.send("  sleep(0.5)\n")
            com.send("  set_tool_digital_out(1, True)\n")
            com.send("  sleep(0.5)\n")
        }
        
        com.send("  end\n")
        com.send("end\n")
        print("I'm here")
    }
    
    func reproduceInversePosition(com: RobotMonitoring) {
        let robpos = Position("p[\(x), \(y), \(z), \(tcpx), \(tcpy), \(tcpz)]")
        robpos.vel = "0.5"
        robpos.acc = "0.5"
        
        com.send("def M():\n")
        com.send("  move = True\n")
        com.send("  while move:\n")
        
        com.movel_to(robpos)
        com.send("  while is_steady() == False:\n")
        com.send("      sleep(0.01)\n")
        com.send("  end\n")
        
        //Because is inverse grab will release and release will grab
        if grab {
            com.send("  set_tool_digital_out(0, False)\n")
            com.send("  sleep(0.5)\n")
            com.send("  set_tool_digital_out(1, True)\n")
            com.send("  sleep(0.5)\n")
        } else if release {
            com.send("  set_tool_digital_out(1, False)\n")
            com.send("  sleep(0.5)\n")
            com.send("  set_tool_digital_out(0, True)\n")
            com.send("  sleep(0.5)\n")
        }
        
        
        
        
        com.send("  end\n")
        com.send("end\n")
    }
}
