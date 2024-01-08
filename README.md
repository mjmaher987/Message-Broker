# Message Broker

## Hierarchy
- Container (has 1 queue)
- Coordinator (managing): talks to client + choose leader container (give the IP of the leader container)
- Leader Container: manage clients (load balancing: using **Hash**)

## Notes
- We have 2 Coordinators
- Coordinator handles if 1 container fails

