//
//  Response.swift
//  speech_hack
//
//  Created by Guillem Garrofé Montoliu on 12/02/2019.
//  Copyright © 2019 Guillem Garrofé Montoliu. All rights reserved.
//



import ApiAI
import Foundation
import CoreData

class Response {
    
    public static let MOVEMENT_ID = "movement-id"
    static let MOVEMENT = "robot-movement"
    static let DIRECTION = "robot-direction"
    static let AMMOUNT = "movement-ammount"
    static let PROGRAM_NAME = "program-name"
    static let ROBOT_JOINT = "robot-joint"
    static let DATA_TYPE = "data-interface"
    static let SMALL_TALK = "smalltalk-keywords"
    static let EMISORES_RADIO = "smalltalk-emisores"
    static let NUM = "number"
    
    var response: AIResponse
    var mov: Movement
    var parameters: NSMutableDictionary
    var movements: RobotMovements
    var vc: ChatViewController
    var name_set = false
    
    var appDelegate: AppDelegate!
    var context: NSManagedObjectContext!
    
    init(_ mov: Movement, _ response: AIResponse, _ movements: RobotMovements, _ vc: ChatViewController) {
        self.mov = mov
        self.response = response
        var parameters_aux =  response.result.parameters as! Dictionary<String, Any>
        parameters = NSMutableDictionary()
        
        for key in parameters_aux.keys {
            let aux = parameters_aux[key] as? AIResponseParameter;
            let value = aux!.stringValue
            parameters.setObject(value, forKey: key as NSCopying)
        }
        
        self.movements = movements
        self.vc = vc
        
        appDelegate = UIApplication.shared.delegate as? AppDelegate
        context = appDelegate.persistentContainer.viewContext
        
        listParameters()
        print(response)
        
    }
    
    func listParameters () {
        print("Listing all the parameters:")
        for (key, value) in parameters {
            print( "\(key): \(value)")
        }
    }
    
    func getParameter(_ param: String) -> String {
        guard let param = parameters[param] else { return "" }
        return param as! String
    }
    
    func hasParameter(_ param: String) -> Bool {
        return (parameters[param] as! String?) != nil
    }
    
    func responseBehaviour() {
        if (hasParameter(Response.MOVEMENT_ID)) {
            
            switch (getParameter(Response.MOVEMENT_ID)) {
            case Movement.MOVE_DEFAULT:
                mov.originPoint()

            case Movement.DANCE:
                mov.dance()
                vc.playSound()
                vc.dancing = true
                
            case Movement.LOGIN:
                if (hasParameter(Response.NUM) && getParameter(Response.NUM) == "3") {
                    mov.sendAlexa("{\"action\":\"login\",\"value\":\"Guillem\"}")
                    mov.sendAlexa("{\"action\":\"speak\",\"value\":\"Guillem se ha conectado al Robot\"}")
                    vc.displayRobotResponse(message: "Conectandome...")
                }

            case Movement.ESPERA:
                if (mov.isProgramming() && !self.saveInstruction()) {
                    vc.displayRobotResponse(message: "Parece que ha habido un error detectándo la instrucción")
                }
                
                
            case Movement.MOVE_DIRECTION:
                self.moveDirection(mov)
                

            case Movement.FREEDRIVE:
                mov.freedrive()
                

            case Movement.PAUSA:
                mov.stopAlexa()
                mov.pauseProgram()
                if vc.dancing == true {
                    vc.player!.pause()
                }
            
            case Movement.CONTINUA:
                mov.continueProgram()
                if (vc.dancing == true) {
                    vc.playSound()
                }

            case Movement.STOP:
                mov.stopAlexa()
                if (mov.isProgramming()) {
                    mov.stopProgramming()
                    
                    let message = response.result.fulfillment.messages[1]["speech"] as! String
                    vc.displayRobotResponse(message: message)
                }else{
        
                    if(mov.isLoaded()) {
                        print("stoping load")
                        mov.stopProgram()
                        if vc.dancing {
                            vc.player!.stop()
                            vc.player!.currentTime = 0
                            vc.dancing = false
                        }
                    }else {
                        print("---> Else de mov.isLoaded")
                        mov.stopFreedrive()
                        mov.stopMovement()
                        mov.setVentosa(false)
                        let message = response.result.fulfillment.messages[0]["speech"] as! String
                        vc.displayRobotResponse(message: message)
                    }
                }
                
                

            case Movement.GET_MOVEMENTS:
                var message = response.result.fulfillment.messages[0]["speech"] as! String
                
                for mov in getMovementsList() {
                    message.append("\n")
                    message.append("- ")
                    message.append(mov.name!)
                }
                
                vc.displayRobotResponse(message: message)
                

            case Movement.SAVE_POSITION:
                
                if mov.saveInstructionPosition() {
                    vc.displayRobotResponse(message: "Posición guardada correctamente")
                } else {
                    vc.displayRobotResponse(message: "No se ha podido guardar la posición")
                }
                

            case Movement.DO_MOVEMENT:
                let movementInstructions = getMovement(name: self.getParameter(Response.MOVEMENT))
                if (movementInstructions.count > 0) {
                    let message = response.result.fulfillment.messages[0]["speech"] as! String
                    vc.displayRobotResponse(message: message)
                    
                    mov.startMovement(movementInstructions)
                    
                } else {
                    print("Movimiento: \(self.getParameter(Response.MOVEMENT))")
                    if (self.getParameter(Response.MOVEMENT) == "") {
                        vc.displayRobotResponse(message: "El movimiento no se ha reconocido")
                    } else {
                        //CARGAR PROGRAMA DEL ROBOT
                        switch(self.getParameter(Response.MOVEMENT)){
                        case "embalaje":
                            mov.loadProgram("phoneBoxing.urp")
                            let message = response.result.fulfillment.messages[0]["speech"] as! String
                            vc.displayRobotResponse(message: message)
                            
                        case "montaje":
                            mov.loadProgram("phoneAssemblyBucle.urp")
                            let message = response.result.fulfillment.messages[0]["speech"] as! String
                            vc.displayRobotResponse(message: message)
                            
                        default:
                            vc.displayRobotResponse(message: "Lo siento, no conozco este programa")
                            print("unknown program to load")
                        }
                    }
                    
                }
                

            case Movement.START_PROGRAMMING:
                mov.startProgramming()
                name_set = false
                if( hasParameter(Response.PROGRAM_NAME) && getParameter(Response.PROGRAM_NAME) != ""){
                    mov.saveName(getParameter(Response.PROGRAM_NAME))
                    vc.displayRobotResponse(message: "El nombre elegido és \(getParameter(Response.PROGRAM_NAME))")
                    name_set = true
                } else {
                    vc.displayRobotResponse(message: "Que nombre quieres poner al programa?")
                }
                

            case Movement.PROGRAM_NAME:
                if !name_set {
                    mov.saveName(getParameter(Response.PROGRAM_NAME))
                    
                    for msg in response.result.fulfillment.messages{
                        if let textResponse = msg["speech"] as? String {
                            vc.displayRobotResponse(message: textResponse)
                        }
                    }
                    
                    name_set = true
                }
                

            case Movement.SHOW_WALLS:
                NotificationCenter.default.post(name: .showWalls, object: true)
                

            case Movement.HIDE_WALLS:
                NotificationCenter.default.post(name: .showWalls, object: false)
                

            case Movement.VENTOSA_ON:
                mov.setVentosa(true)
                

            case Movement.VENTOSA_OFF:
                mov.setVentosa(false)
                

            case Movement.DATA:
                showData()
                

            case Movement.SMALL_TALK:
                if (hasParameter(Response.SMALL_TALK) && getParameter(Response.SMALL_TALK) != "") {
                    if (getParameter(Response.SMALL_TALK) == Movement.SMTLK_RADIO && hasParameter(Response.EMISORES_RADIO)) {
                        
                        mov.smalltalk(getParameter(Response.SMALL_TALK), getParameter(Response.EMISORES_RADIO))
                        vc.showRobotMessage("Mi compañera Alexa te lo dirá")
                    } else if (getParameter(Response.SMALL_TALK) != Movement.SMTLK_RADIO) {
                        
                        mov.smalltalk(getParameter(Response.SMALL_TALK), "")
                        vc.showRobotMessage("Mi compañera Alexa te lo dirá")
                    }
                } else if(hasParameter(Response.EMISORES_RADIO)) {
                    mov.smalltalk(Movement.SMTLK_RADIO, getParameter(Response.EMISORES_RADIO))
                    vc.showRobotMessage("Mi compañera Alexa te lo dirá")
                } else {
                    vc.showRobotMessage("No entiendo lo que quieres")
                }
                

            default:
                print("unknown command")
                vc.showRobotMessage("No te he entendido")
            }
            

        }
    }
    
    
    
    func showData() {
        //TODO get temperatures from robot
        var displayed = false
        if (hasParameter(Response.ROBOT_JOINT) && hasParameter(Response.DATA_TYPE) && getParameter(Response.DATA_TYPE) != "") {
            var retries = 0
            var data = [String]()
            var data_type = ""
            var unit = ""
            
            var rob_data = vc.mainView.readData()
            
            
            data_type = getParameter(Response.DATA_TYPE)
            print(data_type)
            switch (data_type) {
            case Movement.DATA_TEMP:
                data.append(rob_data[0].jointTemp)
                data.append(rob_data[1].jointTemp)
                data.append(rob_data[2].jointTemp)
                data.append(rob_data[3].jointTemp)
                data.append(rob_data[4].jointTemp)
                data.append(rob_data[5].jointTemp)
                unit = "ºC"
            case Movement.DATA_VOLT:
                data.append(rob_data[0].jointVolatge)
                data.append(rob_data[1].jointVolatge)
                data.append(rob_data[2].jointVolatge)
                data.append(rob_data[3].jointVolatge)
                data.append(rob_data[4].jointVolatge)
                data.append(rob_data[5].jointVolatge)
                unit = "V"
            case Movement.DATA_CORR:
                data.append(rob_data[0].jointCurrent)
                data.append(rob_data[1].jointCurrent)
                data.append(rob_data[2].jointCurrent)
                data.append(rob_data[3].jointCurrent)
                data.append(rob_data[4].jointCurrent)
                data.append(rob_data[5].jointCurrent)
                unit = "A"
            default: break
                
            }
            
            /*for (data  ) {
                {
                    NSNumberFormatter *fmt = [[NSNumberFormatter alloc] init];
                    [fmt setPositiveFormat:@"0.##"];
                    NSLog(@"%@", [fmt stringFromNumber:[NSNumber numberWithFloat:25.34]]);
                }
            }*/
            
            if (data.count == 6) {
                displayed = true
                let joint = getParameter(Response.ROBOT_JOINT)
                
                //var test = 0
                switch (joint) {
                case Movement.JOINT_BASE:
                    vc.displayRobotResponse(message: String(format:"La \(data_type) de la base es de \(data[0])\(unit)"));
                case Movement.JOINT_SHOULDER:
                    vc.displayRobotResponse(message: "La \(data_type) del hombro es de \(data[1])\(unit)");
                case Movement.JOINT_ELBOW:
                    vc.displayRobotResponse(message: "La \(data_type) del codo es de \(data[2])\(unit)");
                case Movement.JOINT_WRIST:
                    vc.displayRobotResponse(message: "La \(data_type) de todas las muñecas es la siguiente:")
                    vc.showRobotMessage("La \(data_type) de la muñeca 1 es de \(data[3])\(unit)\n La \(data_type) de la muñeca 2 es de \(data[4])\(unit)\n La \(data_type) de la muñeca 3 es de \(data[5])\(unit)");
                default:
                    //show all
                    vc.displayRobotResponse(message: "La \(data_type) de todos los joints son las siguientes:")
                    vc.showRobotMessage("La \(data_type) de la base es de \(data[0])\(unit)\n La \(data_type) del hombro 2 es de \(data[1])\(unit)\n La \(data_type) del codo es de \(data[2])\(unit)\n La \(data_type) de la muñeca 1 es de \(data[3])\(unit)\n La \(data_type) de la muñeca 2 es de \(data[4])\(unit)\n La \(data_type) de la muñeca 3 es de \(data[5])\(unit)");
                }
                
            }
            
            
            if !displayed {
                vc.displayRobotResponse(message: "No conozco este tipo de dato")
            }
        } else {
            vc.displayRobotResponse(message: "No conozco este tipo de dato")
        }
    }
    
    func moveDirection(_ mov: Movement) {
        var amm = Movement.AMMOUNT_DEFAULT
        if (hasParameter(Response.AMMOUNT)) {
            amm = getParameter(Response.AMMOUNT)
        }
        
        switch (getParameter(Response.DIRECTION)) {
        case Movement.DIRECTION_UP:
            mov.moveUp(ammount: amm)
            
        case Movement.DIRECTION_DOWN:
            mov.moveDown(ammount: amm)
            
        case Movement.DIRECTION_LEFT:
            mov.moveLeft(ammount: amm)
            
        case Movement.DIRECTION_RIGHT:
            mov.moveRight(ammount: amm)
            
        case Movement.DIRECTION_STRAIGHT:
            mov.moveStraight(ammount: amm)
            
        case Movement.DIRECTION_BACK:
            mov.moveBack(ammount: amm)
            
        default:
            print("unknown direction")
            vc.displayRobotResponse(message: "No he entendido a que dirección quieres que me mueva")
        }
    }
    
    
    func getMovementsList() -> Array<Mov> {
        let fr = NSFetchRequest<Mov>(entityName: "Mov")
        let _movements = try! context.fetch(fr)
        
        var movements = Array<Mov>()
        for movement in _movements {
            if (!isRegistered(movements: movements, mov: movement)) {
                movements.append(movement)
            }
        }
        
        return movements
    }
    
    func isRegistered(movements: Array<Mov>, mov: Mov) -> Bool {
        for movement in movements {
            if (movement.name!.caseInsensitiveCompare(mov.name!) == .orderedSame) {
                return true
            }
        }
        return false
    }
    
    func getMovement(name: String) -> Array<(Bool, Int, String)> {
        let fr = NSFetchRequest<Mov>(entityName: "Mov")
        let _movements = try! context.fetch(fr)
        let movOrdered = _movements.sorted(by: {$0.order < $1.order})
        
        var movements = Array<(Bool, Int, String)>()
        for movement in movOrdered {
            if (movement.name!.caseInsensitiveCompare(name) == .orderedSame) {
                if (movement.time != nil) {
                    movements.append((movement.ventosa, 2, "\(movement.time!)"))
                    
                } else {
                    //movements.append((movement.ventosa, 1, "[\(movement.x!), \(movement.y!), \(movement.z!), \(movement.rx!), \(movement.ry!), \(movement.rz!)]"))
                    movements.append((movement.ventosa, 1, movement.positions ?? ""))
                }
            }
        }
        
        return movements
    }
    
    func saveInstruction() -> Bool {
        var amm: String?
        if (hasParameter(Response.AMMOUNT)) {
            amm = getParameter(Response.AMMOUNT)
            if (amm != nil) {
                let num = Int(amm!)
                if (num != nil) {
                    mov.saveInstructionWait(time: num!)
                } else {
                    return false
                }
            } else {
                return false
            }
        }
        return true
    }
    
}
