//
//  Position.swift
//  speech_hack
//
//  Created by Guillem Garrofé Montoliu on 05/02/2019.
//  Copyright © 2019 Guillem Garrofé Montoliu. All rights reserved.
//

import Foundation

class Position {
    var position: String
    var acc: String
    var vel: String
    var radius: String
    var time: String
    var gain: String
    
    init(_ position: String) {
        self.position = position
        self.acc = "0.8"
        self.vel = "1.05"
        self.radius = "0"
        self.time = "0"
        self.gain = "300"
    }
    
    init(_ position: Int) {
        self.position = String(position)
        self.acc = "1.4"
        self.vel = "1.05"
        self.radius = "0"
        self.time = "0"
        self.gain = "300"
    }
    
    init(_ position: String, _ acc: String, _ vel: String, _ time: String, _ radius: String, _ gain: String) {
        self.position = position
        self.acc = acc
        self.vel = vel
        self.radius = radius
        self.time = time
        self.gain = gain
    }
    
    init(_ position: String, _ time: String) {
        self.position = position
        self.acc = "1.4"
        self.vel = "1.05"
        self.radius = "0"
        self.time = time
        self.gain = "300"
    }
}
