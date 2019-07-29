# OSCourses_Linda_ActiveMQ

In this project, we are going to implement Linda with three operations by using Apache ActiveMQ as the middleware. 

## Linda
Linda is a novel system for communication and synchronization. In Linda, independent process communicate via an abstract tuple space, unlike objects, tuples are pure data, they do not have any associated methods. 
In this project you are going to implement three operations that individual workers perform on the tuples and the tuple space: 
* out: produces a tuple, writing it into tuple space
* in: atomically reads and removes—consumes—a tuple from tuple space. 
* read: non-destructively reads a tuple space.

scenario:
1. in ("a", 2, "?i") : waiting for tuple ("a", 2, "?"), if exists assign the variable to i and store in server. After that, delete tuple.
2. out ("a", 2, "4") : add tuple ("a", 2, "4") to the server
3. out ("a", i, "b") : add tuple ("a", "4", "b") to the server. i is a variable in server assigened by the first two command.
4. read ("a", 2, 3) : wait for tuple ("a", 2, 3) but not delete tuple after read it.

## ActiveMQ
1.Apache ActiveMQ is an open source message broker written in Java together with a full Java Message Service (JMS) client.
2. ActiveMQ is celebrated for its flexibility in configuration, and its support for a relatively large number of transport protocols, including OpenWire, STOMP, MQTT, AMQP, REST, and WebSockets.
3. kind of Message-oriented middleware.
4. ActiveMQ can queue the message, waiting for subscriber to dequeue the data. But if there are two subscriber wanna to dequeue the data, ActiveMQ just can ensure that only one subscriber can fetch the data but it does not sure who will get. 
5. from 4. we know that ActiveMQ can keep the property of order in enqueue but not dequeue. only if there is just one subscriber.

install:
1. download activemq tar for the official website: https://activemq.apache.org/components/classic/download/
2. install java environment
3. [activeMQ_Dir]/bin/activemq start or [activeMQ_Dir]/bin/activemq console
* [activeMQ_Dir]/data/activemq.log to see the log file.

## stomp
1. Simple (or Streaming) Text Orientated Messaging Protocol.
2. STOMP provides an interoperable wire format so that STOMP clients can communicate with any STOMP message broker to provide easy and widespread messaging interoperability among many languages, platforms and brokers.

python package:
1. $sudo apt-get install python-pip
2. $pip install --upgrade pip
3. $pip install stomp.py

## concept
1. we use ActiveMQ to keep the linda command in queue. client enqueue, and server dequeue.
2. if client execute "in" command, waiting for tuple transmitted from server. client should subscribe a queue which is only used for this client and server. That is to say, a client and a server will create a queue.
