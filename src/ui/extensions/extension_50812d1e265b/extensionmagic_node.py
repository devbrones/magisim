from shared.builtin import Extension
class ExtensionNode(Extension.Analyzer):
    def __init__(self, uuid: str, name: str, category: str, ):
        self.uuid = uuid
        self.name = name
        self.category = category
        self.nodeobj = f"""
		//node constructor class
		function {uuid}()
		{{
		  this.addInput("2D Space","npspace2d");
		  this.addInput("Cutoff","number");
		  this.addOutput("Density","number");
		  this.properties = {{ precision: 0.001 }};
		}}
		//name to show
		{uuid}.title = "{name}";

		//function to call when the node is executed
		{uuid}.prototype.onExecute = function()
		{{
		  var A = this.getInputData(0);
		  if( A === undefined )
		    A = 0;
		  var B = this.getInputData(1);
		  if( B === undefined )
		    B = 0;
		  this.setOutputData( 0, A + B );
		}}

		//register in the system
		LiteGraph.registerNodeType("{category}", {uuid} );
		"""