package salle.url.edu.ur.hack.impl;

import com.ur.urcap.api.contribution.ViewAPIProvider;
import com.ur.urcap.api.contribution.installation.ContributionConfiguration;
import com.ur.urcap.api.contribution.installation.CreationContext;
import com.ur.urcap.api.contribution.installation.InstallationAPIProvider;
import com.ur.urcap.api.contribution.installation.swing.SwingInstallationNodeService;
import com.ur.urcap.api.domain.SystemAPI;
import com.ur.urcap.api.domain.data.DataModel;

import java.util.Locale;

public class LsInstallationNodeService implements SwingInstallationNodeService<LsInstallationNodeContribution, LsInstallationNodeView> {

	@Override
	public void configureContribution(ContributionConfiguration configuration) {
	}

	@Override
	public String getTitle(Locale locale) {
		return "UR Hackathon 2019 - La Salle Team";
	}

	@Override
	public LsInstallationNodeView createView(ViewAPIProvider apiProvider) {
		SystemAPI systemAPI = apiProvider.getSystemAPI();
		Style style = systemAPI.getSoftwareVersion().getMajorVersion() >= 5 ? new V5Style() : new V3Style();
		return new LsInstallationNodeView(style);
	}

	@Override
	public LsInstallationNodeContribution createInstallationNode(InstallationAPIProvider apiProvider, LsInstallationNodeView view, DataModel model, CreationContext context) {
		return new LsInstallationNodeContribution(apiProvider, model, view);
	}
}
