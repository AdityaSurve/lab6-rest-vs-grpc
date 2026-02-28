| Method          |  Local | Same-Zone | Different Region |
| --------------- | -----: | --------: | ---------------: |
| REST add        |  2.896 |     2.975 |          317.133 |
| gRPC add        |  0.666 |     0.928 |          151.168 |
| REST rawimg     |  4.562 |     6.370 |         1296.851 |
| gRPC rawimg     |  9.557 |    11.309 |          230.953 |
| REST dotproduct |  3.334 |     3.603 |          322.356 |
| gRPC dotproduct |  0.751 |     0.976 |          149.788 |
| REST jsonimg    | 33.472 |    36.551 |         1445.781 |
| gRPC jsonimg    | 21.561 |    21.921 |          217.253 |
| PING            |  0.059 |     0.376 |          168.471 |


### Screenshots:

**Local (localhost):**

![Local PING](screenshots/LocalPing%20-%20US%20Server.png)

![Local REST](screenshots/LocalRest%20-%20US%20Server.png)

![Local gRPC](screenshots/LocalgRPC%20-%20US%20Server.png)

**Same Zone (us-west1-a):**

![Same Zone PING](screenshots/SameZonePing%20-%20US%20Server%20and%20Client.png) 

![Same Zone REST](screenshots/SameZoneRest%20-%20US%20Server%20and%20Client.png)

![Same Zone gRPC](screenshots/SameZonegRPC%20-%20US%20Server%20and%20Client.png)

**Different Region (EU server, US client):**

![Different Region PING](screenshots/DiffRegionPing%20-%20EU%20Server%20and%20US%20Client.png)

![Different Region REST](screenshots/DiffRegionRest%20-%20EU%20Server%20and%20US%20Client.png)

![Different Region gRPC](screenshots/DiffRegiongRPC%20-%20EU%20Server%20and%20US%20Client.png)

In the local and same-zone setups, both REST and gRPC are fast, but gRPC consistently has lower latency for small requests like add and dotproduct (e.g., ~0.67–0.93 ms for gRPC add vs ~2.90–2.98 ms for REST add). This gap becomes much larger in the different-region setup, where the baseline latency from ping rises to ~168 ms and dominates end-to-end time. In that cross-region case, gRPC add (~151 ms) is much closer to the ping baseline than REST add (~317 ms), which suggests extra per-request overhead for REST. A key reason is connection behavior: typical REST/HTTP request patterns can incur more connection setup/handshake overhead (REST makes a new TCP connection per request), while gRPC uses a single long-lived connection (HTTP/2) that is reused for all RPCs, so it avoids repeated setup costs and tracks network RTT more closely. For large payload endpoints, rawimg and especially jsonimg, the cost is driven mainly by data transfer and serialization: jsonimg is much slower than rawimg because base64 + JSON increases payload size and adds encoding/decoding overhead; gRPC generally performs better here because protobuf is a more compact binary format than JSON and avoids base64 expansion.