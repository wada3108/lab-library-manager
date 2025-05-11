<!DOCTYPE html>
<html>
    <head>
        <meta charset = "utf-8">
        <title>登録 - 研究室 蔵書管理システム - 管理用</title>
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
            <p>このページでは、CSVから新しい本を一括登録することができます。</p>
            <h2>ファイルを選択してアップロード</h2>
            <p>「ファイルの選択」をクリックして、アップロードするファイルを選択してください。選択すると、自動的にアップロードされます。</p>
            <p id = "sendbuttoncover">
                <button onclick = "selectfile();" id = "sendbutton">ファイルの選択</button>
            </p>
                <form action="/upload" method="post" enctype="multipart/form-data" class = "hidden" name = "upload">
                <input type="file" name="file" accept = ".csv" onchange = "changeFile(this);">
            </form>
            <h2>アップロードするファイルの要件</h2>
            <p>
                <ul>
                    <li>ファイル形式:CSV(カンマ区切りファイル)</li>
                    <li>エンコード方式:UTF-8</li>
                    <li>データ形式:書名,著者名,出版社名,購入日</li>
                </ul>
                ※アップロードを行うため、ファイルサイズにご注意ください。
            </p>
        </div>
        <script>
            function selectfile(){
                document.querySelector("input").click();
            }
            function changeFile(obj){
                document.upload.action = "upload";
                document.upload.method = "POST";
                document.upload.submit();
            }
        </script>
    </body>
    <footer>
        <small class = "fsmall">
            Copyright &copy; 2022 WADA Towa All rights reserved.
        </small>    
    </footer>
</html>