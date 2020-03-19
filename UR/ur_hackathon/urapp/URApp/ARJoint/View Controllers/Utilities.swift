/*
 See LICENSE folder for this sample’s licensing information.
 
 Abstract:
 Utility functions and type extensions used throughout the projects.
 */

import Foundation
import ARKit

// MARK: - float4x4 extensions

extension float4x4 {
    /**
     Treats matrix as a (right-hand column-major convention) transform matrix
     and factors out the translation component of the transform.
     */
    var translation: float3 {
        get {
            let translation = columns.3
            return float3(translation.x, translation.y, translation.z)
        }
        set(newValue) {
            columns.3 = float4(newValue.x, newValue.y, newValue.z, columns.3.w)
        }
    }
    
    /**
     Factors out the orientation component of the transform.
     */
    var orientation: simd_quatf {
        return simd_quaternion(self)
    }
    
    /**
     Creates a transform matrix with a uniform scale factor in all directions.
     */
    init(uniformScale scale: Float) {
        self = matrix_identity_float4x4
        columns.0.x = scale
        columns.1.y = scale
        columns.2.z = scale
    }
}

// MARK: - CGPoint extensions

extension CGPoint {
    /// Extracts the screen space point from a vector returned by SCNView.projectPoint(_:).
    init(_ vector: SCNVector3) {
        self.init(x: CGFloat(vector.x), y: CGFloat(vector.y))
    }
    
    /// Returns the length of a point when considered as a vector. (Used with gesture recognizers.)
    var length: CGFloat {
        return sqrt(x * x + y * y)
    }
}

class Utilities {
    
    static func cleanSimpleString(str: String) -> [String] {
        if str.count == 0 || str == "-1" {
            return []
        }
        var numbers = [String]()
        var aux = String()
        for c in str {
            if c == "," {
                numbers.append(aux)
                aux = String()
            } else if c != " " && c != "[" && c != "]" {
                aux.append(c)
            }
        }
        return numbers
    }
    
    static func cleanString(str: String) -> [[String]] {
        if str.count == 0 || str == "-1" {
            return []
        }
        var scope = 0
        var numbers = [[String]]()
        var aux = String()
        var flag = false
        var opened = 0
        for c in str {
            if c == "[" {
                opened += 1
                if ( opened == 2) {
                    numbers.append([String]())
                }
            } else if c == "]" {
                opened -= 1
                if (opened == 1) {
                    numbers[scope].append(aux)
                    flag = true
                    scope += 1
                    aux = ""
                }
            } else if c == "," {
                if !flag {
                    numbers[scope].append(aux)
                } else {
                    flag = false
                }
                aux = ""
            } else if c != " " {
                aux.append(c)
            }
            
        }
        return numbers
    }
    
    static func robotToARCoord(robot_position: SCNVector3) -> SCNVector3 {
        
        return SCNVector3(
            robot_position.x * -1 - 0.1325,
            robot_position.z + 0.385,
            robot_position.y - 0.2745)
    }
    
    static func ARToRobotCoord(ar_position: SCNVector3) -> SCNVector3 {

        return SCNVector3(
            ar_position.x * -1 - 0.1325,
            ar_position.z + 0.2745,
            ar_position.y - 0.385)
    }

}
