//
//  ViewController+EditMode.swift
//  URApp
//
//  Created by XavierRoma on 17/03/2019.
//  Copyright © 2019 x.roma_gabriel.cammany. All rights reserved.
//


import UIKit
import ARKit
extension ViewController {
    
    func touchWall(_ wall: SCNNode) {
        changeOpacity(wall, false, "Wall")
        selectedNode = wall
    }
    
    func changeOpacity(_ node: SCNNode,_ defaultOpacity: Bool, _ collection: String) {
        
        node.opacity = CGFloat(defaultOpacity ? settings.robotWallsOpacity:1)
        for nodeC in nodeHolder.childNodes {
            if let string = nodeC.name, string.contains(collection), string != node.name {
                nodeC.opacity = CGFloat(defaultOpacity ? settings.robotWallsOpacity:0.2)
            }
        }
    }
    
}
