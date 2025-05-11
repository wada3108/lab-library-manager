<!DOCTYPE html>
<html>
    <head>
        <meta charset = "utf-8">
        <title>ユーザ情報 - 研究室 蔵書管理システム - 管理用</title>
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
            <li><a href = "user">ユーザ管理</a></li>
        </ul>    
    </nav>    

    <body>
        <div id = "wrapper">
            <h2>ユーザ情報</h2>
            <p>
                現在登録されているユーザ情報です。<br>
                また、このページではパスワードを変更することができます。<br>
                なお、パスワード以外の変更は、[ユーザ管理]→[ユーザの削除・変更]から行ってください。
            </p>
            <div class = "form">
                <dl>
                    <dt>ユーザ名</dt>
                    <dd>{{udata[0]}}</dd>
                    <dt>学籍番号</dt>
                    <dd>{{udata[1]}}</dd>
                    <dt>メールアドレス</dt>
                    <dd>{{udata[2]}}</dd>
                </dl>
            </div>            
            <p id = "sendbuttoncover">
                <a href = "pwchange" class = "button">パスワード変更</a>
            </p>
        </div>
    </body>
    <footer>
        <small class = "fsmall">
            Copyright &copy; 2022 WADA Towa All rights reserved.
        </small>    
    </footer>
</html>