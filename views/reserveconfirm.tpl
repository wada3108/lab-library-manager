<!DOCTYPE html>
<html>
    <head>
        <meta charset = "utf-8">
        <title>予約確認 - 研究室 蔵書管理システム</title>
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
            %if fm == "a":
                <li class = "current"><a href = "uall">一覧・貸出・予約</a></li>
                <li><a href = "usearch">検索・貸出・予約</a></li>
            %elif fm == "s":
                <li><a href = "uall">一覧・貸出・予約</a></li>
                <li class = "current"><a href = "usearch">検索・貸出・予約</a></li>
            %end
            <li><a href = "return">返却</a></li>
            <li><a href = "cancel">予約管理</a></li>
        </ul>    
    </nav>    

    <body>
        <div id = "wrapper">
            <h2>予約確認</h2>
            <p>この書籍を予約しますか。</p>
            <div class = "form">
                <dl>
                    <dt>書名</dt>
                    <dd>{{data["name"]}}</dd>
                    <dt>著者名</dt>
                    <dd>{{data["author"]}}</dd>
                    <dt>出版社名</dt>
                    <dd>{{data["publisher"]}}</dd>
                    <dt>購入日</dt>
                    <dd>{{data["date"]}}</dd>
                </dl>
            </div>
            <form method = "POST">
                <div class = "hidden">
                    <input type = "text" name = "fm" value = {{fm}}>
                </div>
                <p id = "sendbuttoncover">
                    <input type = "submit" value = "予約" id = "sendbutton" formaction = "reserved?id={{id}}&fm={{fm}}">
                    <input type = "submit" value = "取消" id = "modifybutton" formaction = "reserve">
                </p>
        </div>
    </body>
    <footer>
        <small class = "fsmall">
            Copyright &copy; 2022 WADA Towa All rights reserved.
        </small>    
    </footer>
</html>