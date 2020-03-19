//
//  LeftToRightSegue.swift
//  URApp
//
//  Created by XavierRoma on 26/03/2019.
//  Copyright © 2019 x.roma_gabriel.cammany. All rights reserved.
//

import UIKit

class LeftToRightSegue: UIStoryboardSegue {
    override func perform() {
        
        let ourOriginViewController = self.source 
        
        ourOriginViewController.navigationController?.pushViewController(self.destination , animated: false)
        
        let transition = CATransition()
        transition.duration = 0.5
        transition.timingFunction = CAMediaTimingFunction(name: CAMediaTimingFunctionName.easeInEaseOut)
        transition.type = CATransitionType.push //kCATransitionMoveIn; //, kCATransitionPush, kCATransitionReveal, kCATransitionFade
        transition.subtype = CATransitionSubtype.fromLeft //kCATransitionFromLeft, kCATransitionFromRight, kCATransitionFromTop, kCATransitionFromBottom
        
        ourOriginViewController.navigationController?.view.layer.add(transition, forKey: kCATransition)
        
      
        
    

    }
}
