package salle.url.edu.ur.hack.impl;

import com.ur.urcap.api.contribution.installation.InstallationAPIProvider;
import com.ur.urcap.api.domain.data.DataModel;
import com.ur.urcap.api.domain.script.ScriptWriter;
import com.ur.urcap.api.domain.userinteraction.keyboard.KeyboardInputCallback;
import com.ur.urcap.api.domain.userinteraction.keyboard.KeyboardInputFactory;
import com.ur.urcap.api.domain.userinteraction.keyboard.KeyboardTextInput;

public class LsInstallationNodeContribution implements com.ur.urcap.api.contribution.InstallationNodeContribution {

	private static final String POPUPTITLE_KEY = "popuptitle";
	private static final String DEFAULT_VALUE = "Hello World Swing";
	private final LsInstallationNodeView view;
	private final KeyboardInputFactory keyboardFactory;

	private DataModel model;

	public LsInstallationNodeContribution(InstallationAPIProvider apiProvider, DataModel model, LsInstallationNodeView view) {
		this.keyboardFactory = apiProvider.getUserInterfaceAPI().getUserInteraction().getKeyboardInputFactory();
		this.model = model;
		this.view = view;
	}

	@Override
	public void openView() {

		//TODO: Tret by selene view.setPopupText(getPopupTitle());
	}

	@Override
	public void closeView() {

	}

	public boolean isDefined() {
		return !getPopupTitle().isEmpty();
	}

	@Override
	public void generateScript(ScriptWriter writer) {
		// Store the popup title in a global variable so it is globally available to all Hello World Swing program nodes.
		writer.assign("hello_world_swing_popup_title", "\"" + getPopupTitle() + "\"");
	}

	public String getPopupTitle() {
		return model.get(POPUPTITLE_KEY, DEFAULT_VALUE);
	}

	public void setPopupTitle(String message) {
		if ("".equals(message)) {
			resetToDefaultValue();
		} else {
			model.set(POPUPTITLE_KEY, message);
		}
	}

	private void resetToDefaultValue() {
		view.setPopupText(DEFAULT_VALUE);
		model.set(POPUPTITLE_KEY, DEFAULT_VALUE);
	}

	public KeyboardTextInput getInputForTextField() {
		KeyboardTextInput keyboardInput = keyboardFactory.createStringKeyboardInput();
		keyboardInput.setInitialValue(getPopupTitle());
		return keyboardInput;
	}

	public KeyboardInputCallback<String> getCallbackForTextField() {
		return new KeyboardInputCallback<String>() {
			@Override
			public void onOk(String value) {
				setPopupTitle(value);
				view.setPopupText(value);
			}
		};
	}

}
