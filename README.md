Instructions for Accessing Web App:
Code is hosted at http://social-simulator.appspot.com/

See docs/InputOutputSummary.pdf for further explanation of inputs and outputs used in the model.

Twitter:
Click "Twitter" from the main page and log-in to Twitter to authorize the account. For optimization purposes the entire network is not loaded. Around 10 connections from the authorized account will be used, with around 10-15 connections from each of those accounts.

NOTE: The Twitter simulation is buggy because it uses live data, so it may be necessary to reload the page and re-authorize the app with Twitter to get the graph network to display properly. If the visual display is missing or is only a single node with connections, wait a few minutes and then reload the webpage.

Facebook:
Changes to the Facebook API mean that third-parties can no longer get a user's friend network. Because of this we used a pre-existing network graph. The one currently used in the web app is stored at static/data/facebookGraph.gexf This file could be modified or replaced to have a different network graph loaded in for the simulation.

To run the simulation for either social network:
- Select "1 Sharer or Multiple Sharer." "Multiple Sharer" means that more than one person is allowed to introduce content to the network.
- "Step-by-step Visualtions"- if checked, pop-up alerts will display after each level's friends have had a chance to see the new content. This will give the rough equivalent of an animation for how the content spreads through the network, though is is not related to a specific time.
- "Number of Trials"- does not affect the visualization of the data. Only affects how many trials are used when calculating averages for the downloaded data. Must be an integer greater than or equal to 1.
- "Diversity"- The rate of shared interest in a network. In other words, the probability that a friend's content will or will not interest a user. Higher numbers mean higher diversity, which means less shared interest in the network. Must be a number between 0.0 and 1.0.
- "Unique Content"- The rate of unique content being posted to a page. Corresponds to the liklihood that a user will see someone's new content. Must be a number between 0.0 and 1.0
- "Re-Share Probability"- The probability that a person will repost content that interests them. Must be a number between 0.0 and 1.0. 
- Click "Run Simulation"
- Click a node in the graph.
- Colors on the graph and the chart on the top left of the page will update.
- Data can now be downloaded from clicking "Get Current Simulation Data"
- If you're in "1 Sharer" mode, you can click any node in the network to start a new simulation with the same start parameters but with a different starting node.
- If you're in "Multple Sharer" mode, click on other nodes in the network to represent the list of nodes that brought the same content to the network from outsdide sources. Clicking an already selected node will delete it from the list.
- If you want to run the simulation again with different parameters, update the start values and click "Run Simulation" again.
