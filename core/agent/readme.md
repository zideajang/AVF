
- base_agent
  - user_proxy_agent(提供控制)
  - generate_agent
  - chat_agent
- UI
  - message 

- 添加障碍物，根据实时障碍生成路径
  
效用实现通过任务来控制 RectAgent 的行为
task
- name:
- id:
- action:是一个函数，可能访问网络或者进行运算函数，或者其他 IO 操作
- delaytime
- status:isCompleted 内部维护状态
- target_pos

task 按照执行顺序

分为立即执行，task 
延时指定，task 
对于 Agent 提供 add_task 将 task 压入的一个 task ，在运行

要实现
- move_task Agent 等待 10 秒开始移动，移动到某一个目标位置
- http_task Agent 发起 http 然后等待，
  - 如果超时或者请求失败跳转 error_handle_task 任务
  - 如果成功就跳转到 success_task

task 读取 Agent 状态来做动态判断