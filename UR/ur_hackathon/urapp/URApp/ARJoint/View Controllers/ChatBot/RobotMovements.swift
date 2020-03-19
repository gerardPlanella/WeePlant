//
//  RobotMovements.swift
//  speech_hack
//
//  Created by Guillem Garrofé Montoliu on 15/02/2019.
//  Copyright © 2019 Guillem Garrofé Montoliu. All rights reserved.
//

import Foundation

class RobotMovements {
    
    var movements = NSMutableDictionary.init()
    
    init () {
        addMovement("bateria", mov: RobotMovement(["[-3.175, -3.01, -0.15, -1.52, 1.65, 1.6]",
                                                   "[-3.16, -2.62, 0.44, -2.52, 1.54, 1.6]",
                                                   "[-2.44, -2.89, -0.37, -1.4, 1.540, 1.60]",
                                                   "[-1.58, -1.06, -1.2, -1.54, 1.59, 0.775]"]))
        
        addMovement("montaje", mov: RobotMovement(["[-2.63, -2.96, -0.45, -1.32, 1.61, 0]",
                                                   "[-1.78, -2.32, -0.402, -0.408, 1.78, -0.037]",
                                                   "[-0.82, -2.37, -2.22, -0.11, 1.53, 0.046]",
                                                   "[-1.58, -1.06, -1.2, -1.54, 1.59, 0.775]"]))
        
        addMovement("embalaje", mov: RobotMovement(["[-3.2, -2.42, -0.05, -2.34, 1.56, 0.62]",
                                                    "[-2.15, -2.44, -1.7, -0.56, 1.6, 0.8]",
                                                    "[-1.8, -1.99, -1.79, -0.88, 1.53, 0.69]",
                                                    "[-1.34, -2.13, -2.26, -0.32, 1.51, 1.56]"]))
    }
    
    func addMovement(_ movement_id: String, mov: RobotMovement) {
        movements.setValue(mov, forKey: movement_id)
    }
    
    func getMovementsList() -> Array<String>{
        return movements.allKeys as! Array<String>
    }
    
    func getMovement(_ movement_id: String) -> RobotMovement{
        return movements.value(forKey: movement_id) as! RobotMovement
    }
    
    func movementExists(_ movement_id: String) -> Bool {
        return movements.value(forKey: movement_id) != nil
    }
    
}
