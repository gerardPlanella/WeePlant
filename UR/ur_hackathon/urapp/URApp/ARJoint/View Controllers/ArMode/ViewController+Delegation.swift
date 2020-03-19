//
//  ViewController.swift
//  test
//
//  Created by XavierRoma on 08/03/2019.
//  Copyright © 2019 Salle URL. All rights reserved.
//

import UIKit
import SceneKit
import ARKit
import WebKit

extension ViewController: ARSCNViewDelegate{
    
    func renderer(_ renderer: SCNSceneRenderer, updateAtTime time: TimeInterval) {
        
        DispatchQueue.main.async {
            self.updateFocusSquare(isObjectVisible: false)
        }
        
        if self.operations.startJointsMonitor {
            jointBallsNodesInit()
            self.operations.startJointsMonitor = false
        
        } else if self.operations.stopJointsMonitor {
            jointBallsNodesDestroy()
            self.operations.stopJointsMonitor = false
        }
        
        if self.operations.callibrationEnded {
            self.operations.callibrationEnded = false
            let aux = SCNNode()
            
            for node in nodeHolder.childNodes {
                aux.addChildNode(node)
            }
            let anchor = ARAnchor(transform: nodeHolder.simdTransform)
            sceneView.session.add(anchor: anchor)
            
            nodeHolder.removeFromParentNode()
            aux.transform = nodeHolder.transform
            nodeHolder = nil
            aux.transform.m21 = 0.0
            aux.transform.m22 = 1.0
            aux.transform.m23 = 0.0
            
            
            nodeHolder = aux
            sceneView.scene.rootNode.addChildNode(nodeHolder)
            let ball = SCNSphere(radius: 0.01)
            let newBall = SCNNode(geometry: ball)
            newBall.position = Utilities.robotToARCoord(robot_position:  SCNVector3(0,0,0))
            nodeHolder.addChildNode(newBall)
        }
        
        if (self.operations.isJointMonitoring) {
            
                DispatchQueue.main.async {
                    let data = self.readData()
                    
                    for i in 0...(MAX_JOINTS - 1) {
                        guard let x = Float(data[i].position[0]),
                            let z = Float(data[i].position[2]),
                            let y = Float(data[i].position[1]) else {
                                continue
                        }
                        let pos = Utilities.robotToARCoord(robot_position: SCNVector3(x: x, y: y, z: z))
                        self.jointsBalls[i].transform.m41 = pos.x
                        self.jointsBalls[i].transform.m42 = pos.y
                        self.jointsBalls[i].transform.m43 = pos.z
                        self.jointsBalls[i].geometry?.firstMaterial?.diffuse.contents = data[i].jointColor
                        if (self.joinSelected == i) {
                            self.joint.transform = self.jointsBalls[self.joinSelected].transform
                            self.joint.updateValues(temp: "\(data[self.joinSelected].jointTemp) ºC",
                                current: "\(data[self.joinSelected].jointCurrent) A",
                                voltage: "\(data[self.joinSelected].jointVolatge) V",
                                speed: "\(data[self.joinSelected].jointSpeed) rad/s")
                            self.joint.constraints = [SCNBillboardConstraint()]
                        }
                        
                    }
                }
        }
       
        if (self.operations.placeJointInfo) {
            self.joint.removeFromParentNode()
            self.joint.transform = self.jointsBalls[self.joinSelected].transform
            self.nodeHolder.addChildNode(self.joint)
            self.operations.placeJointInfo = false
        }
        
        if (self.operations.isWallChanging) {
            self.updateWalls()
            self.operations.isWallChanging = false
        }
        if self.operations.isInProgramMode {
            DispatchQueue.main.async {
                
                for operation in self.programOperationsQueue {
                    switch operation {
                    case .create:
                        
                        if self.lastARLine != nil {
                            self.programProgrammingMode.append(self.lastARLine)
                            self.lastARLine = nil
                        }
                        
                        if self.lastARPPoint != nil {
                            if self.lastPPoint != nil {
                                self.programPointsRobotData.append(self.lastPPoint)
                                self.lastPPoint = nil
                            }
                            self.programProgrammingMode.append(self.lastARPPoint)
                            self.lastARPPoint = nil
                        }
                        
                        self.addProgramPoint()
                        
                        break
                        
                    case .update:
                       
                        if self.lastARPPoint != nil && self.programProgrammingMode.last != nil {
                            
                            var pos = self.lastARPPoint.position
                            pos.y = self.nodeHolder.position.y + self.zSlider.value - 0.152
                            
                            self.updateLine(
                                fromPos: self.programProgrammingMode.last!.position,
                                pos: pos)
                        }
                        break
                        
                    case .remove:
                        
                        if self.lastARPPoint != nil {
                            self.lastARPPoint.removeFromParentNode()
                            self.lastARPPoint = self.programProgrammingMode.popLast()
                        }
                        
                        if self.lastARLine != nil {
                            self.lastARLine.removeFromParentNode()
                            self.lastARLine = self.programProgrammingMode.popLast()
                        }
                        
                        break
                        
                    case .confirm:
                        
                        if self.lastARLine != nil {
                            self.programProgrammingMode.append(self.lastARLine)
                            self.lastARLine = nil
                        }
                        
                        if self.lastARPPoint != nil {
                            self.programProgrammingMode.append(self.lastARPPoint)
                            var pos = self.lastARPPoint.position
                            pos.y = self.nodeHolder.position.y + self.zSlider.value - 0.152
                            self.lastARPPoint = nil
                            self.createPoint(atPos: pos)
                        }
                        break
                    }
                }
                
                self.programOperationsQueue.removeAll()
                
            }
        }
        
        if (self.operations.isUpdatingOpacity) {
            for wall in sceneWalls {
                wall.opacity = CGFloat(self.settings.robotWallsOpacity/100)
            }
            self.operations.isUpdatingOpacity = false
        }
        
        if self.operations.restartExpirience {
            
            if nodeHolder != nil {
                
                for node in self.programProgrammingMode {
                    node.removeFromParentNode()
                }
                programProgrammingMode.removeAll()
                for node in sceneWalls {
                    node.removeFromParentNode()
                }
                sceneWalls.removeAll()
                for node in jointsBalls {
                    node.removeFromParentNode()
                }
                for node in nodeHolder.childNodes {
                    node.removeFromParentNode()
                }
                jointBallsNodesDestroy()
                
                nodeHolder.removeFromParentNode()
                
            }
            self.operations.restartExpirience = false
            
        }
        
        
        
        
        
        
        
    }
    
    func renderer(_ renderer: SCNSceneRenderer, didAdd node: SCNNode, for anchor: ARAnchor) {
        
        guard operations.isSettingPosition, let imageAnchor = anchor as? ARImageAnchor
            else { return }
        
        switch imageAnchor.name {
        case "1":
            statusViewController.showMessage("Posición de inicio encontrada!", autoHide: true)
            
            if nodeHolder != nil, nodeHolder.parent != nil {
                nodeHolder.removeFromParentNode()
            }
            
            nodeHolder = SCNNode()
            nodeHolder = node
            nodeHolder.transform.m21 = 0.0
            nodeHolder.transform.m22 = 1.0
            nodeHolder.transform.m23 = 0.0
            
            //nodeHolder.transform.m42 = result.worldTransform.columns.3.y
            let scene = SCNScene(named: "art.scnassets/ship.scn")!
            
            for nodeInScene in scene.rootNode.childNodes as [SCNNode] {
                nodeHolder.addChildNode(nodeInScene)
            }
            
            sceneView.scene.rootNode.addChildNode(nodeHolder)
            break
        default:
            break
        }
    }
    func updateWalls() {
        if settings.robotWalls {
 
            for node in sceneWalls {
                node.opacity = CGFloat(settings.robotWallsOpacity)
                nodeHolder.addChildNode(node)
            }
            
        } else {
            for node in sceneWalls {
                node.removeFromParentNode()
            }
        }
    }
    
    
    
    func addProgramPoint() {
        
        guard let result = sceneView.hitTest(CGPoint(x: screenCenter.x, y: screenCenter.y), types: [.existingPlaneUsingExtent, .featurePoint]).first else { return }
        
        let pos =  SCNVector3(x: result.worldTransform.columns.3.x, y: nodeHolder.position.y + self.zSlider.value - 0.152, z: result.worldTransform.columns.3.z)
        
        createPoint(atPos: pos)
        
    }
    
    func createPoint (atPos: SCNVector3) {
        
        let sphere = SCNSphere(radius: 0.005)
        
        lastARPPoint = SCNNode(geometry: sphere)
        
        lastARPPoint.geometry?.firstMaterial?.diffuse.contents = UIColor.blue
        
        lastARPPoint.position = atPos
        
        let robot_pos = Utilities.ARToRobotCoord(ar_position: sceneView.scene.rootNode.convertPosition(atPos, to: nodeHolder))
        
        lastPPoint = RobotPos(x: String(robot_pos.x), y: String(robot_pos.y), z: String(zSlider.value))
        
        lastPPoint.reproducePosition(com: robotSockets[RobotSockets.comunication.rawValue])
        
        
        if programProgrammingMode.count >= 1 {
            
            let line = lineFrom(vector: (programProgrammingMode.last?.position)!, toVector: lastARPPoint.position)
            lastARLine = SCNNode(geometry: line)
            lastARLine.geometry?.firstMaterial?.diffuse.contents = UIColor.blue
            
            sceneView.scene.rootNode.addChildNode(lastARLine)
            
        }
        //It is important to do this append AFTER the line node is appended
        sceneView.scene.rootNode.addChildNode(lastARPPoint)
        
    }
    
    func updateLine(fromPos: SCNVector3, pos: SCNVector3) {
        if programProgrammingMode.count >= 1 {
            
            if (lastARLine != nil) {
                lastARLine.removeFromParentNode()
            }
            let line = lineFrom(vector: fromPos, toVector: pos)
            lastARLine = SCNNode(geometry: line)
            lastARLine.geometry?.firstMaterial?.diffuse.contents = UIColor.blue
            lastARPPoint.position = pos
            sceneView.scene.rootNode.addChildNode(lastARLine)
            
        }
    }
    
}
