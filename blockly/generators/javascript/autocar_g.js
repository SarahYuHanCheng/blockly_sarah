/*
automatic mobile toy car 
*/
'use strict';
goog.require('Blockly.JavaScript');

Blockly.JavaScript['move_forward'] = function(block) {
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
    // 'var addresss = \'\'ws://\'+the_ip+\':9998/echo\'\'',
    'var ws = new WebSocket(addresss);',
    'ws.onopen = function(){',
    '  ws.send("F");',
    '  ws.close();',
    // '  setTimeout(function(){',
    // '     var ws2 = new WebSocket(\'ws://localhost:9998/echo\');',
    // '     ws2.onopen = function(){',
    // '       ws2.send("LOW");ws2.close();};',
    // '       },delay_time',
    // '  );',
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
Blockly.JavaScript['move_backward'] = function(block) {
  var delay_time = Blockly.JavaScript.quote_('1000');//Blockly.JavaScript.quote_(block.getFieldValue('delay_time'));
  var pin =Blockly.JavaScript.quote_('9');
  var the_ip = Blockly.JavaScript.quote_('127.0.0.1');

  var functionName = Blockly.JavaScript.provideFunction_(
    'websocketServer',[
    'function '+Blockly.JavaScript.FUNCTION_NAME_PLACEHOLDER_+
    '(pin,delay_time,the_ip){',
    'var addresss = \'ws://localhost:9998/echo\'',
    'var ws = new WebSocket(addresss);',
    'ws.onopen = function(){',
    '  ws.send("B");',
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
    'var ws = new WebSocket(addresss);',
    'ws.onopen = function(){',
    '  ws.send("R");',
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
    'ws.onopen = function(){',
    '  ws.send("L");',
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
    'var out_msg = \'u#1\';',
    'var back_msg = \'0\';',
    'var ws = new WebSocket(\'ws://localhost:9998/echo\');',
    'ws.onopen = function(){',
    'ws.send("Z");',
    '};',
    'ws.onmessage = function(evt){',
    'window.alert(evt.data);',
    'console.log(evt.data);',
    'back_msg = evt.data;',
    'ws.close();',
    '};',
    'ws.onclose = function(){',
    'ws.close();',
    '};',
    'return back_msg;',
    '}']);
  var code = functionName + '()'+';';
  // return back_msg;
  return [code, Blockly.JavaScript.ORDER_FUNCTION_CALL];  
};



