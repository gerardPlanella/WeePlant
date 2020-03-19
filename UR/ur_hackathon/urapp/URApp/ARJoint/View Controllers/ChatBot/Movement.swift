//
//  Movement.swift
//  speech_hack
//
//  Created by Guillem Garrofé Montoliu on 11/02/2019.
//  Copyright © 2019 Guillem Garrofé Montoliu. All rights reserved.
//

import Foundation
import UIKit
import CoreData

class Movement {
    
    public static let MOVE_DEFAULT = "1"
    public static let DANCE = "2"
    public static let MOVE_DIRECTION = "3"
    public static let FREEDRIVE = "4"
    public static let STOP = "5"
    public static let SAVE_POSITION = "6"
    public static let GET_MOVEMENTS = "7"
    public static let DO_MOVEMENT = "8"
    public static let START_PROGRAMMING = "9"
    public static let PROGRAM_NAME = "10"
    public static let SHOW_WALLS = "11"
    public static let HIDE_WALLS = "12"
    public static let VENTOSA_ON = "13"
    public static let VENTOSA_OFF = "14"
    public static let CONTINUA = "15"
    public static let PAUSA = "16"
    public static let ESPERA = "17"
    public static let DATA = "18"
    public static let SMALL_TALK = "19"
    public static let LOGIN = "20"
    
    public static let DIRECTION_UP = "arriba"
    public static let DIRECTION_DOWN = "abajo"
    public static let DIRECTION_RIGHT = "derecha"
    public static let DIRECTION_LEFT = "izquierda"
    public static let DIRECTION_STRAIGHT = "delante"
    public static let DIRECTION_BACK = "atrás"
    public static let DIRECTION_WAIT = "espera"
    
    public static let AMMOUNT_MUCH = "mucho"
    public static let AMMOUNT_LITTLE = "poco"
    public static let AMMOUNT_DEFAULT = "default"
    
    public static let JOINT_BASE = "base"
    public static let JOINT_WRIST = "muñeca"
    public static let JOINT_ELBOW = "codo"
    public static let JOINT_SHOULDER = "hombro"
    
    public static let DATA_TEMP = "temperatura"
    public static let DATA_VOLT = "tension"
    public static let DATA_CORR = "corriente"
    
    public static let SMTLK_TIEMPO = "tiempo"
    public static let SMTLK_TRAFICO = "trafico"
    public static let SMTLK_NOTICIAS = "noticias"
    public static let SMTLK_CANCION = "cancion"
    public static let SMTLK_STORY = "historia"
    public static let SMTLK_RADIO = "radio"
    
    var smalltalk = ["tiempo": "weather",
                     "trafico": "traffic",
                     "radio": "radio",
                     "cancion": "singasong",
                     "historia":  "tellstory",
                     "noticias":  "flashbriefing"]
    
    
    private var com: RobotComunication
    
    var appDelegate: AppDelegate!
    var context: NSManagedObjectContext!
    
    private var programming: Bool
    private var loaded: Bool
    private var programName: String?
    private var ventosaStatus: Bool
    private var programInstructions: Array<(Bool, Int, String)>?
    
    let dance_poses = ["[-2.52, -2.26, -0.22, -1.42, -0.06, 0.77]",
                       "[-2.49, -2.19, 1.25, -1.42, -0.06, 0.77]",
                       "[-2.52, -2.26, -0.22, -1.42, -0.06, 0.77]",
                       "[-2.49, -2.19, 1.25, -1.42, -0.06, 0.77]",
                       "[-0.93, -1.94, -1.68, -3.06, -1.49, 0.89]"]
    
    init (_ com: RobotComunication) {
        self.com = com
        self.programming = false
        self.loaded = false
        self.programName = nil
        self.ventosaStatus = false
        self.programInstructions = Array<(Bool, Int, String)>()
        
        appDelegate = UIApplication.shared.delegate as? AppDelegate
        context = appDelegate.persistentContainer.viewContext
    }
    
    func dance() {
        loadProgram("mambo2.urp")
        
    }
    
    func stopMovement() {
        com.send("move = False\n")
    }
    
    func originPoint() {
        com.movej_to(Position("[-1.58, -1.06, -1.2, -1.54, 1.59, 0.775]"))
    }
    
    func freedrive() {
        com.freedrive(true)
    }
    
    func stopFreedrive() {
        com.freedrive(false)
    }
    
    func moveRight(ammount: String) {
        var amm = 0.1
        
        if Int(ammount) != nil {
            amm = Double(Int(ammount)!) / 100.0
        }
        
        amm = (ammount == Movement.AMMOUNT_MUCH) ? 0.3 :
            (ammount == Movement.AMMOUNT_LITTLE) ? 0.05 : amm
        
        com.movej_to(Position("pose_add(get_actual_tcp_pose(), p[\(amm), 0, 0, 0, 0, 0])"))
        print("moving right")
    }
    
    func moveLeft(ammount: String) {
        
        var amm = -0.1
        
        if Int(ammount) != nil {
            amm = Double(Int(ammount)!) / -100.0
        }
        
        amm = (ammount == Movement.AMMOUNT_MUCH) ? -0.3 :
            (ammount == Movement.AMMOUNT_LITTLE) ? -0.05 : amm
        
        com.movej_to(Position("pose_add(get_actual_tcp_pose(), p[\(amm), 0, 0, 0, 0, 0])"))
        print("moving left")
    }
    
    func moveUp(ammount: String) {
        var amm = 0.1
        
        if Int(ammount) != nil {
            amm = Double(Int(ammount)!) / 100.0
        }
        
        amm = (ammount == Movement.AMMOUNT_MUCH) ? 0.3 :
            (ammount == Movement.AMMOUNT_LITTLE) ? 0.05 : amm
        
        com.movej_to(Position("pose_add(get_actual_tcp_pose(), p[0, 0, \(amm), 0, 0, 0])"))
        print("moving up")
    }
    
    func moveDown(ammount: String) {
        var amm = -0.1
        
        if Int(ammount) != nil {
            amm = Double(Int(ammount)!) / -100.0
        }
        
        amm = (ammount == Movement.AMMOUNT_MUCH) ? -0.3 :
            (ammount == Movement.AMMOUNT_LITTLE) ? -0.05 : amm
        
        com.movej_to(Position("pose_add(get_actual_tcp_pose(), p[0, 0, \(amm), 0, 0, 0])"))
        print("moving down")
    }
    
    func moveStraight(ammount: String) {
        var amm = -0.1
        
        if Int(ammount) != nil {
            amm = Double(Int(ammount)!) / -100.0
        }
        
        amm = (ammount == Movement.AMMOUNT_MUCH) ? -0.3 :
            (ammount == Movement.AMMOUNT_LITTLE) ? -0.05 : amm
        
        com.movej_to(Position("pose_add(get_actual_tcp_pose(), p[0, \(amm), 0, 0, 0, 0])"))
        print("moving straight")
    }
    
    func moveBack(ammount: String) {
        var amm = 0.1
        
        if Int(ammount) != nil {
            amm = Double(Int(ammount)!) / 100.0
        }
        
        amm = (ammount == Movement.AMMOUNT_MUCH) ? 0.3 :
            (ammount == Movement.AMMOUNT_LITTLE) ? 0.05 : amm
        
        com.movej_to(Position("pose_add(get_actual_tcp_pose(), p[0, \(amm), 0, 0, 0, 0])"))
        print("moving back")
    }
    
    func startMovement(_ poses: Array<(Bool, Int,String)>) {
        
        com.send("def M():\n")
        com.send("  move = True\n")
        com.send("  while move:\n")
        for pose in poses{
            if (pose.0) {
                com.send("set_tool_digital_out(0, False)\n")
                com.send("set_tool_digital_out(1, True)\n")
            } else {
                com.send("set_tool_digital_out(0, True)\n")
                com.send("set_tool_digital_out(1, False)\n")
            }
            
            if (pose.1 == 1) { //moviment normal
                com.movej_to(Position(pose.2))
                com.send("  while is_steady() == False:\n")
                com.send("      sleep(0.01)\n")
                com.send("  end\n")
            } else { //moviment de wait
                com.send("  sleep(\(pose.2))\n")
            }
        }
        com.send("      move = True\n")
        com.send("  end\n")
        com.send("end\n")
    }
    
    func startProgramming() {
        programming = true
    }
    
    func stopProgramming() {
        var order = 1
        
        if (programInstructions != nil) {
            let fr = NSFetchRequest<Mov>(entityName: "Mov")
            let _movements = try! context.fetch(fr)
            
            let movements = Array<Mov>()
            
            for movement in _movements {
                if (movement.name == programName) {
                    context.delete(movement)
                }
                saveContext()
                
            }
            
            for inst in programInstructions! {
                let i = NSEntityDescription.insertNewObject(forEntityName: "Mov", into: context) as! Mov
                i.name = programName
                i.order = Int16(order)
                i.ventosa = inst.0
                if (inst.1 == 1) {
                    //position
                    i.positions = inst.2
                } else {
                    //wait
                    i.time = inst.2
                }
                
                saveContext()
                order += 1
            }
            
            print(movements)
            
            programming = false
            self.programName = nil
            self.ventosaStatus = false
            self.programInstructions = nil
        }
        setVentosa(false)
    }
    
    func isProgramming() -> Bool {
        return self.programming
    }
    
    func isLoaded() -> Bool {
        return self.loaded
    }
    
    func saveName(_ name: String) {
        self.programName = name
    }
    
    func setVentosa(_ status: Bool) {
        self.ventosaStatus = status
        if (status) {
            com.send("set_tool_digital_out(0, False)\n")
            com.send("set_tool_digital_out(1, True)\n")
        } else {
            com.send("set_tool_digital_out(0, True)\n")
            com.send("set_tool_digital_out(1, False)\n")
        }
    }
    
    func saveInstructionWait (time: Int) {
        if (programInstructions == nil) {
            self.programInstructions = Array<(Bool, Int, String)>()
        }
        programInstructions!.append((ventosaStatus, 2, String(time)))
    }
    
    func saveInstructionPosition () -> Bool {
        
        if let pos = getJsonPosition() {
            
            if (programInstructions == nil) {
                self.programInstructions = Array<(Bool, Int, String)>()
            }
            programInstructions!.append((ventosaStatus, 1, pos))
            return true
        } else {
            return false
        }
    }
    
    func saveContext () {
        if context.hasChanges {
            do {
                try context.save()
            } catch {
                let nserror = error as NSError
                fatalError("Unresolved error \(nserror), \(nserror.userInfo)")
            }
        }
    }
    
    func loadProgram(_ program: String) {
        com.sendCommand("load \(program)\n")
        /*usleep(10000)
        let response = com.commands.read(1024)
        var resp: String = ""
        if (response != nil) {
            resp = String(bytes: response! , encoding: .utf8)!
            print("Return robot: \(resp)")
        }*/
        com.sendCommand("play\n")
        loaded = true
    }
    
    func stopProgram() {
        loaded = false
        com.sendCommand("stop\n")
    }
    
    func pauseProgram() {
        com.sendCommand("pause\n")
    }
    
    func continueProgram() {
        com.sendCommand("play\n")
    }
    
    func getJsonPosition() -> String? {
        var text = ""
        var tries = 0
        
        while tries < 1000 {
            com.sendData("actual_q_json")
            let received = com.recvRawData()
            do {
                let array = try (JSONSerialization.jsonObject(with: received as Data) as? [NSNumber])!
                text.append("[")
                var i = 0
                for part in array {
                    i = i + 1
                    text.append(String(part.floatValue))
                    if i != 6 {
                        text.append(", ")
                    }
                }
                text.append("]")
                print("Recived \(text)")
                return text
            } catch  {
                print("Error json \(error)")
                usleep(5000)
                tries += 1
            }
        }
        return nil
        
    }
    
    func smalltalk(_ type: String, _ radio: String) {
        let action = smalltalk[type]
        print("{\"action\":\"\(action ?? "")\",\"value\":\"\(radio)\"}")
        com.sendAlexa("{\"action\":\"\(action ?? "")\",\"value\":\"\(radio)\"}")
    }
    
    func stopAlexa() {
        com.sendAlexa("{\"action\":\"stop\",\"value\":\"\"}")
    }
    
    func sendAlexa(_ message: String) {
        com.sendAlexa(message)
    }
}
