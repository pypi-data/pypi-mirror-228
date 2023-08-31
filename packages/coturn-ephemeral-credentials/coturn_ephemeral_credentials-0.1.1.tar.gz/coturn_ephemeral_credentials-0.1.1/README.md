# Coturn Ephemeral Credentials - v0.1.1

Generate time limited, i.e. ephemeral, long term credentials to authenticate against a coturn server. The _default_ duration for the validity of the credentials is set to _one day_ as recommended in [A REST API For Access To TURN Services](https://datatracker.ietf.org/doc/html/draft-uberti-behave-turn-rest-00#section-2.1:~:text=ttl%3A%20the%20duration%20for%20which%20the%20username%20and%20password%20are%20valid%2C%0A%20%20%20%20%20%20in%20seconds.%20%20A%20value%20of%20one%20day%20(86400%20seconds)%20is%20recommended). The same document describes how to generate the _username_ and _password_ [here](https://datatracker.ietf.org/doc/html/draft-uberti-behave-turn-rest-00#section-2.1:~:text=username%3A%20the%20TURN,algorithm%0A%20%20%20%20%20%20and%20secret.).

## Stack

- Python 3.8.10 on Ubuntu 20.04.2 LTS

## Installation

### From PyPI

```bash
(venv) $ pip install coturn-ephemeral-credentials
```

### From GitHub

```bash
(venv) $ pip install git+https://github.com/p4irin/coturn_ephemeral_credentials.git
```

## Usage

```python
from coturn_ephemeral_credentials import generate

credentials = generate(shared_secret='A shared secret with a coturn server')
coturn_username = credentials['coturn_username']
coturn_password = credentials['coturn_password']
```

## Reference

- [A REST API For Access To TURN Services](https://datatracker.ietf.org/doc/html/draft-uberti-behave-turn-rest-00#section-2.1)
- [coturn](https://github.com/coturn/coturn)
- [RFC 5766. Traversal Using Relays around NAT (TURN):Relay Extensions to Session Traversal Utilities for NAT (STUN)](https://datatracker.ietf.org/doc/html/rfc5766)
- [RFC 5389, Session Traversal Utilities for NAT (STUN)](https://datatracker.ietf.org/doc/html/rfc5389#section-10.2)