<!DOCTYPE html>
<html>
    <head>
        <meta charset = "utf-8">
        <title>ユーザ情報 - 研究室 蔵書管理システム</title>
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
            <li><a href = "return">返却</a></li>
            <li><a href = "cancel">予約管理</a></li>
        </ul>    
    </nav>    

    <body>
        <div id = "wrapper">
            <h2>ユーザ情報</h2>
                <p>現在登録されているユーザ情報です。</p>
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
                    <a href = "uchange?id={{id}}" class = "button">ユーザ情報変更</a>
                </p>
            <h2>貸出・返却履歴</h2>
                <p>これまでに行った、書籍の貸出・返却の履歴です。</p>
                <table>
                <tr>
                    <th>書名</th>
                    <th>著者名</th>
                    <th>出版社名</th>
                    <th>購入日</th>
                    <th>貸出日</th>
                    <th>返却日</th>
                </tr>
                %for record in bookdata:
                <tr>
                    %for element in record:
                        %if element is None:
                        <td>未返却</td>
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