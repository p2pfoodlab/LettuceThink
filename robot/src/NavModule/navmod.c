/*
    navmod.c

    The navigation module for the LettuceThink robot. It receives
    messages from the RC module (remote control), calculates the speed
    and angle of the four wheels, and then sends the speed and angle
    informations to the four wheel modules. All communication takes
    place over plain TCP.

    Copyright (C) 2017 Peter Hanappe, Sony Computer Science
    Laboratories

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

*/
#define _BSD_SOURCE
#include <string.h>
#include <stdio.h>
#include <math.h>
#include <stdarg.h>
#include <unistd.h>
#include <errno.h>
#include <sys/time.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <netinet/in.h>

char* logfile = NULL;
int server = -1;
int rcmod = -1;
int num_wheelmods = 1;
int wheelmod[] = { -1, -1, -1, -1 };
double speed[] = { 0.0, 0.0, 0.0, 0.0 };
double direction[] = { 0.0, 0.0, 0.0, 0.0 };
char* wheelmod_ips[] = { "10.20.30.40",
                         "10.20.30.41",
                         "10.20.30.42",
                         "10.20.30.43" };
struct timeval last_ping; 


void emergency_stop();

void whoops(int err, char* message)
{
        FILE* fp = stderr;        
        if (logfile) {
                fp = fopen(logfile, "a");
                if (fp == NULL) fp = stderr;
        }
        fprintf(fp, "error: %d: %s\n", err, message);
        if (fp != stderr) {
                fclose(fp);
        }
}

void show_status(int stage, char* message)
{
        FILE* fp = stderr;        
        if (logfile) {
                fp = fopen(logfile, "a");
                if (fp == NULL) fp = stderr;
        }
        fprintf(fp, "status: %d: %s\n", stage, message);
        if (fp != stderr) {
                fclose(fp);
        }
}

void close_socket(int sock)
{
        int r;
        char buf[1024];

        shutdown(sock, SHUT_RDWR);
        while (1) {
                r = recv(sock, buf, 1024, 0);
                if ((r == 0) || (r == -1))
                        break;
        }
        close(sock);
}

int open_server_socket(int port)
{
        struct sockaddr_in sockaddr;
        struct in_addr addr;
        struct hostent *hostptr;
        int s = -1;
        
        addr.s_addr = htonl(INADDR_ANY);

        s = socket(AF_INET, SOCK_STREAM, 0);
        if (s == -1) {
                whoops(1, "Failed to create server socket");
                return -1;
        }

        memset((char *)&sockaddr, 0, sizeof(struct sockaddr_in));
        sockaddr.sin_family = AF_INET;
        sockaddr.sin_addr = addr;
        sockaddr.sin_port = htons(port);

        if (bind(s, (const struct sockaddr *) &sockaddr,
                 sizeof(struct sockaddr_in)) == -1) {
                close_socket(s);
                whoops(2, "Failed to bind server socket");
                return -1;
        }

        if (listen(s, 10) == -1) {
                close_socket(s);
                whoops(3, "Failed to listen on server socket");
                return -1;
        }
        
        return s;
}

int wait_for_rcmod(int sock)
{
        int client = -1;
        struct sockaddr_in addr;
        socklen_t addrlen = sizeof(addr);

        while (1) {
                client = accept(sock, (struct sockaddr*) &addr, &addrlen);
  
                if (client != -1) {
                        return client;
                }

                whoops(4, "Accept failed");
                perror("navmod");
	}
        return client;
}

int connect_to_wheelmod(char* ip, int port)
{
        struct sockaddr_in sock_addr;
        struct sockaddr_in serv_addr;
        struct in_addr addr;
        struct hostent *hostptr;
        
        int s = socket(AF_INET, SOCK_STREAM, 0);
        if (s == -1) {
                whoops(6, "Failed to create the client socket");
                return -1;
        }

        /* Bind the socket */
        memset(&sock_addr, 0, sizeof(sock_addr));
        sock_addr.sin_family = AF_INET;
        sock_addr.sin_addr.s_addr = htonl(INADDR_ANY);
        sock_addr.sin_port = 0;

        if (bind(s, (const struct sockaddr *) &sock_addr, sizeof(sock_addr)) == -1)  {
                close_socket(s);
                whoops(7, "Failed to bind the client socket");
                return -1;
        }

        /* Convert the host name to the inet address. */        
        if (inet_aton(ip, &addr) == 0) {  
                whoops(8,
                       "Invalid IP address (are you using the "
                       "numbers-and-dots notation?)");
                return -1;
        }

        /* Connect the socket */
        memset(&serv_addr, 0, sizeof(serv_addr));
        serv_addr.sin_family = AF_INET;
        serv_addr.sin_addr = addr;
        serv_addr.sin_port = htons(port);

        if (connect(s, (const struct sockaddr *) &serv_addr, sizeof(serv_addr)) == -1)  {
                close_socket(s);
                whoops(9, "Failed to connect the client socket");
                return -1;
        }

        return s;
}

void connect_to_wheelmods()
{
        while (1) {
                int err = 0;
                for (int i = 0; i < num_wheelmods; i++) {
                        if (wheelmod[i] == -1) {
                                int r = connect_to_wheelmod(wheelmod_ips[i], 10101);
                                if (r == -1) {
                                        whoops(5, "Failed to connect to wheel module");
                                        err++;
                                } else {
                                        show_status(3, "Connected to wheel module");
                                        wheelmod[i] = r;
                                }
                        }
                }
                if (err == 0)
                        break;
        }
}

enum {
        front_left = 0,
        front_right,
        rear_left,
        rear_right
};


int send_msg_wheelmod(int sock, char ctrl, double value)
{
        char buf[32];
        ssize_t num;
        size_t len;
        int err = -1;

        snprintf(buf, 32, "%c%d;", ctrl, (int) round(value));
        len = strlen(buf);
        
        for (int attempt = 0; attempt < 3; attempt++) {
                num = send(sock, buf, len, MSG_NOSIGNAL);
                if (num == (ssize_t) len) {
                        err = 0;
                        break;
                }
        }
        if (err) perror("navmod");
        return err;
}

int set_speed(int value)
{
        int err = 0;

        for (int i = 0; i < 4; i++) {
                speed[i] = value;
        }

        for (int i = 0; i < num_wheelmods; i++) {
                int r = send_msg_wheelmod(wheelmod[i], 'v', speed[i]);
                if (r == -1) {
                        whoops(10, "Failed to send message to wheel module");
                        err++;
                }
        }

        return (err)? -1 : 0;
}

int set_direction(int value)
{
        int err = 0;

        for (int i = 0; i < 4; i++) {
                direction[i] = value;
        }

        for (int i = 0; i < num_wheelmods; i++) {
                int r = send_msg_wheelmod(wheelmod[i], 'd', direction[i]);
                if (r == -1) {
                        whoops(10, "Failed to send message to wheel module");
                        err++;
                }
        }
        
        return (err)? -1 : 0;
}

void emergency_stop()
{
        while (1) {
                set_speed(0);
                set_direction(0);
        }
}

int set_timeval(struct timeval* tv)
{
        int err = gettimeofday(tv, NULL);
        if (err) perror("navmod");
        return err;
}

int init_ping()
{
        return set_timeval(&last_ping);
}

int handle_ping()
{
        return set_timeval(&last_ping);
}

int check_ping()
{
        struct timeval now;
        if (set_timeval(&now) != 0)
                return -1;
        if (now.tv_sec - last_ping.tv_sec > 3) {
                whoops(12, "Ping from RC module timed-out");
                return -1;
        }
        return 0;
}

int handle_messages()
{
        enum _pstatus {
                _opcode = 0,
                _sign_or_digit = 1,
                _digit = 2,
                _semicolon = 3
        };

        int pstate = _opcode;
        int opcode = 0;
        int sign = 1;
        int value = 0;
        char buf[80];
        ssize_t len;
        int err;
        
        while (1) {
                
                if (check_ping() != 0) {
                        return -1;
                }
                
                len = recv(rcmod, buf, 80, MSG_DONTWAIT);
                if ((len == -1) && (errno != EAGAIN) && (errno != EWOULDBLOCK))  {
                        perror("navmod");
                        return -1;
                }
                
                for (ssize_t i = 0; i < len; i++) {
                        char c = buf[i];
                        err = 0;
                        if (c == 'v') { 
                                if (pstate == _opcode) {
                                        opcode = 'v';
                                        pstate = _sign_or_digit;
                                        value = 0;
                                } else pstate = _opcode;
                        } else if (c == 'd') { 
                                if (pstate == _opcode) {
                                        opcode = 'd';
                                        pstate = _sign_or_digit;
                                        value = 0;
                                } else pstate = _opcode;
                                break;
                        } else if (c == 'P') { 
                                if (pstate == _opcode) {
                                        opcode = 'P';
                                        pstate = _semicolon;
                                        value = 0;
                                } else pstate = _opcode;
                                break;
                        } else if (c == '-') {
                                if (pstate == _sign_or_digit) {
                                        sign = -1;
                                        pstate = _digit;
                                } else pstate = _opcode; 
                        } else if (c >= '0' && c <= '9') {
                                if (pstate == _sign_or_digit) {
                                        sign = 1;
                                        value = c - '0';
                                        pstate = _digit;
                                } else if (pstate == _digit) {
                                        value = value * 10 + (c - '0');
                                } else pstate = _opcode; 
                        } else if (c == ';') {
                                if (pstate == _digit) {
                                        value = sign * value;
                                        if (opcode == 'v') 
                                                err = set_speed(value);
                                        else if (opcode == 'd') 
                                                err = set_direction(value);
                                        pstate = _opcode;
                                } else if (pstate == _semicolon) {
                                        if (opcode == 'P') 
                                                err = handle_ping();
                                        pstate = _opcode;
                                } else pstate = _opcode; 
                        } else {
                                pstate = _opcode;
                        }
                        if (err) {
                                return -1;
                        }
                }
        }
        return 0;
}

int main(int argc, char** argv)
{
        if (argc == 2) {
                logfile = argv[1];
        }
        
        show_status(0, "Starting server");
        server = open_server_socket(10101);
        if (server == -1) {
                return 1;
        }

        show_status(1, "Waiting for RC module to connect");
        rcmod = wait_for_rcmod(server);

        if (init_ping() != 0) {
                whoops(11, "Failed to initialise ping");
                return 1;
        }

        show_status(2, "Connecting to wheel modules");
        connect_to_wheelmods();

        show_status(4, "Handling RC messages");
        int err = handle_messages();
        if (err) {
                show_status(100, "Emergency stop");
                emergency_stop(); // doesn't return;
        }
        
        return 0;
}
