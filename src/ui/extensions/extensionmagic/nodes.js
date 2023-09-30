//your node constructor class
function ExtensionMagic()
{
  //add some input slots
  this.addInput("Input","3darray");
  this.addInput("Color","string");
  //add some output slots
  this.addOutput("Output","image");
  //add some properties
  this.properties = { precision: 0.001 };
}

//name to show on the canvas
ExtensionMagic.title = "ExtensionMagic";

//function to call when the node is executed
ExtensionMagic.prototype.onExecute = function()
{
  //retrieve data from inputs
  var A = this.getInputData(0);
  if( A === undefined )
    A = 0;
  var B = this.getInputData(1);
  if( B === undefined )
    B = 0;
  //assing data to outputs
  this.setOutputData( 0, A + B );
}

//register in the system
LiteGraph.registerNodeType("Visualiser/Image", ExtensionMagic );