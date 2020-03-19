//
//  RobotComunication.swift
//  speech_hack
//
//  Created by Guillem Garrofé Montoliu on 10/01/2019.
//  Copyright © 2019 Guillem Garrofé Montoliu. All rights reserved.
//

import SwiftSocket

class RobotComunication {
    //let ip = "127.0.0.1"
    let ip = "192.168.1.40"
    //let ip = "10.0.47.136"
    let port = 30002
    let port_data = 30100
    let port_comm = 29999
    let port_alexa = 30102
    //let serverPort = 30040
    
    let positions = ["[-0.123, -0.179, 0.441, 2.031, -1.836, 0.498]", "[-0.088, -1, 0.377, 2.031, -1.836, 0.498]", "[-0.42385, 0.18968, -0.17430, 1.31170, 2.84970, 0.068]", "[-0.123, -0.179, 0.441, 2.031, -1.836, 0.498]", "[0.2, 0, -1.57, 0, 0, -2]"]
    
    //var positions = Array<String>()
    var client: TCPClient
    var data: TCPClient
    var commands: TCPClient
    var alexa: TCPClient
    //var server: TCPServer
    var init_succeed = false
    
    init() {
        client = TCPClient(address: ip, port: Int32(port))
        data = TCPClient(address: ip, port: Int32(port_data))
        commands = TCPClient(address: ip, port: Int32(port_comm))
        alexa = TCPClient(address: ip, port: Int32(port_alexa))
        
        
    }
    
    func initCommunication() -> Bool {
        close()
        connect()
        return init_succeed
    }
    
    func close() {
        client.close()
        data.close()
        commands.close()
    }
    
    func connect(){
        switch client.connect(timeout: 10) {
        case .success:
            print("Client connected to \(ip) : \(port)")
            init_succeed = true
            break
            
        case .failure(let error):
            print("Error: \(error)")
            init_succeed = false
            break
        }
        
        switch data.connect(timeout: 10) {
        case .success:
            print("Data connected to \(ip) : \(port_data)")
            init_succeed = true
            break
            
        case .failure(let error):
            print("Error: \(error)")
            init_succeed = false
            break
        }
        
        switch commands.connect(timeout: 10) {
        case .success:
            print("Commands connected to \(ip) : \(port_comm)")
            init_succeed = true
            break
            
        case .failure(let error):
            print("Error: \(error)")
            init_succeed = false
            break
        }
        
        
    }
    
    func sendAlexa(_ msg: String) {
        switch alexa.connect(timeout: 10) {
        case .success:
            print("Connected to \(ip) : \(port_alexa)")
            print(msg)
            alexa.send(string: msg)
            alexa.close()
            break
            
        case .failure(let error):
            print("Error: \(error)")
            init_succeed = false
            break
        }
        
    }
    
    func send(_ msg: String) {
        switch client.send(string: msg) {
        case .success:
            print("Message sent: \(msg)")
            break
            
        case .failure(let error):
            close()
            connect()
            print("Error send: \(error)")
            break
        }
    }
    
    func sendData(_ msg: String) {
        switch data.send(string: msg) {
        case .success:
            print("Message sent: \(msg)")
            break
        case .failure(let error):
            close()
            connect()
            print("Error send data: \(error)")
            break
        }
    }
    
    func sendCommand(_ msg: String) {
        switch commands.send(string: msg) {
        case .success:
            print("Command sent: \(msg)")
            break
            
        case .failure(let error):
            close()
            connect()
            print("Error send command: \(error)")
            break
        }
    }
    
    func recvData() -> String {
        let response = data.read(1024)
        var resp: String = ""
        if (response != nil) {
            resp = String(bytes: response! , encoding: .utf8)!
        }
        return resp
    }

    func recvRawData() -> NSData {
        guard let bytes = data.read(1024) else {return NSData()}
        return NSData(bytes: bytes, length: bytes.count)
        
    }
    
    func movel_to(_ position: Position) {
        stopMovement()
        send("movel(\(position.position), a=\(position.acc), v=\(position.vel), t=\(position.time), r=\(position.radius))\n")
    }
    
    func moveg_to(_ position: Position) {
        stopMovement()
        send("movel(\(position.position), a=\(position.acc), v=\(position.vel), t=\(position.time), r=\(position.radius))\n")
    }
    
    func movej_to(_ position: Position) {
        stopMovement()
        send("movej(\(position.position), a=\(position.acc), v=\(position.vel), t=\(position.time), r=\(position.radius))\n")
    }
    
    func freedrive(_ on: Bool) {
        send("move = False\n")
        if(on ) {//}&& !freeDrive) {
            send("def P():\n")
            send("  fd = True\n")
            send("  while fd:\n")
            send("      freedrive_mode()\n")
            send("      sleep(0.01)\n")
            send("  end\n")
            send("end\n")
        } else {//if(freeDrive){
            send("fd = False\n")
        }
    }
    
    func servoj_to(_ position: Position) {
        stopMovement()
        send("servoj(\(position.position), a=\(position.acc), v=\(position.vel), t=\(position.time), lookahead_time=\(position.time), gain=\(position.gain))\n")
    }
    
    func servoc_to(_ position: Position) {
        stopMovement()
        send("servoc(\(position.position), a=\(position.acc), v=\(position.vel), r=\(position.radius))\n")
    }
    
    func stopMovement() {
        send("move = False\n")
        self.freedrive(false)
    }
    
}
