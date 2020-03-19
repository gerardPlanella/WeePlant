//
//  ChatViewController.swift
//  URApp
//
//  Created by XavierRoma on 26/03/2019.
//  Copyright © 2019 x.roma_gabriel.cammany. All rights reserved.
//

import UIKit
import Speech
import ApiAI
import AVFoundation

struct ChatMessage {
    let text: String
    let isIncoming: Bool
}

class ChatViewController: UIViewController, UITableViewDataSource, UITableViewDelegate,SFSpeechRecognizerDelegate, ChatProtocol{
    
    @IBOutlet weak var labelVeu: UILabel!
    @IBOutlet weak var microphoneButton: UIButton!
    @IBOutlet weak var labelResponse: UILabel!
    var textInput: String!;
    
    @IBOutlet var tableView: UITableView!
    private let speechStynthesizer = AVSpeechSynthesizer()
    private let speechRecognizer = SFSpeechRecognizer(locale: Locale.init(identifier: "es-ES"))
    private var recognitionRequest: SFSpeechAudioBufferRecognitionRequest?
    private var recognitionTask: SFSpeechRecognitionTask?
    private var audioEngine = AVAudioEngine()
    var chatProtocol: ChatProtocol?
    fileprivate let cellId = "id"
    private var mov: Movement!
    var com: RobotComunication!
    private var movements: RobotMovements = RobotMovements()
    var player: AVAudioPlayer?
    var test: String!
    var dancing = false
    var mainView: ViewController!
    var chatMessages = [
        ChatMessage(text: "Estoy aquí para ayudarte. ¿Qué necesitas?", isIncoming: true),
        ]
    
    
    var interactionAction: (() -> ())?
    
    @IBAction func actionButtonPressed(_ sender: Any) {
        if let interactionAction = interactionAction {
            interactionAction()
        } else {
            self.dismiss(animated: true, completion: nil)
        }
    }
    
    override var prefersStatusBarHidden: Bool {
        return true
    }
    
    func initRobotCommunication() -> Bool {
        com = RobotComunication()
        let status = com.initCommunication()
        mov = Movement(com)
        return status
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        modalPresentationCapturesStatusBarAppearance = true
        
        navigationItem.title = "UR Chatbot"
        navigationItem.largeTitleDisplayMode = .always
        navigationController?.navigationBar.prefersLargeTitles = true;
        tableView.register(ChatMessageCell.self, forCellReuseIdentifier: cellId);
        
        tableView.backgroundColor = UIColor(white: 0.95, alpha: 1);
        tableView.separatorStyle = .none;
        
        microphoneButton.layer.cornerRadius = 10
        microphoneButton.isEnabled = true
        
        speechRecognizer?.delegate = self
        
        
        initSound("mambo")
        print(test)
        
        
    }
    
    @IBAction func clearMessages(_ sender: Any) {
        chatMessages = [
            ChatMessage(text: "Estoy aquí para ayudarte. ¿Qué necesitas?", isIncoming: true),
        ]
        tableView.reloadData()
        
        let indexPath = IndexPath(row: 0, section: 0)
        tableView.scrollToRow(at: indexPath, at: .top, animated: false)
        
        microphoneButton.isEnabled = true
    }
    
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return chatMessages.count;
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCell(withIdentifier: cellId, for: indexPath) as! ChatMessageCell;
        
        let chatMessage = chatMessages[indexPath.row];
        cell.chatMessage = chatMessage;
        return cell;
    }
    
    @IBAction func microphoneClick(_ sender: Any) {
            microphoneButton.backgroundColor = UIColor.gray
            microphoneButton.setTitle("Escuchando...", for: .normal)
            startRecording()
    }
    
    @IBAction func microphoneReleased(_ sender: Any) {
        if (self.microphoneButton != nil) {
            UIView.animate(withDuration: 0.25, animations: {
                self.microphoneButton.transform = CGAffineTransform(scaleX: 0.98, y: 0.98)
            }, completion: { _ in
                UIView.animate(withDuration: 0.25, animations: {
                    self.microphoneButton.transform = CGAffineTransform.identity
                }, completion: { _ in
                    UIView.animate(withDuration: 0.25, animations: {
                        self.microphoneButton.transform = CGAffineTransform(scaleX: 0.98, y: 0.98)
                    }, completion: { _ in
                        UIView.animate(withDuration: 0.25) {
                            self.microphoneButton.transform = CGAffineTransform.identity
                        }
                    })
                })
            })
        }
        
        if (self.microphoneButton != nil && audioEngine.isRunning) {
            let delayTime = DispatchTime.now() + .seconds(1)
            DispatchQueue.main.asyncAfter(deadline: delayTime) {
                self.audioEngine.stop()
                self.audioEngine.inputNode.removeTap(onBus: 0) // soluciona el problema de presionar repetidamente el boton de escuchar
                
                self.microphoneButton.backgroundColor = UIColor(red: 0, green: 150.0 / 255.0, blue: 1, alpha: 1)
                self.microphoneButton.setTitle("Escuchar", for: .normal)
                
                self.recognitionRequest?.endAudio()
                
                //Si hi ha algun missatge nou, es començarà el procés de
                if let text = self.textInput, text != "" {
                    self.chatMessages.append(ChatMessage(text: self.textInput, isIncoming: false))
                    self.tableView.reloadData()
                    let ip = NSIndexPath(row: self.chatMessages.count - 1, section: 0)
                    self.tableView.scrollToRow(at: ip as IndexPath, at: .bottom, animated: false)
                    
                    self.sendMessage(text)
                } else {
                    self.playMessage("Te escucho")
                }
            }
        } else {
            print("AUDIO ENGINE IS NOT RUNNING")
            self.audioEngine.stop()
            self.audioEngine.inputNode.removeTap(onBus: 0)
            self.microphoneButton.backgroundColor = UIColor(red: 0, green: 150.0 / 255.0, blue: 1, alpha: 1)
            self.microphoneButton.setTitle("Escuchar", for: .normal)
            self.recognitionRequest?.endAudio()
        }
        
    }
    
    
    func sendMessage(_ text: String) {
        let request = ApiAI.shared().textRequest()
        request?.query = text
        
        request?.setMappedCompletionBlockSuccess({ (request, response) in
            let response = response as! AIResponse
            
            let resp = Response(self.mov, response, self.movements, self)
            for msg in response.result.fulfillment.messages{
                if let textResponse = msg["speech"] as? String {
                    if (resp.hasParameter(Response.MOVEMENT_ID) &&
                        (resp.getParameter(Response.MOVEMENT_ID) == Movement.GET_MOVEMENTS ||
                        resp.getParameter(Response.MOVEMENT_ID) == Movement.DO_MOVEMENT ||
                        resp.getParameter(Response.MOVEMENT_ID) == Movement.STOP ||
                        resp.getParameter(Response.MOVEMENT_ID) == Movement.DATA ||
                        resp.getParameter(Response.MOVEMENT_ID) == Movement.SMALL_TALK ||
                        resp.getParameter(Response.MOVEMENT_ID) == Movement.START_PROGRAMMING ||
                        resp.getParameter(Response.MOVEMENT_ID) == Movement.PROGRAM_NAME  ||
                        resp.getParameter(Response.MOVEMENT_ID) == Movement.LOGIN ||
                        resp.getParameter(Response.MOVEMENT_ID) == Movement.SAVE_POSITION)) {
                        //nothing
                    } else {
                        if textResponse != "" {
                            self.displayRobotResponse(message: textResponse)
                        }
                    }
                }
            }
            
            self.textInput = ""
            resp.responseBehaviour() //farà el que calgui amb la resposta
            
        }, failure: { (request, error) in
            print(error!)
        })
        
        ApiAI.shared().enqueue(request)
    }
    
    func displayRobotResponse(message: String) {
        showRobotMessage(message)
        playMessage(message)
        
    }
    
    func playMessage(_ text: String) {
        
        do {
            try AVAudioSession.sharedInstance().setCategory(AVAudioSession.Category.playAndRecord, mode: .voiceChat, options: .defaultToSpeaker)
            
                try AVAudioSession.sharedInstance().setActive(true, options: .notifyOthersOnDeactivation)
            
        } catch {
            print("audioSession properties weren't set because of an error.")
        }

        
        let speechUtterance = AVSpeechUtterance(string: text)
        speechUtterance.voice = AVSpeechSynthesisVoice(language: "es-ES")

        let synth = AVSpeechSynthesizer()
        synth.speak(speechUtterance)
        /*let sock = RobotMonitoring(com.ip, Int32(com!.port_alexa))
        sock.send("{\"action\": \"speak\",\"value\": \"\(text)\"}")
        sock.close()*/
    }

    
    func showRobotMessage(_ message: String) {
        let chatMessage = ChatMessage(text: message, isIncoming: true);
        self.chatMessages.append(chatMessage);
        self.tableView.reloadData();
        let ip = NSIndexPath(row: self.chatMessages.count - 1, section: 0)
        self.tableView.scrollToRow(at: ip as IndexPath, at: .bottom, animated: false)
    }
    
    override func viewWillAppear(_ animated: Bool) {
    }
    
    override func viewWillDisappear(_ animated: Bool) {
        com.close()
    }
    
    func startRecording() {
        if recognitionTask != nil {
            audioEngine.stop()
            audioEngine.inputNode.removeTap(onBus: 0)
            recognitionTask?.cancel()
            recognitionTask = nil
        }
        
        let audioSession = AVAudioSession.sharedInstance()
        do {
            try audioSession.setCategory(AVAudioSession.Category.playAndRecord, mode: .measurement, options: [])
            try audioSession.setMode(AVAudioSession.Mode.measurement)
            try audioSession.setActive(true, options: .notifyOthersOnDeactivation)
        } catch {
            print("audioSession properties weren't set because of an error.")
        }
        recognitionRequest = SFSpeechAudioBufferRecognitionRequest()
        
        let inputNode = audioEngine.inputNode;
        
        guard let recognitionRequest = recognitionRequest else {
            fatalError("Unable to create an SFSpeechAudioBufferRecognitionRequest object")
        }
        
        recognitionRequest.shouldReportPartialResults = true
        
        recognitionTask = speechRecognizer?.recognitionTask(with: recognitionRequest, resultHandler: { (result, error) in
            
            var isFinal = false
            if result != nil {
                
                self.textInput = (result?.bestTranscription.formattedString)!
                isFinal = (result?.isFinal)!
            }
            
            if (error != nil || isFinal) {
                self.audioEngine.stop()
                inputNode.removeTap(onBus: 0)
                recognitionRequest.endAudio()
                self.recognitionTask?.cancel()
                
                self.recognitionRequest = nil
                self.recognitionTask = nil
                
                self.microphoneButton.isEnabled = true
            }
        })
        
        let recordingFormat = inputNode.outputFormat(forBus: 0)
        inputNode.installTap(onBus: 0, bufferSize: 1024, format: recordingFormat) { (buffer, when) in
            self.recognitionRequest?.append(buffer)
        }
        audioEngine.prepare()
        
        do {
            try audioEngine.start()
        } catch {
            print("audioEngine couldn't start because of an error.")
        }
    }
    
    func speechRecognizer(_ speechRecognizer: SFSpeechRecognizer, availabilityDidChange available: Bool) {
        if available {
            microphoneButton.isEnabled = true
        } else {
            microphoneButton.isEnabled = false
        }
    }
    
    func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
        tableView.deselectRow(at: indexPath, animated: true)
    }
    
    func initSound(_ song: String) {
        guard let url = Bundle.main.url(forResource: song, withExtension: "mp3") else { return }
        
        do {
           
            try AVAudioSession.sharedInstance().setCategory(AVAudioSession.Category.playAndRecord, mode: .voiceChat, options: .defaultToSpeaker)
            
            try AVAudioSession.sharedInstance().setActive(true, options: .notifyOthersOnDeactivation)
            
            
            /* The following line is required for the player to work on iOS 11. Change the file type accordingly*/
            player = try AVAudioPlayer(contentsOf: url, fileTypeHint: AVFileType.mp3.rawValue)
            
            /* iOS 10 and earlier require the following line:
             player = try AVAudioPlayer(contentsOf: url, fileTypeHint: AVFileTypeMPEGLayer3) */
            
            guard let player = player else { return }
            player.numberOfLoops = 0
            
            
        } catch let error {
            print(error.localizedDescription)
        }
    }
    
    func playSound() {
        DispatchQueue.global(qos: .background).async {
            self.player!.play()
        }
    }
    

    
}

