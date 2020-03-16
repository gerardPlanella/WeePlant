//
//  ViewController.swift
//  test
//
//  Created by XavierRoma on 08/03/2019.
//  Copyright © 2019 Salle URL. All rights reserved.
//

import UIKit
import MapKit
import WebKit

class MapWebViewController: UIViewController, WKUIDelegate {
    
    var isWebsite = true
    
    //---------------
    //MARK: - WebView
    //---------------
    var webView: WKWebView!
    var webAddress: String!
    
    override func loadView() {
        let webConfiguration = WKWebViewConfiguration()
        webView = WKWebView(frame: .zero, configuration: webConfiguration)
        webView.uiDelegate = self
        view = webView
    }
    override func viewDidLoad() {
        super.viewDidLoad()
        self.navigationController?.isNavigationBarHidden = false
        
        let myURL = URL(string:"http://urportal.sytes.net:50000")
        let myRequest = URLRequest(url: myURL!)
        webView.load(myRequest)
    }
    
}
    


