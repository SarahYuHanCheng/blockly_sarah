/*
 automatic mobile toy car 
*/
'use strict';

goog.require('Blockly.Blocks');

goog.provide('Blockly.Blocks.ultrasonic');
Blockly.Blocks.ultrasonic.HUE = 215;
// Blockly.Blocks.ultrasonic.image = filepath.media+'/ultrasonic.jpg';
//Define block

Blockly.Blocks['ultrasonic_setting'] = {
  init: function() {
    this.setHelpUrl(Blockly.Msg.ULTRASONIC_SETTING_HELPURL);
    this.setColour(Blockly.Blocks.ultrasonic.HUE);
    this.appendDummyInput()
      .appendField(new Blockly.FieldImage(Blockly.Blocks.ultrasonic.image, 64, 64))
      .appendField(Blockly.Msg.ULTRASONIC_SETTING_TITLE);
    this.appendDummyInput()
      .appendField(Blockly.Msg.ULTRASONIC_SETTING_TRIG);
    this.appendDummyInput()
      .appendField(new Blockly.FieldTextInput("20"),"TRIG")
    this.appendDummyInput()
      .appendField(Blockly.Msg.ULTRASONIC_SETTING_ECHO);
    this.appendDummyInput()
      .appendField(new Blockly.FieldTextInput("21"),"ECHO")
    this.appendDummyInput()
      .appendField(Blockly.Msg.ULTRASONIC_SETTING_RESET);
    this.appendDummyInput()
      .appendField(new Blockly.FieldDropdown([["Right"], ["Left"],["Forward"]]), "SIDE")
    this.setInputsInline(true);
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    // this.setTooltip(Blockly.Msg.ULTRASONIC_SETTING_TOOLTIP);
  }
};


Blockly.Blocks['ultrasonic_distance'] = {
  init: function() {
    this.setHelpUrl(Blockly.Msg.ULTRASONIC_DISTANCE_HELPURL);
    this.setColour(Blockly.Blocks.ultrasonic.HUE);
    this.appendDummyInput()
      // .appendField(new Blockly.FieldImage(Blockly.Blocks.ultrasonic.image, 64, 64))
      .appendField(Blockly.Msg.ULTRASONIC_MAXRANGE_TITLE);
    this.appendDummyInput()
      .appendField(new Blockly.FieldDropdown([["cm", "CM"], ["inch", "INCH"]]), "UNIT");
    this.setInputsInline(true);
    this.setOutput(true, "Number");
    // this.setTooltip(Blockly.Msg.ULTRASONIC_MAXRANGE_TOOLTIP);
  }
};
var ColorsensorJson = {
  "message0": "S0: %1, S1: %2, S2: %3, S3: %4, E0: %5, OUT: %6 ",
  "args0": [
    {"type": "field_number", "name": "S0", "value": "25"},
    {"type": "field_number", "name": "S1", "value": "26"},
    {"type": "field_number", "name": "S2", "value": "27"},
    {"type": "field_number", "name": "S3", "value": "24"},
    {"type": "field_input", "name": "E0", "text": "GND"},
    {"type": "field_number", "name": "OUT", "value": "22"},
  ],
  "previousStatement": true,
  "nextStatement": true,
  "colour": 230
};


Blockly.Blocks['Color_Sense_setting'] = {
  init: function() {
    this.jsonInit(ColorsensorJson);
    this.setInputsInline(true);
    this.setPreviousStatement(true);
    this.setNextStatement(true);
  }
};

Blockly.Blocks['move_forward']={
  init: function(){
    this.jsonInit({
  "message0": " Instruction %1 for %2 secs",
  "args0": [
  {
      "type": "field_dropdown",
      "name": "Instruction",
      "options": [
        [ "Forward", "F" ],
        [ "Backward", "B" ],
        [ "Right", "R" ],
        [ "Left", "L" ]
      ]
    },
  {
      "type": "field_number",
      "name": "delay_time",
      "value":1
    }]
    
  })
    this.setPreviousStatement(true,'Action');
    this.setNextStatement(true, 'Action');
 }
}
//backwards
Blockly.Blocks['move_backward']={
  init: function(){
    this.jsonInit({
  "message0": "Backward %1 secs",
  "args0": [{
      "type": "field_number",
      "name": "delay_time",
      "value":1
    }]
  })
    this.setPreviousStatement(true,'Action');
    this.setNextStatement(true, 'Action');
  }
}

Blockly.Blocks['turn_right']={
  init: function(){
    this.jsonInit({
  "message0": "Turn right %1 secs",
  "args0": [{
      "type": "field_number",
      "name": "delay_time",
      "value":1
    }]
  })
    this.setPreviousStatement(true,'Action');
    this.setNextStatement(true, 'Action');
  }
}
Blockly.Blocks['turn_left']={
  init: function(){
    this.jsonInit({
  "message0": "Turn left %1 secs",
  "args0": [{
      "type": "field_number",
      "name": "delay_time",
      "value":1
    }]
  })
    this.setPreviousStatement(true,'Action');
    this.setNextStatement(true, 'Action');
  }
}
Blockly.Blocks['show_color']={
  init: function(){
    this.jsonInit({
  "message0": "show_color",
  // "args0": [{
  //     "type": "field_variable",
  //     "name": "delay_time",
  //     "check":"Number"
  //   }]
  })
    this.setPreviousStatement(true,'Action');
    this.setNextStatement(true, 'Action');
  }
}