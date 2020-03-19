//
//  ViewController+SetUp.swift
//  URApp
//
//  Created by XavierRoma on 17/03/2019.
//  Copyright © 2019 x.roma_gabriel.cammany. All rights reserved.
//

import UIKit
import SceneKit
import ARKit
import MessageUI
import WebKit

extension ViewController{
    
    private func registerGestureRecognizers() {
        
        let rotationGestureRecognizer = UIRotationGestureRecognizer(target: self, action: #selector(handleRotation))
        self.sceneView.addGestureRecognizer(rotationGestureRecognizer)
        
        let gesture = UIPinchGestureRecognizer(target: self, action: #selector(pinchGesture))
        // Set the delegate to ensure this gesture is only used when there are no virtual objects in the scene.
        sceneView.addGestureRecognizer(gesture)
        
        let panGesture = UIPanGestureRecognizer(target: self, action: #selector(panHandler))
        sceneView.addGestureRecognizer(panGesture)
    }
    
    /// Configures & Runs The ARSession
    func setupARSession(){
        
        //1. Setup Our Tracking Images
        guard let trackingImages =
            ARReferenceImage.referenceImages(inGroupNamed: "AR Resources", bundle: nil) else { return }
        
        nodeHolder = nil
        
        
        
        configuration.detectionImages = trackingImages
        configuration.maximumNumberOfTrackedImages = trackingImages.count
        configuration.worldAlignment = .gravityAndHeading;
        configuration.planeDetection = [.horizontal]
        if #available(iOS 12.0, *) {
            configuration.environmentTexturing = .automatic
        }
        sceneView.delegate = self
        sceneView.debugOptions = [ .showFeaturePoints ]
        sceneView.session.run(configuration, options: [.resetTracking])
        
        registerGestureRecognizers()
        
        self.statusViewController.scheduleMessage("Find the robot workarea", inSeconds: 1.5, messageType: .planeEstimation)
        self.sceneView.scene.rootNode.addChildNode(self.focusSquare)
        
    }
    
    func restartExperience() {
        operations.isMonitoring = false
        operations.restartExpirience = true
        usleep(10000)
        
        statusViewController.cancelAllScheduledMessages()
        setupARSession()
        if settings.programingMode {
            undoProgramButton.isHidden = true
            crossHair.isHidden = true
            shooterProgramButton.isHidden = true
            zSlider.isHidden = true
            endefectorButton.isHidden = true
            saveButton.isHidden = true
            sliderProgramView.isHidden = true
            confirmPointButton.isHidden = true
            settings.programingMode = false
        }
        settings.robotJoints = false
        settings.visualizeProgram = false
        settings.robotWalls = false
        operations = Operations()
        
        if initRobotCommunication() {
            startAllJointMonitor()
            monitorWalls()
        }
        
        okCalibrateButton.isHidden = false
    }
    
    func setupCamera() {
        guard let camera = sceneView.pointOfView?.camera else {
            fatalError("Expected a valid `pointOfView` from the scene.")
        }
        
        /*
         Enable HDR camera settings for the most realistic appearance
         with environmental lighting and physically based materials.
         */
        camera.wantsHDR = true
        camera.exposureOffset = -1
        camera.minimumExposure = -1
        camera.maximumExposure = 3
    }
    
}


