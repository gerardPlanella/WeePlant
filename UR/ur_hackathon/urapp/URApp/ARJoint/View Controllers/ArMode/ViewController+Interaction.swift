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
import MessageUI
import WebKit
import Foundation

extension ViewController{
    
    func findChildByName(_ name: String) -> SCNNode? {
        return nodeHolder.childNode(withName: name, recursively: true)
    }
    
    @objc func handleRotation(rotationGestureRecognizer: UIRotationGestureRecognizer) {
        
        guard selectedNode != nil,
            let pointOfView = sceneView.pointOfView,
            sceneView.isNode(selectedNode, insideFrustumOf: pointOfView) == true else { return }
        
        if rotationGestureRecognizer.state == .began {
            startingRotation = selectedNode.eulerAngles.y
        } else if rotationGestureRecognizer.state == .changed {
            selectedNode.eulerAngles.y = startingRotation - Float(rotationGestureRecognizer.rotation)
        }
    }
    
    @objc func pinchGesture(_ gesture: UIPinchGestureRecognizer) {
        
        guard selectedNode != nil,
            let pointOfView = sceneView.pointOfView,
            sceneView.isNode(selectedNode, insideFrustumOf: pointOfView) == true else { return }

        let action = SCNAction.scale(by: gesture.scale, duration: 0.1)
        selectedNode.runAction(action)
        gesture.scale = 1
        
    }
    
    //-----------------------
    //MARK: - UserInteraction
    //-----------------------
    override func touchesBegan(_ touches: Set<UITouch>, with event: UIEvent?) {
        
        guard let currentTouchLocation = touches.first?.location(in: self.sceneView),
            let hit = self.sceneView.hitTest(currentTouchLocation, options: nil).first, let string = hit.node.name
            else { return }
        
        if nodeHolder == nil {
            statusViewController.showMessage("No se ha podido detectar la posición de inicio", autoHide: true)
            return
        }
        
        if string.contains("Wall") {
            touchWall(hit.node)
        } else if string.contains("Joint") {
            guard let char = string.last, let id = Int(String(char)) else {return}
            joinSelected = id + 1
            operations.placeJointInfo = true
        } else if string.contains("more") {
            performSegue(withIdentifier: "webViewer", sender: nil)
        }
        
    }
    
    
    @objc
    func panHandler(_ gesture: UIPanGestureRecognizer) {
        
        guard selectedNode != nil,
            let pointOfView = sceneView.pointOfView,
            sceneView.isNode(selectedNode, insideFrustumOf: pointOfView) == true else { return }
       
        let position = gesture.location(in: sceneView)
        
        if (currentTrackingPosition == nil) {
             currentTrackingPosition = CGPoint(x: position.x , y: position.y )
        }
        
        let deltaX = Float(position.x - currentTrackingPosition!.x)/700
        let deltaY = Float(position.y - currentTrackingPosition!.y)/700
        
        currentTrackingPosition = CGPoint(x: position.x , y: position.y )
        
        selectedNode!.localTranslate(by: SCNVector3Make(deltaX, 0.0, deltaY))
        
        let state = gesture.state
        
        if (state == .failed || state == .cancelled) {
            return
        }
        
        
        // Translate virtual object
       // let deltaX = Float(position.x - latestTranslatePos!.x)/700
        //let deltaY = Float(position.y - latestTranslatePos!.y)/700
        
        //selectedNode!.localTranslate(by: SCNVector3Make(deltaX, 0.0, deltaY))
        
        
        
    
    }
    
}

