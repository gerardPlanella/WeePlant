//
//  ChatMessageCell.swift
//  speech_hack
//
//  Created by Alumne on 12/12/2018.
//  Copyright © 2018 Guillem Garrofé Montoliu. All rights reserved.
//

import UIKit

class ChatMessageCell: UITableViewCell {

    let messageLabel = UILabel();
    let bubbleBackgroundView = UIView();
    
    var leadingConstrain: NSLayoutConstraint!
    var trailingConstrain: NSLayoutConstraint!
    
    var chatMessage: ChatMessage!{
        didSet{
            bubbleBackgroundView.backgroundColor = chatMessage.isIncoming ? .white : .darkGray;
            messageLabel.textColor = chatMessage.isIncoming ? .black : .white;
            messageLabel.text = chatMessage.text;
            
            if(chatMessage.isIncoming){
                leadingConstrain.isActive = true
                trailingConstrain.isActive = false
            }else{
                leadingConstrain.isActive = false
                trailingConstrain.isActive = true
            }
        }
    }
    
/*    override var isHighlighted: Bool{
        didSet{
            backgroundColor = isHighlighted ? UIColor(red: 8, green: 134/255, blue: 249/255, alpha: 1) : UIColor.white
        }
    }
    var isIcoming: Bool! {
        didSet{
            bubbleBackgroundView.backgroundColor = isIcoming ? .white : .darkGray;
            messageLabel.textColor = isIcoming ? .black : .white;
        }
    }
  */
    override init(style: UITableViewCell.CellStyle, reuseIdentifier: String?) {
        super.init(style: style, reuseIdentifier: reuseIdentifier)
        
        backgroundColor = .clear;
        
        bubbleBackgroundView.backgroundColor = .yellow;
        bubbleBackgroundView.layer.cornerRadius = 16;
        bubbleBackgroundView.translatesAutoresizingMaskIntoConstraints = false;
        addSubview(bubbleBackgroundView);
        
        
        addSubview(messageLabel);
        
        messageLabel.numberOfLines = 0;
        messageLabel.translatesAutoresizingMaskIntoConstraints = false;
        
        
        //setup of constraints
        let constraints = [
            messageLabel.topAnchor.constraint(equalTo: topAnchor, constant: 32),
            messageLabel.bottomAnchor.constraint(equalTo: bottomAnchor, constant: -32),
            messageLabel.widthAnchor.constraint(lessThanOrEqualToConstant: 250),
            bubbleBackgroundView.topAnchor.constraint(equalTo: messageLabel.topAnchor, constant: -16),
            bubbleBackgroundView.leadingAnchor.constraint(equalTo: messageLabel.leadingAnchor, constant: -16),
            bubbleBackgroundView.bottomAnchor.constraint(equalTo: messageLabel.bottomAnchor, constant: 16),
            bubbleBackgroundView.widthAnchor.constraint(equalTo: messageLabel.widthAnchor, constant: 25)]
        
        
        NSLayoutConstraint.activate(constraints)
        
        leadingConstrain = messageLabel.leadingAnchor.constraint(equalTo: leadingAnchor, constant: 32)
        leadingConstrain.isActive = false
        
        trailingConstrain = messageLabel.trailingAnchor.constraint(equalTo: trailingAnchor, constant: -32)
        trailingConstrain.isActive = true;

        
    }
    
    required init?(coder aDecoder: NSCoder) {
        fatalError("init(coder:) has not been implemented")
    }
}
