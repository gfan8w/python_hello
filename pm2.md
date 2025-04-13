



| 功能       | 命令                                                                 |
|------------|----------------------------------------------------------------------|
| 首次启动（方式1） | pm2 start {py文件} --interpreter python3                          |
| 首次启动（方式2） | pm2 start {json文件}                                             |
| 非首次启动   | pm2 start {id}                                                      |
| 查看       | pm2 list                                                             |
| 停止       | pm2 stop {id}                                                        |
| 重启       | pm2 restart {id}                                                     |
| 日志       | pm2 logs {id} \| pm2 logs {id} --err \| pm2 logs {id} --lines 1000   |
| 删除       | pm2 delete {id}                                                      |





