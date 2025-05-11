<!DOCTYPE html>
<html>
    <head>
        <meta charset = "utf-8">
        <title>返却 - 研究室 蔵書管理システム</title>
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
            <li><a href = "index">ホーム</a></li>
            <li><a href = "uall">一覧・貸出・予約</a></li>
            <li><a href = "usearch">検索・貸出・予約</a></li>
            <li class = "current"><a href = "return">返却</a></li>
            <li><a href = "cancel">予約管理</a></li>
        </ul>    
    </nav>    

    <body>
        <div id = "wrapper">
            <h2>書籍返却</h2>
            <p>
                現在貸出中の書籍の一覧です。<br>
                返却ボタンをクリックすることで、返却手続きができます。
            </p>
            <table>
                <tr>
                    <th>書名</th>
                    <th>著者名</th>
                    <th>出版社名</th>
                    <th>購入日</th>
                    <th>返却期限</th>
                    <th>操作</th>
                </tr>
                %for record in allbooks:
                <tr>
                    %for i, element in enumerate(record):
                        %if i == 0:
                            <%
                                continue
                            %>
                        %else:
                            <td>{{element}}</td>
                        %end
                    %end
                    <td><a href = "?id={{record[0]}}" class = "modifybutton">返却</a></td>
                <tr>
                %end
            </table>
        </div>
    </body>
    <footer>
        <small class = "fsmall">
            Copyright &copy; 2022 WADA Towa All rights reserved.
        </small>    
    </footer>
</html>