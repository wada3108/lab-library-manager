<!DOCTYPE html>
<html>
    <head>
        <meta charset = "utf-8">
        <title>登録内容の修正 - 研究室 蔵書管理システム - 管理用</title>
        <link rel = "stylesheet" href = "/static/style.css">
        <link rel = "stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@48,400,0,0" />
    </head>

    <header class = "header">
        <div class = "spacer"></div>
        <h1>研究室 蔵書管理システム 管理用ページ</h1>
        <div class = "accountmenu">
            <a class = "account" href = "">
                <span class="material-symbols-outlined">
                    account_circle
                </span>
                ログイン中
            </a>
            <ul class = "dropdown">
                <li>{{uname}}さん</li>
                <li><a href = "user?id={{uid}}">ユーザ情報</a></li>
                <li><a href = "logout">ログアウト</a></li>
            </ul>
        </div>
    </header>

    <nav id = "gnavi">
        <ul>
            <li><a href = "admin">ホーム</a></li>
            <li><a href = "register">書籍登録</a></li>
            <li><a href = "all">書籍一覧</a></li>
            <li class = "current"><a href = "manage">書籍管理</a></li>
            <li><a href = "user">ユーザ管理</a></li>
        </ul>    
    </nav>    

    <body>
        <div id = "wrapper">
            <h2>登録内容の修正</h2>
            <p class = "error">{{errormsg}}</p>
            <form method = "POST" class =  "form">
                <dl>
                    <dt>書名</dt>
                    <dd><input type = "text" name = "name" value = "{{data[0]|space}}"></dd>
                    <dt>著者名</dt>
                    <dd><input type = "text" name = "author" value = "{{data[1]|space}}"></dd>
                    <dt>出版社名</dt>
                    <dd><input type = "text" name = "publisher" value = "{{data[2]|space}}"></dd>
                    <dt>購入日</dt>
                    <dd><input type = "text" name = "date" placeholder = "YYYY-MM-DD" value = "{{data[3]|space}}"></dd>
                </dl>
                    <p id = "sendbuttoncover">
                        <input type = "submit" value = "変更" id = "sendbutton" formaction = "bookmodify?id={{id}}&fm={{fm}}">
                        <input type = "submit" value = "取消" id = "modifybutton" formaction = "bookmodify?id={{id}}&fm={{fm}}&cancel=True">
                    </p>
                </form>
        </div>
    </body>
    <footer>
        <small class = "fsmall">
            Copyright &copy; 2022 WADA Towa All rights reserved.
        </small>    
    </footer>
</html>