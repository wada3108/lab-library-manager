<!DOCTYPE html>
<html>
    <head>
        <meta charset = "utf-8">
        <title>新規ユーザ作成 - 研究室 蔵書管理システム - 管理用</title>
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
            <li><a href = "manage">書籍管理</a></li>
            <li class = "current"><a href = "user">ユーザ管理</a></li>
        </ul>    
    </nav>    

    <body>
        <div id = "wrapper">
            <p>このページでは、新しいユーザを作成することができます。</p>
            <h2>ユーザ情報の入力</h2>
            <p>すべて半角英数で入力してください。</p>
            <p class = "error">{{errormsg}}</p>
            <form method = "POST" class =  "form">
                <dl>
                    <dt>ユーザ名</dt>
                    <dd><input type = "text" name = "name" value = "{{data[0]}}"></dd>
                    <dt>学籍番号</dt>
                    <dd><input type = "text" name = "number" value = "{{data[1]}}"></dd>
                    <dt>メールアドレス</dt>
                    <dd><input type = "email" name = "email" value = "{{data[2]}}"></dd>
                    <dt>初期パスワード(8文字以上)</dt>
                    <dd><input type = "password" name = "password" value = "{{data[3]}}"></dd>
                    <dt>初期パスワード(確認用)</dt>
                    <dd><input type = "password" name = "password2" value = "{{data[4]}}"></dd>
                </dl>
                    <p id = "sendbuttoncover">
                        <input type = "submit" value = "作成" id = "sendbutton" formaction = "createuser">
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