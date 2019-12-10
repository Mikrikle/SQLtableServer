import sqlite3
import socket
import json

# files
with open('html/add_user.html', 'r', encoding='utf-8') as f:
    add_user_html = f.read()

with open('css/main.css', 'r', encoding='utf-8') as f:
    css = f.read()

with open('html/root.html', 'r', encoding='utf-8') as f:
    root_html = f.read()

with open('html/r.html', 'r', encoding='utf-8') as f:
    readress_html = f.read()

with open('html/redact_user.html', 'r', encoding='utf-8') as f:
    redact_html = f.read()


def table():
    global conn
    with open('html/table.html', 'r', encoding='utf-8') as f:
        begin_table = ''
        end_table = ''
        for _ in range(54):
            begin_table += f.readline()
        for _ in range(50):
            end_table += f.readline()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    for row in cursor:
        begin_table += '\t\t\t<tr>' + '<th scope="row" class="ids">' + \
            str(row[0]) + '</th>' + '<td class="name">' + row[1] + '</td>' + \
            '<td class="email">' + row[2] + '</td>' + '<td class="password">' + row[3] + '</td>' + \
            '<td class="button-place"><button type="button" class="btn btn-danger btn-sm">&#10008;</button>' + \
            '<button type="button" class="btn btn-info btn-sm">&#10000;</button></td>' '</tr>\n'
    cursor.close()
    html_table = begin_table + end_table
    return html_table


def generate_response(request, method, url):
        # url:body
    URLS = {
        '/': root_html,
        '/users': table(),
        '/new_user': add_user_html,
        '/redact_user': redact_html,
        '/css/main.css': css,
        'return': readress_html
    }

    # API_____________________________
    # __ADD
    def parse_newuser(request):
        data = request.split('\n')[-1]
        j = json.loads(data)
        name = j["name"]
        email = j["email"]
        password = j["password"]
        add_user(name, email, password)

    def add_user(name, email, password):
        global conn

        def id_generation():
            f = open('logid.txt', 'r')
            userid = f.read()
            f.close()
            userid = int(userid) + 1
            f = open('logid.txt', 'w')
            f.write(str(userid))
            f.close()
            return userid

        userid = id_generation()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (id, name, email, password) VALUES (?, ?, ?, ?)",
                       (userid, name, email, password))
        conn.commit()
        cursor.close()
        print('< Добавлен новый пользователь >')

    # __DELITE
    def parse_delite(request):
        data = request.split('\n')[-1]
        j = json.loads(data)
        user_id = j["id"]
        delite_user(user_id)

    def delite_user(user_id):
        global conn
        cursor = conn.cursor()
        sql = 'DELETE FROM users WHERE id=?'
        print('<', user_id, '>', end='')
        cursor.execute(sql, (user_id,))
        conn.commit()
        cursor.close()
        print('< удален пользователь >')

    # __REDACT
    def parse_redact(request):
        data = request.split('\n')[-1]
        j = json.loads(data)
        userid = j['id']
        name = j['name']
        email = j['email']
        password = j['password']
        redact_user(userid, name, email, password)

    def redact_user(user_id, name, email, password):
        global conn
        cursor = conn.cursor()
        print('<', user_id, '>', end='')
        sql = """UPDATE users
                       SET name = ?, email = ?, password = ?
                        WHERE id = ?;"""
        cursor.execute(sql, (name, email, password, user_id,))
        conn.commit()
        cursor.close()
        print('< данные изменены >')

    # GET____________________________
    def generate_headers(url):
        if not url in URLS:
            return ('HTTP/1.1 404 Not found\n\n', 404)

        return('HTTP/1.1 200 OK', 200)

    def generate_content(code, url):
        if code == 404:
            return('<h1>404</h1><p>Not Found</p>')
        else:
            return(URLS[url])

    # HTTP___________________________
    if method == 'GET':
        if url[:15] == '/redact_user?id':
            headers = 'HTTP/1.1 200 OK'
            body = URLS['/redact_user']
            return (headers + body).encode()
        elif '?' in url:
            headers = 'HTTP/1.1 200 OK'
            body = URLS['return']
            return (headers + body).encode()
        else:
            headers, code = generate_headers(url)
            body = generate_content(code, url)
            return (headers + body).encode()
    if method == 'PUT' and url[:8] == '/api/add':
        print('<api method add>', end='')
        parse_newuser(request)
        return('HTTP/1.1 200 OK').encode()
    elif method == 'DELITE' and url[:11] == '/api/delite':
        print('<api method delite>', end='')
        parse_delite(request)
        return('HTTP/1.1 200 OK').encode()
    elif method == 'POST' and url[:11] == '/api/redact':
        print('<api method redact>', end='')
        parse_redact(request)
        return('HTTP/1.1 200 OK').encode()
    else:
        return('HTTP/1.1 405 Method not allowed\n\n<h1>405</h1><p>Method not allowed</p>').encode()


def main():
    def request_processing(request):
        if request != '':
            parsed = request.split(' ')
            try:
                method = parsed[0]
                url = parsed[1]
                print(url, method)
                return generate_response(request, method, url)
            except:
                return generate_response(request, None, None)
        else:
            return generate_response(request, None, None)

    def run():
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        serversocket.bind(('localhost', 5000))
        serversocket.listen(5)
        print('\t\t\t\t<--Сервер запущен-->')

        while True:
            client_socket, addr = serversocket.accept()
            request = client_socket.recv(1024)
            try:
                print('<--ОК-->', addr, end=' ')
                response = request_processing(request.decode('utf-8'))
                client_socket.sendall(response)
            except:
                print('<--ОШИБКА-->')
            client_socket.close()
    run()


if __name__ == "__main__":
    conn = sqlite3.connect("usersbase.db")
    main()
    conn.close()
