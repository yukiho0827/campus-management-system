def write2file(status_code):
    if status_code in [4, 9]:
        cont = "prove_fail"
    elif status_code in [5, 10]:
        cont = 'isolate'
    elif status_code == 6:
        cont = 'health_fail'
    elif status_code == 11:
        cont = 'success'
    else:
        cont = None
    print(f'内容是{cont}')
    with open('status.txt', mode='w', encoding='utf-8') as f:
        print('正在写入')
        f.write('111')
