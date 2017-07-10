/*
wifi connection
*/
'use strict';

goog.require('Blockly.Blocks');

//Define block
Blockly.Blocks['send_to_Server']={
  init: function(){
    this.jsonInit({
  "message0": "send",
  "args0": [{
      "type": "input_value",
      "name": "VALUE"
    }]
  })
    this.setPreviousStatement(true,'Action');
    this.setNextStatement(true, 'Action');
  }
}
Blockly.Blocks['Connect_to_Server'] = {
  init: function() {
    this.setColour(186);
    this.appendDummyInput()
        .appendField("SERVER IP:")
        .appendField(new Blockly.FieldTextInput('192.168.0.1'),
                     'server_ip');
      }
};
var UltrasoundJson = {
  "message0": "change %1 by %2",
  "args0": [
    {"type": "field_variable", "name": "VAR", "variable": "item"},
    {"type": "input_value", "name": "DELTA", "check": "Number"}
  ],
  "previousStatement": null,
  "nextStatement": null,
  "colour": 230
};

Blockly.Blocks['Ultrasound'] = {
  init: function() {
    this.jsonInit(UltrasoundJson);
    // Assign 'this' to a variable for use in the tooltip closure below.
    this.setOutput(true, 'Number');
    var thisBlock = this;
    this.setTooltip(function() {
      return 'Returns the distance of object in cm,"%1".'.replace('%1',
          thisBlock.getFieldValue('VAR'));
    });
  }
};
Blockly.Blocks['recv_device'] = {
  init: function() {
    this.jsonInit({"colour": 118})
    this.setPreviousStatement(true, 'Action');
    this.setNextStatement(true, 'Action');
    this.appendDummyInput()
        .appendField('device:')
        .appendField(new Blockly.FieldDropdown([
                       ['arduino_uno', '1'],
                       ['max', '2']
                     ]),
                     'dest_device');
  }
};
Blockly.Blocks['Ja_test_motor'] = {
  init: function() {
    var textInput = new Blockly.FieldTextInput('19216801');
    
    textInput.setSpellcheck(false);    
    this.appendDummyInput()
        .appendField("Server IP:")
        .appendField(textInput, 'server_ip');
    
    this.appendDummyInput()
        .appendField('motor Pin:')
        .appendField(new Blockly.FieldDropdown([
                       ['pin9', '9'],
                       ['pin10', '10'],
                       ['pin11', '11']
                     ]),
                     'J_motorPin');
    this.appendDummyInput()
        .appendField('angle:')
        .appendField(new Blockly.FieldAngle(90), 'J_motorAngle');
  }
};
