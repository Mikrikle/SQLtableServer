import sqlite3
import socket


# files
with open('html/add_user.html', 'r', encoding='utf-8') as f:
    add_user_html = f.read()

with open('css/main.css', 'r', encoding='utf-8') as f:
    css = f.read()

with open('html/root.html', 'r', encoding='utf-8') as f:
    root_html = f.read()

# table
def table():
    global conn
    with open('html/table.html', 'r', encoding='utf-8') as f:
        begin_table = ''
        end_table = ''
        for _ in range(54):
            begin_table += f.readline()
        for _ in range(14):
            end_table += f.readline()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    for row in cursor:
        begin_table += '\t\t\t<tr>' + '<th scope="row" class="ids">' + \
            str(row[0]) + '</th>' + '<td>' + row[1] + '</td>' + \
            '<td>' + row[2] + '</td>' + '<td>' + row[3] + '</td>' + '</tr>\n'
    cursor.close()
    html_table = begin_table + end_table
    return html_table

# answer
def generate_response(request, method, url):
        # url:body
    URLS = {
        '/': root_html,
        '/users': table(),
        '/new_user': add_user_html,
        '/css/main.css': css,
    }
    # API_____________________________

    def parse_post_newuser(request):
        data = request.split('\n')[-1]
        data_parsed = data.split('&')
        name = data_parsed[0].split('=')[1]
        email = data_parsed[1].split('=')[1]
        password = data_parsed[2].split('=')[1]
        add_user(name, email, password)

    def add_user(name, email, password):
        global conn
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                       (name, email, password))
        conn.commit()
        cursor.close()
        print('< Добавлен новый пользователь >')

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
        headers, code = generate_headers(url)
        body = generate_content(code, url)
        return (headers + body).encode()
    elif method == 'POST' and url[:4] == '/api':
        if url[4:] == '/add':
            parse_post_newuser(request)
        else:
            print(url)
        return('HTTP/1.1 201 OK').encode()
    else:
        return('HTTP/1.1 405 Method not allowed\n\n<h1>405</h1><p>Method not allowed</p>').encode()

def main():
    def request_processing(request):
        #print(request)
        if request != '':
            parsed = request.split(' ')
            try:
                method = parsed[0]
                url = parsed[1]
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
            print(request)
            try:
                response = request_processing(request.decode('utf-8'))
                client_socket.sendall(response)
                print('<--ОК-->', addr, end=' ')
                print(request.decode('utf-8')[:4])
            except:
                print('<--ОШИБКА-->')
            client_socket.close()
    run()


if __name__ == "__main__":
    conn = sqlite3.connect("usersbase.db")
    main()
    conn.close()
