var unseenColor = '#eee';
var seenUninterestedColor = '#00FFFF';
var interestedNoPostColor = '#00FF00';
var repostColor = '#000000';
var diversity = "";
var uniqueness = "";
var reshare = "";
var startNode = "";
var reshareCt = 0;
var interestCt = 0;
var uninterestCt = 0;
var unseenCt = 0;
var simulating;

function isValidInput(n) {
    return parseFloat(n) >= 0 && parseFloat(n) <= 1 && n != "";
}

function runSimulation(frm) {
    diversity = frm.diversityP.value;
    uniqueness = frm.uniquenessP.value;
    reshare = frm.reshareP.value;
    if (isValidInput(diversity) && isValidInput(uniqueness) && isValidInput(reshare)) {
        simulating = true;
    } else {
        alert("Oops- make sure all fields are filled out! Accepted values are between 0.0 and 1.0.");
    }
}

$(function() {
    //Queue of nodes to be visited
    var queue = [];

    // Add a method to the graph model that returns an
    // object with every neighbors of a node inside:
    sigma.classes.graph.addMethod('neighbors', function (nodeId) {
        var k,
            neighbors = {},
            index = this.allNeighborsIndex[nodeId] || {};

        for (k in index)
            neighbors[k] = this.nodesIndex[k];

        return neighbors;
    });

    sigma.parsers.gexf(
      "{{ url_for('static', filename='data/LesMiserables.gexf') }}",
      {
          container: 'sigma-parent'
      },
      function (s) {
          // We first need to save the original colors of our
          // nodes and edges, like this:
          s.graph.nodes().forEach(function (n) {
              n.originalColor = n.color;
              n.visited = false;
              n.counted = false;
          });
          s.graph.edges().forEach(function (e) {
              e.originalColor = e.color;
          });

          function color(e) {
              var nodeId = e.data.node.id,
                    toKeep = s.graph.neighbors(nodeId);
              toKeep[nodeId] = e.data.node;

              s.graph.nodes().forEach(function (n) {
                  if (toKeep[n.id])
                      n.color = n.originalColor;
                  else
                      n.color = unseenColor;
              });

              s.graph.edges().forEach(function (e) {
                  if (toKeep[e.source] && toKeep[e.target])
                      e.color = e.originalColor;
                  else
                      e.color = unseenColor;
              });

              s.refresh();
          }

          function colorQueue(node) {
              queue.push(node);
              while (queue.length > 0) {
                  colorSim(queue.shift());
              }
          }

          function colorSim(node) {
              var nodeId = node.id,
                    toKeep = s.graph.neighbors(nodeId);
              toKeep[nodeId] = node;

              s.graph.nodes().forEach(function (n) {
                  if (!Boolean(n.visited)) {
                      if (toKeep[n.id]) {
                          //Does this user scan the screen or post new content?
                          postsNewContent = Math.random();

                          if (postsNewContent >= uniqueness) {
                              catchesEye = Math.random();

                              if (catchesEye >= diversity) {
                                  //If a post catches a person's eye, 
                                  //assume that they won't repost even if they
                                  //see it later at another point in time
                                  n.visited = true;
                                  if (Boolean(n.counted)) {
                                      unseen = unseen - 1;
                                  }

                                  willRepost = Math.random();
                                  if (willRepost < reshare) {
                                      reshareCt = reshareCt + 1;
                                      n.color = repostColor;
                                      queue.push(n);
                                  } else {
                                      interestCt = interestCt + 1;
                                      n.color = interestedNoPostColor;
                                  }
                              } else {
                                  uninterestCt = uninterestCt + 1;
                                  n.color = seenUninterestedColor;
                              }
                          } else {
                              if (Boolean(n.counted)) {
                                  unseenCt = unseenCt + 1;
                                  n.counted = true;
                              }
                              n.color = unseenColor;
                          }
                      } else {
                          n.color = unseenColor;
                      }
                  }
              });

              s.refresh();
          }

          // When a node is clicked, we check for each node
          // if it is a neighbor of the clicked one. If not,
          // we set its color as grey, and else, it takes its
          // original color.
          // We do the same for the edges, and we only keep
          // edges that have both extremities colored.
          s.bind('clickNode', function (e) {
              s.graph.nodes().forEach(function (n) {
                  n.visited = false;
              });

              if (!Boolean(simulating)) {
                  color(e);
              } else {
                  startNode = e.data.node.label;
                  reshareCt = 0;
                  uninterestCt = 0;
                  interestCt = 0;
                  unseenCt = 0;
                  document.getElementById("startingNode").innerText = startNode;
                  e.data.node.visited = true;
                  e.data.node.color = e.data.node.originalColor;
                  colorQueue(e.data.node);
                  document.getElementById("resharedCount").innerText = reshareCt;
                  document.getElementById("uninterestedCount").innerText = uninterestCt;
                  document.getElementById("interestedCount").innerText = interestCt;

                  //Subtract 1 to account for the node that is sharing the data.
                  document.getElementById("unseenCount").innerText = s.graph.nodes().length - reshareCt - uninterestCt - interestCt - 1 + ' (' + unseenCt + ' unseen in friend network)';
              }
          });

          function reset(e) {
              s.graph.nodes().forEach(function (n) {
                  n.color = n.originalColor;
                  n.visited = false;
              });

              s.graph.edges().forEach(function (e) {
                  e.color = e.originalColor;
              });

              // Same as in the previous event:
              s.refresh();
          }

          // When the stage is clicked, we just color each
          // node and edge with its original color.
          s.bind('clickStage', function (e) {
              reset(e);
          });
      }
    );

});