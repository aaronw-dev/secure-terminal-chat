## Introduction
STC is a fully-featured version of my previous web-based messaging application, TermChat. TermChat was styled after a terminal but built with HTML and JS, allowing for more stylistic options.

The aim with STC is to create a secure, encrypted terminal chat that actually runs in the terminal. For this, I'll be using Python with a new server architecture.


## Tech
In this implementation, a new server architecture is established, with explicit server and client separation and a new initialization method. Different functions of packetry are clearly separated through namespaces.

The cryptography is an important aspect in a secure terminal chat application. STC uses RSA cryptography to encrypt messages and SocketIO for packet exchange. Absolutely no content is transmitted in the clear, as key exchange is the very first step in client intialization.

## Good use cases for STC
- chatting with friends in a cryptographically secure manner

## Not good use cases for STC
- planning airstrikes in Yemen