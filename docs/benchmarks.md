Отдача статического документа напрямую через nginx:

```shell
ab -n 1000 -c 10 http://127.0.0.1/static/sample.html
```

```txt
Server Software:        nginx/1.25.5
Server Hostname:        127.0.0.1
Server Port:            80

Document Path:          /static/sample.html
Document Length:        233 bytes

Concurrency Level:      10
Time taken for tests:   0.059 seconds
Complete requests:      1000
Failed requests:        0
Total transferred:      502000 bytes
HTML transferred:       233000 bytes
Requests per second:    17026.20 [#/sec] (mean)
Time per request:       0.587 [ms] (mean)
Time per request:       0.059 [ms] (mean, across all concurrent requests)
Transfer rate:          8346.83 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    0   0.2      0       1
Processing:     0    0   0.2      0       1
Waiting:        0    0   0.2      0       1
Total:          0    1   0.3      0       1
ERROR: The median and mean for the total time are more than twice the standard
       deviation apart. These results are NOT reliable.

Percentage of the requests served within a certain time (ms)
  50%      0
  66%      0
  75%      1
  80%      1
  90%      1
  95%      1
  98%      1
  99%      1
 100%      1 (longest request)
```

Отдача статического документа напрямую через gunicorn:

```shell
ab -n 1000 -c 10 http://127.0.0.1:8000/static/sample.html
```

```txt
Server Software:        gunicorn
Server Hostname:        127.0.0.1
Server Port:            8000

Document Path:          /static/sample.html
Document Length:        233 bytes

Concurrency Level:      10
Time taken for tests:   0.526 seconds
Complete requests:      1000
Failed requests:        0
Total transferred:      598000 bytes
HTML transferred:       233000 bytes
Requests per second:    1900.36 [#/sec] (mean)
Time per request:       5.262 [ms] (mean)
Time per request:       0.526 [ms] (mean, across all concurrent requests)
Transfer rate:          1109.78 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    0   0.0      0       1
Processing:     1    5   1.1      5      14
Waiting:        1    5   1.0      5      14
Total:          2    5   1.1      5      14

Percentage of the requests served within a certain time (ms)
  50%      5
  66%      5
  75%      5
  80%      5
  90%      5
  95%      6
  98%      9
  99%     14
 100%     14 (longest request)
```

Отдача динамического документа напрямую через gunicorn:

```shell
ab -n 1000 -c 10 http://127.0.0.1:8000/
```

```txt
Server Software:        gunicorn
Server Hostname:        127.0.0.1
Server Port:            8000

Document Path:          /
Document Length:        28725 bytes

Concurrency Level:      10
Time taken for tests:   28.147 seconds
Complete requests:      1000
Failed requests:        0
Total transferred:      29157000 bytes
HTML transferred:       28725000 bytes
Requests per second:    35.53 [#/sec] (mean)
Time per request:       281.467 [ms] (mean)
Time per request:       28.147 [ms] (mean, across all concurrent requests)
Transfer rate:          1011.62 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    0   0.1      0       1
Processing:    45  280 134.8    185     453
Waiting:       44  280 134.8    184     453
Total:         45  280 134.9    185     453

Percentage of the requests served within a certain time (ms)
  50%    185
  66%    425
  75%    430
  80%    432
  90%    436
  95%    440
  98%    445
  99%    448
 100%    453 (longest request)
```

Отдача динамического документа через проксирование запроса с nginx на gunicorn:

```shell```

```txt
Server Software:        nginx/1.25.5
Server Hostname:        127.0.0.1
Server Port:            80

Document Path:          /
Document Length:        28725 bytes

Concurrency Level:      10
Time taken for tests:   18.803 seconds
Complete requests:      1000
Failed requests:        0
Total transferred:      29161000 bytes
HTML transferred:       28725000 bytes
Requests per second:    53.18 [#/sec] (mean)
Time per request:       188.035 [ms] (mean)
Time per request:       18.803 [ms] (mean, across all concurrent requests)
Transfer rate:          1514.48 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    0   0.1      0       1
Processing:    45  186  15.8    188     217
Waiting:       45  186  15.8    188     217
Total:         45  187  15.8    188     218

Percentage of the requests served within a certain time (ms)
  50%    188
  66%    193
  75%    196
  80%    197
  90%    202
  95%    205
  98%    210
  99%    212
 100%    218 (longest request)
```

Отдача динамического документа через проксирование запроса с nginx на gunicorn, при кэшировние ответа на nginx (proxy cache):

```shell
ab -n 1000 -c 10 http://127.0.0.1/
```

```txt
Server Software:        nginx/1.25.5
Server Hostname:        127.0.0.1
Server Port:            80

Document Path:          /
Document Length:        28726 bytes

Concurrency Level:      10
Time taken for tests:   9.858 seconds
Complete requests:      1000
Failed requests:        0
Total transferred:      29183000 bytes
HTML transferred:       28726000 bytes
Requests per second:    101.44 [#/sec] (mean)
Time per request:       98.582 [ms] (mean)
Time per request:       9.858 [ms] (mean, across all concurrent requests)
Transfer rate:          2890.91 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    0   0.1      0       1
Processing:    63   97   9.7     95     185
Waiting:       63   97   9.7     95     184
Total:         63   97   9.8     95     185

Percentage of the requests served within a certain time (ms)
  50%     95
  66%     98
  75%     99
  80%    100
  90%    105
  95%    116
  98%    127
  99%    139
 100%    185 (longest request)
```

Насколько быстрее отдается статика по сравнению с WSGI? nginx раздает статику быстрее, чем wsgi в 8.9 раз

Во сколько раз ускоряет работу proxy_cache? proxy_cache ускоряет раздачу динамики в 1.8 на nginx
