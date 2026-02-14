const net = require('net');

const server = net.createServer((socket) => {
  socket.write('220 localhost ESMTP\r\n');
  socket.on('data', (data) => {
    const str = data.toString();
    console.log(str);
    if (str.startsWith('HELO') || str.startsWith('EHLO')) socket.write('250 localhost\r\n');
    else if (str.startsWith('MAIL FROM')) socket.write('250 OK\r\n');
    else if (str.startsWith('RCPT TO')) socket.write('250 OK\r\n');
    else if (str.startsWith('DATA')) socket.write('354 End data with <CR><LF>.<CR><LF>\r\n');
    else if (str.endsWith('\r\n.\r\n')) {
        socket.write('250 OK: queued as 12345\r\n');
    }
    else if (str.startsWith('QUIT')) socket.write('221 Bye\r\n');
  });
});

server.listen(2525, '0.0.0.0', () => {
  console.log('SMTP Catcher running on port 2525');
});
