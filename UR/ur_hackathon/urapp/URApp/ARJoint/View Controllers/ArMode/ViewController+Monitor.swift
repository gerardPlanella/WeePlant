//
//  File.swift
//  URApp
//
//  Created by XavierRoma on 29/03/2019.
//  Copyright © 2019 x.roma_gabriel.cammany. All rights reserved.
//

import Foundation
import ARKit

extension ViewController {
    
    func jointBallsNodesDestroy () {
        
        for joint in jointsBalls {
            joint.removeFromParentNode()
        }
        jointsBalls.removeAll()
        self.joint.removeFromParentNode()
        
    }
    
    func jointBallsNodesInit() {
        for i in 0...(MAX_JOINTS - 1) {
            let node = SCNNode(geometry: SCNSphere(radius: 0.05))
            node.opacity = 0.1
            node.name = "Joint-\(i)"
            jointsBalls.append(node)
            self.nodeHolder.addChildNode(node)
        }
    }
    
    func startAllJointMonitor() {
        DispatchQueue.global(qos: .userInitiated).async {
            while (self.operations.isMonitoring) {
                
                let out =  self.robotSockets[RobotSockets.joints_pos.rawValue].read(information.get_all_joint_positions_json)
                
                do {
                    var json = try JSONSerialization.jsonObject(with: out as Data) as? [[[Any]]]
                    
                    //self.semaphore.wait()
                    for i in 0...MAX_JOINTS - 1 {
                        var j = 0
                        for pos in json?[0][i] as! [NSNumber] {
                            self.data.jointData[i].position[j] = "\(pos)"
                            j += 1
                            if j == 3 {
                                break
                            }
                        }
                    }
                   // self.semaphore.signal()
                   
                    usleep(10000)
                }
                catch {
                    usleep(4000)
                }
            }
        }
        
        DispatchQueue.global(qos: .background).async {
            while (self.operations.isMonitoring) {
                
                let out = self.robotSockets[RobotSockets.info.rawValue]
                    .read(information.get_info_json)
                
                
                do {
                    let json = try JSONSerialization.jsonObject(with: out as Data) as? [[Any]]
                   
                    guard json?[0].count == 6, json?[1].count == 6, json?[2].count == 6, json?[3].count == 6 else {continue}
                    
                    
                    for i in 0...(MAX_JOINTS - 1) {
                        let curr_str = "\(json?[0][i] ?? self.data.jointData[i].jointCurrent)"
                        
                        let temp_str = "\(json?[1][i] ?? self.data.jointData[i].jointTemp)"
                        
                        let volt_str = "\(json?[2][i] ?? self.data.jointData[i].jointVolatge)"
                        
                        let speed_str = "\(json?[3][i] ?? self.data.jointData[i].jointSpeed)"
                        
                        let curr: String!
                        let temp: String!
                        let volt: String!
                        let speed: String!
                        
                        if curr_str.count >= 5 {
                            curr = String(curr_str[curr_str.startIndex ..< (curr_str.index(curr_str.startIndex, offsetBy: 5))])
                        } else {
                            curr = curr_str
                        }
                        
                        if temp_str.count >= 4 {
                            temp = String(temp_str[temp_str.startIndex ..< (temp_str.index(temp_str.startIndex, offsetBy: 4))])
                        } else {
                            temp = temp_str
                        }
                        
                        if volt_str.count >= 5 {
                            volt = String(volt_str[volt_str.startIndex ..< (volt_str.index(volt_str.startIndex, offsetBy: 5))])
                        } else {
                            volt = volt_str
                        }
                        
                        if speed_str.count >= 5 {
                            speed = String(speed_str[speed_str.startIndex ..< (speed_str.index(speed_str.startIndex, offsetBy: 5))])
                        } else {
                            speed = speed_str
                        }
                        
                        let temp_i = Int(Float(temp) ?? 30.0)
                        let color = self.tempBarColor[temp_i > 35 ? temp_i - (temp_i % 3): temp_i + (temp_i % 3)]
                        
                        self.semaphore.wait()
                        
                        self.data.jointData[i].jointCurrent = curr
                        
                        self.data.jointData[i].jointTemp = temp
                        
                        self.data.jointData[i].jointColor = color
                        
                        self.data.jointData[i].jointVolatge = volt
                        
                        self.data.jointData[i].jointSpeed = speed
                        
                        self.semaphore.signal()
                    }
                    
                    
                    usleep(1000000)
                } catch {
                    usleep(10000)
                }
            }
        }
        
    }
    
    func monitorWalls () {
        let client = RobotMonitoring(settings.robotIP, Int32(settings.robotPort))
        client.connect()
        var nothing = true
        if client.init_succeed {
            
            while nothing {
                do {
                    let out = client.read(.get_walls_json) as Data
                    print(out)
                    let json = try JSONSerialization.jsonObject(with: out) as? [[Any]]
                    
                    for wall in json ?? [[]] {
                        let x = Int(roundf(Float("\(wall[0])")!))
                        let y = Int(roundf(Float("\(wall[1])")!))
                        let z = Int(roundf(Float("\(wall[2])")!))
                        let distance = Float("\(wall[3])")
                        
                        let wall = SCNNode()
                        
                        if  x == 1 || x == -1 {
                            wall.position.x = distance!
                            wall.position.z += 1
                            wall.geometry = SCNBox(width: 0.02, height: 2, length: 2, chamferRadius: 0)
                        } else if y == 1 || y == -1 {
                            wall.position.y = distance!
                            wall.position.z += 0.7
                            wall.geometry = SCNBox(width: 2, height: 2, length: 0.02, chamferRadius: 0)
                        } else if z == 1 || z == -1 {
                            wall.position.z = distance!
                            wall.geometry = SCNBox(width: 1, height: 0.02, length: 1, chamferRadius: 0)
                        }
                        wall.position = Utilities.robotToARCoord(robot_position: wall.position)
                        wall.geometry?.firstMaterial?.diffuse.contents = UIColor.red
                        wall.opacity = CGFloat(settings.robotWallsOpacity/100)
                        sceneWalls.append(wall)
                    }
                    
                    nothing = false
                    operations.isWallChanging = true
                } catch {
                    usleep(1000000)
                }
                
            }
            client.close()
        }
        
    }
    
}
