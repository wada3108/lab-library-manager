<!DOCTYPE html>
<html>
    <head>
        <meta charset = "utf-8">
        <title>登録内容の変更 - 研究室 蔵書管理システム</title>
        <link rel = "stylesheet" href = "/static/style.css">
        <link rel = "stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@48,400,0,0" />
    </head>

    <header class = "header">
        <div class = "spacer"></div>
        <h1>研究室 蔵書管理システム</h1>
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
            <li><a href = "manage">書籍管理</a></li>
            <li><a href = "user">ユーザ管理</a></li>
        </ul>    
    </nav>    

    <body>
        <div id = "wrapper">
            <h2>変更内容の確認</h2>
            <p>この変更内容で確定してもよろしいですか。</p>
            <div class = "form">
                <dl>
                    <dt>新しいパスワード</dt>
                    <dd>{{data[3]}}</dd>
                </dl>
            </div>
            <form method = "POST" class = "form">
                <div class = "hidden">
                    <input type = "password" name = "currentpassword" value = "{{data[0]}}">
                    <input type = "password" name = "newpassword" value = "{{data[1]}}">
                    <input type = "password" name = "newpassword2" value = "{{data[2]}}">
                </div>
                <p id = "sendbuttoncover">
                    <input type = "submit" value = "確定" id = "sendbutton" formaction = "pwchanged">
                    <input type = "submit" value = "修正" id = "modifybutton" formaction = "pwchange?modify=True">
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