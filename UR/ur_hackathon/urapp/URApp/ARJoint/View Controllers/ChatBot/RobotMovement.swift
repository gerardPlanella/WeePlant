//
//  RobotMovement.swift
//  speech_hack
//
//  Created by Guillem Garrofé Montoliu on 15/02/2019.
//  Copyright © 2019 Guillem Garrofé Montoliu. All rights reserved.
//

import Foundation

class RobotMovement {
    
    public var positions: Array<String>
    
    init (_ positions: Array<String>) {
        self.positions = positions
    }
    
    func setPositions(_ positions: Array<String>) {
        self.positions.removeAll()
        self.positions.append(contentsOf: positions)
    }
    
}
