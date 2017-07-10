/*
connect
*/
'use strict';
goog.require('Blockly.JavaScript');

Blockly.JavaScript['Connect_to_Server'] = function(block) {
var pin = Blockly.JavaScript.quote_(block.getFieldValue('J_motorPin'));
  var angle =Blockly.JavaScript.quote_(block.getFieldValue('J_motorAngle'));
	var ws =new WebSocket("ws://localhost:9998/echo");
  // ws.onopen = function(){
  //   var out_msg = ""+pin+angle;
  //   ws.send(out_msg);
  //   };
};

Blockly.JavaScript['recv_device'] = function(block) {
  var pin = block.getFieldValue('J_motorPin');
  var angle = block.getFieldValue('J_motorAngle');
  
};

Blockly.JavaScript['Ja_test_motor'] = function(block) {
  // Text value.
  var pin = Blockly.JavaScript.quote_(block.getFieldValue('J_motorPin'));
  var angle =Blockly.JavaScript.quote_(block.getFieldValue('J_motorAngle'));
  var the_ip =Blockly.JavaScript.quote_(block.getFieldValue('server_ip'));

  var functionName = Blockly.JavaScript.provideFunction_(
    'websocketServer',[
    'function '+Blockly.JavaScript.FUNCTION_NAME_PLACEHOLDER_+
    '(pin,angle,the_ip){',
    'var out_msg = pin+\'#\'+angle;',
    'var ws = new WebSocket(\'ws://localhost:9998/echo\');',
    'ws.onopen = function(){',
    'ws.send(out_msg);',
    'ws.close();',
    '};',
    'ws.onmessage = function(evt){',
    '};',
    'ws.onclose = function(){',
    '};',
    'return out_msg;',
    '}']);
  var code = functionName + '(' + pin + ', ' + angle + ', '+the_ip+')';
  return [code, Blockly.JavaScript.ORDER_FUNCTION_CALL];
};