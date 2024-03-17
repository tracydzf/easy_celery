from tasks.add import add_task

res = add_task.delay(1, 2)
print(res)