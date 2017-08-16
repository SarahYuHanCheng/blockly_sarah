/*
automatic mobile toy car 
*/
'use strict';
goog.require('Blockly.JavaScript');

Blockly.JavaScript['ultrasonic_setting'] = function(block) {
  var trig_pin = this.getFieldValue('TRIG');
  var echo_pin = this.getFieldValue('ECHO');
  var reset_pin = this.getFieldValue('RESET');

  var functionName = Blockly.JavaScript.provideFunction_(
    'websocketServer',[
    'function '+Blockly.JavaScript.FUNCTION_NAME_PLACEHOLDER_+
    '(pin,delay_time,the_ip){',
    'var addresss = \'ws://localhost:9998/echo\'',
    'var ws = new WebSocket(addresss);',
    'var back_msg=0;',
    'ws.onopen = function(){',
    '  ws.send("F");',
    '};',
    'ws.onmessage = function(evt){',
    'back_msg=evt.data;',
    '};',
    'ws.onclose = function(){',
    '};',
    'return back_msg;',
    '}']);
  var code = functionName + '(' + pin + ', ' + delay_time + ', '+the_ip+')';
  return [code, Blockly.JavaScript.ORDER_FUNCTION_CALL];  
};
Blockly.JavaScript['ultrasonic_maxrange'] = function(block) {
  // Text value.
  // var delay_time = Blockly.JavaScript.quote_(block.getFieldValue('delay_time'));
  var delay_time = Blockly.JavaScript.quote_(block.getFieldValue('delay_time'));
  var pin =Blockly.JavaScript.quote_('9');
  var the_ip = Blockly.JavaScript.quote_('127.0.0.1');

  var functionName = Blockly.JavaScript.provideFunction_(
    'websocketServer',[
    'function '+Blockly.JavaScript.FUNCTION_NAME_PLACEHOLDER_+
    '(pin,delay_time,the_ip){',
    'var addresss = \'ws://localhost:9998/echo\'',
    'var ws = new WebSocket(addresss);',
    'var back_msg=0;',
    'ws.onopen = function(){',
    '  ws.send("F");',
    '};',
    'ws.onmessage = function(evt){',
    'back_msg=evt.data;',
    '};',
    'ws.onclose = function(){',
    '};',
    'return back_msg;',
    '}']);
  var code = functionName + '(' + pin + ', ' + delay_time + ', '+the_ip+')';
  return [code, Blockly.JavaScript.ORDER_FUNCTION_CALL];  
};
Blockly.JavaScript['ultrasonic_distance'] = function(block) {
  // Text value.
  // var delay_time = Blockly.JavaScript.quote_(block.getFieldValue('delay_time'));
  var delay_time = Blockly.JavaScript.quote_(block.getFieldValue('delay_time'));
  var pin =Blockly.JavaScript.quote_('9');
  var the_ip = Blockly.JavaScript.quote_('127.0.0.1');

  var functionName = Blockly.JavaScript.provideFunction_(
    'websocketServer',[
    'function '+Blockly.JavaScript.FUNCTION_NAME_PLACEHOLDER_+
    '(pin,delay_time,the_ip){',
    'var addresss = \'ws://localhost:9998/echo\'',
    'var ws = new WebSocket(addresss);',
    'var back_msg=0;',
    'ws.onopen = function(){',
    '  ws.send("F");',
    '};',
    'ws.onmessage = function(evt){',
    'back_msg=evt.data;',
    '};',
    'ws.onclose = function(){',
    '};',
    'return back_msg;',
    '}']);
  var code = functionName + '(' + pin + ', ' + delay_time + ', '+the_ip+')';
  return [code, Blockly.JavaScript.ORDER_FUNCTION_CALL];  
};

Blockly.JavaScript['move_forward'] = function(block) {
  // Text value.
  // var delay_time = Blockly.JavaScript.quote_(block.getFieldValue('delay_time'));
  var delay_time = Blockly.JavaScript.quote_(block.getFieldValue('delay_time'));
  var Instruction = Blockly.JavaScript.quote_(block.getFieldValue('Instruction'));
  var pin =Blockly.JavaScript.quote_('9');
  var the_ip = Blockly.JavaScript.quote_('127.0.0.1');

  var functionName = Blockly.JavaScript.provideFunction_(
    'websocketServer',[
    'function '+Blockly.JavaScript.FUNCTION_NAME_PLACEHOLDER_+
    '(Instruction,delay_time,the_ip){',
    'var addresss = \'ws://localhost:9998/echo\'',
    // 'var addresss = \'\'ws://\'+the_ip+\':9998/echo\'\'',
    'var ws = new WebSocket(addresss);',
    'var out_msg = Instruction+\'#\'+delay_time*1000+\'@\';',
    'ws.onopen = function(){',
    '  ws.send(out_msg);',
    '  ws.close();',
    // '  setTimeout(function(){',
    // '     var ws2 = new WebSocket(\'ws://localhost:9998/echo\');',
    // '     ws2.onopen = function(){',
    // '       ws2.send("LOW");ws2.close();};',
    // '       },delay_time',
    // '  );',
    '};',
    'ws.onmessage = function(evt){',
    'back_msg=evt.data;',
    '};',
    'ws.onclose = function(){',
    '};',
    'return 0;',
    '}']);
  // var code = functionName + '(' + pin + ', ' + delay_time + ', '+the_ip+')';
  // return [code, Blockly.JavaScript.ORDER_FUNCTION_CALL];  
    var code = functionName + '(' + Instruction + ', ' + delay_time + ', '+the_ip+');';
  return code;
};
Blockly.JavaScript['move_backward'] = function(block) {
  var delay_time = Blockly.JavaScript.quote_(block.getFieldValue('delay_time'));
  var pin =Blockly.JavaScript.quote_('9');
  var the_ip = Blockly.JavaScript.quote_('127.0.0.1');
  var functionName = Blockly.JavaScript.provideFunction_(
    'websocketServer',[
    'function '+Blockly.JavaScript.FUNCTION_NAME_PLACEHOLDER_+
    '(pin,delay_time,ws){',
    'var addresss = \'ws://localhost:9998/echo\'',
    'var ws = new WebSocket(addresss);',
    'var out_msg = \'B#\'+delay_time*1000;',
    'ws.onopen = function(){',
    '  ws.send(out_msg);',
    '  ws.close();',
    '};',
    'ws.onmessage = function(evt){',
    '};',
    'ws.onclose = function(){',
    '};',
    'return \'true\';',
    '}']);
  var code = functionName + '(' + pin + ', ' + delay_time + ', '+the_ip+');';
  return code;
};
Blockly.JavaScript['turn_right'] = function(block) {
  var delay_time = Blockly.JavaScript.quote_(block.getFieldValue('delay_time'));
  var pin =Blockly.JavaScript.quote_('9');
  var the_ip = Blockly.JavaScript.quote_('127.0.0.1');

  var functionName = Blockly.JavaScript.provideFunction_(
    'websocketServer',[
    'function '+Blockly.JavaScript.FUNCTION_NAME_PLACEHOLDER_+
    '(pin,delay_time,the_ip){',
    'var addresss = \'ws://localhost:9998/echo\'',
    'var out_msgr = \'R#\'+delay_time*1000;',
    
    'var ws = new WebSocket(addresss);',
    'ws.onopen = function(){',
    '  ws.send(out_msgr);',
    '  ws.close();',
    '};',
    'ws.onmessage = function(evt){',
    '};',
    'ws.onclose = function(){',
    '};',
    'return \'true\';',
    '}']);
  var code = functionName + '(' + pin + ', ' + delay_time + ', '+the_ip+');';
  return code;
};
Blockly.JavaScript['turn_left'] = function(block) {
  var delay_time = Blockly.JavaScript.quote_(block.getFieldValue('delay_time'));
  var pin =Blockly.JavaScript.quote_('9');
  var the_ip = Blockly.JavaScript.quote_('127.0.0.1');

  var functionName = Blockly.JavaScript.provideFunction_(
    'websocketServer',[
    'function '+Blockly.JavaScript.FUNCTION_NAME_PLACEHOLDER_+
    '(pin,delay_time,the_ip){',
    'var addresss = \'ws://localhost:9998/echo\'',
    'var ws = new WebSocket(addresss);',
    'var out_msg = \'L#\'+delay_time*1000;',
    'ws.onopen = function(){',
    '  ws.send(out_msg);',
    '  ws.close();',
    '};',
    'ws.onmessage = function(evt){',
    '};',
    'ws.onclose = function(){',
    '};',
    'return \'true\';',
    '}']);
  var code = functionName + '(' + pin + ', ' + delay_time + ', '+the_ip+');';
  return code;
};
Blockly.JavaScript['show_color'] = function(block) {

    var functionName = Blockly.JavaScript.provideFunction_(
    'websocketServer',[
    'function '+Blockly.JavaScript.FUNCTION_NAME_PLACEHOLDER_+
    '(){',
    'var out_msg = \'z#0@\';',
    'var back_msg = \'0\';',
    'var ws = new WebSocket(\'ws://localhost:9998/echo\');',
    'ws.onopen = function(){',
    'ws.send(out_msg);',
    '};',
    'ws.onmessage = function(evt){',
    // 'window.alert(evt.data);',
    // 'console.log(evt.data);',
    'back_msg = evt.data;',
    'ws.close();',
    '};',
    'ws.onclose = function(){',
    'ws.close();',
    '};',
    'return back_msg;',
    '}']);
  var code = functionName + '();';
  return code;  
};



