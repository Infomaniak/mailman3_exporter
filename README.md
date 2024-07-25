# Mailman3 Exporter for Prometheus 

This prometheus exporter monitors the [mailman3](https://www.mailman.org/) mailing list server. 
Stats are collected using mailman3 core process own REST API and include status, number of lists,
list names, number of users per list, and more.

## Installing

`git clone` this repository.  Create a virtual environment, e.g.:

```shell script
python3 -m venv .
```

and then install the required packages:

```shell script
pip3 install -r requirements.txt
```

The program can then be run, e.g. by:

```shell script
python3 ./mailman3_exporter.py -p PASS -u USER
```

If python complains packages are missing, check that you are invoking the
program with the correct virtual environment.

## Usage

By default, the exporter serves on port `9934` at `/metrics`. The help message
includes: 

```
usage: mailman_exporter.py [-h]
                           [--log-level {debug,info,warning,error,critical}]
                           [--log-config {true,false}] [-l WEB_LISTEN]
                           [-m MAILMAN_ADDRESS] [-u MAILMAN_USER]
                           [-p MAILMAN_PASSWORD] [--namespace NAMESPACE]
                           [--cache {true,false}]
                           [--cache.duration CACHE_DURATION]
                           [--metrics.gc {true,false}]
                           [--metrics.platform {true,false}]
                           [--metrics.process {true,false}]
                           [--metrics.domains {true,false}]
                           [--metrics.lists {true,false}]
                           [--metrics.up {true,false}]
                           [--metrics.users {true,false}]
                           [--metrics.queue {true,false}]

Mailman3 Prometheus metrics exporter

options:
  -h, --help            show this help message and exit
  --log-level {debug,info,warning,error,critical}
                        Detail level to log. (default: info)
  --log-config {true,false}
                        Log the current configuration except for sensitive
                        information (log level: info). Can be used for
                        debugging purposes. (default: false)
  -l WEB_LISTEN, --web.listen WEB_LISTEN
                        HTTPServer metrics listen address (default:
                        localhost:9934)
  -m MAILMAN_ADDRESS, --mailman.address MAILMAN_ADDRESS
                        Mailman3 Core REST API address (default:
                        http://mailman-core:8001)
  -u MAILMAN_USER, --mailman.user MAILMAN_USER
                        Mailman3 Core REST API username (default: restadmin)
  -p MAILMAN_PASSWORD, --mailman.password MAILMAN_PASSWORD
                        Mailman3 Core REST API password (default: restpass)
  --namespace NAMESPACE
                        Metrics namespace (default: )
  --cache {true,false}  Enable caching (default: true)
  --cache.duration CACHE_DURATION
                        Cache duration in seconds (default: 30)
  --metrics.gc {true,false}
                        Enable garbage collection metrics (default: true)
  --metrics.platform {true,false}
                        Enable platform metrics (default: true)
  --metrics.process {true,false}
                        Enable process metrics (default: true)
  --metrics.domains {true,false}
                        Enable domains metrics (default: true)
  --metrics.lists {true,false}
                        Enable lists metrics (default: true)
  --metrics.up {true,false}
                        Enable up metrics (default: true)
  --metrics.users {true,false}
                        Enable users metrics (default: true)
  --metrics.queue {true,false}
                        Enable queue metrics (default: true)
```

## Metrics

```
  # HELP mailman3_domains Number of configured list domains
  # TYPE mailman3_domains gauge
  mailman3_domains 1.0
  # HELP mailman3_lists Number of configured lists
  # TYPE mailman3_lists gauge
  mailman3_lists 8.0
  # HELP mailman3_list_members_total Count members per list
  # TYPE mailman3_list_members_total counter
  mailman3_list_members_total{list="list1@example.com"} 104.0
  mailman3_list_members_total{list="list2@example.com"} 26.0
  mailman3_list_members_total{list="list3@example.com"} 7.0
  mailman3_list_members_total{list="list4@example.com"} 74.0
  mailman3_list_members_total{list="list5@example.com"} 30.0
  mailman3_list_members_total{list="list6@example.com"} 6.0
  mailman3_list_members_total{list="list7@example.com"} 1.0
  mailman3_list_members_total{list="list8@example.com"} 1.0
  # HELP mailman3_up Status of mailman-core; 1 if accessible, 0 otherwise
  # TYPE mailman3_up gauge
  mailman3_up 1.0
  # HELP mailman3_users_total Number of list users recorded in mailman-core
  # TYPE mailman3_users_total counter
  mailman3_users_total 288.0
  # HELP mailman3_queues Queue length for mailman-core internal queues
  # TYPE mailman3_queues gauge
  mailman3_queues{queue="archive"} 10.0
  mailman3_queues{queue="bad"} 0.0
  mailman3_queues{queue="bounces"} 0.0
  mailman3_queues{queue="command"} 0.0
  mailman3_queues{queue="digest"} 0.0
  mailman3_queues{queue="in"} 1.0
  mailman3_queues{queue="nntp"} 0.0
  mailman3_queues{queue="out"} 0.0
  mailman3_queues{queue="pipeline"} 0.0
  mailman3_queues{queue="retry"} 0.0
  mailman3_queues{queue="shunt"} 1.0
  mailman3_queues{queue="virgin"} 0.0
  # HELP processing_time_ms Time taken to collect metrics
  # TYPE processing_time_ms gauge
  processing_time_ms{method="domains"} 0.04233299999967244
  processing_time_ms{method="lists"} 0.22640099999993168
  processing_time_ms{method="up"} 5.324605999999843
  processing_time_ms{method="users"} 7.315147000000355
  processing_time_ms{method="queue"} 3.1242169999998737
```

## Docker

See: [docker.md](./docker.md)

