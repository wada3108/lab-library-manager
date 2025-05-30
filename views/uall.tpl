<!DOCTYPE html>
<html>
    <head>
        <meta charset = "utf-8">
        <title>一覧・貸出・予約 - 研究室 蔵書管理システム</title>
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
            <li class = "current"><a href = "uall">一覧・貸出・予約</a></li>
            <li><a href = "usearch">検索・貸出・予約</a></li>
            <li><a href = "return">返却</a></li>
            <li><a href = "cancel">予約管理</a></li>
        </ul>    
    </nav>    

    <body>
        <div id = "wrapper">
            <h2>書籍一覧</h2>
            <p>
                現在データベースに登録されている書籍と、その貸出・予約状況の一覧です。<br>
                予約ボタン・貸出ボタンをクリックすることで、貸出・予約の手続きができます。
            </p>
            <table>
                <tr>
                    <th>書名</th>
                    <th>著者名</th>
                    <th>出版社名</th>
                    <th>購入日</th>
                    <th>状態</th>
                    <th>操作</th>
                </tr>
                %for record in allbooks:
                <tr>
                    %for i, element in enumerate(record):
                        %if i == 0:
                            <%
                                continue
                            %>
                        %elif i == 5:
                            %if element == "貸出可能":
                                <td>{{element}}</td>
                                <td>
                                    <a href = "?id={{record[0]}}&type=lend" class = "modifybutton">貸出</a>
                                    <a href = "?id={{record[0]}}&type=review" class = "modifybutton">書評</a>
                                </td>
                            %else:
                                <td>{{element}}</td>
                                <td>
                                    <a href = "?id={{record[0]}}&type=reserve" class = "modifybutton">予約</a>
                                    <a href = "?id={{record[0]}}&type=review" class = "modifybutton">書評</a>
                                </td>
                            %end
                        %else:
                            <td>{{element}}</td>
                        %end
                    %end
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