/*
 automatic mobile toy car 
*/
'use strict';

goog.require('Blockly.Blocks');

//Define block
Blockly.Blocks['move_forward']={
  init: function(){
    this.jsonInit({
  "message0": "Forward %1 secs",
  "args0": [{
      "type": "field_variable",
      "name": "delay_time",
      "check":"Number"
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
  "message0": "Backward secs",
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

Blockly.Blocks['turn_right']={
  init: function(){
    this.jsonInit({
  "message0": "Turn right %1 secs",
  "args0": [{
      "type": "field_variable",
      "name": "delay_time",
      "check":"Number"
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
      "type": "field_variable",
      "name": "delay_time",
      "check":"Number"
    }]
  })
    this.setPreviousStatement(true,'Action');
    this.setNextStatement(true, 'Action');
  }
}
Blockly.Blocks['show_color']={
  init: function(){
    this.jsonInit({
  "message0": "show_color %1 secs",
  "args0": [{
      "type": "field_variable",
      "name": "delay_time",
      "check":"Number"
    }]
  })
    this.setPreviousStatement(true,'Action');
    this.setNextStatement(true, 'Action');
  }
}