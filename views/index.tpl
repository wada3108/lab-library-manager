<!DOCTYPE html>
<html>
    <head>
        <meta charset = "utf-8">
        <title>ホーム - 研究室 蔵書管理システム</title>
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
            <li class = "current"><a href = "index">ホーム</a></li>
            <li><a href = "uall">一覧・貸出・予約</a></li>
            <li><a href = "usearch">検索・貸出・予約</a></li>
            <li><a href = "return">返却</a></li>
            <li><a href = "cancel">予約管理</a></li>
        </ul>    
    </nav>    

    <body>
        <div id = "wrapper">
            <h2>研究室の蔵書管理システムへようこそ</h2>
            <div class = "index">
                <div class = "date">
                    <table>
                        <tr>
                            <th>貸出日</th>
                        <tr>
                        <tr>
                            <td>{{today}}</td>
                        </tr>
                    </table>
                    <table class = "date">
                        <tr>
                            <th>返却日</th>
                        <tr>
                        <tr>
                            <td>{{due}}</td>
                        </tr>
                    </table>
                </div>
                <p><a href = "uall" class = "indexbutton">一覧・貸出・予約</a>書籍を一覧から選択し、貸出・予約することができます。</p>
                <p><a href = "usearch" class = "indexbutton">検索・貸出・予約</a>書籍を条件で検索し、貸出・予約することができます。</p>
                <p><a href = "return" class = "indexbutton">　　　返却　　　</a>書籍を返却することができます。</p>
                <p><a href = "cancel" class = "indexbutton">　　予約管理　　</a>予約した書籍の状況を確認したり、予約を取り消したりできます。</p>
                </div>
        </div>
    </body>
    <footer class = "indexfooter">
        <small class = "fsmall">
            Copyright &copy; 2022 WADA Towa All rights reserved.
        </small>    
    </footer>
</html>