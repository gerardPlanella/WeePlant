package salle.url.edu.ur.hack.impl;

import com.ur.urcap.api.contribution.installation.swing.SwingInstallationNodeView;
import com.ur.urcap.api.domain.userinteraction.keyboard.KeyboardTextInput;

import javax.swing.*;
import javax.swing.text.SimpleAttributeSet;
import javax.swing.text.StyleConstants;
import java.awt.*;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;

public class LsInstallationNodeView implements SwingInstallationNodeView<LsInstallationNodeContribution> {

	private final Style style;
	private JTextField jTextField;
	private JTabbedPane jTabbedPane;
	//TODO: tret per la selene private JButton jButton;

	public LsInstallationNodeView(Style style) {
		this.style = style;
	}

	@Override
	public void buildUI(JPanel jPanel, final LsInstallationNodeContribution installationNode) {
		jPanel.setLayout(new BoxLayout(jPanel, BoxLayout.Y_AXIS));

		jTabbedPane = new JTabbedPane();
		jTabbedPane.setBorder(BorderFactory.createLineBorder(Color.BLACK));
		jTabbedPane.setBounds(50,50,200,200);
		jTabbedPane.add("INTRO",new MainChallengeTab());
		jTabbedPane.add("DASHBOARD",new DataChallengeTab());
		jTabbedPane.add("VISUALIZACIÓN 3D", new D3ChallengeTab());
		jTabbedPane.add("RECONOCIMIENTO DE VOZ",new ChatChallengeTab());
		jTabbedPane.add("REALIDAD AUMENTADA",new ARChallengeTab());
		jPanel.add(jTabbedPane);

		//TODO: Tret per la Selene jButton = new JButton("Save");
		//jButton.addActionListener();

		//jPanel.add(createInput(installationNode));
		//TODO: tret per la Selene jPanel.add(new JButton("Save"));

	}


	private Box createInput(final LsInstallationNodeContribution installationNode) {
		Box inputBox = Box.createHorizontalBox();
		inputBox.setAlignmentX(Component.LEFT_ALIGNMENT);

		//inputBox.add(new JLabel("Popup title:"));
		inputBox.add(createHorizontalSpacing());

		jTextField = new JTextField();
		jTextField.setFocusable(false);
		jTextField.setPreferredSize(style.getInputfieldSize());
		jTextField.setMaximumSize(jTextField.getPreferredSize());
		jTextField.addMouseListener(new MouseAdapter() {
			@Override
			public void mousePressed(MouseEvent e) {
				KeyboardTextInput keyboardInput = installationNode.getInputForTextField();
				keyboardInput.show(jTextField, installationNode.getCallbackForTextField());
			}
		});
		inputBox.add(jTextField);

		return inputBox;
	}

	private Component createHorizontalSpacing() {
		return Box.createRigidArea(new Dimension(style.getHorizontalSpacing(), 0));
	}

	private Component createVerticalSpacing() {
		return Box.createRigidArea(new Dimension(0, style.getVerticalSpacing()));
	}

	public void setPopupText(String t) {
		jTextField.setText(t);
	}
}
