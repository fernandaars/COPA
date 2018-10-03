var server = {}

var http = require('http');
var express = require('express');
var io = require('socket.io');
var pty = require('pty.js');
var terminal = require('term.js');

var fs = require('fs');
var https = require('https');
var url = require('url');

var socket;
var term;
var buff = [];

// DEFAULTS //
var COPA_HOME = "/copa/COPA/"
var CERT_HOME = COPA_HOME + "certs/" //Location of the lxd certs and keys.
//Location of the `bash_generator.py` file
var BASH_GENERATOR = COPA_HOME + "containers_site/core/static/core/xterm/dist/"

clients_ws = {}

function first_stage(server, container_name, connection_id, socket){
    var exec = require('child_process').exec;
    var child;
    command = ("python " + BASH_GENERATOR + "bash_generator.py '"
              + server + "'" + " 'https://" + server +  "' '"
              + container_name + "'")

    return exec(command,
                function (error, stdout, stderr) {
                     if(stdout.length > 0){
                         arr = stdout.split("keys=");
                         key_bash = arr[1];
                         execution(connection_id, key_bash.trim(), socket);
                     }
                     if (error !== null) {
                         console.log('exec error: ' + error);
                     }
                });
}

function execution(id_connection, key_bash, socket){

    const WebSocket = require('ws');

    clients_ws[id_connection] = new WebSocket(key_bash, {
        ssl: false,
            ssl_key: CERT_HOME+'lxd.key',
            ssl_cert: CERT_HOME+'lxd.crt',
            rejectUnauthorized : false,
        strictSSL : true
    });

    clients_ws[id_connection].onopen = function (e) {
        clients_ws[id_connection].onmessage = function (msg) {
            buffer = new Buffer(msg.data, 'binary' );
            output_command = buffer.toString('utf-8');
            !socket ? buff.push(output_command) : socket.emit('data', output_command);
        };

        clients_ws[id_connection].onclose = function (msg) {
            console.log('WebSocket closed');
        };
        clients_ws[id_connection].onerror = function (err) {
            console.error(err);
        };
    };
}

server.run = function(options){

    var app = express();
    var server = http.createServer(app);
    app.use(terminal.middleware());

    options = options || {};
    server.listen(options.port || 8100);

    io = io.listen(server, {log: false});

    io.sockets.on('connection', function(s) {
        socket = s;
        socket.on('data', function(data) {
            if(clients_ws[s.id]){
                binary_buffer = new Buffer(data, "binary");
                clients_ws[s.id].send(binary_buffer);
            }
        });

        socket.on("join", function(astring){
            ops = astring.split("/");
            first_stage(ops[0], ops[1], s.id, s);
        });

        socket.on('disconnect', function() {
            socket = null;
        });

        while (buff.length) {
            s.emit('data', buff.shift());
        };
    });
};

server.run({port: 8100});

module.exports = server;
