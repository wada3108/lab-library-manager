<!DOCTYPE html>
<html>
    <head>
        <meta charset = "utf-8">
        <title>書籍登録 - 研究室 蔵書管理システム - 管理用</title>
        <link rel = "stylesheet" href = "/static/style.css">
        <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@48,400,0,0" />
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
            <li class = "current"><a href = "register">書籍登録</a></li>
            <li><a href = "all">書籍一覧</a></li>
            <li><a href = "manage">書籍管理</a></li>
            <li><a href = "user">ユーザ管理</a></li>
        </ul>    
    </nav>    

    <body>
        <div id = "wrapper">
            <h2>登録内容の確認</h2>
            <p>CSVファイルから読み込まれた書籍の一覧です。この内容で登録してもよろしいですか。</p>
            <table>
                <tr>
                    <th>書名</th>
                    <th>著者名</th>
                    <th>出版社名</th>
                    <th>購入日</th>
                </tr>
                %for record in data:
                <tr>
                    %for element in record:
                    <td>{{element}}</td>
                    %end
                <tr>
                %end
            </table>
            <form class = "form" method = "POST">
                <div class = "hidden">
                    <textarea name = "data">{{rawdata}}</textarea>
                </div>
                <p id = "sendbuttoncover">
                <input type = "submit" value = "登録" id = "sendbutton" formaction = "uploaded">
                <input type = "submit" value = "取消" id = "modifybutton" formaction = "uploaded?cancel=True">
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