import requests

def push(key, value):
    response = requests.post('http://127.0.0.1:8000/push/', json={'key': key, 'value': value})
    print('\033[92m' + '############## PUSH ##############' + '\033[0m')
    print(response.status_code)
    print('\033[92m' + '##################################' + '\033[0m')

def pull():
    response = requests.post('http://127.0.0.1:8000/pull/')
    print('\033[94m' + '############## PULL ##############' + '\033[0m')
    print(response.status_code, response.json())
    print('\033[94m' + '##################################' + '\033[0m')

if __name__ == '__main__':
    push('abcd', 'first push')
    push('mbmbm', 'second push')
    pull()
    pull()