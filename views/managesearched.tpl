<!DOCTYPE html>
<html>
    <head>
        <meta charset = "utf-8">
        <title>書籍管理 - 研究室 蔵書管理システム - 管理用</title>
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
            <h2>検索結果</h2>
            <p class = "float">
                {{number}}件の検索結果が見つかりました。<br>
                書籍を削除するには削除ボタン、修正するには修正ボタンをクリックしてください。
            </p>
            <form method = "POST" action = "managesearch" class = "form">
            <div class = "hidden">
                <input type = "text" name = "name" value = "{{data[0]|space}}">
                <input type = "text" name = "author" value = "{{data[1]|space}}">
                <input type = "text" name = "publisher" value = "{{data[2]|space}}">
                <input type = "text" name = "date" value = "{{data[3]|space}}">
                <input type = "text" name = "change" value = "change">
            </div>
                <p id = "changebuttoncover">
                    <input type = "submit" value = "検索条件を変更" id = "changebutton">
                </p>
            </form>
            <table>
                <tr>
                    <th>ID</th>
                    <th>書名</th>
                    <th>著者名</th>
                    <th>出版社名</th>
                    <th>購入日</th>
                    <th>管理</th>
                </tr>
                {%for record in searcheddata %}
                <tr>
                    {%for element in record %}
                    <td>{{element}}</td>
                    {% endfor %}
                    <td>
                        <a href = "?id={{record[0]}}&type=delete" class = "delbutton">削除</a>
                        <a href = "?id={{record[0]}}&type=modify" class = "modifybutton">変更</a>
                    </td>
                <tr>
                {% endfor %}
            </table>
        </div>
    </body>
    <footer>
        <small class = "fsmall">
            Copyright &copy; 2022 WADA Towa All rights reserved.
        </small>    
    </footer>
</html>